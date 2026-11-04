"""Exercise real local recompression and preservation of the accepted master."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from PIL import Image

SKILL=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(SKILL/'scripts'))
import preview_recompression as review


@unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'),'FFmpeg required')
class RecompressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture=tempfile.TemporaryDirectory(prefix='recompression-master-')
        cls.master=Path(cls.fixture.name)/'master.mp4'
        subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','testsrc2=size=1080x1920:rate=10',
                        '-vf','setparams=range=tv:color_primaries=bt709:color_trc=bt709:colorspace=bt709',
                        '-frames:v','4','-c:v','libx264','-preset','ultrafast','-threads','2',
                        '-pix_fmt','yuv420p','-color_range','tv','-colorspace','bt709',
                        '-color_primaries','bt709','-color_trc','bt709',str(cls.master)],check=True)

    @classmethod
    def tearDownClass(cls):
        cls.fixture.cleanup()

    def setUp(self):
        temp=tempfile.TemporaryDirectory(prefix='recompression-test-')
        self.addCleanup(temp.cleanup)
        self.root=Path(temp.name)
        self.args=argparse.Namespace(video=self.master,out=self.root/'review',at=[.1],
                                     overwrite=False,ffmpeg='ffmpeg',ffprobe='ffprobe')

    def test_copied_skill_encodes_two_previews_and_preserves_source(self):
        original=review.digest(self.master)
        installed=self.root/'installed-skill'
        shutil.copytree(SKILL,installed,ignore=shutil.ignore_patterns('__pycache__'))
        result=subprocess.run([sys.executable,'-B',str(installed/'scripts/preview_recompression.py'),str(self.master),
                               '--out',str(self.args.out),'--at','.1'],cwd=self.root,capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        report=json.loads((self.args.out/'review-report.json').read_text())
        self.assertEqual(review.digest(self.master),original)
        self.assertEqual(report['source']['sha256'],original)
        self.assertTrue(report['source_preserved'])
        self.assertEqual(report['manual_visual_review'],'pending')
        self.assertFalse(report['actual_instagram_result_verified'])
        self.assertEqual([v['dimensions'] for v in report['variants']],[[1080,1920],[720,1280]])
        self.assertEqual(report['variants'][1]['input'],'review-only-1080p.mp4')
        for variant in report['variants']:
            self.assertTrue(variant['measured']['decode_verified'])
            streams=review.probe(self.args.out/variant['file'],'ffprobe')['streams']
            self.assertEqual(len(streams),1)
            self.assertEqual(int(streams[0]['nb_frames']),4)
        with Image.open(self.args.out/'comparison.jpg') as sheet:
            self.assertEqual(sheet.size,(1080,716))

    def test_occupied_output_and_failed_encode_preserve_previous_files(self):
        self.args.out.mkdir()
        previous=self.args.out/'review-only-1080p.mp4'
        previous.write_bytes(b'previous review')
        with self.assertRaisesRegex(ValueError,'not empty'):
            review.run(self.args)
        self.args.overwrite=True
        self.args.ffmpeg='false'
        with self.assertRaises(subprocess.CalledProcessError):
            review.run(self.args)
        self.assertEqual(previous.read_bytes(),b'previous review')
        self.assertEqual(list(self.root.glob('.recompression-*')),[])

    def test_invalid_timestamps_and_source_overlap_write_nothing(self):
        for times in ([.4],[-1],[float('nan')],[]):
            self.args.at=times
            with self.assertRaisesRegex(ValueError,'timestamps'):
                review.run(self.args)
            self.assertFalse(self.args.out.exists())
        self.args.out=self.master.parent
        with self.assertRaisesRegex(ValueError,'outside'):
            review.run(self.args)

    def test_audio_is_rejected_instead_of_silently_removed(self):
        audible=self.root/'audible.mp4'
        subprocess.run(['ffmpeg','-v','error','-i',str(self.master),'-f','lavfi',
                        '-i','sine=frequency=440:duration=0.4','-map','0:v','-map','1:a','-c:v','copy',
                        '-c:a','aac','-shortest',str(audible)],check=True)
        self.args.video=audible
        with self.assertRaisesRegex(ValueError,'zero audio'):
            review.run(self.args)
        self.assertFalse(self.args.out.exists())


if __name__=='__main__':
    unittest.main()
