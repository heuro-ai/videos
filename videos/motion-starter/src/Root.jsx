import React from 'react';
import {Composition} from 'remotion';
import {LaunchFilm} from './LaunchFilm';

export const Root = () => (
  <>
    <Composition
      id="LaunchLandscape"
      component={LaunchFilm}
      width={1920}
      height={1080}
      fps={30}
      durationInFrames={540}
      defaultProps={{
        brand: 'YOUR BRAND',
        headline: 'From complexity.\nTo clarity.',
        supportingLine: 'One clear story. Real product proof.',
        cta: 'Explore what comes next.',
        accent: '#a9c7a1',
        founderName: 'Founder',
        founderRole: 'Your company',
        productClip: '',
        founderClip: '',
        voiceover: '',
        founderMuted: false,
        demoMode: true,
      }}
    />
    <Composition
      id="LaunchVertical"
      component={LaunchFilm}
      width={1080}
      height={1920}
      fps={30}
      durationInFrames={540}
      defaultProps={{
        brand: 'YOUR BRAND',
        headline: 'From complexity.\nTo clarity.',
        supportingLine: 'One clear story. Real product proof.',
        cta: 'Explore what comes next.',
        accent: '#a9c7a1',
        founderName: 'Founder',
        founderRole: 'Your company',
        productClip: '',
        founderClip: '',
        voiceover: '',
        founderMuted: false,
        demoMode: true,
      }}
    />
  </>
);
