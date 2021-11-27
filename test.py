from unittest import TestCase
from pathlib import Path
import unittest

from quran import ayeh_extractor


class VerseExtractionTest(TestCase):

    def test_extraction(self):
        tests_dir = Path('tests')
        for i in range(1, len(list((tests_dir / 'in').iterdir())) + 1):
            test_in = (tests_dir / 'in' / f'input{i}.txt').read_text(encoding="utf-8")
            test_out = (tests_dir / 'out' / f'output{i}.txt').read_text(encoding="utf-8").strip().split('\n')
            if test_out == ['']:
                test_out = []
            with self.subTest(test=f"Test#{i}"):
                func_out = ayeh_extractor(test_in)
                self.assertSetEqual(set(func_out), set(test_out))
    
    #python3 test.py VerseExtractionTest.test_coverage
    def test_coverage(self):
        test_in= (Path('tests')/'in'/'input20.txt').read_text(encoding='utf-8')
        test_out = (Path('tests') / 'out' / 'output20.txt').read_text(encoding="utf-8").strip().split('\n')
        if test_out == ['']:
                test_out = []
        func_out = ayeh_extractor(test_in)
        self.assertSetEqual(set(func_out),set(test_out))


if __name__ == "__main__":
    unittest.main()
