from unittest import TestCase
from pathlib import Path
import unittest

from quran import ayeh_extractor

class VerseExtractionTest(TestCase):

    def test_extraction(self):
        tests_dir=Path('tests')
        for i in range(1,len(list((tests_dir / 'in').iterdir()))+1):
            input=(tests_dir / 'in' / f'input{i}.txt').read_text(encoding="utf-8")
            output=(tests_dir / 'out' / f'output{i}.txt').read_text(encoding="utf-8").split()
            with self.subTest(test=f"Test#{i}"):
                self.assertListEqual(ayeh_extractor(input), output)


if __name__ == "__main__":
    unittest.main()