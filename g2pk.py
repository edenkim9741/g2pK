# -*- coding: utf-8 -*-
'''
https://github.com/kyubyong/g2pK
'''

import os, re

import nltk
import mecab
from jamo import h2j
from nltk.corpus import cmudict
from copy import deepcopy

# For further info. about cmu dict, consult http://www.speech.cs.cmu.edu/cgi-bin/cmudict.
try:
    nltk.data.find('corpora/cmudict.zip')
except LookupError:
    nltk.download('cmudict')

from special import jyeo, ye, consonant_ui, josa_ui, vowel_ui, jamo, rieulgiyeok, rieulbieub, verb_nieun, balb, palatalize, modifying_rieul
from regular import link1, link2, link3, link4
from utils import annotate, compose, group, gloss, parse_table, get_rule_id2text
from english import convert_eng
from numerals import convert_num
import random

class G2p(object):
    def __init__(self):
        self.mecab = self.get_mecab()
        self.table = parse_table()

        self.cmu = cmudict.dict() # for English

        self.rule2text = get_rule_id2text() # for comments of main rules
        self.idioms_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "idioms.txt")

    def get_mecab(self):
        try:
            return mecab.MeCab()
        except Exception as e:
            raise Exception(
                'If you want to install mecab, The command is... pip install python-mecab-ko'
            )

    def idioms(self, strings_by_idx, descriptive=False, verbose=False):
        '''Process each line in `idioms.txt`
        Each line is delimited by "===",
        and the left string is replaced by the right one.
        inp: input string.
        descriptive: not used.
        verbose: boolean.

        >>> idioms("지금 mp3 파일을 다운받고 있어요")
        지금 엠피쓰리 파일을 다운받고 있어요
        '''
        rule = "from idioms.txt"
        outs = dict()
        for idx, strings in strings_by_idx.items():
            outs[idx] = set()
            for string in strings:
                out = string

                for line in open(self.idioms_path, 'r', encoding="utf8"):
                    line = line.split("#")[0].strip()
                    if "===" in line:
                        str1, str2 = line.split("===")
                        out = re.sub(str1, str2, out)
                gloss(verbose, out, string, rule)
                outs[idx].add(out)

        return outs
    

    #TODO: [srt]을 반환하도록 변경
    def __call__(self, input_string_by_idx, descriptive=False, verbose=False, group_vowels=False, to_syl=True, print_output=False, sampling_num=None):
        '''Main function
        string: input string
        descriptive: boolean.
        verbose: boolean
        group_vowels: boolean. If True, the vowels of the identical sound are normalized.
        to_syl: boolean. If True, hangul letters or jamo are assembled to form syllables.

        For example, given an input string "나의 친구가 mp3 file 3개를 다운받고 있다",
        STEP 1. idioms
        -> 나의 친구가 엠피쓰리 file 3개를 다운받고 있다

        STEP 2. English to Hangul
        -> 나의 친구가 엠피쓰리 파일 3개를 다운받고 있다

        STEP 3. annotate
        -> 나의/J 친구가 엠피쓰리 파일 3개/B를 다운받고 있다

        STEP 4. Spell out arabic numbers
        -> 나의/J 친구가 엠피쓰리 파일 세개/B를 다운받고 있다

        STEP 5. decompose
        -> 나의/J 친구가 엠피쓰리 파일 세개/B를 다운받고 있다

        STEP 6-9. Hangul
        -> 나의 친구가 엠피쓰리 파일 세개를 다운받꼬 읻따
        '''
        strings_by_idx = input_string_by_idx
        # 1. idioms
        strings_by_idx = self.idioms(strings_by_idx, descriptive, verbose)

        # 2 English to Hangul
        temp_strings_by_idx = deepcopy(strings_by_idx)
        for idx, strings in temp_strings_by_idx.items():
            strings_by_idx[idx] = {convert_eng(string, self.cmu) for string in strings}
        # updated_strings_w_idx = {idx : {convert_eng(string, self.cmu) for idx, string in strings_by_idx}}
        # strings_by_idx = updated_strings_w_idx  # 업데이트된 set으로 갱신

        # 3. annotate
        temp_strings_by_idx = deepcopy(strings_by_idx)
        for idx, strings in temp_strings_by_idx.items():
            strings_by_idx[idx] = {annotate(string, self.mecab) for string in strings}

        # updated_strings_w_idx = {(idx, annotate(string, self.mecab)) for idx, string in strings_by_idx}
        # strings_by_idx = updated_strings_w_idx  # 업데이트된 set으로 갱신

        # 4. Spell out arabic numbers
        temp_strings_by_idx = deepcopy(strings_by_idx)
        for idx, strings in temp_strings_by_idx.items():
            strings_by_idx[idx] = {convert_num(string) for string in strings}

        # updated_strings_w_idx = {(idx, convert_num(string)) for idx, string in strings_by_idx}
        # strings_by_idx = updated_strings_w_idx
        # string = convert_num(string)

        # 5. decompose
        # inps = {(idx, h2j(string)) for idx, string in strings_by_idx}
        # inps = strings_by_idx
        # inps.add(h2j(string))
        temp_strings_by_idx = deepcopy(strings_by_idx)
        for idx, strings in temp_strings_by_idx.items():
            strings_by_idx[idx] = {h2j(string) for string in strings}

        # 6. special
        for func in (jyeo, ye, consonant_ui, josa_ui, vowel_ui, \
                     jamo, rieulgiyeok, rieulbieub, verb_nieun, \
                     balb, palatalize, modifying_rieul):
            # print(func.__name__, inps)
            strings_by_idx = func(strings_by_idx, descriptive, verbose)
            if sampling_num is not None:
                for idx, strings in strings_by_idx.items():
                    strings_by_idx[idx] = set(random.sample(list(strings), min(sampling_num, len(strings))))
        
        temp_strings_by_idx = deepcopy(strings_by_idx)
        for idx, strings in temp_strings_by_idx.items():
            strings_by_idx[idx] = {re.sub("/[PJEB]", "", string) for string in strings}

        # 7. regular table: batchim + onset
        temp_strings_by_idx = deepcopy(strings_by_idx)
        for str1, str2, rule_ids, sc in self.table:
            for idx, strings in temp_strings_by_idx.items():
                strings_by_idx[idx].update({re.sub(str1, str2, string) for string in strings})



            # if updated_inps != inps:
            #     print("updated_inps", updated_inps)
            #     print(sc)
            # if verbose:
            #     for idx, inp in inps:
            #         _inp = re.sub(str1, str2, inp)
            #         rule = "\n".join(self.rule2text.get(rule_id, "") for rule_id in rule_ids) if rule_ids else ""
            #         gloss(verbose, inp, _inp, rule)

        
        for func in (link1, link2, link3, link4):
            # print(func.__name__, inps)
            strings_by_idx = func(strings_by_idx, descriptive, verbose)
            if sampling_num is not None:
                for idx, strings in strings_by_idx.items():
                    strings_by_idx[idx] = set(random.sample(list(strings), min(sampling_num, len(strings))))

        if group_vowels:
            temp_strings_by_idx = deepcopy(strings_by_idx)
            for idx, strings in temp_strings_by_idx.items():
                strings_by_idx[idx] = {group(string) for string in strings}
            # updated_inps = {(idx, group(inp)) for idx, inp in inps}
            # inps.update(updated_inps)

        if to_syl:
            temp_strings_by_idx = deepcopy(strings_by_idx)
            for idx, strings in temp_strings_by_idx.items():
                strings_by_idx[idx] = {compose(string) for string in strings}
            # updated_inps = {(idx, compose(inp)) for idx, inp in inps}
            # inps.update(updated_inps)

        if sampling_num is not None:
            # inps = random.sample(inps, min(sampling_num, len(inps)))
            # for idx, inps_list in inps_dict.items():
            #     inps_dict[idx] = random.sample(inps_list, min(sampling_num, len(inps_list)))
            for idx, strings in strings_by_idx.items():
                strings_by_idx[idx] = set(random.sample(list(strings), min(sampling_num, len(strings))))
        
        temp_strings_by_idx = deepcopy(strings_by_idx)
        for idx, strings in temp_strings_by_idx.items():
            strings_by_idx[idx] = list(strings)

        if print_output:
            print(strings_by_idx)

        del temp_strings_by_idx
        

        return strings_by_idx

if __name__ == "__main__":
    g2p = G2p()
    g2p({1:{"나의 친구가 mp3 file 3개를 다운받고 있다"}, 2:{"가는 말이 고와야 오는 말이 곱다"}}, print_output=True, sampling_num=3)