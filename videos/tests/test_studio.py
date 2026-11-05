import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

MODULE = Path(__file__).resolve().parents[1] / 'scripts' / 'studio.py'
spec = importlib.util.spec_from_file_location('studio', MODULE)
studio = importlib.util.module_from_spec(spec)
spec.loader.exec_module(studio)


class StudioTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.project = studio.init_project('test-video', 'personal', self.root / 'projects')
        self.context = self.root / 'context'
        self.context.mkdir()

    def tearDown(self):
        self.temp.cleanup()

    def test_init_protects_existing_work_and_path_boundaries(self):
        brief = self.project / 'brief.json'
        original = brief.read_bytes()
        with self.assertRaises(ValueError):
            studio.init_project('test-video', 'personal', self.root / 'projects')
        self.assertEqual(original, brief.read_bytes())
        for slug in ('../escape', '/absolute', 'a/b', 'a;touch', '$(touch)', 'Upper', '-leading', ''):
            with self.subTest(slug=slug), self.assertRaises(ValueError):
                studio.init_project(slug, 'heuro', self.root / 'projects')
        self.assertFalse((self.root / 'escape').exists())

    def test_pack_without_private_context_is_honest_and_does_not_submit(self):
        before = (self.project / 'provider-jobs.json').read_bytes()
        output = studio.build_pack(self.project, self.context)
        self.assertTrue((output / 'production.md').exists())
        self.assertIn('identity name unresolved', (output / 'synthesia.md').read_text())
        self.assertIn('unverified', (output / 'synthesia.md').read_text())
        report = studio.project_status(self.project, self.context)
        self.assertFalse(report['local_plan_complete'])
        self.assertFalse(report['provider_ready'])
        self.assertTrue(any('No private preference' in x for x in report['warnings']))
        self.assertEqual(before, (self.project / 'provider-jobs.json').read_bytes())

    def test_job_round_trip_duplicate_guard_and_update_preserve_handle(self):
        handle = 'workspace-123:conversation-456'
        studio.record_job(self.project, 'synthesia', 'job-123', 'running', handle, 'https://example.test/project/123')
        original = (self.project / 'provider-jobs.json').read_bytes()
        with self.assertRaises(ValueError):
            studio.record_job(self.project, 'synthesia', 'job-456', 'running')
        self.assertEqual(original, (self.project / 'provider-jobs.json').read_bytes())
        record = studio.record_job(self.project, 'synthesia', 'job-123', 'done')
        self.assertEqual(record['conversation_id'], handle)
        self.assertEqual(record['url'], 'https://example.test/project/123')
        studio.record_job(self.project, 'synthesia', 'job-456', 'running')
        report = studio.project_status(self.project, self.context)
        self.assertEqual(len(report['in_flight_jobs']), 1)
        self.assertEqual(report['in_flight_jobs'][0]['job_id'], 'job-456')

    def test_ledger_rejects_download_tokens_and_credentials(self):
        for url in ('https://example.test/project?token=secret', 'https://user:password@example.test/project',
                    'https://example.test/api/blob/private', 'http://example.test/project'):
            with self.subTest(url=url), self.assertRaises(ValueError):
                studio.record_job(self.project, 'google', 'job-1', 'running', url=url)
        with self.assertRaises(ValueError):
            studio.record_job(self.project, 'google', 'sk-do-not-store', 'running')
        ledger = {'version': 1, 'jobs': [{'provider': 'google', 'job_id': 'j-1', 'state': 'running',
                   'conversation_id': '', 'url': '', 'api_key': 'should-never-be-here'}]}
        (self.project / 'provider-jobs.json').write_text(json.dumps(ledger))
        with self.assertRaises(ValueError):
            studio.build_pack(self.project, self.context)

    def test_complete_local_plan_remains_distinct_from_provider_readiness(self):
        brief = studio.read_json(self.project / 'brief.json')
        brief.update(audience='Example audience', goal='Educate', language='English', message='One useful idea',
                     cta='Learn more', script='An explicitly supplied example script.', duration_seconds=5,
                     avatar_id='avatar-confirmed', voice_id='voice-confirmed', budget={'max': 10, 'currency': 'USD'})
        studio.write_json(self.project / 'brief.json', brief)
        rows = [dict(zip(studio.SHOT_FIELDS, ('1','0','5','speaking','Supplied narration','Static frame','')))]
        studio.write_csv(self.project / 'storyboard.csv', studio.SHOT_FIELDS, rows)
        studio.write_csv(self.project / 'assets.csv', studio.ASSET_FIELDS,
                         [dict(zip(studio.ASSET_FIELDS, ('ref-1','portrait','private-store:ref-1','checksum','own asset','ready')))])
        report = studio.project_status(self.project, self.context)
        self.assertTrue(report['local_plan_complete'])
        self.assertFalse(report['provider_ready'])
        self.assertEqual(report['routes'], [{'shot_id': '1', 'kind': 'speaking', 'provider': 'synthesia'}])

    def test_malformed_csv_and_unsupported_shots_are_visible(self):
        (self.project / 'storyboard.csv').write_text('wrong,columns\n1,2\n')
        with self.assertRaises(ValueError):
            studio.project_status(self.project, self.context)

    def test_track_context_is_carried_to_all_prompts_without_other_track_leakage(self):
        (self.context / 'persona.md').write_text('PERSONAL_ONLY_BACKGROUND')
        (self.context / 'heuro.md').write_text('PRODUCT_ONLY_BASELINE')
        (self.context / 'product-context.md').write_text('PRODUCT_ONLY_EXPANDED')
        (self.context / 'source-register.json').write_text('{"sources": []}')
        (self.context / 'preferences.json').write_text(json.dumps({'confirmed': {'synthesia_identity_name': 'Example own identity'}, 'unresolved': {}}))
        out = studio.build_pack(self.project, self.context)
        for filename in ('production.md', 'synthesia.md', 'google-scenes.md', 'descript-edit.md'):
            text = (out / filename).read_text()
            self.assertIn('PERSONAL_ONLY_BACKGROUND', text)
            self.assertNotIn('PRODUCT_ONLY', text)
            self.assertIn('source-register.json', text)
        text = (out / 'synthesia.md').read_text()
        self.assertIn('Example own identity', text)
        self.assertIn('avatar ID: unverified', text)
        self.assertIn('voice ID: unverified', text)
        brief = studio.read_json(self.project / 'brief.json')
        brief['track'] = 'heuro'
        studio.write_json(self.project / 'brief.json', brief)
        out = studio.build_pack(self.project, self.context)
        for filename in ('production.md', 'synthesia.md', 'google-scenes.md', 'descript-edit.md'):
            text = (out / filename).read_text()
            self.assertIn('PRODUCT_ONLY_BASELINE', text)
            self.assertIn('PRODUCT_ONLY_EXPANDED', text)
            self.assertNotIn('PERSONAL_ONLY_BACKGROUND', text)

    def test_finite_duration_and_single_track_timeline_coverage(self):
        brief = studio.read_json(self.project / 'brief.json')
        for value in (True, float('nan'), float('inf'), 0, -1):
            with self.subTest(duration=value):
                brief['duration_seconds'] = value
                studio.write_json(self.project / 'brief.json', brief)
                report = studio.project_status(self.project, self.context)
                self.assertIn('positive duration_seconds', report['missing_brief_fields'])
        brief['duration_seconds'] = 10
        studio.write_json(self.project / 'brief.json', brief)
        def issues(second_start, second_duration):
            rows = [dict(zip(studio.SHOT_FIELDS, ('1', '0', '5', 'speaking', 'One', '', ''))),
                    dict(zip(studio.SHOT_FIELDS, ('2', str(second_start), str(second_duration), 'speaking', 'Two', '', '')))]
            studio.write_csv(self.project / 'storyboard.csv', studio.SHOT_FIELDS, rows)
            return studio.project_status(self.project, self.context)['storyboard_issues']
        self.assertTrue(any('gap' in issue for issue in issues(6, 4)))
        self.assertTrue(any('overlap' in issue for issue in issues(4, 6)))
        self.assertEqual(issues(5.00000001, 4.99999999), [])
        self.assertTrue(any('invalid start/duration' in issue for issue in issues(float('nan'), 5)))


if __name__ == '__main__':
    unittest.main()
