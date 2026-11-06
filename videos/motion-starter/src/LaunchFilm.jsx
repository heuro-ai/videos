import React from 'react';
import {AbsoluteFill, Sequence, interpolate, Easing, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {Video, Audio} from '@remotion/media';

const ease = Easing.bezier(0.16, 1, 0.3, 1);
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease};
const media = (file) => {
  if (!file || /^(https?:|data:|blob:)/i.test(file)) throw new Error('Use a local public/ media path.');
  return staticFile(file);
};

function Scene({children, seconds}) {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return <AbsoluteFill style={{opacity: interpolate(frame, [0, 0.45 * fps, (seconds - 0.45) * fps, seconds * fps], [0, 1, 1, 0], clamp)}}>{children}</AbsoluteFill>;
}

function Title({text, small = false, color = '#f5f2eb'}) {
  const frame = useCurrentFrame();
  const {fps, width} = useVideoConfig();
  const vertical = width < 1200;
  return <div style={{fontSize: small ? (vertical ? 86 : 88) : (vertical ? 108 : 134), lineHeight: 1.01, letterSpacing: '-0.065em', fontWeight: 500, whiteSpace: 'pre-line', color, opacity: interpolate(frame, [0.2 * fps, 1.1 * fps], [0, 1], clamp), translate: `0 ${interpolate(frame, [0.2 * fps, 1.2 * fps], [55, 0], clamp)}px`}}>{text}</div>;
}

function SpatialCards({accent}) {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return <div style={{position: 'relative', width: 650, height: 450, perspective: 1400}}>
    {[0, 1, 2].map((index) => <div key={index} style={{position: 'absolute', inset: 28, borderRadius: 30, border: '1px solid rgba(230,240,228,0.2)', background: index === 2 ? 'linear-gradient(145deg,#28332d,#131a17)' : 'rgba(105,136,110,0.12)', boxShadow: '0 32px 80px rgba(0,0,0,0.16)', opacity: interpolate(frame, [(0.25 + index * 0.12) * fps, (1.3 + index * 0.12) * fps], [0, 1], clamp), transform: `translate3d(${index * 32}px,${index * -28 + interpolate(frame, [0, 2 * fps], [70, 0], clamp)}px,${index * 48}px) rotateY(-19deg) rotateX(12deg)`}}>
      {index === 2 && <div style={{padding: 40}}>
        <div style={{fontSize: 18, letterSpacing: '0.16em', color: accent}}>SPATIAL LAYOUT STUDY</div>
        <svg width="480" height="230" viewBox="0 0 480 230" style={{marginTop: 25}}>
          <path d="M20 155 L140 55 L260 116 L444 25 M140 55 L180 204 L360 174 L444 25 M20 155 L180 204 M260 116 L360 174" stroke={accent} strokeWidth="1.5" fill="none" opacity="0.5"/>
          {[[20,155],[140,55],[260,116],[444,25],[180,204],[360,174]].map(([x,y],i) => <g key={i}><circle cx={x} cy={y} r="13" fill={accent} opacity="0.14"/><circle cx={x} cy={y} r="4" fill={accent}/></g>)}
        </svg>
        <div style={{fontSize: 17, letterSpacing: '0.13em', color: '#a3aca6'}}>SYNTHETIC GEOMETRY · NO PRODUCT DATA</div>
      </div>}
    </div>)}
  </div>;
}

function ProductScene({productClip, demoMode, accent}) {
  const {width, fps} = useVideoConfig();
  const vertical = width < 1200;
  const frame = useCurrentFrame();
  return <AbsoluteFill style={{padding: vertical ? '160px 90px' : '115px 135px', gap: 55}}>
    <div style={{fontSize: 22, letterSpacing: '0.2em', color: accent}}>02 / PRODUCT PROOF</div>
    <Title text={'See the real thing.'} small />
    <div style={{flex: 1, minHeight: 0, borderRadius: 28, overflow: 'hidden', border: '1px solid #4c5d50', background: '#151e19', boxShadow: '0 40px 100px #0008', opacity: interpolate(frame, [0.4 * fps, 1.3 * fps], [0, 1], clamp), transform: `perspective(2200px) rotateX(${interpolate(frame, [0, 2 * fps], [7, 0], clamp)}deg)`, position: 'relative'}}>
      {productClip ? <Video src={media(productClip)} muted objectFit="contain" style={{width: '100%', height: '100%'}}/> : <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', gap: 40}}>
        <div style={{width: '70%', height: '48%', border: '1px solid #526a57', borderRadius: 18, display: 'flex', gap: 24, padding: 28}}>
          <div style={{width: '22%', background: '#2d3d31', borderRadius: 10}}/>
          <div style={{flex: 1, display: 'grid', gridTemplateRows: '1fr 2fr', gap: 22}}><div style={{background: '#28372d', borderRadius: 10}}/><div style={{border: '1px dashed #526a57', borderRadius: 10}}/></div>
        </div>
        <div style={{fontSize: vertical ? 34 : 32, textAlign: 'center', color: '#c3cec4', maxWidth: '80%'}}>Replace with a real product screen recording.</div>
        <div style={{fontSize: 19, letterSpacing: '0.13em', color: accent}}>LAYOUT DEMO · NOT PRODUCT DATA</div>
      </AbsoluteFill>}
      {demoMode && productClip && <div style={{position: 'absolute', left: 24, bottom: 24, fontSize: 18, background: '#101713d9', padding: '10px 16px', borderRadius: 8}}>SUPPLIED PRODUCT FOOTAGE</div>}
    </div>
  </AbsoluteFill>;
}

function FounderScene({founderClip, founderName, founderRole, accent, voiceover, founderMuted = false}) {
  const {width} = useVideoConfig();
  const vertical = width < 1200;
  return <AbsoluteFill style={{padding: vertical ? '145px 90px' : '120px 135px', flexDirection: vertical ? 'column' : 'row', gap: vertical ? 55 : 110, alignItems: 'center', justifyContent: vertical ? 'center' : undefined}}>
    <div style={{flex: vertical ? '0 0 auto' : 1, width: '100%'}}><div style={{fontSize: 22, letterSpacing: '0.18em', color: accent, marginBottom: 38}}>03 / THE HUMAN BEHIND IT</div><Title text={'Built with intent.\nTold by its founder.'} small/><div style={{marginTop: 44, fontSize: 28, color: '#aebcb0'}}>{founderName}<span style={{color: '#607265'}}> / </span>{founderRole}</div></div>
    <div style={{width: vertical ? '100%' : 680, height: vertical ? 830 : '100%', position: 'relative', border: '1px solid #415346', borderRadius: 28, background: 'radial-gradient(ellipse at 50% 30%,#3a4b3b,#17231b 70%)', overflow: 'hidden'}}>
      {founderClip ? <Video src={media(founderClip)} muted={Boolean(voiceover) || founderMuted} objectFit="contain" style={{width: '100%', height: '100%'}}/> : <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', textAlign: 'center', padding: 70, gap: 28}}><div style={{width: 90, height: 90, border: '1px solid #9ab394', borderRadius: '50%', display: 'grid', placeItems: 'center', fontSize: 35, color: accent}}>↗</div><div style={{fontSize: 36, lineHeight: 1.2}}>Your real founder clip belongs here.</div><div style={{fontSize: 18, letterSpacing: '0.13em', color: accent}}>FOOTAGE PLACEHOLDER</div></AbsoluteFill>}
    </div>
  </AbsoluteFill>;
}

export function LaunchFilm(props) {
  const {fps, width} = useVideoConfig();
  const vertical = width < 1200;
  const {brand, headline, supportingLine, cta, accent, productClip, founderClip, voiceover, demoMode} = props;
  if (!demoMode && (!productClip || !founderClip)) throw new Error('Production mode requires real productClip and founderClip; demo placeholders cannot ship.');
  return <AbsoluteFill style={{background: '#101713', color: '#f5f2eb', fontFamily: 'Arial, Helvetica, sans-serif', overflow: 'hidden'}}>
    <AbsoluteFill style={{background: 'radial-gradient(ellipse at 80% 20%,#30463455,transparent 64%),linear-gradient(130deg,#0e1510,#19251d)'}}/>
    <AbsoluteFill style={{backgroundImage: 'linear-gradient(#8fa58d0a 1px, transparent 1px),linear-gradient(90deg,#8fa58d0a 1px,transparent 1px)', backgroundSize: '90px 90px'}}/>
    <Sequence name="Opening thesis" from={0} durationInFrames={4.5 * fps}>
      <Scene seconds={4.5}><AbsoluteFill style={{padding: vertical ? '185px 90px' : '180px 135px', flexDirection: vertical ? 'column' : 'row', alignItems: vertical ? 'flex-start' : 'center', gap: vertical ? 100 : 80, justifyContent: vertical ? 'center' : undefined}}>
        <div style={{flex: vertical ? '0 0 auto' : 1, minWidth: 0, zIndex: 2}}><div style={{fontSize: 22, letterSpacing: '0.22em', color: accent, marginBottom: 65}}>{brand}</div><Title text={headline}/><div style={{marginTop: 45, fontSize: vertical ? 38 : 34, color: '#afbcaf', lineHeight: 1.3, maxWidth: 620}}>{supportingLine}</div></div>
        <div style={{scale: vertical ? 1.15 : 1, width: 650, height: 450, marginLeft: vertical ? 25 : 0}}><SpatialCards accent={accent}/></div>
      </AbsoluteFill></Scene>
    </Sequence>
    <Sequence name="Real product demonstration" from={4 * fps} durationInFrames={6.5 * fps}><Scene seconds={6.5}><ProductScene {...props}/></Scene></Sequence>
    <Sequence name="Founder footage" from={10 * fps} durationInFrames={5.5 * fps}><Scene seconds={5.5}><FounderScene {...props}/></Scene></Sequence>
    <Sequence name="Brand close" from={15 * fps} durationInFrames={3 * fps}><Scene seconds={3}><AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', padding: vertical ? 90 : 135, textAlign: 'center', gap: 45}}><div style={{fontSize: 22, color: accent, letterSpacing: '0.22em'}}>{brand}</div><Title text={cta}/><div style={{height: 2, width: 140, background: accent, marginTop: 25}}/></AbsoluteFill></Scene></Sequence>
    {voiceover && <Audio src={media(voiceover)} volume={0.8}/>}
    {demoMode && <div style={{position: 'absolute', bottom: vertical ? 70 : 50, left: vertical ? 90 : 135, right: vertical ? 90 : 135, fontSize: 17, letterSpacing: '0.17em', color: '#9daf9e'}}>MOTION TEMPLATE DEMO · PLACEHOLDERS ARE NOT PRODUCT CLAIMS</div>}
  </AbsoluteFill>;
}
