import json
import re
import csv

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

vavs = {}

with open('Vav.csv') as fp:
    reader = csv.reader(fp, delimiter=',')
    for i, row in enumerate(reader):
        if i == 0:
            continue
        else:
            vavs[row[0]] = int(row[1])
vavs_keys = set(vavs.keys())


def normalize_text(text):
    text = re.sub(r'[' + analysis_data['pun'] + ']', '', text)
    text = re.sub(r'[\s]+', ' ', text)
    for key, val in analysis_data['repl'].items():
        text = re.sub(r'[' + key + ']', val, text)
    for vav in vavs:
        if vavs[vav] == 2:
            text = re.sub(vav, vav[0] + ' ' + vav[1:], text)
    return text


def encode_text(text):
    seq_wo = text.split(' ')
    seq_id = encode_seq(seq_wo)
    return seq_id


def encode_seq(seq_wo):
    return [words_map[w] if w in words_map else words_map['[UNK]'] for w in seq_wo]


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
    return [f"{text} {verse_id}" for verse_id in sorted(selected_verses)]


def get_known_parts(seq_id):
    print(seq_id)
    if len(seq_id) <= 1:
        return
    part_start = 0
    last_part_end = -1
    while part_start < len(seq_id) - 1:
        ayehs=[]
        running_intersection_of_ayehs = set()
        part_end = part_start
        if seq_id[part_start] != UNK_C:
            #TODO: optimization part_end=last_part_end
            while part_end < len(seq_id) and seq_id[part_end] != UNK_C:
                running_intersection_of_ayehs = running_intersection_of_ayehs | set(index[str(seq_id[part_end])])
                print(part_start,part_end)
                candidate_ayehs = find_text_in(seq_id[part_start:part_end+1],running_intersection_of_ayehs)
                if not candidate_ayehs:
                    break
                ayehs=candidate_ayehs
                part_end += 1
            if part_end - part_start >= 2 and part_end != last_part_end:
                last_part_end = part_end
                yield ayehs
        part_start += 1


def ayeh_extractor(input_sentence):
    text = normalize_text(input_sentence)
    seq_id = encode_text(text)

    results = []
    for parts in get_known_parts(seq_id):
        results += parts

    return sorted(results)

