import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'click_log_data/CleanData/cleanData.py'
spec = importlib.util.spec_from_file_location('clean_data', SCRIPT)
clean = importlib.util.module_from_spec(spec)
spec.loader.exec_module(clean)


class CleanerTests(unittest.TestCase):
    def sample(self):
        return {'adId': 7, 'title': '  Runner\'s,   Shoe. ', 'query': ' SHOES ',
                'brand': "Runner's", 'keyWords': ['shoe'], 'price': 12.5,
                'category': None, 'active': True}

    def test_normalization(self):
        result = clean.normalize(self.sample())
        self.assertEqual(result['title'], 'runners shoe')
        self.assertEqual(result['query'], 'shoes')
        self.assertEqual(result['brand'], 'Runners')
        self.assertEqual(result['keyWords'], ['shoe', 'runners'])

    def test_preserves_business_values(self):
        result = clean.normalize(self.sample())
        for key in ('adId', 'price', 'category', 'active'):
            self.assertEqual(result[key], self.sample()[key])

    def test_deterministic_and_non_mutating(self):
        record = self.sample()
        before = json.dumps(record)
        self.assertEqual(clean.normalize(record), clean.normalize(record))
        self.assertEqual(json.dumps(record), before)

    def test_rejects_bad_shapes(self):
        for record in ([], {}, {'title': None}, dict(self.sample(), keyWords=[1])):
            with self.subTest(record=record), self.assertRaises(ValueError):
                clean.normalize(record)

    def test_unicode_json_round_trip(self):
        record = dict(self.sample(), title='跑步鞋', note='quote " slash \\ newline\n')
        with tempfile.TemporaryDirectory() as tmp:
            source, dest = Path(tmp)/'in', Path(tmp)/'out'
            source.write_text(json.dumps(record), encoding='utf-8')
            self.assertEqual(clean.convert(source, dest), 1)
            self.assertEqual(json.loads(dest.read_text())['note'], record['note'])

    def test_invalid_record_has_no_partial_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, dest = Path(tmp)/'in', Path(tmp)/'out'
            source.write_text(json.dumps(self.sample()) + '\nnot json\n')
            with self.assertRaisesRegex(ValueError, 'line 2'):
                clean.convert(source, dest)
            self.assertFalse(dest.exists())
            self.assertEqual(sorted(p.name for p in Path(tmp).iterdir()), ['in'])

    def test_existing_output_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp)/'out'
            dest.write_text('original')
            with self.assertRaises(ValueError):
                clean.convert(Path(tmp)/'missing', dest)
            self.assertEqual(dest.read_text(), 'original')

    def test_rejects_nonfinite_numbers(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, dest = Path(tmp)/'in', Path(tmp)/'out'
            source.write_text(json.dumps(dict(self.sample(), price=float('nan'))))
            with self.assertRaises(ValueError):
                clean.convert(source, dest)
            self.assertFalse(dest.exists())

    def test_cli(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, dest = Path(tmp)/'in', Path(tmp)/'out'
            source.write_text('\n' + json.dumps(self.sample()) + '\n')
            proc = subprocess.run([sys.executable, str(SCRIPT), '--input', str(source),
                                   '--output', str(dest)], capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertEqual(json.loads(proc.stdout)['records_written'], 1)


if __name__ == '__main__':
    unittest.main()
