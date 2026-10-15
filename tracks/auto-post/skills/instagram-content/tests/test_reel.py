"""Observable Reel delivery invariants, including a copied global installation."""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from PIL import Image, ImageChops

SKILL=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(SKILL/'scripts'))
import run_reel as harness


class ReelTests(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory(prefix='reel-harness-')
        self.addCleanup(temp.cleanup)
        self.root=Path(temp.name)
        self.manifest,self.brief_path=self.root/'episode.json',self.root/'brief.json'
        self.post=json.loads((SKILL/'references/reel.example.json').read_text())
        self.brief=json.loads((SKILL/'references/reel-brief.example.json').read_text())
        self.post['demo']=False
        self.post['scenes']=self.post['scenes'][:1]
        self.post['scenes'][0]['duration']=.6
        self.brief['deliverable'].update(width=360,height=640,min_short_side=360,fps=10,duration_seconds=.6,min_scene_seconds=.1)
        self.args=argparse.Namespace(manifest=self.manifest,brief=self.brief_path,out=self.root/'out',validate_only=False,overwrite=False,font_regular=None,font_bold=None,font_dir=None,ffmpeg='ffmpeg',ffprobe='ffprobe')

    def save(self):
        self.manifest.write_text(json.dumps(self.post,ensure_ascii=False))
        self.brief_path.write_text(json.dumps(self.brief,ensure_ascii=False))

    def fonts(self):
        return harness.common.find_fonts(self.args,{'slides':self.post['scenes']})

    def test_exact_resolution_aspect_duration_and_no_audio_policy(self):
        cases=[({'width':1080,'height':1920,'min_short_side':2048},'min_short_side'),
               ({'width':2160,'height':3838},'9:16'),
               ({'duration_seconds':1},'durations'),
               ({'audio':'muted'},'audio: none'),
               ({'fps':True},'integer'),
               ({'fps':float('nan')},'integer')]
        original=deepcopy(self.brief['deliverable'])
        for changes,error in cases:
            with self.subTest(changes=changes):
                self.brief['deliverable']={**original,**changes}
                self.save()
                with self.assertRaisesRegex(ValueError,error):
                    harness.preflight(self.manifest,self.brief_path)

    def test_caption_boundary_acknowledgement_korean_tags_and_url_fragment(self):
        self.brief['caption_policy']={'max_characters':499,'hashtag_count':3}
        self.brief['acknowledgement']='Credit'
        tail=' #AI뉴스 #로봇 #치와와 https://example.com/#anchor'
        self.post['caption']='가'*(490-len(tail))+tail
        self.save()
        _,_,caption,report=harness.preflight(self.manifest,self.brief_path)
        self.assertEqual(len(caption),499)
        self.assertEqual(report['hashtags'],3)
        self.post['caption']='가'+self.post['caption']
        self.save()
        with self.assertRaisesRegex(ValueError,'500 characters'):
            harness.preflight(self.manifest,self.brief_path)
        self.assertFalse(self.args.out.exists())

    def test_news_dates_and_claim_references(self):
        self.post['content_type']='news'
        self.post['sources']=[{'id':'primary','publisher':'Publisher','title':'Announcement','url':'https://example.com/news','published_at':'2026-10-14T10:00:00+09:00','checked_at':'2026-10-15T12:00:00+09:00'}]
        self.post['freshness']={'reference_time':'2026-10-15T12:00:00+09:00','max_age_hours':48}
        scene=self.post['scenes'][0]
        scene['requires_sources']=True
        self.save()
        with self.assertRaisesRegex(ValueError,'connect claims'):
            harness.preflight(self.manifest,self.brief_path)
        scene.update(source_ids=['primary'],evidence_note='Supporting passage from original announcement')
        self.save()
        harness.preflight(self.manifest,self.brief_path)
        self.post['sources'][0]['published_at']='2026-10-11T10:00:00+09:00'
        self.save()
        with self.assertRaisesRegex(ValueError,'freshness window'):
            harness.preflight(self.manifest,self.brief_path)
        self.post['sources'][0]['published_at']='2026-10-16T10:00:00+09:00'
        self.save()
        with self.assertRaisesRegex(ValueError,'later than'):
            harness.preflight(self.manifest,self.brief_path)

    def test_validate_only_needs_no_ffmpeg_or_fonts_and_never_rewrites_copy(self):
        self.post['scenes'][0]['title']=['A title.']
        self.post['scenes'][0]['visual']['value']='3.5%'
        self.post['caption']='Short opening\n\nSentence one. Sentence two.'
        self.args.validate_only=True
        self.args.ffmpeg='not-installed'
        self.save()
        before=self.manifest.read_bytes()
        report=harness.run(self.args)
        self.assertFalse(report['exports_verified'])
        self.assertTrue(report['punctuation_review'])
        self.assertEqual(self.manifest.read_bytes(),before)
        self.assertFalse(self.args.out.exists())

    def test_motion_changes_graphic_while_explanation_stays_fixed(self):
        example=json.loads((SKILL/'references/reel.example.json').read_text())
        self.post['scenes']=[example['scenes'][2]]
        self.post['scenes'][0]['duration']=6
        self.brief['deliverable']['duration_seconds']=6
        self.save()
        post,brief,_,_=harness.preflight(self.manifest,self.brief_path)
        renderer=harness.Renderer(post,brief,self.fonts())
        before=renderer.frame(0,1)
        hidden=renderer.frame(0,30)
        crop=lambda a,b:tuple(round(v*renderer.scale) for v in (renderer.x(.02),renderer.y(a),renderer.x(.98),renderer.y(b)))
        self.assertIsNotNone(ImageChops.difference(before.crop(crop(.33,.785)),hidden.crop(crop(.33,.785))).getbbox())
        self.assertIsNone(ImageChops.difference(before.crop(crop(.80,.925)),hidden.crop(crop(.80,.925))).getbbox())
        self.assertEqual(before.size,(360,640))

    @unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'),'FFmpeg required')
    def test_render_failure_preserves_delivery_and_unrelated_files(self):
        self.args.out.mkdir()
        (self.args.out/'reel.mp4').write_bytes(b'previous delivery')
        (self.args.out/'keep.txt').write_text('unrelated')
        self.args.overwrite=True
        self.post['scenes'][0]['title']=['Much too long '*15]
        self.save()
        with self.assertRaisesRegex(ValueError,'safe area|region'):
            harness.run(self.args)
        self.assertEqual((self.args.out/'reel.mp4').read_bytes(),b'previous delivery')
        self.assertEqual((self.args.out/'keep.txt').read_text(),'unrelated')
        self.assertEqual(list(self.root.glob('.reel-*')),[])

    @unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'),'FFmpeg required')
    def test_native_4k_output_and_encoded_metadata(self):
        self.brief['deliverable'].update(width=2160,height=3840,min_short_side=2048)
        self.save()
        report=harness.run(self.args)
        self.assertTrue(report['exports_verified'])
        self.assertTrue(report['native_text_and_geometry'])
        self.assertEqual(report['dimensions'],[2160,3840])
        self.assertEqual(report['audio_streams'],0)
        self.assertEqual(report['frames'],6)
        with Image.open(self.args.out/'cover.jpg') as image:
            self.assertEqual(image.size,(2160,3840))
        sl,st,sr,sb=report['safe_area_pixels']
        for item in report['layout_bounds']:
            l,t,r,b=item['pixels']
            self.assertTrue(sl<=l<=r<=sr and st<=t<=b<=sb,item)

    @unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'),'FFmpeg required')
    def test_copied_skill_decodes_relative_video_and_removes_source_audio(self):
        media=self.root/'assets'; media.mkdir()
        source=media/'source.mp4'
        subprocess.run(['ffmpeg','-y','-v','error','-f','lavfi','-i','color=c=red:s=320x180:r=10:d=0.6','-f','lavfi','-i','sine=frequency=440:sample_rate=8000:duration=0.6','-c:v','libx264','-threads','1','-pix_fmt','yuv420p','-c:a','aac','-shortest',str(source)],check=True)
        self.assertEqual(len(harness.probe(source,'ffprobe')['streams']),2)
        scene=self.post['scenes'][0]
        scene.update(layout='media',visual={'label':'Local video'},media={'kind':'video','path':'assets/source.mp4','credit':'Test fixture','usage_note':'Synthetic owned video with tone'})
        self.save()
        fonts=self.fonts()
        copied=self.root/'installed'/'instagram-content'
        shutil.copytree(SKILL,copied)
        unrelated=self.root/'other-project'; unrelated.mkdir()
        cmd=[sys.executable,'-B',str(copied/'scripts/run_reel.py'),str(self.manifest),'--brief',str(self.brief_path),'--out',str(self.args.out),'--font-regular',str(fonts['regular']),'--font-bold',str(fonts['bold'])]
        result=subprocess.run(cmd,cwd=unrelated,capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        report=json.loads(result.stdout)
        self.assertEqual(report['audio_streams'],0)
        self.assertEqual(report['media'][0]['source_dimensions'],[320,180])
        self.assertIn('Synthetic owned video',(self.args.out/'sources.md').read_text())
        # A failed source range also leaves the earlier package intact.
        original=(self.args.out/'reel.mp4').read_bytes()
        scene['media']['start']=10
        self.save(); self.args.overwrite=True
        with self.assertRaisesRegex(ValueError,'source range'):
            harness.run(self.args)
        self.assertEqual((self.args.out/'reel.mp4').read_bytes(),original)


if __name__=='__main__':
    unittest.main()
