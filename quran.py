import json
import re

from unittest import TestCase

with open('quran_prep.json') as fp:
    verses = json.load(fp)

with open('analysis.json') as fp:
    analysis_data = json.load(fp)

with open('word_codes.json') as fp:
    words_map = json.load(fp)
UNK_C = words_map['[UNK]']

with open('words.txt') as fp:
    words = [line.strip() for line in fp.readlines()]

with open('verse_index.json') as fp:
    index = json.load(fp)


def normalize_text(text):
    text = re.sub(r'[' + analysis_data['pun'] + ']', '', text)
    text = re.sub(r'[\s]+', ' ', text)
    text = re.sub(r'[و]\s', 'و', text)
    for key, val in analysis_data['repl'].items():
        text = re.sub(r'[' + key + ']', val, text)
    return text


def encode_text(text):
    seq_wo = text.split(' ')
    seq_id = encode_seq(seq_wo)
    return seq_id


def encode_seq(seq_wo):
    return [words_map[w] if w in words_map else words_map['[UNK]'] for w in seq_wo]


def get_known_parts(seq_id):
    part_start = 0
    last_part_end=-1
    while part_start < len(seq_id):
        if seq_id[part_start] != UNK_C:
            running_intersection_of_ayehs=set()
            part_end = part_start
            while part_end < len(seq_id) and seq_id[part_end] != UNK_C:
                running_intersection_of_ayehs=running_intersection_of_ayehs | set(index[str(seq_id[part_end])])
                if not running_intersection_of_ayehs:
                    part_end-=1
                    break
                else:
                    part_end += 1
            if part_end!=last_part_end:
                last_part_end=part_end
                yield seq_id[part_start:part_end]
        part_start += 1


def find_text_in(seq, verse_ids):
    text = ' '.join([words[s] for s in seq])
    selected_verses = []
    for verse_id in verse_ids:
        verse_seq = encode_seq(verses[verse_id])
        i = 0
        while i < len(verse_seq):
            if verse_seq[i] == seq[0]:
                j = 0
                while j < len(seq) and verse_seq[i + j] == seq[j]:
                    j += 1
                if j == len(seq):
                    selected_verses.append(verse_id)
                i += j
            i += 1
    return [text, ','.join(sorted(selected_verses))]


def ayeh_extractor(input_sentence):
    text = normalize_text(input_sentence)
    seq_id = encode_text(text)

    results = []
    for part in get_known_parts(seq_id):
        indices = [set(index[str(wid)]) for wid in part]
        intersect = set.intersection(*indices)
        res = find_text_in(part, intersect)
        if res[1]:
            results.append(res)

    return results


class VerseExtractionTest(TestCase):
    test_data = [
        ('رب العالمین همه چیزی خیلی خوب پیش رفت.',
         [['رب العالمين', ','.join(['1##2',
                                    '10##10',
                                    '10##37',
                                    '26##109',
                                    '26##127',
                                    '26##145',
                                    '26##16',
                                    '26##164',
                                    '26##180',
                                    '26##192',
                                    '26##23',
                                    '26##77',
                                    '27##44',
                                    '27##8',
                                    '28##30',
                                    '32##2',
                                    '37##182',
                                    '39##75',
                                    '40##64',
                                    '40##65',
                                    '41##9',
                                    '43##46',
                                    '45##36',
                                    '5##28',
                                    '56##80',
                                    '59##16',
                                    '6##162',
                                    '6##45',
                                    '69##43',
                                    '7##104',
                                    '7##54',
                                    '7##61',
                                    '7##67',
                                    '81##29'])]]),
        ('ایاک نعبد است زمستان دعای باغ در نوبهار گوید وایاک نستعین',
         [
             ['اياك نعبد', '1##5'],
             ['باغ', '16##115,2##173,6##145'],
             ['واياك نستعين', '1##5']
         ])

    ]

    def test_extraction(self):
        for text, res in self.test_data:
            self.assertListEqual(ayeh_extractor(text), res)
