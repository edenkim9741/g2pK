# -*- coding: utf-8 -*-
'''
https://github.com/kyubyong/g2pK
'''

from utils import gloss, get_rule_id2text
from copy import deepcopy
rule_id2text = get_rule_id2text()


def link1(strings_by_idx, descriptive=False, verbose=False):
    rule = rule_id2text["13"]
    outs = deepcopy(strings_by_idx)
    for idx, strings in strings_by_idx.items():
        for inp in strings:
            out = inp
            pairs = [ ("ᆨᄋ", "ᄀ"),
                    ("ᆩᄋ", "ᄁ"),
                    ("ᆫᄋ", "ᄂ"),
                    ("ᆮᄋ", "ᄃ"),
                    ("ᆯᄋ", "ᄅ"),
                    ("ᆷᄋ", "ᄆ"),
                    ("ᆸᄋ", "ᄇ"),
                    ("ᆺᄋ", "ᄉ"),
                    ("ᆻᄋ", "ᄊ"),
                    ("ᆽᄋ", "ᄌ"),
                    ("ᆾᄋ", "ᄎ"),
                    ("ᆿᄋ", "ᄏ"),
                    ("ᇀᄋ", "ᄐ"),
                    ("ᇁᄋ", "ᄑ")]
            for str1, str2 in pairs:
                out = out.replace(str1, str2)

            gloss(verbose, out, inp, rule)
            outs[idx].add(out)
    return outs


def link2(strings_by_idx, descriptive=False, verbose=False):
    rule = rule_id2text["14"]
    outs = deepcopy(strings_by_idx)

    for idx, strings in strings_by_idx.items():
        for inp in strings:
            out = inp
            pairs = [ ("ᆪᄋ", "ᆨᄊ"),
                    ("ᆬᄋ", "ᆫᄌ"),
                    ("ᆰᄋ", "ᆯᄀ"),
                    ("ᆱᄋ", "ᆯᄆ"),
                    ("ᆲᄋ", "ᆯᄇ"),
                    ("ᆳᄋ", "ᆯᄊ"),
                    ("ᆴᄋ", "ᆯᄐ"),
                    ("ᆵᄋ", "ᆯᄑ"),
                    ("ᆹᄋ", "ᆸᄊ") ]
            for str1, str2 in pairs:
                out = out.replace(str1, str2)

            gloss(verbose, out, inp, rule)
            outs[idx].add(out)
    return outs


def link3(strings_by_idx, descriptive=False, verbose=False):
    rule = rule_id2text["15"]

    outs = deepcopy(strings_by_idx)

    for idx, strings in strings_by_idx.items():
        for inp in strings:
            out = inp
            pairs = [ ("ᆨ ᄋ", " ᄀ"),
                    ("ᆩ ᄋ", " ᄁ"),
                    ("ᆫ ᄋ", " ᄂ"),
                    ("ᆮ ᄋ", " ᄃ"),
                    ("ᆯ ᄋ", " ᄅ"),
                    ("ᆷ ᄋ", " ᄆ"),
                    ("ᆸ ᄋ", " ᄇ"),
                    ("ᆺ ᄋ", " ᄉ"),
                    ("ᆻ ᄋ", " ᄊ"),
                    ("ᆽ ᄋ", " ᄌ"),
                    ("ᆾ ᄋ", " ᄎ"),
                    ("ᆿ ᄋ", " ᄏ"),
                    ("ᇀ ᄋ", " ᄐ"),
                    ("ᇁ ᄋ", " ᄑ"),

                    ("ᆪ ᄋ", "ᆨ ᄊ"),
                    ("ᆬ ᄋ", "ᆫ ᄌ"),
                    ("ᆰ ᄋ", "ᆯ ᄀ"),
                    ("ᆱ ᄋ", "ᆯ ᄆ"),
                    ("ᆲ ᄋ", "ᆯ ᄇ"),
                    ("ᆳ ᄋ", "ᆯ ᄊ"),
                    ("ᆴ ᄋ", "ᆯ ᄐ"),
                    ("ᆵ ᄋ", "ᆯ ᄑ"),
                    ("ᆹ ᄋ", "ᆸ ᄊ") ]

            for str1, str2 in pairs:
                out = out.replace(str1, str2)

            gloss(verbose, out, inp, rule)
            outs[idx].add(out)
    return outs


def link4(strings_by_idx, descriptive=False, verbose=False):
    rule = rule_id2text["12.4"]

    outs = deepcopy(strings_by_idx)

    for idx, strings in strings_by_idx.items():
        for inp in strings:
            out = inp
            pairs = [ ("ᇂᄋ", "ᄋ"),
                    ("ᆭᄋ", "ᄂ"),
                    ("ᆶᄋ", "ᄅ") ]

            for str1, str2 in pairs:
                out = out.replace(str1, str2)

            gloss(verbose, out, inp, rule)
            outs[idx].add(out)
    return outs

