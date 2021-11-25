from unittest import TestCase
from pathlib import Path
import unittest

from quran import ayeh_extractor


class VerseExtractionTest(TestCase):

    def test_extraction(self):
        tests_dir = Path('tests')
        for i in range(1, len(list((tests_dir / 'in').iterdir())) + 1):
            text_in = (tests_dir / 'in' / f'input{i}.txt').read_text(encoding="utf-8")
            test_out = (tests_dir / 'out' / f'output{i}.txt').read_text(encoding="utf-8").strip().split('\n')
            if test_out == ['']:
                test_out = []
            with self.subTest(test=f"Test#{i}"):
                func_out = ayeh_extractor(text_in)
                self.assertListEqual(func_out, test_out)


if __name__ == "__main__":
    unittest.main()
