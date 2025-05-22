# -*- coding: utf-8 -*-
'''
Special rule for processing Hangul
https://github.com/kyubyong/g2pK
'''

import re
from copy import deepcopy

from utils import gloss, get_rule_id2text

rule_id2text = get_rule_id2text()


############################ vowels ############################
def jyeo(inps, descriptive=False, verbose=False):
    rule = rule_id2text["5.1"]
    # 일반적인 규칙으로 취급한다 by kyubyong
    outs = deepcopy(inps)
    for inp in inps:
        out = re.sub("([ᄌᄍᄎ])ᅧ", r"\1ᅥ", inp)
        gloss(verbose, out, inp, rule)
        outs.add(out)
        
    return outs


def ye(inps, descriptive=False, verbose=False):
    rule = rule_id2text["5.2"]
    # 실제로 언중은 예, 녜, 셰, 쎼 이외의 'ㅖ'는 [ㅔ]로 발음한다. by kyubyong
    outs = deepcopy(inps)
    for inp in inps:
        if descriptive:
            out = re.sub("([ᄀᄁᄃᄄㄹᄆᄇᄈᄌᄍᄎᄏᄐᄑᄒ])ᅨ", r"\1ᅦ", inp)
        else:
            out = inp
        gloss(verbose, out, inp, rule)
        outs.add(out)
    return outs


def consonant_ui(inps, descriptive=False, verbose=False):
    rule = rule_id2text["5.3"]

    outs = deepcopy(inps)
    for inp in inps:
        out = re.sub("([ᄀᄁᄂᄃᄄᄅᄆᄇᄈᄉᄊᄌᄍᄎᄏᄐᄑᄒ])ᅴ", r"\1ᅵ", inp)
        gloss(verbose, out, inp, rule)
        outs.add(out)
    return outs


def josa_ui(inps, descriptive=False, verbose=False):
    rule = rule_id2text["5.4.2"]
    # 실제로 언중은 높은 확률로 조사 '의'는 [ㅔ]로 발음한다.
    outs = deepcopy(inps)
    for inp in inps:
        if descriptive:
            out = re.sub("의/J", "에", inp)
        else:
            out = inp.replace("/J", "")
        gloss(verbose, out, inp, rule)
        outs.add(out)
    return outs


def vowel_ui(inps, descriptive=False, verbose=False):
    rule = rule_id2text["5.4.1"]
    # 실제로 언중은 높은 확률로 단어의 첫음절 이외의 '의'는 [ㅣ]로 발음한다."""
    outs = deepcopy(inps)
    for inp in inps:
        if descriptive:
            out = re.sub("(\Sᄋ)ᅴ", r"\1ᅵ", inp)
        else:
            out = inp
        gloss(verbose, out, inp, rule)
        outs.add(out)
    return outs


def jamo(inps, descriptive=False, verbose=False):
    rule = rule_id2text["16"]
    outs = deepcopy(inps)
    for inp in inps:
        out = inp

        out = re.sub("([그])ᆮᄋ", r"\1ᄉ", out)
        out = re.sub("([으])[ᆽᆾᇀᇂ]ᄋ", r"\1ᄉ", out)
        out = re.sub("([으])[ᆿ]ᄋ", r"\1ᄀ", out)
        out = re.sub("([으])[ᇁ]ᄋ", r"\1ᄇ", out)

        gloss(verbose, out, inp, rule)
        outs.add(out)
    return outs


    ############################ 어간 받침 ############################
def rieulgiyeok(inps, descriptive=False, verbose=False):
    rule = rule_id2text["11.1"]
    outs = deepcopy(inps)

    for inp in inps:
        out = inp
        out = re.sub("ᆰ/P([ᄀᄁ])", r"ᆯᄁ", out)

        gloss(verbose, out, inp, rule)
        outs.add(out)
    return outs


def rieulbieub(inps, descriptive=False, verbose=False):
    rule = rule_id2text["25"]
    outs = deepcopy(inps)
    for inp in inps:
        out = inp

        out = re.sub("([ᆲᆴ])/Pᄀ", r"\1ᄁ", out)
        out = re.sub("([ᆲᆴ])/Pᄃ", r"\1ᄄ", out)
        out = re.sub("([ᆲᆴ])/Pᄉ", r"\1ᄊ", out)
        out = re.sub("([ᆲᆴ])/Pᄌ", r"\1ᄍ", out)

        gloss(verbose, out, inp, rule)
        outs.add(out)
    return outs


def verb_nieun(inps, descriptive=False, verbose=False):
    rule = rule_id2text["24"]

    outs = deepcopy(inps)
    for inp in inps:
        out = inp

        pairs = [ ("([ᆫᆷ])/Pᄀ", r"\1ᄁ"),
                ("([ᆫᆷ])/Pᄃ", r"\1ᄄ"),
                ("([ᆫᆷ])/Pᄉ", r"\1ᄊ"),
                ("([ᆫᆷ])/Pᄌ", r"\1ᄍ"),

                ("ᆬ/Pᄀ", "ᆫᄁ"),
                ("ᆬ/Pᄃ", "ᆫᄄ"),
                ("ᆬ/Pᄉ", "ᆫᄊ"),
                ("ᆬ/Pᄌ", "ᆫᄍ"),

                ("ᆱ/Pᄀ", "ᆷᄁ"),
                ("ᆱ/Pᄃ", "ᆷᄄ"),
                ("ᆱ/Pᄉ", "ᆷᄊ"),
                ("ᆱ/Pᄌ", "ᆷᄍ")  ]

        for str1, str2 in pairs:
            out = re.sub(str1, str2, out)

        gloss(verbose, out, inp, rule)
        outs.add(out)

    return outs


def balb(inps, descriptive=False, verbose=False):
    rule = rule_id2text["10.1"]
    outs = deepcopy(inps)
    for inp in inps:
        out = inp
        syllable_final_or_consonants = "($|[^ᄋᄒ])"

        # exceptions
        out = re.sub(f"(바)ᆲ({syllable_final_or_consonants})", r"\1ᆸ\2", out)
        out = re.sub(f"(너)ᆲ([ᄌᄍ]ᅮ|[ᄃᄄ]ᅮ)", r"\1ᆸ\2", out)
        gloss(verbose, out, inp, rule)
        outs.add(out)
    return outs


def palatalize(inps, descriptive=False, verbose=False):
    rule = rule_id2text["17"]
    outs = deepcopy(inps)
    for inp in inps:
        out = inp

        out = re.sub("ᆮᄋ([ᅵᅧ])", r"ᄌ\1", out)
        out = re.sub("ᇀᄋ([ᅵᅧ])", r"ᄎ\1", out)
        out = re.sub("ᆴᄋ([ᅵᅧ])", r"ᆯᄎ\1", out)

        out = re.sub("ᆮᄒ([ᅵ])", r"ᄎ\1", out)

        gloss(verbose, out, inp, rule)
        outs.add(out)
    return outs


def modifying_rieul(inps, descriptive=False, verbose=False):
    rule = rule_id2text["27"]
    outs = deepcopy(inps)

    for inp in inps:
        out = inp
        
        pairs = [   ("ᆯ/E ᄀ", r"ᆯ ᄁ"),
                    ("ᆯ/E ᄃ", r"ᆯ ᄄ"),
                    ("ᆯ/E ᄇ", r"ᆯ ᄈ"),
                    ("ᆯ/E ᄉ", r"ᆯ ᄊ"),
                    ("ᆯ/E ᄌ", r"ᆯ ᄍ"),

                    ("ᆯ걸", "ᆯ껄"),
                    ("ᆯ밖에", "ᆯ빠께"),
                    ("ᆯ세라", "ᆯ쎄라"),
                    ("ᆯ수록", "ᆯ쑤록"),
                    ("ᆯ지라도", "ᆯ찌라도"),
                    ("ᆯ지언정", "ᆯ찌언정"),
                    ("ᆯ진대", "ᆯ찐대") ]

        for str1, str2 in pairs:
            out = re.sub(str1, str2, out)

        gloss(verbose, out, inp, rule)
        outs.add(out)
    return outs
