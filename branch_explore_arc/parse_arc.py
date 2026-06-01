#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parse SCRDATA.ARC SCR 2.00 script sections.

This is intentionally conservative: it records the byte-level structure,
known text/label/choice/script-call records, and graph edges whose source is
clear. Unknown opcode payloads are preserved in hex for later decoding.
"""

from __future__ import annotations

import html
import json
import re
import shutil
import struct
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


MAGIC = b"SCR 2.00"
ROOT = Path(__file__).resolve().parents[1]
ARC_PATH = ROOT / "SCRDATA.ARC"
OUT_DIR = ROOT / "branch_explore_arc"
BOOKISH_DIR = ROOT / "bookish"
BOOKISH_ZHCN_DIR = ROOT / "bookish_zhcn"
BOOKISH_APPENDIX_DIR = BOOKISH_DIR / "appendix"
BOOKISH_EPUB_DIR = BOOKISH_DIR / "epub"
BOOKISH_EPUB_FILE = BOOKISH_DIR / "bookish_complete.epub"
BOOKISH_JA_ZH_EPUB_FILE = BOOKISH_DIR / "bookish_complete.ja.zh.epub"
BOOKISH_COMPLETE_MD = BOOKISH_DIR / "complete_epub.md"
BOOKISH_READING_ORDER_DIRNAME = "reading_order"
BOOKISH_ZHCN_EPUB_DIR = BOOKISH_ZHCN_DIR / "epub"
BOOKISH_ZHCN_EPUB_FILE = ROOT / "bookish_complete.zh.epub"
BOOKISH_ZHCN_COMPLETE_MD = BOOKISH_ZHCN_DIR / "complete_epub.md"
BOOKISH_ZHCN_AUDIT_DIR = BOOKISH_ZHCN_DIR / "_audit"
BOOKISH_ZHCN_READER_MANUAL_FILE = "reader_manual.md"
BOOKISH_ZHCN_BOOK_TOC_FILE = "book_toc.md"
BOOKISH_ZHCN_COVER_IMAGE = BOOKISH_ZHCN_DIR / "cover.jpg"
PROCESSED_V2_DIR = ROOT / "processed_output_v2"
TRANSLATED_PROCESSED_V2_DIR = ROOT / "translated_processed_output_v2"
MODIFIED_JA_ZH_DIR = ROOT / "Modified" / "ja_zh"
CHOICES_MAP_PATH = ROOT / "choices_map_v3_1.md"
CHOICES_PATH = ROOT / "choices.txt"

PROTAGONIST_NAME = "紗夜"
PROTAGONIST_FULL_NAME = "遠野　紗夜"
INTERACTIVE_TERM_RE = re.compile(r"\$([^$\n]+)\$")
INTERACTIVE_BOLD_RE = re.compile(r"\*\*([^*\n]+)\*\*")

INTERACTIVE_TERM_TRANSLATION_HINTS = {
    "愛": ["爱"],
    "始め": ["开始"],
    "お姫様": ["公主"],
    "司書": ["图书管理员", "司书"],
    "平和": ["和平"],
    "国": ["国家", "国"],
    "言葉": ["话语", "言语", "语言", "话"],
    "太宰ともゑの姉": ["太宰友惠的姐姐", "太宰ともゑ的姐姐", "太宰友惠姐姐"],
    "忘れた": ["忘记", "忘掉"],
    "真実": ["真相", "真实"],
    "解釈": ["解释", "解读"],
    "続ける": ["继续"],
    "津島修治": ["津岛修治"],
    "特別": ["特别", "特殊"],
    "気障": ["装腔作势", "耍帅", "做作"],
    "ユメミルセカイ": ["梦见世界"],
    "主人公": ["主人公", "主角"],
    "猟師": ["猎人"],
    "夢": ["梦", "梦想"],
    "読み手": ["读者", "阅读者"],
    "ヴィルヘルム・猫田": ["威廉·猫田", "维尔赫尔姆·猫田"],
    "お嬢様": ["大小姐", "小姐"],
    "Ｉ　Ａｍ　ａ　Ｃａｔ": ["I Am a Cat"],
    "信じて": ["相信", "信任"],
    "医者": ["医生"],
    "運命": ["命运"],
    "姉": ["姐姐", "姐"],
    "金": ["金钱", "钱"],
    "友": ["朋友", "友"],
    "魔法使い": ["魔法师", "魔法使"],
    "お父様": ["父亲大人", "父亲", "爸爸"],
    "使い": ["使者", "派人", "跑腿"],
    "王子様": ["王子"],
    "優しい": ["温柔", "善良", "友善"],
    "嘘": ["谎言", "谎", "撒谎"],
    "詐欺師": ["骗子", "诈骗师", "欺诈师"],
    "家政婦": ["家政妇", "女佣", "佣人"],
    "賭け": ["赌注", "赌"],
    "家族": ["家人", "家族"],
    "狭間": ["狭间", "夹缝", "间隙"],
    "起承転結": ["起承转合", "起承转结"],
    "正しい": ["正确", "正当"],
    "永遠": ["永远", "永恒"],
    "憧れ": ["憧憬", "向往"],
    "鏡": ["镜子", "镜"],
    "おじ様": ["叔叔", "伯父", "大叔"],
    "美": ["美丽", "美"],
    "選択": ["选择"],
    "闇": ["黑暗", "暗"],
    "生": ["活", "生"],
    "時": ["时间", "时"],
    "証明": ["证明"],
    "相対": ["对抗", "相对"],
    "記憶": ["记忆"],
    "何もない": ["一无所有", "什么都没有", "什么也没有", "没有任何东西"],
    "死": ["死亡", "死"],
    "終わり": ["终结", "结束", "终点"],
    "涙": ["眼泪", "泪"],
    "私": ["自己", "我"],
    "客観": ["客观"],
    "作者": ["作者"],
    "物語": ["故事", "物语"],
}

BOOKISH_CHAPTER_FILES = [
    {"file": "00_hajimari.md", "chapter": "はじまり", "title": "はじまり"},
    {"file": "01_prologue.md", "chapter": "序章", "title": "序章"},
    {"file": "02_chapter1.md", "chapter": "一章", "title": "一章"},
    {"file": "03_chapter2.md", "chapter": "二章", "title": "二章"},
    {"file": "04_chapter3.md", "chapter": "三章", "title": "三章"},
    {"file": "05_natsuko.md", "chapter": "夏帆", "title": "夏帆"},
    {"file": "06_chapter4.md", "chapter": "四章", "title": "四章"},
    {"file": "07_hinase.md", "chapter": "日生", "title": "日生"},
    {"file": "08_chapter5.md", "chapter": "五章", "title": "五章"},
    {"file": "09_kirishima.md", "chapter": "桐島", "title": "桐島"},
    {"file": "10_chiyo.md", "chapter": "千代", "title": "千代"},
    {"file": "11_chapter6.md", "chapter": "六章", "title": "六章"},
    {"file": "12_kuro.md", "chapter": "黒の章", "title": "黒の章"},
    {"file": "13_ao.md", "chapter": "蒼の章", "title": "蒼の章"},
    {"file": "14_atogaki.md", "chapter": "あとがき", "title": "あとがき"},
]

BOOKISH_ROUTE_BLOCKS = [
    {"key": "hinase", "name": "日生光", "start": 1, "end": 123, "kind": "main"},
    {"key": "kirishima", "name": "桐島七葵", "start": 124, "end": 253, "kind": "main"},
    {"key": "chiyo", "name": "千代", "start": 254, "end": 291, "kind": "main"},
    {"key": "toya", "name": "遠野十夜", "start": 298, "end": 424, "kind": "main"},
    {"key": "chapter6_bad", "name": "六章-終", "start": 428, "end": 441, "kind": "bad"},
    {"key": "ao", "name": "蒼", "start": 447, "end": 572, "kind": "main"},
    {"key": "chapter1_alt", "name": "一章-結末２", "start": 585, "end": 613, "kind": "appendix"},
    {"key": "natsuko", "name": "夏帆-結末", "start": 617, "end": 644, "kind": "appendix"},
    {"key": "hinase25_2", "name": "日生25-2", "start": 648, "end": 708, "kind": "appendix"},
    {"key": "recovery_4_37_6_03", "name": "四章37-2、六章03-1", "start": 712, "end": 827, "kind": "appendix"},
    {"key": "ao39_2", "name": "蒼の章39-2", "start": 831, "end": 843, "kind": "appendix"},
]

BOOKISH_PRIMARY_ROUTE_KEYS = ["hinase", "kirishima", "chiyo", "toya", "ao"]
BOOKISH_ROUTE_NAMES = {route["key"]: route["name"] for route in BOOKISH_ROUTE_BLOCKS}
BOOKISH_ENDINGS_AND_RECOVERY_FILE = "appendix/endings_and_recovery.md"
BOOKISH_INTERNAL_STORIES_FILE = "appendix/internal_stories.md"
BOOKISH_EPUB_TITLE = "死神と少女 Bookish Complete Script"
BOOKISH_EPUB_AUTHOR = "ProjectSTS"
BOOKISH_EPUB_LANGUAGE = "ja"
BOOKISH_ZHCN_EPUB_TITLE = "死神与少女 Bookish 中文完整剧本"
BOOKISH_ZHCN_EPUB_LANGUAGE = "zh-CN"

BOOKISH_ZHCN_HEADING_MAP = {
    "名前": "名字",
    "はじまり": "开端",
    "序章": "序章",
    "一章": "一章",
    "二章": "二章",
    "三章": "三章",
    "夏帆": "夏帆",
    "四章": "四章",
    "日生": "日生",
    "五章": "五章",
    "桐島": "桐岛",
    "千代": "千代",
    "六章": "六章",
    "黒の章": "黑之章",
    "蒼の章": "苍之章",
    "あとがき": "后记",
    "全員共通": "全员共通",
    "日生光": "日生光",
    "桐島七葵": "桐岛七葵",
    "遠野十夜": "远野十夜",
    "蒼": "苍",
    "六章-終": "六章-终",
    "一章-結末２": "一章-结末2",
    "夏帆-結末": "夏帆-结末",
    "日生25-2": "日生25-2",
    "四章37-2、六章03-1": "四章37-2、六章03-1",
    "蒼の章39-2": "苍之章39-2",
}

BOOKISH_ZHCN_SPEAKER_MAP = {
    "遠野　紗夜": "远野纱夜",
    "遠野 紗夜": "远野纱夜",
    "遠野紗夜": "远野纱夜",
    "紗夜": "纱夜",
    "遠野　十夜": "远野十夜",
    "遠野 十夜": "远野十夜",
    "遠野十夜": "远野十夜",
    "十夜": "十夜",
    "桐島 七葵": "桐岛七葵",
    "桐島七葵": "桐岛七葵",
    "七葵": "七葵",
    "日生 光": "日生光",
    "日生光": "日生光",
    "日生 紫": "日生紫",
    "日生紫": "日生紫",
    "日生祖母": "日生祖母",
    "蒼": "苍",
    "千代": "千代",
    "宮沢 夏帆": "宫泽夏帆",
    "宮沢夏帆": "宫泽夏帆",
    "夏帆": "夏帆",
    "夏目 悠希": "夏目悠希",
    "夏目悠希": "夏目悠希",
    "臥待 春夫": "卧待春夫",
    "臥待春夫": "卧待春夫",
    "ルイス": "路易斯",
    "ヴィルヘルム": "威廉",
    "司書": "司书",
    "国語教師": "国语教师",
    "太宰 ともゑ": "太宰友惠",
    "太宰ともゑ": "太宰友惠",
    "女子生徒Ａ": "女学生A",
    "女子生徒Ｂ": "女学生B",
    "女子生徒Ｃ": "女学生C",
    "女子生徒Ｄ": "女学生D",
    "女子生徒": "女学生",
    "男子生徒Ａ": "男学生A",
    "男子生徒Ｂ": "男学生B",
    "男子生徒": "男学生",
    "剣道部員Ａ": "剑道部员A",
    "剣道部員Ｂ": "剑道部员B",
    "剣道部員Ｃ": "剑道部员C",
    "剣道部員Ｄ": "剑道部员D",
    "剣道部員達": "剑道部员们",
    "剣道部員": "剑道部员",
    "父": "父亲",
    "母": "母亲",
    "兄": "哥哥",
    "妹": "妹妹",
    "七葵兄": "七葵哥哥",
    "家政婦": "家政妇",
    "太宰姉": "太宰姐姐",
    "夏目姉": "夏目姐姐",
    "男の子": "男孩",
    "女の子": "女孩",
    "養護教諭": "保健老师",
    "生活指導主任": "生活指导主任",
    "執事": "管家",
    "魔法使い": "魔法师",
    "友人": "友人",
    "死神": "死神",
    "猟師Ａ": "猎人A",
    "猟師Ｂ": "猎人B",
    "猟師Ｃ": "猎人C",
    "猟師": "猎人",
    "医者": "医生",
    "白雪": "白雪",
    "教師": "教师",
    "看護士Ａ": "护士A",
    "看護士Ｂ": "护士B",
    "看護士Ｃ": "护士C",
    "看護士": "护士",
    "王子様": "王子",
    "お姫様": "公主",
    "ウエイトレス": "女服务员",
    "椿姫": "椿姬",
    "少女": "少女",
    "担任教師": "班主任",
    "船主": "船主",
    "老紳士": "老绅士",
    "上級生Ａ": "高年级生A",
    "上級生Ｂ": "高年级生B",
    "上級生": "高年级生",
    "他校生Ａ": "外校生A",
    "他校生Ｂ": "外校生B",
    "おばさん": "大妈",
    "おじさんＡ": "大叔A",
    "おじさんＢ": "大叔B",
    "おじさん": "大叔",
    "店の親父": "店老板",
    "店員": "店员",
    "貴婦人Ａ": "贵妇人A",
    "貴婦人Ｂ": "贵妇人B",
    "着ぐるみ": "玩偶装",
    "審判": "裁判",
    "精神科医": "精神科医生",
    "子供Ａ": "孩子A",
    "子供Ｂ": "孩子B",
    "使用人Ａ": "佣人A",
    "使用人Ｂ": "佣人B",
    "管理人": "管理员",
    "主婦Ａ": "主妇A",
    "主婦Ｂ": "主妇B",
    "男": "男人",
    "侍女": "侍女",
    "黒猫": "黑猫",
    "白猫": "白猫",
    "？？？": "？？？",
}

BOOKISH_ZHCN_NAME_REPLACEMENTS = {
    **{
        source: target
        for source, target in BOOKISH_ZHCN_SPEAKER_MAP.items()
        if source not in {"父", "母", "兄", "妹", "男"}
    },
    "遠野 纱夜": "远野纱夜",
    "遠野纱夜": "远野纱夜",
    "遠野": "远野",
    "桐岛 七葵": "桐岛七葵",
    "宮沢": "宫泽",
    "臥待": "卧待",
    "ともゑ": "友惠",
    "桐島": "桐岛",
    "黒の章": "黑之章",
    "蒼の章": "苍之章",
    "黒": "黑",
    "蒼": "苍",
    "分岐": "分歧",
    "まで": "为止",
    "結末": "结末",
    "終": "终",
    "先輩": "前辈",
    "死神と少女": "死神与少女",
    "籠の鳥": "笼中鸟",
    "西の村の猟師": "西边村子的猎人",
    "塔の魔女と盗賊": "塔中的魔女与盗贼",
}

JAPANESE_KANA_RE = re.compile(r"[\u3040-\u30ff]")

BOOKISH_SCENE_SOURCE_FOLDERS = {
    "序章": ("prologue", "prologue"),
    "一章": ("chapter1", "chapter1"),
    "二章": ("chapter2", "chapter2"),
    "三章": ("chapter3", "chapter3"),
    "夏帆": ("natsuko", "natsuko"),
    "四章": ("chapter4", "chapter4"),
    "日生": ("hinase", "hinase"),
    "五章": ("chapter5", "chapter5"),
    "桐島": ("kirishima", "kirishima"),
    "千代": ("chiyo", "chiyo"),
    "六章": ("chapter6", "chapter6"),
    "黒の章": ("chapter7_kuro", "chapter7_kuro"),
    "蒼の章": ("chapter7_ao", "chapter7_ao"),
    "あとがき": ("ending", "ending"),
}

BOOKISH_CHAPTER_ROUTE_KEYS = {
    "はじまり": ["toya"],
    "序章": ["hinase"],
    "一章": ["hinase", "kirishima", "chiyo", "toya", "ao"],
    "二章": ["hinase", "kirishima", "chiyo", "toya", "ao"],
    "三章": ["hinase", "kirishima", "chiyo", "toya", "ao"],
    "夏帆": [],
    "四章": ["hinase", "kirishima", "chiyo", "toya", "ao"],
    "日生": ["hinase"],
    "五章": ["kirishima", "chiyo", "toya", "ao"],
    "桐島": ["kirishima"],
    "千代": ["chiyo"],
    "六章": [],
    "黒の章": ["toya"],
    "蒼の章": ["ao"],
    "あとがき": ["ao"],
}

BOOKISH_RECOVERY_ROUTE_CHAPTERS = {
    "chapter1_alt": ["一章"],
    "natsuko": ["三章", "夏帆"],
    "hinase25_2": ["二章", "三章", "四章", "日生"],
    "recovery_4_37_6_03": ["序章", "一章", "二章", "三章", "四章", "五章", "六章"],
    "ao39_2": ["蒼の章"],
}

BOOKISH_CANONICAL_COMMON_SCENE_CUTOFFS = {
    "一章": 21,
}

BOOKISH_BAD_END_TITLE_PATTERNS = [
    "一章-終",
    "日生-終",
    "六章-終",
    "黒の章-終",
    "蒼の章-終",
]

BOOKISH_OTHER_END_TITLE_PATTERNS = [
    "一章-結末２",
    "夏帆-結末",
]

BOOKISH_SOFT_SKIPPABLE_PLAN_CHOICES = {
    "スナイパー",
    "宇宙人",
    "コンビニ店員",
    "ウェイター",
    "清掃員",
    "助手",
    "諦める",
}

OP_LABEL = 0x001A
OP_JUMP = 0x0018
OP_CALL = 0x001E
OP_END = 0x001F
OP_ASSIGN = 0x0025
OP_IF_SKIP = 0x0022
OP_JUMP_OVER = 0x0021
OP_BLOCK_MARK = 0x0023
OP_EXPR_START = 0x0030
OP_CMP_LT_OR_EQ = 0x0035
OP_CMP_EQ = 0x0036
OP_CMP_NE = 0x0037
OP_LOGICAL_OR = 0x003A
OP_TEXT = 0x005A
OP_SELECT = 0x005C
OP_FORMAT_TEXT = 0x00FC
OP_VALUE = 0x00FD
OP_TITLE = 0x00F0

EXPR_OPS = {OP_CMP_LT_OR_EQ, OP_CMP_EQ, OP_CMP_NE, OP_LOGICAL_OR}

COMPARE_OPERATORS = {
    OP_CMP_LT_OR_EQ: "<= or flag-test",
    OP_CMP_EQ: "==",
    OP_CMP_NE: "!=",
}

EXTRA_MENU_SCRIPTS = {
    "shinigami_pic.scr",
    "ehon01.scr",
    "ehon02.scr",
    "ehon03.scr",
    "ehon04.scr",
    "ehon05.scr",
}

BOOKISH_INTERNAL_STORY_SPECS = [
    {"section_index": 442, "script": "shinigami_pic.scr", "title": "死神と少女"},
    {"section_index": 443, "script": "ehon01.scr", "title": "籠の鳥"},
    {"section_index": 444, "script": "ehon02.scr", "title": "西の村の猟師"},
    {"section_index": 445, "script": "ehon03.scr", "title": "ehon03"},
    {"section_index": 446, "script": "ehon04.scr", "title": "塔の魔女と盗賊"},
    {"section_index": 447, "script": "ehon05.scr", "title": "淡紅"},
]

NON_SCENARIO_CALLS = {
    "INIT.SCR",
    "INITFLG.scr",
    "DEBUG.SCR",
    "DEBUG.scr",
}

MANUAL_CONDITION_MEANINGS = {
    ("var_0900", 0): "章节入口选择：序章/开端",
    ("var_0900", 1): "章节入口选择：一章",
    ("var_0900", 2): "章节入口选择：二章",
    ("var_0900", 3): "章节入口选择：三章",
    ("var_0900", 4): "章节入口选择：四章",
    ("var_0900", 5): "章节入口选择：五章",
    ("var_0900", 6): "章节入口选择：六章",
    ("var_0900", 7): "章节入口选择：黒の章",
    ("var_0900", 8): "章节入口选择：蒼の章",
    ("var_0900", 9): "章节入口选择：あとがき",
}

ROUTE_LABEL_NAMES = {
    "ROOT_OP": "序章/开端",
    "ROOT_1": "一章",
    "ROOT_2": "二章",
    "ROOT_3": "三章/夏帆",
    "ROOT_4": "四章/共通",
    "ROOT_5": "五章/共通",
    "nana": "桐島",
    "CHAPTER_START": "章节选择入口",
}


def hx(value: int, width: int = 6) -> str:
    return f"0x{value:0{width}x}"


def decode_sjis(data: bytes) -> str:
    return data.decode("cp932", errors="replace")


def find_sections(data: bytes) -> list[int]:
    offsets: list[int] = []
    pos = 0
    while True:
        found = data.find(MAGIC, pos)
        if found < 0:
            return offsets
        offsets.append(found)
        pos = found + 1


def extract_type3_strings(payload: bytes) -> list[str]:
    """Extract null-terminated strings marked by byte 0x03."""
    strings: list[str] = []
    i = 0
    while i < len(payload):
        if payload[i] != 0x03:
            i += 1
            continue
        i += 1
        end = payload.find(b"\x00", i)
        if end < 0:
            break
        strings.append(decode_sjis(payload[i:end]))
        i = end + 1
    return strings


def parse_choice_payload(strings: list[str]) -> list[dict[str, Any]]:
    options: list[dict[str, Any]] = []
    for item in strings:
        if not item:
            continue
        if "," in item:
            text, target = item.rsplit(",", 1)
            options.append({"text": text.strip(), "target": target.strip()})
        else:
            options.append({"text": item.strip(), "target": None})
    return options


def classify_choice_menu(options: list[dict[str, Any]]) -> str:
    if options and all((opt.get("text") or "").startswith("【分岐") for opt in options):
        return "branch_marker"
    return "user_choice"


def payload_bytes(record: dict[str, Any]) -> bytes:
    return bytes.fromhex(record.get("payload_hex") or "")


def decode_u16(data: bytes, pos: int) -> int | None:
    if pos + 2 > len(data):
        return None
    return struct.unpack_from("<H", data, pos)[0]


def decode_i32(data: bytes, pos: int) -> int | None:
    if pos + 4 > len(data):
        return None
    return struct.unpack_from("<i", data, pos)[0]


def decode_block_id(record: dict[str, Any]) -> str | None:
    data = payload_bytes(record)
    if len(data) == 3 and data[0] == 0x04:
        return f"b{struct.unpack_from('<H', data, 1)[0]:04x}"
    return None


def read_ref_token(data: bytes, pos: int) -> tuple[str, int] | None:
    if pos + 3 > len(data) or data[pos] != 0x02:
        return None
    return f"t{struct.unpack_from('<H', data, pos + 1)[0]:04x}", pos + 3


def read_int_token(data: bytes, pos: int) -> tuple[int, int] | None:
    if pos + 5 > len(data) or data[pos] != 0x01:
        return None
    value = struct.unpack_from("<i", data, pos + 1)[0]
    return value, pos + 5


def decode_expression_record(record: dict[str, Any]) -> dict[str, Any]:
    opcode = record["opcode"]
    data = payload_bytes(record)
    decoded: dict[str, Any] = {
        "offset": record["offset_hex"],
        "line": record["line"],
        "opcode": record["opcode_hex"],
        "payload": record.get("payload_hex") or "",
    }

    if opcode in COMPARE_OPERATORS and len(data) >= 11:
        dest = read_ref_token(data, 0)
        lhs = read_ref_token(data, 3)
        rhs = read_int_token(data, 6)
        if dest and lhs and rhs:
            decoded.update(
                {
                    "kind": "compare",
                    "dest": dest[0],
                    "var": lhs[0].replace("t", "var_", 1),
                    "operator": COMPARE_OPERATORS[opcode],
                    "value": rhs[0],
                }
            )
            decoded["text"] = f"{decoded['var']} {decoded['operator']} {decoded['value']}"
            return decoded

    if opcode == OP_LOGICAL_OR and len(data) >= 9:
        dest = read_ref_token(data, 0)
        lhs = read_ref_token(data, 3)
        rhs = read_ref_token(data, 6)
        if dest and lhs and rhs:
            decoded.update(
                {
                    "kind": "logical",
                    "dest": dest[0],
                    "operator": "OR",
                    "left": lhs[0],
                    "right": rhs[0],
                }
            )
            decoded["text"] = f"{decoded['left']} OR {decoded['right']}"
            return decoded

    decoded["kind"] = "unknown_expr"
    decoded["text"] = f"{record['opcode_hex']}({record.get('payload_hex') or ''})"
    return decoded


def decode_expression(records: list[dict[str, Any]]) -> dict[str, Any]:
    decoded_records: list[dict[str, Any]] = []
    temp_texts: dict[str, str] = {}
    final_text: str | None = None

    for record in records:
        if record["opcode"] not in EXPR_OPS:
            continue
        decoded = decode_expression_record(record)
        decoded_records.append(decoded)

        if decoded.get("kind") == "compare":
            temp_texts[decoded["dest"]] = decoded["text"]
            final_text = decoded["text"]
        elif decoded.get("kind") == "logical":
            left = temp_texts.get(decoded["left"], decoded["left"])
            right = temp_texts.get(decoded["right"], decoded["right"])
            text = f"({left}) {decoded['operator']} ({right})"
            temp_texts[decoded["dest"]] = text
            decoded["expanded_text"] = text
            final_text = text
        else:
            final_text = decoded["text"]

    return {
        "text": final_text or "(undecoded condition)",
        "records": decoded_records,
    }


def decode_assignment_record(record: dict[str, Any]) -> dict[str, Any] | None:
    if record["opcode"] != OP_ASSIGN:
        return None
    data = payload_bytes(record)
    dest = read_ref_token(data, 0)
    value = read_int_token(data, 3) if dest else None
    if not dest or not value:
        return None
    return {
        "offset": record["offset_hex"],
        "line": record["line"],
        "var": dest[0].replace("t", "var_", 1),
        "value": value[0],
        "payload": record.get("payload_hex") or "",
    }


def clean_script_text(text: str) -> str:
    cleaned = text.replace("\\n", "\n").replace("\\d", "")
    cleaned = re.sub(r"#[A-Z0-9_]+\\[^#]+#", "", cleaned)
    cleaned = re.sub(r"#(?:STAND|BG|BGM|SE|SOUND|CUT|EV|MOVIE)[^#]*#", "", cleaned)
    cleaned = re.sub(r"@m[0-9A-Fa-f]+", "", cleaned)
    cleaned = cleaned.replace("@0", "")
    return cleaned


def format_interactive_terms(text: str) -> str:
    return strip_interactive_markers(text)


def strip_interactive_markers(text: str) -> str:
    text = INTERACTIVE_BOLD_RE.sub(r"\1", text)
    return INTERACTIVE_TERM_RE.sub(r"\1", text)


def extract_interactive_terms(text: str) -> list[str]:
    terms = [match.group(1) for match in INTERACTIVE_TERM_RE.finditer(text)]
    terms.extend(match.group(1) for match in INTERACTIVE_BOLD_RE.finditer(text))
    return unique_ordered([term for term in terms if term])


def interactive_term_candidates(term: str) -> list[str]:
    return unique_ordered([term, *INTERACTIVE_TERM_TRANSLATION_HINTS.get(term, [])])


def bold_interactive_terms_in_translation(text: str, source_text: str) -> str:
    return text


def resolve_protagonist_placeholder(text: str) -> str:
    return format_interactive_terms(clean_script_text(text).replace("%s", PROTAGONIST_NAME))


def is_probable_speaker_name(value: str) -> bool:
    stripped = value.strip()
    if not stripped:
        return False
    upper = stripped.upper()
    if "\\" in stripped or "/" in stripped or "." in stripped:
        return False
    if upper.endswith((".BMP", ".WAV", ".SCR", ".PRG")):
        return False
    if stripped.startswith("bg"):
        return False
    return True


def parse_records(data: bytes, section_offsets: list[int], section_index: int) -> tuple[list[dict[str, Any]], str]:
    start = section_offsets[section_index]
    end = section_offsets[section_index + 1] if section_index + 1 < len(section_offsets) else len(data)
    pos = start + 16
    records: list[dict[str, Any]] = []

    while pos + 6 <= end:
        opcode, length, line = struct.unpack_from("<HHH", data, pos)
        if opcode == 0 and length == 0 and line == 0:
            return records, "zeros"
        if length < 6 or pos + length > end:
            records.append(
                {
                    "offset": pos,
                    "offset_hex": hx(pos),
                    "opcode": opcode,
                    "opcode_hex": f"0x{opcode:04x}",
                    "length": length,
                    "line": line,
                    "parse_error": "invalid_length",
                }
            )
            return records, "invalid"

        payload = data[pos + 6 : pos + length]
        strings = extract_type3_strings(payload)
        record = {
            "offset": pos,
            "offset_hex": hx(pos),
            "rel_offset": pos - start,
            "rel_offset_hex": hx(pos - start, 4),
            "opcode": opcode,
            "opcode_hex": f"0x{opcode:04x}",
            "length": length,
            "line": line,
            "strings": strings,
            "payload_hex": payload.hex(),
        }
        if opcode == OP_SELECT:
            record["choices"] = parse_choice_payload(strings)
        records.append(record)

        pos += length
        if opcode == OP_END:
            return records, "term"

    return records, "next"


def is_scenario_call(script_name: str) -> bool:
    if not script_name.lower().endswith(".scr"):
        return False
    if script_name.upper().startswith("PRG_"):
        return False
    if script_name in NON_SCENARIO_CALLS:
        return False
    return True


def first_title(records: list[dict[str, Any]]) -> str | None:
    if not records:
        return None
    first = records[0]
    if first["opcode"] == OP_TITLE and first["strings"]:
        return first["strings"][0].lstrip("†")
    return None


def chapter_from_title(title: str) -> str:
    match = re.search(r"【(.+?)(?:-|】)", title)
    return match.group(1) if match else title


def unique_ordered(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def extract_calls(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    calls: list[dict[str, Any]] = []
    for rec in records:
        if rec["opcode"] == OP_CALL and len(rec["strings"]) >= 2:
            script, label = rec["strings"][0], rec["strings"][1]
            calls.append(
                {
                    "offset": rec["offset_hex"],
                    "line": rec["line"],
                    "script": script,
                    "label": label,
                    "scenario_like": is_scenario_call(script),
                }
            )
    return calls


def extract_calls_with_context(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    calls: list[dict[str, Any]] = []
    current_label: str | None = None
    for rec in records:
        if rec["opcode"] == OP_LABEL and rec["strings"]:
            current_label = rec["strings"][0]
        if rec["opcode"] == OP_CALL and len(rec["strings"]) >= 2:
            script, label = rec["strings"][0], rec["strings"][1]
            calls.append(
                {
                    "offset": rec["offset_hex"],
                    "line": rec["line"],
                    "controller_label": current_label,
                    "script": script,
                    "label": label,
                    "scenario_like": is_scenario_call(script),
                }
            )
    return calls


def parse_choices_map(path: Path) -> list[str]:
    if not path.exists():
        return []
    result: list[str] = []
    pattern = re.compile(r"^\s*\d+\.\s+(.+?)\s*$", re.M)
    for match in pattern.finditer(path.read_text(encoding="utf-8")):
        result.append(match.group(1).strip().strip("『』"))
    return result


def build_scene_script_map(
    sections: list[dict[str, Any]],
    scene_sections: list[dict[str, Any]],
) -> tuple[dict[str, int], list[str], list[str]]:
    """Map .scr names to scene section indexes using the chapter menu section."""
    chapter_menu = None
    for section in sections:
        labels = [r["strings"][0] for r in section["records"] if r["opcode"] == OP_LABEL and r["strings"]]
        if "CHAPTER_MENU_0" in labels:
            chapter_menu = section
            break
    if not chapter_menu:
        return {}, [], ["CHAPTER_MENU_0 section not found"]

    names = [
        call["script"]
        for call in extract_calls(chapter_menu["records"])
        if call["scenario_like"] and call["script"] not in EXTRA_MENU_SCRIPTS
    ]
    names = unique_ordered(names)

    warnings: list[str] = []
    if len(names) != len(scene_sections):
        warnings.append(
            f"script name count {len(names)} does not match scenario title count {len(scene_sections)}"
        )

    mapping: dict[str, int] = {}
    for script_name, scene_section in zip(names, scene_sections):
        mapping[script_name] = scene_section["section_index"]
    return mapping, names, warnings


def find_next_block_mark(records: list[dict[str, Any]], start: int, block_id: str) -> int | None:
    for index in range(start, len(records)):
        record = records[index]
        if record["opcode"] == OP_BLOCK_MARK and decode_block_id(record) == block_id:
            return index
    return None


def parse_if_block(records: list[dict[str, Any]], start: int, end: int) -> dict[str, Any] | None:
    if start >= end or records[start]["opcode"] != OP_EXPR_START:
        return None

    cursor = start + 1
    expression_records: list[dict[str, Any]] = []
    while cursor < end and records[cursor]["opcode"] != OP_IF_SKIP:
        if records[cursor]["opcode"] in EXPR_OPS:
            expression_records.append(records[cursor])
        cursor += 1

    if cursor >= end or records[cursor]["opcode"] != OP_IF_SKIP:
        return None

    if_id = decode_block_id(records[cursor])
    if not if_id:
        return None
    false_marker = find_next_block_mark(records, cursor + 1, if_id)
    if false_marker is None or false_marker > end:
        return None

    jump_over_index: int | None = None
    if false_marker > cursor + 1 and records[false_marker - 1]["opcode"] == OP_JUMP_OVER:
        jump_over_index = false_marker - 1

    expression = decode_expression(expression_records)
    info: dict[str, Any] = {
        "start": start,
        "if_index": cursor,
        "if_id": if_id,
        "condition": expression,
        "true_range": [cursor + 1, false_marker if jump_over_index is None else jump_over_index],
        "false_marker": false_marker,
        "false_range": None,
        "end_index": false_marker + 1,
    }

    if jump_over_index is not None:
        end_id = decode_block_id(records[jump_over_index])
        if end_id:
            end_marker = find_next_block_mark(records, false_marker + 1, end_id)
            if end_marker is not None and end_marker <= end:
                info.update(
                    {
                        "jump_over_index": jump_over_index,
                        "end_id": end_id,
                        "false_range": [false_marker + 1, end_marker],
                        "end_index": end_marker + 1,
                    }
                )
    return info


def negated_condition_text(condition_text: str) -> str:
    if condition_text.startswith("(") and condition_text.endswith(")"):
        return f"NOT {condition_text}"
    return f"NOT ({condition_text})"


def find_route_section(sections: list[dict[str, Any]], script_to_section: dict[str, int]) -> dict[str, Any] | None:
    best: tuple[int, dict[str, Any]] | None = None
    for section in sections:
        labels = {
            record["strings"][0]
            for record in section["records"]
            if record["opcode"] == OP_LABEL and record["strings"]
        }
        if "ROOT_SELECT" not in labels:
            continue
        scenario_calls = sum(
            1
            for call in extract_calls(section["records"])
            if call["scenario_like"] and call["script"] in script_to_section
        )
        if best is None or scenario_calls > best[0]:
            best = (scenario_calls, section)
    return best[1] if best else None


def build_route_logic(
    route_section: dict[str, Any] | None,
    script_to_scene: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    if not route_section:
        return {"section_index": None, "labels": [], "calls": [], "edges": [], "jumps": [], "unresolved_jumps": []}

    records = route_section["records"]
    label_positions = [
        (index, record["strings"][0])
        for index, record in enumerate(records)
        if record["opcode"] == OP_LABEL and record["strings"]
    ]
    label_set = {label for _, label in label_positions}
    label_ranges: list[dict[str, Any]] = []
    for pos, (index, label) in enumerate(label_positions):
        next_index = label_positions[pos + 1][0] if pos + 1 < len(label_positions) else len(records)
        label_ranges.append({"label": label, "start": index + 1, "end": next_index})

    calls: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    jumps: list[dict[str, Any]] = []
    branch_blocks: list[dict[str, Any]] = []
    call_counter = 0

    def is_terminal_candidate(scene: dict[str, Any]) -> bool:
        title = scene.get("title") or ""
        script = (scene.get("script") or "").lower()
        return "-終" in title or "bad" in script

    def add_call(record: dict[str, Any], label: str, conditions: list[str], predecessors: list[str]) -> str | None:
        nonlocal call_counter
        if record["opcode"] != OP_CALL or len(record["strings"]) < 2:
            return None
        script, target_label = record["strings"][0], record["strings"][1]
        if script not in script_to_scene:
            return None

        call_counter += 1
        scene = script_to_scene[script]
        call_id = f"call_{call_counter:04d}"
        call = {
            "id": call_id,
            "controller_label": label,
            "offset": record["offset_hex"],
            "line": record["line"],
            "script": script,
            "label": target_label,
            "scene_index": scene["scene_index"],
            "scene_title": scene["title"],
            "conditions": conditions,
            "terminal_candidate": is_terminal_candidate(scene),
        }
        calls.append(call)
        for predecessor in predecessors:
            prev_call = next((item for item in calls if item["id"] == predecessor), None)
            if prev_call and prev_call["script"] != script:
                edge_confidence = "medium-high"
                note = None
                if prev_call.get("terminal_candidate"):
                    edge_confidence = "low"
                    note = "Previous scene looks like an ending/bad-end candidate; script-call fallthrough may not be runtime story flow."
                edges.append(
                    {
                        "from": prev_call["script"],
                        "to": script,
                        "from_call": predecessor,
                        "to_call": call_id,
                        "controller_label": label,
                        "conditions": conditions,
                        "source": "route_controller_structured",
                        "confidence": edge_confidence,
                        **({"note": note} if note else {}),
                    }
                )
        return call_id

    def walk(label: str, start: int, end: int, conditions: list[str], predecessors: list[str]) -> list[str]:
        current_predecessors = list(predecessors)
        cursor = start
        while cursor < end:
            if_info = parse_if_block(records, cursor, end)
            if if_info:
                condition_text = if_info["condition"]["text"]
                branch_blocks.append(
                    {
                        "controller_label": label,
                        "line": records[if_info["if_index"]]["line"],
                        "offset": records[if_info["if_index"]]["offset_hex"],
                        "if_id": if_info["if_id"],
                        "condition": if_info["condition"],
                        "true_range": if_info["true_range"],
                        "false_range": if_info["false_range"],
                    }
                )
                true_start, true_end = if_info["true_range"]
                true_predecessors = walk(label, true_start, true_end, conditions + [condition_text], current_predecessors)

                if if_info["false_range"]:
                    false_start, false_end = if_info["false_range"]
                    false_predecessors = walk(
                        label,
                        false_start,
                        false_end,
                        conditions + [negated_condition_text(condition_text)],
                        current_predecessors,
                    )
                else:
                    false_predecessors = list(current_predecessors)

                seen: set[str] = set()
                current_predecessors = []
                for predecessor in [*true_predecessors, *false_predecessors]:
                    if predecessor not in seen:
                        seen.add(predecessor)
                        current_predecessors.append(predecessor)
                cursor = if_info["end_index"]
                continue

            record = records[cursor]
            call_id = add_call(record, label, conditions, current_predecessors)
            if call_id:
                current_predecessors = [call_id]
            elif record["opcode"] == OP_JUMP and record["strings"]:
                target = record["strings"][0]
                jumps.append(
                    {
                        "controller_label": label,
                        "offset": record["offset_hex"],
                        "line": record["line"],
                        "target": target,
                        "target_label_exists": target in label_set,
                        "conditions": conditions,
                    }
                )
                current_predecessors = []
            cursor += 1
        return current_predecessors

    for label_range in label_ranges:
        walk(label_range["label"], label_range["start"], label_range["end"], [], [])

    unresolved_jumps = [jump for jump in jumps if not jump["target_label_exists"]]
    return {
        "section_index": route_section["section_index"],
        "section_offset": route_section["offset_hex"],
        "labels": label_ranges,
        "calls": calls,
        "edges": edges,
        "jumps": jumps,
        "unresolved_jumps": unresolved_jumps,
        "branch_blocks": branch_blocks,
    }


def build_variable_semantics(scene_table: list[dict[str, Any]], sections: list[dict[str, Any]]) -> dict[str, Any]:
    section_to_scene = {scene["section_index"]: scene for scene in scene_table}
    semantics: dict[str, Any] = {}
    writes: list[dict[str, Any]] = []

    for section in sections:
        scene = section_to_scene.get(section["section_index"])
        if not scene:
            continue

        choice_by_label: dict[str, list[dict[str, Any]]] = {}
        for choice in scene["choices"]:
            for option in choice["options"]:
                target = option.get("target")
                if not target:
                    continue
                choice_by_label.setdefault(target, []).append(
                    {
                        "choice_line": choice["line"],
                        "choice_kind": choice["kind"],
                        "option_text": option["text"],
                        "target": target,
                    }
                )

        current_label: str | None = None
        for record in section["records"]:
            if record["opcode"] == OP_LABEL and record["strings"]:
                current_label = record["strings"][0]

            assignment = decode_assignment_record(record)
            if not assignment:
                continue

            choice_sources = choice_by_label.get(current_label or "", [])
            write = {
                **assignment,
                "scene_index": scene["scene_index"],
                "script": scene["script"],
                "scene_title": scene["title"],
                "label": current_label,
                "choice_sources": choice_sources,
            }
            writes.append(write)

            value_key = str(assignment["value"])
            entry = semantics.setdefault(assignment["var"], {}).setdefault(value_key, [])
            entry.append(write)

    return {"writes": writes, "by_var_value": semantics}


def source_to_phrase(source: dict[str, Any]) -> str:
    choice_sources = source.get("choice_sources") or []
    if choice_sources:
        choice = choice_sources[0]
        text = choice["option_text"]
        if choice.get("choice_kind") == "branch_marker":
            return f"满足内部分岐「{text}」"
        return f"选择「{text}」"
    label = source.get("label")
    if label:
        return f"到达 label `{label}` 后设置"
    return "脚本设置"


def semantic_phrase(var: str, value: int, variable_semantics: dict[str, Any]) -> str | None:
    manual = MANUAL_CONDITION_MEANINGS.get((var, value))
    if manual:
        return manual

    sources = variable_semantics.get("by_var_value", {}).get(var, {}).get(str(value), [])
    if not sources:
        return None

    sources = [source for source in sources if source.get("choice_sources")]
    if not sources:
        return None

    phrases: list[str] = []
    seen: set[str] = set()
    for source in sources:
        phrase = source_to_phrase(source)
        detail = f"{phrase}（{source['script']} / {source['scene_title']}）"
        if detail not in seen:
            seen.add(detail)
            phrases.append(detail)
        if len(phrases) >= 3:
            break
    return "；".join(phrases)


def humanize_condition(condition: str, variable_semantics: dict[str, Any]) -> str:
    not_match = re.fullmatch(r"NOT \((.+)\)", condition)
    if not_match:
        inner = humanize_condition(not_match.group(1), variable_semantics)
        return f"不满足：{inner}"

    def replace_compare(match: re.Match[str]) -> str:
        var = match.group(1)
        op = match.group(2)
        value = int(match.group(3))
        phrase = semantic_phrase(var, value, variable_semantics)
        if not phrase:
            return match.group(0)
        if op == "==":
            return phrase
        if op == "!=":
            return f"不满足：{phrase}"
        return f"{match.group(0)}（{phrase}）"

    return re.sub(r"(var_[0-9a-f]{4})\s*(==|!=|<= or flag-test)\s*(-?\d+)", replace_compare, condition)


def add_condition_humanization(target: dict[str, Any], variable_semantics: dict[str, Any]) -> None:
    conditions = target.get("conditions") or []
    target["conditions_humanized"] = [humanize_condition(condition, variable_semantics) for condition in conditions]


def annotate_route_logic_semantics(route_logic: dict[str, Any], variable_semantics: dict[str, Any]) -> None:
    for collection_name in ("calls", "edges", "jumps", "unresolved_jumps"):
        for item in route_logic.get(collection_name, []):
            add_condition_humanization(item, variable_semantics)
    for block in route_logic.get("branch_blocks", []):
        text = block.get("condition", {}).get("text")
        if text:
            block["condition"]["humanized"] = humanize_condition(text, variable_semantics)


def unresolved_jump_for_target(route_logic: dict[str, Any], target: str, preferred_label: str | None = None) -> dict[str, Any] | None:
    candidates = [jump for jump in route_logic.get("unresolved_jumps", []) if jump["target"] == target]
    if preferred_label:
        for jump in candidates:
            if jump.get("controller_label") == preferred_label:
                return jump
    return candidates[0] if candidates else None


def build_inferred_route_contexts(scene_table: list[dict[str, Any]], route_logic: dict[str, Any]) -> dict[str, Any]:
    route_specs = [
        {
            "target": "hina",
            "chapter": "日生",
            "route_name": "日生",
            "entry_script": "hina01.scr",
            "preferred_label": "ROOT_4",
            "source_kind": "story_jump",
            "note": "Inferred from unresolved ROOT_4 jump target `hina`; chapter-menu labels map this route to hina01.scr onward.",
        },
        {
            "target": "ROOT_6",
            "chapter": "六章",
            "route_name": "六章",
            "entry_script": "6-01.scr",
            "preferred_label": "ROOT_5",
            "source_kind": "story_jump",
            "note": "Inferred from unresolved ROOT_5 jump to ROOT_6; route label is absent in the controller section.",
        },
        {
            "target": "ROOT_KURO",
            "chapter": "黒の章",
            "route_name": "黒の章",
            "entry_script": "kuro01.scr",
            "preferred_label": "CHAPTER_START",
            "source_kind": "chapter_selector",
            "note": "Inferred from chapter-selector jump target ROOT_KURO plus chapter-menu script order.",
        },
        {
            "target": "ROOT_AO",
            "chapter": "蒼の章",
            "route_name": "蒼の章",
            "entry_script": "aono00.scr",
            "preferred_label": "CHAPTER_START",
            "source_kind": "chapter_selector",
            "note": "Inferred from chapter-selector jump target ROOT_AO plus chapter-menu script order.",
        },
        {
            "target": "ROOT_EPILOGUE",
            "chapter": "あとがき",
            "route_name": "あとがき",
            "entry_script": "atogaki.scr",
            "preferred_label": "CHAPTER_START",
            "source_kind": "chapter_selector",
            "note": "Inferred from chapter-selector jump target ROOT_EPILOGUE plus chapter-menu script order.",
        },
    ]

    contexts_by_script: dict[str, list[dict[str, Any]]] = {}
    inferred_edges: list[dict[str, Any]] = []
    scene_by_script = {scene["script"]: scene for scene in scene_table if scene["script"]}

    for spec in route_specs:
        jump = unresolved_jump_for_target(route_logic, spec["target"], spec.get("preferred_label"))
        route_scenes = [scene for scene in scene_table if scene["chapter"] == spec["chapter"]]
        if not jump or not route_scenes:
            continue

        for index, scene in enumerate(route_scenes):
            context = {
                "id": f"inferred_{spec['target']}_{index + 1:03d}",
                "controller_label": jump["controller_label"],
                "offset": jump["offset"],
                "line": jump["line"],
                "script": scene["script"],
                "label": "START",
                "scene_index": scene["scene_index"],
                "scene_title": scene["title"],
                "conditions": jump.get("conditions") or [],
                "conditions_humanized": jump.get("conditions_humanized") or [],
                "route_name": spec["route_name"],
                "source_target": spec["target"],
                "source_kind": spec["source_kind"],
                "confidence": "inferred",
                "note": spec["note"],
            }
            contexts_by_script.setdefault(scene["script"], []).append(context)

        predecessor_script = None
        if spec["target"] == "hina":
            predecessor_script = "4-16.scr"
        elif spec["target"] == "ROOT_6":
            predecessor_script = "comm5-45ed.scr"

        entry_script = spec["entry_script"]
        if predecessor_script in scene_by_script and entry_script in scene_by_script:
            inferred_edges.append(
                {
                    "from": predecessor_script,
                    "to": entry_script,
                    "controller_label": jump["controller_label"],
                    "conditions": jump.get("conditions") or [],
                    "conditions_humanized": jump.get("conditions_humanized") or [],
                    "source": "unresolved_route_target_inference",
                    "confidence": "medium",
                    "note": spec["note"],
                }
            )

        for prev, nxt in zip(route_scenes, route_scenes[1:]):
            inferred_edges.append(
                {
                    "from": prev["script"],
                    "to": nxt["script"],
                    "controller_label": spec["target"],
                    "conditions": [],
                    "conditions_humanized": [],
                    "source": "chapter_route_order_inference",
                    "confidence": "low" if spec["source_kind"] == "chapter_selector" else "medium-low",
                    "note": "Linear order inferred from chapter-menu/archive scene order; exact runtime branch predicates may still be inside scene scripts.",
                }
            )

    return {"contexts_by_script": contexts_by_script, "edges": inferred_edges}


def build_inferred_choice_edges(scene_table: list[dict[str, Any]]) -> list[dict[str, Any]]:
    inferred_edges: list[dict[str, Any]] = []

    for index, scene in enumerate(scene_table):
        script = scene.get("script")
        if not script:
            continue
        next_scene = scene_table[index + 1] if index + 1 < len(scene_table) else None

        for choice in scene["choices"]:
            if choice["kind"] != "user_choice":
                continue
            for option in choice["options"]:
                target = option.get("target")
                if not target or option.get("target_label_exists"):
                    continue

                inferred_script = None
                inference_note = None
                if (
                    target.lower() == "bad"
                    and next_scene
                    and next_scene.get("script")
                    and (
                        "bad" in next_scene["script"].lower()
                        or "-終" in (next_scene.get("title") or "")
                    )
                ):
                    inferred_script = next_scene["script"]
                    inference_note = (
                        "Choice target label is absent in the source scene; inferred to the next archive scene "
                        "because it is a bad/end script."
                    )

                if not inferred_script:
                    continue

                option["inferred_script_target"] = inferred_script
                option["target_resolution"] = "archive_next_bad_scene"
                inferred_edges.append(
                    {
                        "from": script,
                        "to": inferred_script,
                        "line": choice["line"],
                        "choice_text": option["text"],
                        "target": target,
                        "conditions": [f"选择「{option['text']}」"],
                        "conditions_humanized": [f"选择「{option['text']}」"],
                        "source": "missing_choice_target_inference",
                        "confidence": "medium",
                        "note": inference_note,
                    }
                )

    return inferred_edges


def build_scene_annotations(
    scene_table: list[dict[str, Any]],
    route_logic: dict[str, Any],
    inferred_routes: dict[str, Any],
    inferred_choice_edges: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    calls_by_script: dict[str, list[dict[str, Any]]] = {}
    incoming_by_script: dict[str, list[dict[str, Any]]] = {}
    outgoing_by_script: dict[str, list[dict[str, Any]]] = {}

    for call in route_logic.get("calls", []):
        calls_by_script.setdefault(call["script"], []).append(call)
    for edge in [*route_logic.get("edges", []), *inferred_routes.get("edges", []), *inferred_choice_edges]:
        outgoing_by_script.setdefault(edge["from"], []).append(edge)
        incoming_by_script.setdefault(edge["to"], []).append(edge)

    annotations: list[dict[str, Any]] = []
    for index, scene in enumerate(scene_table):
        script = scene.get("script")
        route_contexts = calls_by_script.get(script, []) if script else []
        inferred_contexts = inferred_routes.get("contexts_by_script", {}).get(script, []) if script else []
        all_contexts = [*route_contexts, *inferred_contexts]
        incoming = incoming_by_script.get(script, []) if script else []
        outgoing = outgoing_by_script.get(script, []) if script else []
        missing_choice_targets = [
            {
                "line": choice["line"],
                "text": option["text"],
                "target": option["target"],
            }
            for choice in scene["choices"]
            for option in choice["options"]
            if option.get("target") and not option.get("target_label_exists") and not option.get("inferred_script_target")
        ]
        inferred_choice_targets = [
            {
                "line": choice["line"],
                "text": option["text"],
                "target": option["target"],
                "inferred_script_target": option["inferred_script_target"],
                "target_resolution": option["target_resolution"],
            }
            for choice in scene["choices"]
            for option in choice["options"]
            if option.get("inferred_script_target")
        ]
        note = None
        if route_contexts:
            status = "route_controller_annotated"
        elif inferred_contexts:
            status = "inferred_route_annotated"
            note = "Route context inferred from unresolved controller target and chapter-menu script order."
        else:
            status = "scene_order_only"
            note = "No structured route-controller call was found; use chapter-menu/archive order plus local choices for now."

        annotations.append(
            {
                "scene_index": scene["scene_index"],
                "section_index": scene["section_index"],
                "section_offset": scene["section_offset"],
                "script": script,
                "title": scene["title"],
                "chapter": scene["chapter"],
                "prev_scene_order": scene_table[index - 1]["script"] if index > 0 else None,
                "next_scene_order": scene_table[index + 1]["script"] if index + 1 < len(scene_table) else None,
                "status": status,
                "route_contexts": all_contexts,
                "incoming_edges": incoming,
                "outgoing_edges": outgoing,
                "choice_menus": scene["choices"],
                "local_jumps": scene["local_jumps"],
                "missing_choice_targets": missing_choice_targets,
                "inferred_choice_targets": inferred_choice_targets,
                "terminal_candidate": any(call.get("terminal_candidate") for call in all_contexts)
                or "-終" in scene["title"]
                or ("bad" in (script or "").lower()),
                "note": note,
            }
        )
    return annotations


def build_outputs() -> dict[str, Any]:
    data = ARC_PATH.read_bytes()
    section_offsets = find_sections(data)

    sections: list[dict[str, Any]] = []
    opcode_counts: Counter[int] = Counter()
    parse_reasons: Counter[str] = Counter()

    for index, offset in enumerate(section_offsets):
        records, reason = parse_records(data, section_offsets, index)
        parse_reasons[reason] += 1
        for rec in records:
            opcode_counts[rec["opcode"]] += 1
        sections.append(
            {
                "section_index": index,
                "offset": offset,
                "offset_hex": hx(offset),
                "record_count": len(records),
                "parse_end_reason": reason,
                "title": first_title(records),
                "records": records,
            }
        )

    scene_sections = [s for s in sections if s["title"]]
    script_to_section, script_names, warnings = build_scene_script_map(sections, scene_sections)
    section_to_script = {section: script for script, section in script_to_section.items()}

    scene_table: list[dict[str, Any]] = []
    choice_edges: list[dict[str, Any]] = []
    local_jumps: list[dict[str, Any]] = []

    for scene_index, section in enumerate(scene_sections, start=1):
        records = section["records"]
        labels = [r["strings"][0] for r in records if r["opcode"] == OP_LABEL and r["strings"]]
        label_set = set(labels)
        choices: list[dict[str, Any]] = []
        jumps: list[dict[str, Any]] = []

        for rec in records:
            if rec["opcode"] == OP_SELECT:
                options = []
                menu_kind = classify_choice_menu(rec.get("choices", []))
                for opt_index, opt in enumerate(rec.get("choices", []), start=1):
                    target = opt.get("target")
                    option = {
                        "option_index": opt_index,
                        "text": opt.get("text"),
                        "target": target,
                        "target_label_exists": target in label_set if target else False,
                    }
                    options.append(option)
                    choice_edges.append(
                        {
                            "scene_index": scene_index,
                            "script": section_to_script.get(section["section_index"]),
                            "scene_title": section["title"],
                            "record_offset": rec["offset_hex"],
                            "line": rec["line"],
                            "menu_kind": menu_kind,
                            **option,
                        }
                    )
                choices.append(
                    {
                        "record_offset": rec["offset_hex"],
                        "line": rec["line"],
                        "kind": menu_kind,
                        "options": options,
                    }
                )

            if rec["opcode"] == OP_JUMP and rec["strings"]:
                jumps.append(
                    {
                        "record_offset": rec["offset_hex"],
                        "line": rec["line"],
                        "target": rec["strings"][0],
                        "target_label_exists": rec["strings"][0] in label_set,
                    }
                )

        for jump in jumps:
            local_jumps.append(
                {
                    "scene_index": scene_index,
                    "script": section_to_script.get(section["section_index"]),
                    "scene_title": section["title"],
                    **jump,
                }
            )

        scene_table.append(
            {
                "scene_index": scene_index,
                "section_index": section["section_index"],
                "section_offset": section["offset_hex"],
                "script": section_to_script.get(section["section_index"]),
                "title": section["title"],
                "chapter": chapter_from_title(section["title"]),
                "record_count": section["record_count"],
                "text_records": sum(1 for r in records if r["opcode"] == OP_TEXT),
                "labels": labels,
                "choices": choices,
                "local_jumps": jumps,
            }
        )

    graph_nodes = [
        {
            "id": scene["script"] or f"section_{scene['section_index']}",
            "scene_index": scene["scene_index"],
            "title": scene["title"],
            "section_offset": scene["section_offset"],
        }
        for scene in scene_table
    ]

    graph_edges: list[dict[str, Any]] = []
    for prev, nxt in zip(scene_table, scene_table[1:]):
        graph_edges.append(
            {
                "from": prev["script"],
                "to": nxt["script"],
                "source": "archive_scene_order",
                "confidence": "low",
                "note": "Physical scenario section order; not necessarily runtime control flow.",
            }
        )

    script_to_scene = {scene["script"]: scene for scene in scene_table if scene["script"]}
    variable_semantics = build_variable_semantics(scene_table, sections)
    route_section = find_route_section(sections, script_to_section)
    route_logic = build_route_logic(route_section, script_to_scene)
    annotate_route_logic_semantics(route_logic, variable_semantics)
    inferred_routes = build_inferred_route_contexts(scene_table, route_logic)
    inferred_choice_edges = build_inferred_choice_edges(scene_table)
    scene_annotations = build_scene_annotations(scene_table, route_logic, inferred_routes, inferred_choice_edges)
    route_calls = route_logic["calls"]
    for edge in route_logic["edges"]:
        graph_edges.append(edge)
    for edge in inferred_routes["edges"]:
        graph_edges.append(edge)
    for edge in inferred_choice_edges:
        graph_edges.append(edge)

    arc_user_options = [edge["text"].strip("『』") for edge in choice_edges if edge["menu_kind"] == "user_choice"]
    choices_map_options = parse_choices_map(CHOICES_MAP_PATH)
    arc_user_set = set(arc_user_options)
    choices_map_set = set(choices_map_options)
    choice_crosscheck = {
        "arc_user_options_total": len(arc_user_options),
        "arc_user_options_unique": len(arc_user_set),
        "choices_map_options_total": len(choices_map_options),
        "choices_map_options_unique": len(choices_map_set),
        "in_choices_map_not_arc": sorted(choices_map_set - arc_user_set),
        "in_arc_not_choices_map": sorted(arc_user_set - choices_map_set),
    }

    return {
        "meta": {
            "source": str(ARC_PATH.name),
            "sha256": __import__("hashlib").sha256(data).hexdigest(),
            "size_bytes": len(data),
            "section_count": len(sections),
            "scenario_title_sections": len(scene_sections),
            "mapped_scene_scripts": len(script_to_section),
            "parse_reasons": dict(parse_reasons),
            "opcode_counts": {f"0x{k:04x}": v for k, v in opcode_counts.most_common()},
            "warnings": warnings,
            "select_menus": sum(len(scene["choices"]) for scene in scene_table),
            "user_choice_menus": sum(
                1 for scene in scene_table for choice in scene["choices"] if choice["kind"] == "user_choice"
            ),
            "branch_marker_menus": sum(
                1 for scene in scene_table for choice in scene["choices"] if choice["kind"] == "branch_marker"
            ),
            "select_options": len(choice_edges),
            "user_choice_options": sum(1 for edge in choice_edges if edge["menu_kind"] == "user_choice"),
            "branch_marker_options": sum(1 for edge in choice_edges if edge["menu_kind"] == "branch_marker"),
            "scene_annotations_route_controller": sum(
                1 for scene in scene_annotations if scene["status"] == "route_controller_annotated"
            ),
            "scene_annotations_inferred_route": sum(
                1 for scene in scene_annotations if scene["status"] == "inferred_route_annotated"
            ),
            "scene_annotations_order_only": sum(1 for scene in scene_annotations if scene["status"] == "scene_order_only"),
            "variable_assignment_writes": len(variable_semantics["writes"]),
            "inferred_route_contexts": sum(
                len(contexts) for contexts in inferred_routes["contexts_by_script"].values()
            ),
            "inferred_route_edges": len(inferred_routes["edges"]),
            "inferred_choice_edges": len(inferred_choice_edges),
        },
        "sections": [
            {
                key: value
                for key, value in section.items()
                if key != "records"
            }
            for section in sections
        ],
        "scene_script_order": script_names,
        "scene_table": scene_table,
        "choice_edges": choice_edges,
        "local_jumps": local_jumps,
        "variable_semantics": variable_semantics,
        "route_controller_calls": route_calls,
        "route_logic": route_logic,
        "inferred_routes": inferred_routes,
        "inferred_choice_edges": inferred_choice_edges,
        "scene_annotations": scene_annotations,
        "choice_crosscheck": choice_crosscheck,
        "scene_graph": {
            "nodes": graph_nodes,
            "edges": graph_edges,
        },
        "full_disasm": sections,
    }


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def write_report(path: Path, data: dict[str, Any]) -> None:
    meta = data["meta"]
    lines: list[str] = []
    lines.append("# SCRDATA.ARC Inspection Report")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Source: `{meta['source']}`")
    lines.append(f"- SHA-256: `{meta['sha256']}`")
    lines.append(f"- Size: {meta['size_bytes']} bytes")
    lines.append(f"- SCR sections: {meta['section_count']}")
    lines.append(f"- Scenario title sections: {meta['scenario_title_sections']}")
    lines.append(f"- Scene scripts mapped: {meta['mapped_scene_scripts']}")
    lines.append(f"- Parse reasons: `{meta['parse_reasons']}`")
    if meta["warnings"]:
        lines.append("")
        lines.append("## Warnings")
        lines.extend(f"- {warning}" for warning in meta["warnings"])
    lines.append("")
    lines.append("## Scene Coverage")
    lines.append("")
    by_chapter = Counter(scene["chapter"] for scene in data["scene_table"])
    lines.append("| Chapter | Scenes |")
    lines.append("|---|---:|")
    for chapter, count in by_chapter.items():
        lines.append(f"| {chapter} | {count} |")
    lines.append("")
    lines.append("## Choice Coverage")
    lines.append("")
    scenes_with_choices = sum(1 for scene in data["scene_table"] if scene["choices"])
    lines.append(f"- Select menus: {meta['select_menus']}")
    lines.append(f"- User-visible choice menus: {meta['user_choice_menus']}")
    lines.append(f"- Internal branch marker menus: {meta['branch_marker_menus']}")
    lines.append(f"- Select options total: {meta['select_options']}")
    lines.append(f"- User-visible choice options: {meta['user_choice_options']}")
    lines.append(f"- Internal branch marker options: {meta['branch_marker_options']}")
    lines.append(f"- Scenes with choices: {scenes_with_choices}")
    lines.append(f"- Local jumps: {len(data['local_jumps'])}")
    lines.append(f"- Route controller calls mapped: {len(data['route_controller_calls'])}")
    lines.append(f"- Route condition blocks decoded: {len(data['route_logic']['branch_blocks'])}")
    lines.append(f"- Route unresolved jumps: {len(data['route_logic']['unresolved_jumps'])}")
    lines.append(f"- Scene annotations with route context: {meta['scene_annotations_route_controller']}")
    lines.append(f"- Scene annotations with inferred route context: {meta['scene_annotations_inferred_route']}")
    lines.append(f"- Scene annotations using scene order only: {meta['scene_annotations_order_only']}")
    lines.append(f"- Variable assignment writes decoded: {meta['variable_assignment_writes']}")
    lines.append(f"- Inferred route edges: {meta['inferred_route_edges']}")
    lines.append(f"- Inferred choice edges: {meta['inferred_choice_edges']}")
    lines.append("")
    lines.append("## Choice Cross-Check")
    lines.append("")
    cc = data["choice_crosscheck"]
    lines.append(f"- ARC user-visible options: {cc['arc_user_options_total']} total / {cc['arc_user_options_unique']} unique")
    lines.append(
        f"- choices_map_v3_1 options: {cc['choices_map_options_total']} total / {cc['choices_map_options_unique']} unique"
    )
    lines.append(f"- In choices_map but not ARC user choices: {len(cc['in_choices_map_not_arc'])}")
    lines.append(f"- In ARC user choices but not choices_map: {len(cc['in_arc_not_choices_map'])}")
    lines.append("")
    lines.append("## Outputs")
    lines.append("")
    lines.append("- `arc_structure.json`: section summaries and global metadata")
    lines.append("- `scene_table.json`: mapped scene list with labels, choices, and local jumps")
    lines.append("- `choice_edges.json`: option text to local target label mapping")
    lines.append("- `variable_semantics.json`: decoded variable writes linked back to choice options when possible")
    lines.append("- `scene_graph.json`: graph edges with confidence labels")
    lines.append("- `inferred_routes.json`: inferred route contexts for unresolved controller targets")
    lines.append("- `inferred_choice_edges.json`: inferred cross-scene choice target fixes")
    lines.append("- `scene_annotations.json`: per-scene annotation draft for localization context")
    lines.append("- `scene_annotations.md`: compact per-scene annotation table")
    lines.append("- `route_paths.md`: route-controller calls grouped by label, including decoded conditions")
    lines.append("- `route_logic.json`: structured route-controller conditions, calls, jumps, and graph edges")
    lines.append("- `script_annotated.md`: full script draft with scene-level route/condition headers")
    lines.append("- `choice_crosscheck.json`: ARC choices vs choices_map_v3_1 comparison")
    lines.append("- `disasm.json`: full record dump including unknown opcode payload hex")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def md_cell(value: Any) -> str:
    text = str(value) if value is not None else ""
    return text.replace("|", "\\|").replace("\n", "<br>")


def preferred_conditions(item: dict[str, Any]) -> list[str]:
    return item.get("conditions_humanized") or item.get("conditions") or []


def conditions_cell(item: dict[str, Any]) -> str:
    return "<br>".join(md_cell(condition) for condition in preferred_conditions(item)) or "-"


def context_route_name(context: dict[str, Any]) -> str:
    if context.get("route_name"):
        return context["route_name"]
    label = context.get("controller_label") or "(unknown)"
    return ROUTE_LABEL_NAMES.get(label, label)


def normalize_speaker_name(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("\u3000", " ")).strip()


def write_route_paths(path: Path, route_calls: list[dict[str, Any]]) -> None:
    lines = ["# Route Controller Calls", ""]
    grouped: dict[str, list[dict[str, Any]]] = {}
    for call in route_calls:
        grouped.setdefault(call.get("controller_label") or "(none)", []).append(call)
    for label, calls in grouped.items():
        lines.append(f"## {label}")
        lines.append("")
        lines.append("| # | Line | Script | Scene | Title | Conditions |")
        lines.append("|---:|---:|---|---:|---|---|")
        for idx, call in enumerate(calls, start=1):
            lines.append(
                f"| {idx} | {call['line']} | `{call['script']}` | {call['scene_index']} | {md_cell(call['scene_title'])} | {conditions_cell(call)} |"
            )
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_route_logic(path: Path, route_logic: dict[str, Any]) -> None:
    lines = ["# Route Logic", ""]
    lines.append(f"- Section: `{route_logic.get('section_index')}`")
    lines.append(f"- Calls: {len(route_logic.get('calls', []))}")
    lines.append(f"- Structured edges: {len(route_logic.get('edges', []))}")
    lines.append(f"- Branch blocks: {len(route_logic.get('branch_blocks', []))}")
    lines.append(f"- Unresolved jumps: {len(route_logic.get('unresolved_jumps', []))}")
    lines.append("")

    if route_logic.get("unresolved_jumps"):
        lines.append("## Unresolved Jumps")
        lines.append("")
        lines.append("| Label | Line | Target | Conditions |")
        lines.append("|---|---:|---|---|")
        for jump in route_logic["unresolved_jumps"]:
            lines.append(f"| {jump['controller_label']} | {jump['line']} | `{jump['target']}` | {conditions_cell(jump)} |")
        lines.append("")

    lines.append("## Branch Blocks")
    lines.append("")
    lines.append("| Label | Line | Condition |")
    lines.append("|---|---:|---|")
    for block in route_logic.get("branch_blocks", []):
        condition = block.get("condition", {})
        condition_text = condition.get("humanized") or condition.get("text") or "-"
        lines.append(f"| {block['controller_label']} | {block['line']} | {md_cell(condition_text)} |")
    lines.append("")

    lines.append("## Structured Edges")
    lines.append("")
    lines.append("| From | To | Label | Confidence | Conditions |")
    lines.append("|---|---|---|---|---|")
    for edge in route_logic.get("edges", []):
        lines.append(
            f"| `{edge['from']}` | `{edge['to']}` | {edge['controller_label']} | {edge.get('confidence', '-')} | {conditions_cell(edge)} |"
        )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_scene_annotations(path: Path, annotations: list[dict[str, Any]]) -> None:
    lines = ["# Scene Annotations", ""]
    lines.append("| # | Script | Title | Status | Route Context | Choices | Notes |")
    lines.append("|---:|---|---|---|---|---:|---|")
    for scene in annotations:
        route_contexts = []
        for context in scene["route_contexts"]:
            condition_list = preferred_conditions(context)
            conditions = conditions_cell(context)
            route_name = context_route_name(context)
            if condition_list:
                route_contexts.append(f"{route_name} ({context['controller_label']}:{context['line']})<br>{conditions}")
            else:
                route_contexts.append(f"{route_name} ({context['controller_label']}:{context['line']})")
        route_context_text = "<br>".join(route_contexts) if route_contexts else "-"
        choice_count = sum(len(choice["options"]) for choice in scene["choice_menus"])
        notes = []
        if scene.get("terminal_candidate"):
            notes.append("terminal_candidate")
        if scene.get("missing_choice_targets"):
            targets = ", ".join(f"{item['text']}->{item['target']}" for item in scene["missing_choice_targets"])
            notes.append(f"missing_choice_target: {targets}")
        if scene.get("inferred_choice_targets"):
            targets = ", ".join(
                f"{item['text']}->{item['target']}=>{item['inferred_script_target']}"
                for item in scene["inferred_choice_targets"]
            )
            notes.append(f"inferred_choice_target: {targets}")
        if scene.get("note"):
            notes.append(scene["note"])
        note_text = "<br>".join(notes) if notes else "-"
        lines.append(
            f"| {scene['scene_index']} | `{scene['script']}` | {md_cell(scene['title'])} | {scene['status']} | {route_context_text} | {choice_count} | {md_cell(note_text)} |"
        )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def scene_route_cell(scene: dict[str, Any]) -> str:
    routes: list[str] = []
    for context in scene["route_contexts"]:
        name = context_route_name(context)
        if context.get("confidence") == "inferred":
            name = f"{name} (inferred)"
        if name not in routes:
            routes.append(name)
    if not routes:
        routes.append(scene["chapter"])
    return "<br>".join(md_cell(route) for route in routes)


def scene_entry_cell(scene: dict[str, Any]) -> str:
    items: list[str] = []
    for context in scene["route_contexts"]:
        prefix = f"{context_route_name(context)} / {context.get('controller_label')}:{context.get('line')}"
        if context.get("confidence") == "inferred":
            prefix += " / inferred"
        conditions = preferred_conditions(context)
        if conditions:
            items.extend(f"{prefix}: {condition}" for condition in conditions)
        else:
            items.append(f"{prefix}: 无额外条件")

    if not items:
        prev_scene = scene.get("prev_scene_order")
        if prev_scene:
            items.append(f"未找到 route-controller 入口；暂按 archive 顺序从 `{prev_scene}` 之后进入")
        else:
            items.append("archive 中的首个场景；未找到更上层入口条件")
    return "<br>".join(md_cell(item) for item in items)


def scene_upstream_cell(scene: dict[str, Any]) -> str:
    items: list[str] = []
    for edge in scene["incoming_edges"]:
        prefix = f"`{edge.get('from')}` -> `{edge.get('to')}` / {edge.get('source')} / {edge.get('confidence', '-')}"
        conditions = preferred_conditions(edge)
        if conditions:
            items.extend(f"{prefix}: {condition}" for condition in conditions)
        else:
            items.append(prefix)
    return "<br>".join(md_cell(item) for item in items) or "-"


def scene_choices_cell(scene: dict[str, Any]) -> str:
    items: list[str] = []
    for choice in scene["choice_menus"]:
        kind = "内部分岐" if choice["kind"] == "branch_marker" else "选择肢"
        options = []
        for option in choice["options"]:
            target = option.get("target") or "-"
            if option.get("inferred_script_target"):
                suffix = f" => {option['inferred_script_target']} (inferred)"
            else:
                suffix = "" if option.get("target_label_exists") else " (?)"
            options.append(f"{option['text']} -> {target}{suffix}")
        items.append(f"line {choice['line']} / {kind}: " + " ; ".join(options))
    return "<br>".join(md_cell(item) for item in items) or "-"


def scene_notes_cell(scene: dict[str, Any]) -> str:
    notes: list[str] = []
    if scene.get("terminal_candidate"):
        notes.append("terminal_candidate")
    if scene.get("missing_choice_targets"):
        targets = ", ".join(f"{item['text']}->{item['target']}" for item in scene["missing_choice_targets"])
        notes.append(f"missing_choice_target: {targets}")
    if scene.get("inferred_choice_targets"):
        targets = ", ".join(
            f"{item['text']}->{item['target']}=>{item['inferred_script_target']}"
            for item in scene["inferred_choice_targets"]
        )
        notes.append(f"inferred_choice_target: {targets}")
    if scene.get("note"):
        notes.append(scene["note"])
    return "<br>".join(md_cell(note) for note in notes) or "-"


def script_body_lines(records: list[dict[str, Any]], include_technical: bool = True) -> list[str]:
    lines: list[str] = []
    current_speaker: str | None = None
    pending_name: str | None = None
    last_content_line: str | None = None

    def append_structural(line: str = "") -> None:
        nonlocal last_content_line
        lines.append(line)
        last_content_line = None

    def append_content(line: str, dedupe_name_variant: bool = False) -> None:
        nonlocal last_content_line
        if dedupe_name_variant and line == last_content_line:
            return
        lines.append(line)
        last_content_line = line

    for record in records:
        if record["opcode"] == OP_LABEL and record["strings"]:
            label = record["strings"][0]
            if include_technical and label != "TOP":
                if lines and lines[-1]:
                    append_structural("")
                append_structural(f"> local label: `{label}`")
            elif not include_technical:
                last_content_line = None
            continue

        if record["opcode"] == OP_VALUE and record["strings"]:
            value = record["strings"][0]
            if is_probable_speaker_name(value):
                pending_name = normalize_speaker_name(value)
            continue

        if record["opcode"] == OP_CALL and len(record["strings"]) >= 2:
            script, label = record["strings"][0], record["strings"][1]
            if script.upper() == "PRG_NAME.SCR":
                if label == "NAME_NON":
                    current_speaker = None
                elif label == "PLAYER":
                    current_speaker = PROTAGONIST_FULL_NAME
                elif label == "NAME":
                    current_speaker = pending_name or "NAME"
                continue
            if include_technical and is_scenario_call(script):
                if lines and lines[-1]:
                    append_structural("")
                append_structural(f"> scenario call: `{script}` / `{label}`")
            continue

        if record["opcode"] in (OP_TEXT, OP_FORMAT_TEXT) and record["strings"]:
            text = resolve_protagonist_placeholder(record["strings"][0])
            dedupe_name_variant = record["opcode"] == OP_FORMAT_TEXT
            for raw_line in text.splitlines() or [text]:
                line = raw_line.strip()
                if not line:
                    continue
                if current_speaker:
                    append_content(f"{current_speaker}: {line}", dedupe_name_variant)
                else:
                    append_content(line, dedupe_name_variant)
            continue

        if record["opcode"] == OP_SELECT:
            if lines and lines[-1]:
                append_structural("")
            kind = "内部分岐" if classify_choice_menu(record.get("choices", [])) == "branch_marker" else "选择肢"
            append_structural(f"> {kind} line {record['line']}")
            for option in record.get("choices", []):
                target = option.get("target") or "-"
                append_structural(f"> - {option.get('text')} -> `{target}`")
            continue

        if record["opcode"] == OP_JUMP and record["strings"]:
            if include_technical:
                if lines and lines[-1]:
                    append_structural("")
                append_structural(f"> jump -> `{record['strings'][0]}`")
            else:
                last_content_line = None

    return lines


def normalize_choice_text(value: str | None) -> str:
    text = resolve_protagonist_placeholder(str(value or ""))
    text = text.replace("\xa0", " ")
    text = re.sub(r"[（(].*?[）)]", "", text)
    replacements = {
        "湊": "港",
        "先程": "先ほど",
        "出来": "でき",
        "無い": "ない",
        "事": "こと",
        "訊": "尋",
        "訪": "尋",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = re.sub(r"[『』「」“”\"'`]", "", text)
    text = re.sub(r"[。．.、,，！？!?]", "", text)
    text = re.sub(r"[\s\u3000]+", "", text)
    return text


def clean_route_plan_choice(raw: str) -> str:
    text = raw.strip().replace("\xa0", " ")
    text = re.sub(r"[（(]※.*?[）)]", "", text).strip()
    return text


def is_route_plan_skip_line(raw: str, block: dict[str, Any], line_no: int) -> bool:
    text = raw.strip().replace("\xa0", " ")
    chapter_headings = {
        "序章",
        "序章はじまり",
        "１章",
        "一章",
        "２章",
        "二章",
        "３章",
        "三章",
        "４章",
        "四章",
        "５章",
        "五章",
        "黒の章",
        "蒼の章",
    }
    result_labels = {
        "一章-結末２",
        "夏帆-結末",
        "日生25-2",
        "四章37-2、六章03-1",
        "蒼の章39-2",
        "六章-終",
        "千代エンド",
        "ベストエンド",
    }
    exact_skip = {
        "",
        "↓",
        "　↓",
        "→",
        "その他シーン回収",
        "最初から物語を開始",
        "未読部分を回収すれば終了。",
    }

    if line_no == block["start"]:
        return True
    if text in exact_skip or text in chapter_headings or text in result_labels:
        return True
    if text.startswith("※") or text.startswith("♪"):
        return True
    if "SAVE" in text and ("より" in text or "♪" in text or "回収用" in text):
        return True
    if "メニュー画面" in text or "言の葉" in text:
        return True
    if "→" in text:
        return True
    return False


def parse_bookish_route_blocks(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []

    raw_lines = path.read_text(encoding="utf-8").splitlines()
    routes: list[dict[str, Any]] = []
    for spec in BOOKISH_ROUTE_BLOCKS:
        choices: list[dict[str, Any]] = []
        end = min(spec["end"], len(raw_lines))
        for line_no in range(spec["start"], end + 1):
            raw = raw_lines[line_no - 1]
            if is_route_plan_skip_line(raw, spec, line_no):
                continue
            text = clean_route_plan_choice(raw)
            if not text:
                continue
            choices.append(
                {
                    "line": line_no,
                    "text": text,
                    "normalized": normalize_choice_text(text),
                }
            )
        routes.append(
            {
                "key": spec["key"],
                "name": spec["name"],
                "kind": spec["kind"],
                "source_line_range": [spec["start"], spec["end"]],
                "choices": choices,
            }
        )
    return routes


def is_bad_choice_option(option: dict[str, Any]) -> bool:
    text = str(option.get("text") or "")
    target = str(option.get("target") or "")
    combined = f"{text} {target}".lower()
    return any(token in combined for token in ("bad", "badroute", "バッド", "ＢＡＤ", "終"))


def fallback_bookish_user_option(
    options: list[dict[str, Any]],
    route_key: str,
    plan_norms: set[str],
) -> dict[str, Any] | None:
    if not options:
        return None

    route_terms = {
        "hinase": ["日生", "hina", "hinase"],
        "kirishima": ["桐島", "七葵", "nana", "nanaki", "kiri"],
        "chiyo": ["千代", "tiyo", "chiyo"],
        "toya": ["十夜", "兄", "ani", "kuro", "黒"],
        "ao": ["蒼", "ao", "aono"],
        "natsuko": ["夏帆", "kaho"],
    }

    scored: list[tuple[float, dict[str, Any]]] = []
    for index, option in enumerate(options):
        text = str(option.get("text") or "")
        target = str(option.get("target") or "")
        combined = f"{text} {target}"
        normalized = normalize_choice_text(text)
        score = -float(index) / 1000.0
        if is_bad_choice_option(option):
            score -= 1000
        if normalized in plan_norms:
            score += 100
        for term in route_terms.get(route_key, []):
            if term in combined:
                score += 8
        scored.append((score, option))

    scored.sort(key=lambda item: item[0], reverse=True)
    return scored[0][1]


def select_bookish_route_choices(data: dict[str, Any], route: dict[str, Any]) -> dict[str, Any]:
    plan_choices = route["choices"]
    plan_norms = {choice["normalized"] for choice in plan_choices if choice["normalized"]}
    matched_plan_indices: set[int] = set()
    soft_skipped_plan_indices: set[int] = set()
    selected_choices: list[dict[str, Any]] = []
    cursor = 0

    for scene in data["scene_annotations"]:
        for choice in scene["choice_menus"]:
            if choice["kind"] != "user_choice":
                continue

            option_by_norm: dict[str, dict[str, Any]] = {}
            for option in choice["options"]:
                normalized = normalize_choice_text(option.get("text"))
                if normalized:
                    option_by_norm.setdefault(normalized, option)

            matched_index: int | None = None
            selected_option: dict[str, Any] | None = None
            while cursor < len(plan_choices):
                current = plan_choices[cursor]
                if current["normalized"] in option_by_norm:
                    break
                if current["text"] not in BOOKISH_SOFT_SKIPPABLE_PLAN_CHOICES:
                    break
                soft_skipped_plan_indices.add(cursor)
                cursor += 1
            if cursor < len(plan_choices):
                normalized = plan_choices[cursor]["normalized"]
                if normalized in option_by_norm:
                    matched_index = cursor
                    selected_option = option_by_norm[normalized]

            fallback = False
            if selected_option is None:
                selected_option = fallback_bookish_user_option(choice["options"], route["key"], plan_norms)
                fallback = True
            else:
                matched_plan_indices.add(matched_index if matched_index is not None else cursor)
                cursor = (matched_index if matched_index is not None else cursor) + 1

            if selected_option is None:
                continue

            planned_choice = plan_choices[matched_index] if matched_index is not None else None
            selected_choices.append(
                {
                    "scene_index": scene["scene_index"],
                    "script": scene["script"],
                    "title": scene["title"],
                    "record_offset": choice["record_offset"],
                    "line": choice["line"],
                    "selected_text": selected_option.get("text"),
                    "selected_target": selected_option.get("target"),
                    "planned_text": planned_choice["text"] if planned_choice else None,
                    "planned_line": planned_choice["line"] if planned_choice else None,
                    "fallback": fallback,
                }
            )

    unmatched = [
        choice
        for index, choice in enumerate(plan_choices)
        if index not in matched_plan_indices and index not in soft_skipped_plan_indices
    ]
    soft_skipped = [choice for index, choice in enumerate(plan_choices) if index in soft_skipped_plan_indices]
    return {
        "selected_choices": selected_choices,
        "matched_choice_count": len(matched_plan_indices),
        "soft_skipped_choice_count": len(soft_skipped_plan_indices),
        "soft_skipped_planned_choices": soft_skipped,
        "fallback_choice_count": sum(1 for choice in selected_choices if choice["fallback"]),
        "unmatched_planned_choices": unmatched,
    }


def build_bookish_route_plan(data: dict[str, Any]) -> dict[str, Any]:
    routes = []
    for route in parse_bookish_route_blocks(CHOICES_PATH):
        selection = select_bookish_route_choices(data, route)
        routes.append({**route, **selection})
    return {
        "source": str(CHOICES_PATH.name),
        "line_ranges_are_1_based": True,
        "notes": [
            "Route choices are parsed from choices.txt and matched against ARC user-choice menus in scene order.",
            "fallback=true means no walkthrough choice matched that menu within the local scan window; the generator chose a non-bad option for rendering.",
            "soft-skipped choices are walkthrough items from looping/paged mini-menus that are not used to block later story choices.",
            "Internal branch markers are selected by route/plan heuristics during Markdown rendering and are not printed as reader-facing choices.",
        ],
        "routes": routes,
    }


def bookish_selection_lookup(route_plan: dict[str, Any]) -> dict[str, dict[int, dict[str, dict[str, Any]]]]:
    lookup: dict[str, dict[int, dict[str, dict[str, Any]]]] = {}
    for route in route_plan.get("routes", []):
        route_lookup: dict[int, dict[str, dict[str, Any]]] = {}
        for selected in route.get("selected_choices", []):
            scene_lookup = route_lookup.setdefault(selected["scene_index"], {})
            scene_lookup[selected["record_offset"]] = selected
            scene_lookup[f"line:{selected['line']}"] = selected
        lookup[route["key"]] = route_lookup
    return lookup


def bookish_plan_norms_by_route(route_plan: dict[str, Any]) -> dict[str, set[str]]:
    return {
        route["key"]: {choice["normalized"] for choice in route.get("choices", []) if choice.get("normalized")}
        for route in route_plan.get("routes", [])
    }


def option_from_selected_record(options: list[dict[str, Any]], selected: dict[str, Any] | None) -> dict[str, Any] | None:
    if not selected:
        return None
    selected_norm = normalize_choice_text(selected.get("selected_text"))
    selected_target = selected.get("selected_target")
    for option in options:
        if normalize_choice_text(option.get("text")) == selected_norm and option.get("target") == selected_target:
            return option
    for option in options:
        if normalize_choice_text(option.get("text")) == selected_norm:
            return option
    return None


def option_from_forced_choice(options: list[dict[str, Any]], forced: str | None) -> dict[str, Any] | None:
    if not forced:
        return None
    forced_norm = normalize_choice_text(forced)
    for option in options:
        if option.get("target") == forced:
            return option
    for option in options:
        if normalize_choice_text(option.get("text")) == forced_norm:
            return option
    return None


def select_bookish_branch_marker_option(
    options: list[dict[str, Any]],
    route_key: str,
    plan_norms: set[str],
) -> dict[str, Any] | None:
    if not options:
        return None

    route_terms = {
        "hinase": ["日生", "hina", "hinase"],
        "kirishima": ["桐島", "七葵", "nana", "nanaki", "kiri"],
        "chiyo": ["千代", "tiyo", "chiyo"],
        "toya": ["十夜", "兄", "ani", "黒", "kuro", "運命"],
        "ao": ["蒼", "ao", "aono", "aotalk", "aoroute", "aosan", "aoshifuku", "aoisyou"],
        "natsuko": ["夏帆", "kaho"],
        "chapter1_alt": ["蒼", "ao"],
        "hinase25_2": ["日生", "hina", "hinase", "追加"],
        "recovery_4_37_6_03": ["蒼", "ao", "追加"],
        "ao39_2": ["蒼", "ao", "aono", "追加"],
    }

    def has_plan_choice(text: str) -> bool:
        normalized = normalize_choice_text(text)
        return any(normalized and (normalized in item or item in normalized) for item in plan_norms)

    scored: list[tuple[float, dict[str, Any]]] = []
    for index, option in enumerate(options):
        text = str(option.get("text") or "")
        target = str(option.get("target") or "")
        combined = f"{text} {target}"
        lower_combined = combined.lower()
        score = -float(index) / 1000.0

        if is_bad_choice_option(option) or "足らない" in text or "足りない" in text:
            score -= 1000
        if "好感度足りている" in text or "攻略可能" in text:
            score += 20
        if "追加" in text:
            score += 6
        if "クリア済" in text and route_key in {"hinase", "toya", "ao"}:
            score += 2

        if "おにぎり弁当" in plan_norms and "おにぎり" in text:
            score += 30
        if "サンドイッチ弁当" in plan_norms and "サンドイッチ" in text:
            score += 30
        if "ルイス" in plan_norms and "ルイス" in text:
            score += 30
        if "日生" in plan_norms and "日生と行動" in text:
            score += 30
        if "剣道場" in plan_norms and "剣道場" in text:
            score += 30
        if "夏帆にお弁当作りを頼む" in plan_norms and ("夏帆製" in text or "kaho" in lower_combined):
            score += 30

        for term in route_terms.get(route_key, []):
            if term in combined:
                score += 10
        if route_key != "chiyo" and ("千代" in combined or "tiyo" in lower_combined):
            score -= 5
        if route_key not in {"ao", "chapter1_alt", "recovery_4_37_6_03", "ao39_2"} and (
            "蒼" in combined or "ao" in lower_combined
        ):
            score -= 3
        if has_plan_choice(text):
            score += 15

        scored.append((score, option))

    scored.sort(key=lambda item: item[0], reverse=True)
    return scored[0][1]


def bookish_scene_body_lines(
    records: list[dict[str, Any]],
    scene_index: int,
    route_key: str,
    selected_choices: dict[int, dict[str, dict[str, Any]]],
    plan_norms: set[str],
    forced_choices: dict[str, str] | None = None,
    forced_choice_targets: list[str] | None = None,
    emit_choice_markers: bool = True,
) -> list[str]:
    lines: list[str] = []
    current_speaker: str | None = None
    pending_name: str | None = None
    last_content_line: str | None = None
    label_positions: dict[str, int] = {}
    for index, record in enumerate(records):
        if record["opcode"] == OP_LABEL and record["strings"]:
            label_positions.setdefault(record["strings"][0], index)

    def append_structural(line: str = "") -> None:
        nonlocal last_content_line
        lines.append(line)
        last_content_line = None

    def append_content(line: str, dedupe_name_variant: bool = False) -> None:
        nonlocal last_content_line
        if dedupe_name_variant and line == last_content_line:
            return
        lines.append(line)
        last_content_line = line

    def jump_index(target: str | None) -> int | None:
        if target and target in label_positions:
            return label_positions[target] + 1
        return None

    scene_selected = selected_choices.get(scene_index, {})
    cursor = 0
    steps = 0
    max_steps = len(records) * 6 + 100
    select_visits: Counter[str] = Counter()
    forced_target_index = 0

    while cursor < len(records) and steps < max_steps:
        steps += 1
        record = records[cursor]

        if record["opcode"] == OP_VALUE and record["strings"]:
            value = record["strings"][0]
            if is_probable_speaker_name(value):
                pending_name = normalize_speaker_name(value)
            cursor += 1
            continue

        if record["opcode"] == OP_CALL and len(record["strings"]) >= 2:
            script, label = record["strings"][0], record["strings"][1]
            if script.upper() == "PRG_NAME.SCR":
                if label == "NAME_NON":
                    current_speaker = None
                elif label == "PLAYER":
                    current_speaker = PROTAGONIST_FULL_NAME
                elif label == "NAME":
                    current_speaker = pending_name or "NAME"
            cursor += 1
            continue

        if record["opcode"] in (OP_TEXT, OP_FORMAT_TEXT) and record["strings"]:
            text = resolve_protagonist_placeholder(record["strings"][0])
            dedupe_name_variant = record["opcode"] == OP_FORMAT_TEXT
            for raw_line in text.splitlines() or [text]:
                line = raw_line.strip()
                if not line:
                    continue
                if current_speaker:
                    append_content(f"{current_speaker}: {line}", dedupe_name_variant)
                else:
                    append_content(line, dedupe_name_variant)
            cursor += 1
            continue

        if record["opcode"] == OP_SELECT:
            visit_key = record.get("offset_hex") or f"line:{record['line']}"
            select_visits[visit_key] += 1
            if select_visits[visit_key] > 1:
                break
            options = record.get("choices", [])
            selected_option: dict[str, Any] | None = None
            choice_kind = classify_choice_menu(options)
            key = record.get("offset_hex") or f"line:{record['line']}"
            forced_target = None
            if forced_choices:
                forced_target = forced_choices.get(key) or forced_choices.get(f"line:{record['line']}")
            if forced_target is None and forced_choice_targets and forced_target_index < len(forced_choice_targets):
                forced_target = forced_choice_targets[forced_target_index]
                forced_target_index += 1

            if forced_target is not None:
                selected_option = option_from_forced_choice(options, forced_target)

            if selected_option is None and choice_kind == "user_choice":
                selected_record = scene_selected.get(key) or scene_selected.get(f"line:{record['line']}")
                selected_option = option_from_selected_record(options, selected_record)
                if selected_option is None:
                    selected_option = fallback_bookish_user_option(options, route_key, plan_norms)
                if selected_option is not None and emit_choice_markers:
                    if lines and lines[-1]:
                        append_structural("")
                    append_structural(f"> 選択：{resolve_protagonist_placeholder(selected_option.get('text') or '')}")
            elif selected_option is None:
                selected_option = select_bookish_branch_marker_option(options, route_key, plan_norms)

            target_index = jump_index(selected_option.get("target") if selected_option else None)
            if target_index is not None:
                cursor = target_index
                continue
            cursor += 1
            continue

        if record["opcode"] == OP_JUMP and record["strings"]:
            target_index = jump_index(record["strings"][0])
            if target_index is None:
                break
            cursor = target_index
            continue

        if record["opcode"] == OP_END:
            break

        cursor += 1

    return lines


def is_bookish_bad_end_scene(scene: dict[str, Any]) -> bool:
    title = scene.get("title") or ""
    script = (scene.get("script") or "").lower()
    return any(pattern in title for pattern in BOOKISH_BAD_END_TITLE_PATTERNS) or "bad" in script


def is_bookish_other_end_scene(scene: dict[str, Any]) -> bool:
    title = scene.get("title") or ""
    return any(pattern in title for pattern in BOOKISH_OTHER_END_TITLE_PATTERNS)


def is_bookish_main_omitted_scene(scene: dict[str, Any]) -> bool:
    return is_bookish_bad_end_scene(scene) or is_bookish_other_end_scene(scene)


def bookish_display_scene_title(scene: dict[str, Any]) -> str:
    title = scene.get("title") or ""
    match = re.search(r"【(.+?)】", title)
    return match.group(1) if match else title


def route_variant_label(route_keys: list[str]) -> str:
    if set(route_keys) == set(BOOKISH_PRIMARY_ROUTE_KEYS):
        return "全員共通"
    return "・".join(BOOKISH_ROUTE_NAMES.get(key, key) for key in route_keys)


def write_script_annotated(path: Path, data: dict[str, Any]) -> None:
    sections_by_index = {section["section_index"]: section for section in data["full_disasm"]}
    meta = data["meta"]
    lines: list[str] = [
        "# Annotated Script Draft",
        "",
        f"- Source: `{meta['source']}`",
        f"- SHA-256: `{meta['sha256']}`",
        "- Scope: 每个 scene 前置路线/条件/上游关系标注，随后保留原始日文剧本文本。",
        f"- Note: speaker reconstruction uses `PRG_NAME.SCR` calls and nearby name values; PLAYER is rendered as `{PROTAGONIST_FULL_NAME}` and `%s` is rendered as `{PROTAGONIST_NAME}`.",
        "- Note: adjacent duplicate `%s` format-text variants are folded into one default-name line.",
        "- Note: `$...$` in source text marks interactive terms; marker symbols are stripped in readable output.",
        "- Note: `inferred` means route context comes from unresolved controller jump plus chapter-menu/archive order, not an exact decoded label.",
        "",
    ]

    for scene in data["scene_annotations"]:
        section = sections_by_index.get(scene["section_index"])
        lines.append(f"## {scene['scene_index']:03d}. {scene['title']} (`{scene['script']}`)")
        lines.append("")
        lines.append("| Field | Value |")
        lines.append("|---|---|")
        lines.append(f"| Chapter | {md_cell(scene['chapter'])} |")
        lines.append(f"| Route | {scene_route_cell(scene)} |")
        lines.append(f"| Status | `{scene['status']}` |")
        lines.append(f"| Entry Conditions | {scene_entry_cell(scene)} |")
        lines.append(f"| Upstream Edges | {scene_upstream_cell(scene)} |")
        lines.append(f"| Local Choices | {scene_choices_cell(scene)} |")
        lines.append(f"| Archive Prev/Next | `{scene.get('prev_scene_order')}` / `{scene.get('next_scene_order')}` |")
        lines.append(f"| Notes | {scene_notes_cell(scene)} |")
        lines.append("")
        lines.append("### Script")
        lines.append("")
        if not section:
            lines.append("_Missing section records._")
        else:
            body = script_body_lines(section["records"])
            lines.extend(body if body else ["_No text records extracted._"])
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def build_bookish_scene_entries(data: dict[str, Any]) -> list[dict[str, Any]]:
    sections_by_index = {section["section_index"]: section for section in data["full_disasm"]}
    entries: list[dict[str, Any]] = []

    for scene in data["scene_annotations"]:
        section = sections_by_index.get(scene["section_index"])
        route_names = unique_ordered(
            [
                f"{context_route_name(context)} (inferred)"
                if context.get("confidence") == "inferred"
                else context_route_name(context)
                for context in scene["route_contexts"]
            ]
        )
        if not route_names:
            route_names = [scene["chapter"]]

        entries.append(
            {
                "scene_index": scene["scene_index"],
                "script": scene["script"],
                "title": scene["title"],
                "chapter": scene["chapter"],
                "routes": route_names,
                "status": scene["status"],
                "terminal_candidate": scene["terminal_candidate"],
                "choice_menus": scene["choice_menus"],
                "body_lines": script_body_lines(section["records"], include_technical=False) if section else [],
            }
        )

    return entries


def write_bookish_archive_order(path: Path, entries: list[dict[str, Any]]) -> None:
    lines: list[str] = [
        "# Bookish Source: Archive Order",
        "",
        f"- Protagonist speaker: `{PROTAGONIST_FULL_NAME}`",
        f"- Protagonist name placeholder: `%s` -> `{PROTAGONIST_NAME}`",
        "- Adjacent duplicate name-variant lines are folded.",
        "- This is a cleaned source layer in archive order, not the final ladder reading order.",
        "",
    ]

    for scene in entries:
        lines.append(f"## {scene['scene_index']:03d}. {scene['title']} (`{scene['script']}`)")
        lines.append("")
        lines.append(f"_Chapter:_ {scene['chapter']}  ")
        lines.append(f"_Route:_ {', '.join(scene['routes'])}")
        if scene["terminal_candidate"]:
            lines.append("_Note:_ terminal candidate")
        lines.append("")
        body = scene["body_lines"]
        lines.extend(body if body else ["_No text records extracted._"])
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def write_bookish_readme(
    path: Path,
    data: dict[str, Any],
    entries: list[dict[str, Any]],
    route_plan: dict[str, Any],
    appendix_files: list[str],
) -> None:
    meta = data["meta"]
    lines = [
        "# Bookish Workspace",
        "",
        "This directory is the staging area for the readable, book-like script.",
        "",
        "## Current Scope",
        "",
        f"- Source ARC: `{meta['source']}`",
        f"- SHA-256: `{meta['sha256']}`",
        f"- Scenes available: {len(entries)}",
        f"- Protagonist speaker: `{PROTAGONIST_FULL_NAME}`",
        f"- Name placeholder: `%s` -> `{PROTAGONIST_NAME}`",
        "- Adjacent duplicate default-name format-text variants have been folded.",
        "- Source `$...$` interactive word markers are stripped while keeping the marked word as plain text.",
        "- Chapter files follow the original large-chapter count and order.",
        "- Chapter-internal body order follows ascending ARC scene index; route labels are emitted inside that scene order.",
        "- EPUB output uses `reading_order/`, which keeps the original chapter files as source/debug layers while arranging the ladder as branch side-stories that return to the main route.",
        "- `00_hajimari.md` starts with the original `PRG_NAME.scr` default-name path, without displaying the name choices.",
        "- The `はじまり` unlock conversation is noted but omitted from reader-facing body text.",
        "- The route ladder is generated from `choices.txt`; bad/end branches are omitted from reader-facing chapters.",
        "- Internal story scripts from the end of the extracted ARC text are generated as appendix files.",
        "- `bookish_zhcn` mirrors this structure using `translated_processed_output_v2`.",
        "",
        "## Files",
        "",
        "- `DESIGN.md`: current bookish structure proposal and route-flow diagram.",
        "- `_source/scenes_default.json`: structured scene bodies after default-name normalization.",
        "- `_source/archive_order_default.md`: same cleaned bodies in archive order for inspection.",
        "- `route_plan.json`: parsed walkthrough blocks and matched ARC choices.",
        "- `manifest.json`: generation metadata and chapter file names.",
        "- `reading_order/`: EPUB source layer ordered as main ladder, side route, return point.",
        "- `appendix/internal_stories.md`: internal story texts separated from the main body.",
        f"- `{BOOKISH_ENDINGS_AND_RECOVERY_FILE}`: walkthrough recovery, other endings, and bad/end scenes separated from the main body.",
        f"- `{BOOKISH_COMPLETE_MD.relative_to(BOOKISH_DIR).as_posix()}`: complete EPUB-ready Markdown assembled from `reading_order/`.",
        f"- `{BOOKISH_EPUB_DIR.relative_to(BOOKISH_DIR).as_posix()}/`: expanded EPUB source tree.",
        f"- `{BOOKISH_EPUB_FILE.relative_to(BOOKISH_DIR).as_posix()}`: packaged complete EPUB.",
        "",
        "## Chapter Files",
        "",
    ]
    lines.extend(f"- `{item['file']}`" for item in BOOKISH_CHAPTER_FILES)
    lines.extend(["", "## Appendix Files", ""])
    lines.extend(f"- `{item}`" for item in appendix_files)
    lines.extend(
        [
            "",
            "## Route Plan Summary",
            "",
            "| Route | Parsed choices | Matched | Soft-skipped | Fallback menus | Unmatched planned choices |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )
    for route in route_plan.get("routes", []):
        lines.append(
            f"| {md_cell(route['name'])} | {len(route.get('choices', []))} | {route.get('matched_choice_count', 0)} | "
            f"{route.get('soft_skipped_choice_count', 0)} | "
            f"{route.get('fallback_choice_count', 0)} | {len(route.get('unmatched_planned_choices', []))} |"
        )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_bookish_zhcn_readme(
    path: Path,
    data: dict[str, Any],
    route_plan: dict[str, Any],
    translator: BookishTranslator,
    appendix_files: list[str],
) -> None:
    meta = data["meta"]
    lines = [
        "# Bookish zh-CN Workspace",
        "",
        "这个目录是 `bookish` 的简体中文阅读版草稿。",
        "",
        "## Current Scope",
        "",
        f"- Source ARC: `{meta['source']}`",
        f"- SHA-256: `{meta['sha256']}`",
        "- Structure source: `bookish` scene-order ladder generated from `choices.txt`.",
        "- Translation source: `bookish/bookish_complete.ja.zh.epub` is the authoritative JP/ZH source; `translated_processed_output_v2`, `processed_output_v2`, `Json/v0.1.0`, and `Modified/ja_zh` are fallbacks.",
        "- Source `$...$` interactive word markers are stripped while keeping the marked word as plain text.",
        "- EPUB output uses `reading_order/`, mirroring the Japanese main-ladder plus side-route return structure.",
        "- `reader_manual.md` is inserted before the story body in the generated EPUB.",
        "- `cover.jpg` is packaged as the generated EPUB cover image.",
        "- `_audit/translation_alignment_audit.md` lists likely untranslated, structurally mismatched, or length-outlier lines.",
        f"- Translation source files loaded: {translator.stats['source_files']}",
        f"- Translation line pairs loaded: {translator.stats['paired_lines']}",
        f"- Authoritative EPUB pairs loaded: {translator.stats['authoritative_epub_pairs']}",
        "- Missing translation hits are left as Japanese so they can be reviewed directly.",
        "",
        "## Chapter Files",
        "",
    ]
    lines.extend(f"- `{item['file']}`" for item in BOOKISH_CHAPTER_FILES)
    lines.extend(["", "## Appendix Files", ""])
    lines.extend(f"- `{item}`" for item in appendix_files)
    lines.extend(
        [
            "",
            "## Route Plan Summary",
            "",
            "| Route | Parsed choices | Matched | Soft-skipped | Fallback menus | Unmatched planned choices |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )
    for route in route_plan.get("routes", []):
        lines.append(
            f"| {md_cell(route['name'])} | {len(route.get('choices', []))} | {route.get('matched_choice_count', 0)} | "
            f"{route.get('soft_skipped_choice_count', 0)} | "
            f"{route.get('fallback_choice_count', 0)} | {len(route.get('unmatched_planned_choices', []))} |"
        )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def chapter_file_specs_for_manifest() -> list[dict[str, str]]:
    return [{"file": item["file"], "chapter": item["chapter"]} for item in BOOKISH_CHAPTER_FILES]


def normalize_translation_key(line: str) -> str:
    text = line.strip()
    text = text.removeprefix("###").strip()
    text = text.replace("遠野 十夜", "遠野　十夜").replace("遠野 紗夜", "遠野　紗夜")
    text = re.sub(r"^([^:：「」]+):\s*「(.*)」$", r"\1「\2」", text)
    text = re.sub(r"^([^:：]+):\s*(.*)$", r"\1「\2」", text)
    text = strip_interactive_markers(text)
    return re.sub(r"[\s\u3000]+", "", text)


def clean_translated_choice(text: str) -> str:
    cleaned = text.strip().removeprefix("###").strip()
    if len(cleaned) >= 2 and cleaned[0] in "「『" and cleaned[-1] in "」』":
        cleaned = cleaned[1:-1]
    return cleaned


def extract_dialogue_content(line: str) -> str | None:
    text = line.strip().removeprefix("###").strip()
    match = re.fullmatch(r"[^「『]+[「『](.*)[」』]", text)
    if match:
        return match.group(1)
    match = re.fullmatch(r"[「『](.*)[」』]", text)
    if match:
        return match.group(1)
    match = re.fullmatch(r"[^「『]+[「『](.*)", text)
    if match:
        return match.group(1)
    match = re.fullmatch(r"[「『](.*)", text)
    if match:
        return match.group(1)
    return None


def normalize_bookish_name(name: str) -> str:
    cleaned = strip_interactive_markers(name.strip().removeprefix("###").strip())
    cleaned = cleaned.replace("　", " ")
    cleaned = re.sub(r"\s+", " ", cleaned)
    compact = cleaned.replace(" ", "")
    for key, value in BOOKISH_ZHCN_SPEAKER_MAP.items():
        if cleaned == key or compact == key.replace("　", "").replace(" ", ""):
            return value
    return BOOKISH_ZHCN_SPEAKER_MAP.get(cleaned, cleaned)


def normalize_zhcn_names(text: str) -> str:
    result = text
    for source, target in sorted(BOOKISH_ZHCN_NAME_REPLACEMENTS.items(), key=lambda item: len(item[0]), reverse=True):
        result = result.replace(source, target)
        compact_source = source.replace("　", "").replace(" ", "")
        if compact_source != source:
            result = result.replace(compact_source, target)
    return result


def clean_stray_dialogue_ascii_quotes(text: str) -> str:
    cleaned = re.sub(r"([「『])\s*\"", r"\1", text)
    cleaned = re.sub(r"\"\s*([」』])", r"\1", cleaned)
    return cleaned


def sanitize_translation_text(text: str) -> str:
    cleaned = text.strip().removeprefix("###").strip()
    cleaned = strip_interactive_markers(cleaned)
    cleaned = normalize_zhcn_names(cleaned)
    cleaned = clean_stray_dialogue_ascii_quotes(cleaned)
    return cleaned


def split_dialogue_line(line: str) -> tuple[str, str, str] | None:
    text = line.strip().removeprefix("###").strip()
    match = re.fullmatch(r"([^:：「」『』]+)[:：]\s*[「『](.*)[」』]?", text)
    if match:
        return (match.group(1).strip(), match.group(2).strip("「『」』").strip(), "colon_quote")
    match = re.fullmatch(r"([^:：「」『』]+)[:：]\s*(.+)", text)
    if match:
        return (match.group(1).strip(), match.group(2).strip("「『」』").strip(), "colon")
    match = re.fullmatch(r"([^:：「」『』]+)[「『](.*)[」』]?", text)
    if match:
        speaker = match.group(1).strip()
        normalized = normalize_bookish_name(speaker)
        if speaker in BOOKISH_ZHCN_SPEAKER_MAP or normalized in set(BOOKISH_ZHCN_SPEAKER_MAP.values()):
            return (speaker, match.group(2).strip("「『」』").strip(), "quote")
    return None


def clean_dialogue_content(text: str) -> str:
    content = sanitize_translation_text(text)
    content = content.strip()
    while len(content) >= 2 and content[0] in "「『" and content[-1] in "」』":
        content = content[1:-1].strip()
    content = content.strip("「『」』").strip()
    while content.startswith("\""):
        content = content[1:].strip()
    while content.endswith("\""):
        content = content[:-1].strip()
    return content


def format_zhcn_dialogue(speaker: str, content: str) -> str:
    return f"{normalize_bookish_name(speaker)}: 「{clean_dialogue_content(content)}」"


def translate_bookish_heading(text: str) -> str:
    if text in BOOKISH_ZHCN_HEADING_MAP:
        return BOOKISH_ZHCN_HEADING_MAP[text]
    translated = normalize_zhcn_names(text)
    for separator in ("・", "、", " / "):
        if separator in translated:
            return separator.join(translate_bookish_heading(part) for part in translated.split(separator))
    return translated


def zhcn_reader_note(kind: str) -> str:
    notes = {
        "hajimari_unlocked": "这段开端在原作中属于通关一次后解锁的场景。",
        "hajimari_gate": "这段开端在原作中属于通关一次后解锁的场景。你可以先阅读它，也可以直接进入序章。",
        "chapter6_bad": "六章的终局分支按坏结局处理，正文只保留主阅读流。",
        "moved_to_appendix": "本章的支线结局、坏结局与回收内容，收录于卷末附录。",
        "empty_main_text": "本章没有单独收入正文的主线段落；相关内容请见卷末附录。",
    }
    return notes[kind]


def is_untranslated_candidate(source: str, candidate: str) -> bool:
    return normalize_translation_key(source) == normalize_translation_key(candidate)


class BookishTranslator:
    def __init__(
        self,
        processed_dir: Path = PROCESSED_V2_DIR,
        translated_dir: Path = TRANSLATED_PROCESSED_V2_DIR,
    ) -> None:
        self.processed_dir = processed_dir
        self.translated_dir = translated_dir
        self.by_file: dict[str, dict[str, list[dict[str, Any]]]] = {}
        self.content_by_file: dict[str, dict[str, list[dict[str, Any]]]] = {}
        self.global_map: dict[str, list[dict[str, Any]]] = {}
        self.global_content_map: dict[str, list[dict[str, Any]]] = {}
        self.stats = {
            "source_files": 0,
            "paired_lines": 0,
            "missing_translated_files": 0,
            "authoritative_epub_pairs": 0,
        }
        self._pick_cache: dict[tuple[str, str | None, str | None, bool, bool], str | None] = {}
        self._load_authoritative_epub()
        self._load()
        self._load_modified_ja_zh()
        self._add_manual_defaults()

    def _load(self) -> None:
        if not self.processed_dir.exists() or not self.translated_dir.exists():
            return
        for jp_path in sorted(self.processed_dir.glob("*/*.txt")):
            rel = jp_path.relative_to(self.processed_dir).as_posix()
            zh_path = self.translated_dir / jp_path.parent.name / f"{jp_path.stem}_translated.txt"
            if not zh_path.exists():
                self.stats["missing_translated_files"] += 1
                continue
            jp_lines = jp_path.read_text(encoding="utf-8").splitlines()
            zh_lines = zh_path.read_text(encoding="utf-8").splitlines()
            for index, jp_line in enumerate(jp_lines):
                key = normalize_translation_key(jp_line)
                if not key:
                    continue
                for offset in (0, -1, 1, -2, 2):
                    zh_index = index + offset
                    if zh_index < 0 or zh_index >= len(zh_lines):
                        continue
                    self._add_candidate(jp_line, zh_lines[zh_index], rel, offset)
                self.stats["paired_lines"] += 1
            self.stats["source_files"] += 1

    def _load_authoritative_epub(self) -> None:
        if not BOOKISH_JA_ZH_EPUB_FILE.exists():
            return

        paragraph_re = re.compile(r"<p([^>]*)>(.*?)</p>", re.S)

        def html_text(raw: str) -> str:
            text = re.sub(r"<[^>]+>", "", raw)
            text = html.unescape(text)
            return re.sub(r"\s+", " ", text).strip()

        with zipfile.ZipFile(BOOKISH_JA_ZH_EPUB_FILE) as archive:
            for name in sorted(archive.namelist()):
                if not name.startswith("OEBPS/text/") or not name.endswith(".xhtml"):
                    continue
                html_source = archive.read(name).decode("utf-8", errors="replace")
                paragraphs = [
                    {
                        "attrs": match.group(1),
                        "text": html_text(match.group(2)),
                    }
                    for match in paragraph_re.finditer(html_source)
                ]
                index = 0
                while index < len(paragraphs) - 1:
                    current = paragraphs[index]
                    next_paragraph = paragraphs[index + 1]
                    if "opacity" in current["attrs"] and current["text"] and next_paragraph["text"]:
                        self._add_candidate(
                            current["text"],
                            next_paragraph["text"],
                            f"authoritative_epub/{Path(name).name}",
                            0,
                            manual=True,
                        )
                        self.stats["authoritative_epub_pairs"] += 1
                        index += 2
                    else:
                        index += 1

    def _load_modified_ja_zh(self) -> None:
        if not MODIFIED_JA_ZH_DIR.exists():
            return
        for path in sorted(MODIFIED_JA_ZH_DIR.glob("*.ja.zh.txt")):
            raw_lines = [line.strip() for line in path.read_text(encoding="utf-8").splitlines()]
            lines = [line for line in raw_lines if line]
            for index in range(0, len(lines) - 1, 2):
                jp_line = lines[index]
                zh_line = lines[index + 1]
                if not jp_line or not zh_line or jp_line == zh_line:
                    continue
                self._add_candidate(jp_line, zh_line, f"Modified/ja_zh/{path.name}", 0)

    def _add_manual_defaults(self) -> None:
        manual = {
            "ええ、そうでしたね。遠野紗夜。それが、貴方のお名前……": "是啊，没错。远野纱夜。那就是，您的名字……",
            "では、お行きなさい、遠野紗夜。今から読むのは貴方の物語。美しい幻想物語": "那么，去吧，远野纱夜。现在要讲述的是您的故事。一个美丽的幻想故事",
            "夢ではなかったのですね": "原来不是梦啊。",
            "当然だろう。夢だと思っていたのか？": "当然。你以为那是梦吗？",
            "……少し。現実だと感じるには、余りにも幻想的だったので": "……有一点。因为那实在太过幻想，很难让人觉得是现实。",
            "ですが、お嬢さん。俺は貴方に知って欲しいんです": "但是，小姐。我希望你能知道。",
        }
        for jp, zh in manual.items():
            self._add_candidate(jp, zh, "prologue/name.txt", 0, manual=True)
            key = normalize_translation_key(jp)
            candidate = {"text": zh, "source_file": "manual", "offset": 0, "manual": True, "speaker": None}
            self.global_content_map.setdefault(key, []).append(candidate)
        hajimari_manual = {
            "遠野 十夜: 「紗夜は俺の世界で一番大切な人だ。心配をするのは当たり前のことだろう」": "远野十夜: 「纱夜是我世界上最重要的人。担心你是理所当然的吧。」",
            "遠野　紗夜: 「ありがとうございます」": "远野纱夜: 「谢谢您。」",
        }
        for jp, zh in hajimari_manual.items():
            self._add_candidate(jp, zh, "prologue/hajimari.txt", 0, manual=True)

    def _add_candidate(self, jp_line: str, zh_line: str, rel: str, offset: int, manual: bool = False) -> None:
        key = normalize_translation_key(jp_line)
        if not key:
            return
        zh_dialogue = split_dialogue_line(zh_line)
        candidate = {
            "text": zh_line,
            "source_file": rel,
            "offset": offset,
            "manual": manual,
            "speaker": zh_dialogue[0] if zh_dialogue else None,
        }
        self.by_file.setdefault(rel, {}).setdefault(key, []).append(candidate)
        self.global_map.setdefault(key, []).append(candidate)

        jp_content = extract_dialogue_content(jp_line)
        zh_content = zh_dialogue[1] if zh_dialogue else extract_dialogue_content(zh_line)
        if jp_content and zh_content:
            content_key = normalize_translation_key(jp_content)
            content_candidate = {**candidate, "text": zh_content}
            self.content_by_file.setdefault(rel, {}).setdefault(content_key, []).append(content_candidate)
            self.global_content_map.setdefault(content_key, []).append(content_candidate)

    def _candidate_score(
        self,
        candidate: dict[str, Any],
        source: str,
        source_file: str | None,
        expected_speaker: str | None = None,
        content_only: bool = False,
    ) -> int:
        text = sanitize_translation_text(candidate["text"])
        score = 0
        if candidate.get("manual"):
            score += 100
        if source_file and candidate.get("source_file") == source_file:
            score += 12 if content_only else 25
        offset = int(candidate.get("offset") or 0)
        score += 18 if offset == 0 else -abs(offset) * 8
        if "###" in candidate["text"]:
            score -= 60
        if JAPANESE_KANA_RE.search(text):
            score -= 80
        if is_untranslated_candidate(source, text):
            score -= 100
        if text:
            ratio = len(strip_interactive_markers(text)) / max(len(strip_interactive_markers(source)), 1)
            if ratio < 0.25 or ratio > 3.5:
                score -= 60

        candidate_dialogue = split_dialogue_line(candidate["text"])
        candidate_speaker_raw = candidate.get("speaker") or (candidate_dialogue[0] if candidate_dialogue else None)
        if expected_speaker and candidate_speaker_raw:
            candidate_speaker = normalize_bookish_name(candidate_speaker_raw)
            expected = normalize_bookish_name(expected_speaker)
            if candidate_speaker == expected:
                score += 70
            elif candidate_speaker not in {"？？？", expected}:
                score -= 110
        elif expected_speaker and not candidate_dialogue and not content_only:
            score -= 90
        elif content_only and candidate_dialogue:
            score -= 15

        return score

    def _pick_candidate(
        self,
        key: str,
        source: str,
        source_file: str | None = None,
        expected_speaker: str | None = None,
        content_only: bool = False,
        content_key: bool = False,
    ) -> str | None:
        if not key:
            return None
        candidates: list[dict[str, Any]] = []
        cache_key = (key, source_file, normalize_bookish_name(expected_speaker) if expected_speaker else None, content_only, content_key)
        if cache_key in self._pick_cache:
            return self._pick_cache[cache_key]
        by_file_map = self.content_by_file if content_key else self.by_file
        global_map = self.global_content_map if content_key else self.global_map
        if source_file:
            candidates.extend(by_file_map.get(source_file, {}).get(key, []))
        candidates.extend(global_map.get(key, []))
        if not candidates:
            self._pick_cache[cache_key] = None
            return None
        unique_candidates: dict[tuple[str, str, int, str | None], dict[str, Any]] = {}
        for candidate in candidates:
            unique_key = (
                candidate["text"],
                candidate.get("source_file") or "",
                int(candidate.get("offset") or 0),
                candidate.get("speaker"),
            )
            unique_candidates.setdefault(unique_key, candidate)

        scored = [
            (self._candidate_score(candidate, source, source_file, expected_speaker, content_only), candidate)
            for candidate in unique_candidates.values()
        ]
        best_score, best = max(scored, key=lambda item: item[0])
        if best_score < -50:
            self._pick_cache[cache_key] = None
            return None
        result = sanitize_translation_text(best["text"])
        self._pick_cache[cache_key] = result
        return result

    def lookup(self, line: str, source_file: str | None = None) -> str | None:
        key = normalize_translation_key(line)
        if not key:
            return None
        speaker = split_dialogue_line(line)
        return self._pick_candidate(
            key,
            line,
            source_file,
            expected_speaker=speaker[0] if speaker else None,
            content_only=False,
            content_key=False,
        )

    def lookup_content(self, line: str, source_file: str | None = None) -> str | None:
        key = normalize_translation_key(line)
        if not key:
            return None
        translated = self._pick_candidate(
            key,
            line,
            source_file,
            expected_speaker=None,
            content_only=True,
            content_key=True,
        )
        return translated or self.lookup(line, source_file)

    def translate_structural_line(self, line: str) -> str:
        if not line:
            return line
        if line.startswith("> 選択："):
            selected = line.removeprefix("> 選択：")
            translated = self.lookup(selected)
            return f"> 选择：{clean_translated_choice(translated) if translated else normalize_zhcn_names(selected)}"
        if line.startswith("> 注：はじまり"):
            return f"> 注：{zhcn_reader_note('hajimari_unlocked')}"
        if line.startswith("> 注：六章-終"):
            return f"> 注：{zhcn_reader_note('chapter6_bad')}"
        if line.startswith("> 注：この章に属する回収"):
            return f"> 注：{zhcn_reader_note('moved_to_appendix')}"
        if line == "_この章では、現在の bookish 方針で表示する本文はありません。_":
            return f"_{zhcn_reader_note('empty_main_text')}_"
        if line.startswith("# "):
            return f"# {translate_bookish_heading(line[2:])}"
        if line.startswith("## "):
            return f"## {translate_bookish_heading(line[3:])}"
        if line.startswith("### "):
            return f"### {translate_bookish_heading(line[4:])}"
        return normalize_zhcn_names(line)

    def translate_line(self, line: str, source_file: str | None = None) -> str:
        if not line:
            return line
        if line.startswith(("#", ">", "_")):
            return self.translate_structural_line(line)
        source_dialogue = split_dialogue_line(line)
        if source_dialogue:
            speaker, source_content, _ = source_dialogue
            content = self._pick_candidate(
                normalize_translation_key(source_content),
                source_content,
                source_file,
                expected_speaker=speaker,
                content_only=True,
                content_key=True,
            )
            if not content:
                full = self.lookup(line, source_file)
                full_dialogue = split_dialogue_line(full) if full else None
                content = full_dialogue[1] if full_dialogue else full
            if content:
                return format_zhcn_dialogue(speaker, content)
            return format_zhcn_dialogue(speaker, source_content)
        translated = self.lookup(line, source_file)
        if translated:
            translated_dialogue = split_dialogue_line(translated)
            if translated_dialogue:
                return format_zhcn_dialogue(translated_dialogue[0], translated_dialogue[1])
            return sanitize_translation_text(translated)
        quote_match = re.fullmatch(r"[「『](.*)[」』]", line)
        if quote_match:
            content = self.lookup_content(quote_match.group(1), source_file)
            if content:
                return f"{line[0]}{clean_dialogue_content(content)}{line[-1]}"
            return normalize_zhcn_names(line)
        quote_match = re.fullmatch(r"[「『](.*)", line)
        if quote_match:
            content = self.lookup_content(quote_match.group(1), source_file)
            if content:
                return f"{line[0]}{clean_dialogue_content(content)}"
            return normalize_zhcn_names(line)
        return normalize_zhcn_names(line)

    def translate_lines(self, lines: list[str], source_file: str | None = None) -> list[str]:
        return [self.translate_line(line, source_file) for line in lines]

    def translate_structural_lines(self, lines: list[str]) -> list[str]:
        return [self.translate_structural_line(line) for line in lines]


def build_bookish_scene_source_files(data: dict[str, Any]) -> dict[int, str]:
    counters: Counter[str] = Counter()
    mapping: dict[int, str] = {}
    for scene in data["scene_annotations"]:
        chapter = scene["chapter"]
        if chapter == "はじまり":
            mapping[scene["scene_index"]] = "prologue/hajimari.txt"
            continue
        folder_stem = BOOKISH_SCENE_SOURCE_FOLDERS.get(chapter)
        if not folder_stem:
            continue
        folder, stem = folder_stem
        counters[chapter] += 1
        mapping[scene["scene_index"]] = f"{folder}/{stem}_{counters[chapter]}.txt"
    return mapping


def find_section_with_label(data: dict[str, Any], label: str) -> dict[str, Any] | None:
    for section in data["full_disasm"]:
        for record in section["records"]:
            if record["opcode"] == OP_LABEL and record["strings"] and record["strings"][0] == label:
                return section
    return None


def render_bookish_name_setup(data: dict[str, Any]) -> list[str]:
    section = find_section_with_label(data, "ENTRY_NORMAL_DEFAULT")
    if not section:
        return [PROTAGONIST_FULL_NAME]
    body = bookish_scene_body_lines(
        section["records"],
        -1,
        "name_default",
        {},
        set(),
        forced_choice_targets=["ENTRY_NORMAL_DEFAULT", "ENTRY_NORMAL_FINISH"],
        emit_choice_markers=False,
    )
    return body if body else [PROTAGONIST_FULL_NAME]


def render_bookish_hajimari_body(data: dict[str, Any]) -> list[str]:
    sections_by_index = {section["section_index"]: section for section in data["full_disasm"]}
    lines: list[str] = []
    scenes = [
        scene
        for scene in data["scene_annotations"]
        if scene.get("chapter") == "はじまり"
    ]
    for scene in sorted(scenes, key=lambda item: item["scene_index"]):
        section = sections_by_index.get(scene["section_index"])
        if not section:
            continue
        body = bookish_scene_body_lines(
            section["records"],
            scene["scene_index"],
            "toya",
            {},
            set(),
            emit_choice_markers=False,
        )
        if not body:
            continue
        if lines:
            lines.extend(["", "---", ""])
        lines.extend(body)
    return lines


def write_bookish_internal_stories(
    path: Path,
    data: dict[str, Any],
    translator: BookishTranslator | None = None,
) -> None:
    sections_by_index = {section["section_index"]: section for section in data["full_disasm"]}
    if translator:
        lines: list[str] = [
            "# 附录：内部故事",
            "",
            "这些文本来自章节菜单末尾的内部阅读资料，不放入正文 ladder。",
            "",
        ]
    else:
        lines = [
            "# 附录：内部故事",
            "",
            "这些文本来自章节菜单末尾的内部阅读资料，不放入正文 ladder。",
            "",
        ]

    for spec in BOOKISH_INTERNAL_STORY_SPECS:
        section = sections_by_index.get(spec["section_index"])
        title = translate_bookish_heading(spec["title"]) if translator else spec["title"]
        lines.append(f"## {title}")
        lines.append("")
        body = script_body_lines(section["records"], include_technical=False) if section else []
        if translator:
            body = translator.translate_lines(body, "ending/ending_1.txt")
        lines.extend(body if body else ["_这个内部资料没有可抽取的正文文本。_"])
        lines.append("")

    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_bookish_endings_and_recovery(
    path: Path,
    data: dict[str, Any],
    route_plan: dict[str, Any],
    translator: BookishTranslator | None = None,
) -> None:
    sections_by_index = {section["section_index"]: section for section in data["full_disasm"]}
    source_file_by_scene = build_bookish_scene_source_files(data)
    scenes_by_chapter: dict[str, list[dict[str, Any]]] = {}
    for scene in data["scene_annotations"]:
        scenes_by_chapter.setdefault(scene["chapter"], []).append(scene)

    selection_lookup = bookish_selection_lookup(route_plan)
    plan_norms_lookup = bookish_plan_norms_by_route(route_plan)
    routes_by_key = {route["key"]: route for route in route_plan.get("routes", [])}
    rendered_cache: dict[tuple[str, int], list[str]] = {}

    def body_signature(body: list[str]) -> str:
        return "\n".join(line.rstrip() for line in body).strip()

    def render_scene(scene: dict[str, Any], route_key: str, allow_bad: bool = False) -> list[str]:
        cache_key = (route_key, scene["scene_index"])
        if cache_key in rendered_cache:
            return rendered_cache[cache_key]
        if is_bookish_bad_end_scene(scene) and not allow_bad:
            rendered_cache[cache_key] = []
            return []
        section = sections_by_index.get(scene["section_index"])
        if not section:
            rendered_cache[cache_key] = []
            return []
        rendered = bookish_scene_body_lines(
            section["records"],
            scene["scene_index"],
            route_key,
            selection_lookup.get(route_key, {}),
            plan_norms_lookup.get(route_key, set()),
        )
        rendered_cache[cache_key] = rendered
        return rendered

    def primary_compare_keys(chapter: str, scene: dict[str, Any]) -> list[str]:
        if scene["scene_index"] <= BOOKISH_CANONICAL_COMMON_SCENE_CUTOFFS.get(chapter, 0):
            return ["hinase"]
        return [
            key
            for key in BOOKISH_CHAPTER_ROUTE_KEYS.get(chapter, BOOKISH_PRIMARY_ROUTE_KEYS)
            if key in BOOKISH_PRIMARY_ROUTE_KEYS
        ]

    def append_scene_block(lines: list[str], scene: dict[str, Any], body: list[str]) -> None:
        title = bookish_display_scene_title(scene)
        if translator:
            title = translate_bookish_heading(title)
        lines.append(f"### {scene['scene_index']:03d}. {title}")
        lines.append("")
        source_file = source_file_by_scene.get(scene["scene_index"])
        if translator:
            body = translator.translate_lines(body, source_file)
        lines.extend(body if body else ["_这个场景没有可抽取的正文文本。_"])

    lines: list[str] = [
        "# 附录：结局与回收",
        "",
        "这里集中放置从正文阅读路径中剔除的攻略回收、other end 和 bad/end 场景。",
        "正文章节只保留通向各路线 true ending 的主阅读流。",
        "",
        "## 攻略回收 / 其他结局",
        "",
    ]

    for route_key, chapters in BOOKISH_RECOVERY_ROUTE_CHAPTERS.items():
        route = routes_by_key.get(route_key)
        route_name = route["name"] if route else BOOKISH_ROUTE_NAMES.get(route_key, route_key)
        lines.append(f"## {translate_bookish_heading(route_name) if translator else route_name}")
        lines.append("")

        wrote_route = False
        seen_signatures: set[str] = set()
        for chapter in chapters:
            for scene in sorted(scenes_by_chapter.get(chapter, []), key=lambda item: item["scene_index"]):
                body = render_scene(scene, route_key)
                signature = body_signature(body)
                if not signature:
                    continue
                primary_signatures = {
                    body_signature(render_scene(scene, primary_key))
                    for primary_key in primary_compare_keys(chapter, scene)
                }
                primary_signatures.discard("")
                if (
                    not is_bookish_other_end_scene(scene)
                    and primary_signatures
                    and signature in primary_signatures
                ):
                    continue
                if signature in seen_signatures:
                    continue
                if wrote_route:
                    lines.extend(["", "---", ""])
                append_scene_block(lines, scene, body)
                seen_signatures.add(signature)
                wrote_route = True

        if not wrote_route:
            lines.append("_没有发现区别于正文主路径的可抽取文本；这个攻略块可能只是进入同一文本的回收条件。_")
        lines.append("")

    lines.extend(
        [
            "## Bad End / 终局分支",
            "",
            "以下场景按 bad/end 处理，不进入正文阅读流。",
            "",
        ]
    )
    wrote_bad = False
    for scene in sorted(data["scene_annotations"], key=lambda item: item["scene_index"]):
        if not is_bookish_bad_end_scene(scene):
            continue
        section = sections_by_index.get(scene["section_index"])
        body = script_body_lines(section["records"], include_technical=False) if section else []
        if wrote_bad:
            lines.extend(["", "---", ""])
        append_scene_block(lines, scene, body)
        wrote_bad = True

    if not wrote_bad:
        lines.append("_没有发现 bad/end 场景。_")

    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_bookish_appendix_files(
    data: dict[str, Any],
    route_plan: dict[str, Any],
    output_dir: Path = BOOKISH_DIR,
    translator: BookishTranslator | None = None,
) -> list[str]:
    appendix_dir = output_dir / "appendix"
    appendix_dir.mkdir(parents=True, exist_ok=True)
    write_bookish_internal_stories(appendix_dir / "internal_stories.md", data, translator)
    write_bookish_endings_and_recovery(
        appendix_dir / Path(BOOKISH_ENDINGS_AND_RECOVERY_FILE).name,
        data,
        route_plan,
        translator,
    )
    return [BOOKISH_INTERNAL_STORIES_FILE, BOOKISH_ENDINGS_AND_RECOVERY_FILE]


def build_bookish_chapter_section_blocks(
    data: dict[str, Any],
    route_plan: dict[str, Any],
    chapter: str,
    route_keys: list[str],
) -> list[dict[str, Any]]:
    sections_by_index = {section["section_index"]: section for section in data["full_disasm"]}
    source_file_by_scene = build_bookish_scene_source_files(data)
    scenes = [
        scene
        for scene in data["scene_annotations"]
        if scene["chapter"] == chapter
    ]

    selection_lookup = bookish_selection_lookup(route_plan)
    plan_norms_lookup = bookish_plan_norms_by_route(route_plan)
    route_kind = {route["key"]: route["kind"] for route in route_plan.get("routes", [])}
    rendered_cache: dict[tuple[str, int], list[str]] = {}

    def body_signature(body: list[str]) -> str:
        return "\n".join(line.rstrip() for line in body).strip()

    def render_scene(scene: dict[str, Any], route_key: str) -> list[str]:
        cache_key = (route_key, scene["scene_index"])
        if cache_key in rendered_cache:
            return rendered_cache[cache_key]
        if is_bookish_main_omitted_scene(scene) or route_kind.get(route_key) == "bad":
            rendered_cache[cache_key] = []
            return []
        section = sections_by_index.get(scene["section_index"])
        if not section:
            rendered_cache[cache_key] = []
            return []
        rendered = bookish_scene_body_lines(
            section["records"],
            scene["scene_index"],
            route_key,
            selection_lookup.get(route_key, {}),
            plan_norms_lookup.get(route_key, set()),
        )
        rendered_cache[cache_key] = rendered
        return rendered

    def add_scene(
        blocks: list[dict[str, Any]],
        label: str | None,
        body: list[str],
        scene: dict[str, Any],
    ) -> None:
        if body_signature(body):
            blocks.append(
                {
                    "label": label,
                    "body": body,
                    "scene_index": scene["scene_index"],
                    "source_file": source_file_by_scene.get(scene["scene_index"]),
                }
            )

    blocks: list[dict[str, Any]] = []
    for scene in sorted(scenes, key=lambda item: item["scene_index"]):
        if scene["scene_index"] <= BOOKISH_CANONICAL_COMMON_SCENE_CUTOFFS.get(chapter, 0):
            scene_route_keys = ["hinase"]
        else:
            scene_route_keys = route_keys
        primary_keys = [key for key in scene_route_keys if key in BOOKISH_PRIMARY_ROUTE_KEYS]
        appendix_keys = [
            key for key in scene_route_keys if key not in BOOKISH_PRIMARY_ROUTE_KEYS and route_kind.get(key) != "bad"
        ]
        scene_signatures: set[str] = set()
        if len(primary_keys) > 1:
            variants: dict[str, dict[str, Any]] = {}
            for route_key in primary_keys:
                body = render_scene(scene, route_key)
                signature = body_signature(body)
                if not signature:
                    continue
                entry = variants.setdefault(signature, {"route_keys": [], "body": body})
                entry["route_keys"].append(route_key)
            if not variants:
                continue
            if len(variants) == 1:
                signature, only = next(iter(variants.items()))
                label = "全員共通" if set(only["route_keys"]) == set(primary_keys) else route_variant_label(only["route_keys"])
                add_scene(blocks, label, only["body"], scene)
                scene_signatures.add(signature)
            else:
                for signature, variant in variants.items():
                    add_scene(blocks, route_variant_label(variant["route_keys"]), variant["body"], scene)
                    scene_signatures.add(signature)
        elif len(primary_keys) == 1:
            label = None if len(scene_route_keys) == 1 else BOOKISH_ROUTE_NAMES.get(primary_keys[0], primary_keys[0])
            body = render_scene(scene, primary_keys[0])
            signature = body_signature(body)
            add_scene(blocks, label, body, scene)
            if signature:
                scene_signatures.add(signature)

        for route_key in appendix_keys:
            label = BOOKISH_ROUTE_NAMES.get(route_key, route_key)
            body = render_scene(scene, route_key)
            signature = body_signature(body)
            if signature and signature not in scene_signatures:
                add_scene(blocks, label, body, scene)
                scene_signatures.add(signature)

    return blocks


def route_label_names(label: str | None) -> list[str]:
    if not label or label == "全員共通":
        return []
    return [item for item in label.split("・") if item]


def filtered_bookish_blocks(
    blocks: list[dict[str, Any]],
    *,
    scene_min: int | None = None,
    scene_max: int | None = None,
    active_route_keys: list[str] | None = None,
) -> list[dict[str, Any]]:
    active_names = [BOOKISH_ROUTE_NAMES.get(key, key) for key in active_route_keys or []]
    active_name_set = set(active_names)
    filtered: list[dict[str, Any]] = []

    for block in blocks:
        scene_index = block["scene_index"]
        if scene_min is not None and scene_index < scene_min:
            continue
        if scene_max is not None and scene_index > scene_max:
            continue

        label = block.get("label")
        names = route_label_names(label)
        if active_route_keys is not None:
            if names and not (set(names) & active_name_set):
                continue
            if names:
                names = [name for name in names if name in active_name_set]
                if not names:
                    continue
                if len(active_names) == 1:
                    label = None
                elif set(names) == active_name_set:
                    label = "全員共通"
                else:
                    label = "・".join(names)

        filtered.append({**block, "label": label})

    return filtered


def bookish_blocks_to_markdown_lines(
    title: str,
    blocks: list[dict[str, Any]],
    translator: BookishTranslator | None = None,
) -> list[str]:
    title = translate_bookish_heading(title) if translator else title
    lines: list[str] = [f"# {title}", ""]
    previous_label: str | None = None
    wrote_body = False
    for block in blocks:
        label = block.get("label")
        if wrote_body:
            lines.extend(["", "---", ""])

        if label:
            if label != previous_label:
                if lines and lines[-1]:
                    lines.append("")
                lines.append(f"## {translate_bookish_heading(label) if translator else label}")
                lines.append("")
        elif lines and lines[-1]:
            lines.append("")

        body = block["body"]
        if translator:
            body = translator.translate_lines(body, block.get("source_file"))
        lines.extend(body)
        previous_label = label
        wrote_body = True

    if not wrote_body:
        lines.append(
            f"_{zhcn_reader_note('empty_main_text')}_"
            if translator
            else "_この章では、現在の bookish 方針で表示する本文はありません。_"
        )
    return lines


BOOKISH_READER_NAVIGATION_LINKS = {
    "reading_order/00_name.md": [("继续阅读：", "开端", "reading_order/00_hajimari_gate.md")],
    "reading_order/00_hajimari_gate.md": [
        ("继续阅读：", "开端内容", "reading_order/00_hajimari.md"),
        ("跳至：", "序章", "reading_order/01_prologue.md"),
    ],
    "reading_order/00_hajimari.md": [("继续阅读：", "序章", "reading_order/01_prologue.md")],
    "reading_order/01_prologue.md": [("继续阅读：", "一章", "reading_order/02_chapter1.md")],
    "reading_order/02_chapter1.md": [("继续阅读：", "二章", "reading_order/03_chapter2.md")],
    "reading_order/03_chapter2.md": [("继续阅读：", "三章", "reading_order/04_chapter3.md")],
    "reading_order/04_chapter3.md": [("继续阅读：", "夏帆", "reading_order/05_natsuko.md")],
    "reading_order/05_natsuko.md": [("继续阅读：", "四章", "reading_order/06_chapter4_to_hinase_branch.md")],
    "reading_order/06_chapter4_to_hinase_branch.md": [
        ("继续阅读：", "日生光线", "reading_order/07_hinase_chapter4_branch.md"),
        ("跳至：", "四章后半", "reading_order/09_chapter4_after_hinase_branch.md"),
    ],
    "reading_order/07_hinase_chapter4_branch.md": [("继续阅读：", "日生光线", "reading_order/08_hinase.md")],
    "reading_order/08_hinase.md": [("返回主线：", "四章后半", "reading_order/09_chapter4_after_hinase_branch.md")],
    "reading_order/09_chapter4_after_hinase_branch.md": [("继续阅读：", "五章", "reading_order/10_chapter5_to_kirichiyo_branch.md")],
    "reading_order/10_chapter5_to_kirichiyo_branch.md": [
        ("继续阅读：", "桐岛七葵线", "reading_order/11_kirishima_chapter5_branch.md"),
        ("继续阅读：", "千代线", "reading_order/13_chiyo_chapter5_branch.md"),
        ("跳至：", "五章后半", "reading_order/16_chapter5_after_kirichiyo_branch.md"),
    ],
    "reading_order/11_kirishima_chapter5_branch.md": [("继续阅读：", "桐岛七葵线", "reading_order/12_kirishima.md")],
    "reading_order/12_kirishima.md": [("返回主线：", "五章后半", "reading_order/16_chapter5_after_kirichiyo_branch.md")],
    "reading_order/13_chiyo_chapter5_branch.md": [("继续阅读：", "千代线", "reading_order/14_chiyo_kirishima_branch.md")],
    "reading_order/14_chiyo_kirishima_branch.md": [("继续阅读：", "千代线", "reading_order/15_chiyo.md")],
    "reading_order/15_chiyo.md": [("返回主线：", "五章后半", "reading_order/16_chapter5_after_kirichiyo_branch.md")],
    "reading_order/16_chapter5_after_kirichiyo_branch.md": [("继续阅读：", "六章", "reading_order/17_chapter6.md")],
    "reading_order/17_chapter6.md": [("继续阅读：", "黑之章", "reading_order/18_kuro.md")],
    "reading_order/18_kuro.md": [("继续阅读：", "苍之章", "reading_order/19_ao.md")],
    "reading_order/19_ao.md": [("继续阅读：", "后记", "reading_order/20_atogaki.md")],
    "reading_order/20_atogaki.md": [("继续阅读：", "附录", BOOKISH_ENDINGS_AND_RECOVERY_FILE)],
}

BOOKISH_FINE_NAVIGATION_ACTIVE_ROUTES = {
    "reading_order/02_chapter1.md": ["hinase", "kirishima", "chiyo", "toya", "ao"],
    "reading_order/03_chapter2.md": ["hinase", "kirishima", "chiyo", "toya", "ao"],
    "reading_order/04_chapter3.md": ["hinase", "kirishima", "chiyo", "toya", "ao"],
    "reading_order/06_chapter4_to_hinase_branch.md": ["hinase", "kirishima", "chiyo", "toya", "ao"],
    "reading_order/09_chapter4_after_hinase_branch.md": ["kirishima", "chiyo", "toya", "ao"],
    "reading_order/16_chapter5_after_kirichiyo_branch.md": ["toya", "ao"],
}

BOOKISH_FINE_NAVIGATION_LABEL_TO_ROUTE = {
    "日生光": "hinase",
    "桐岛七葵": "kirishima",
    "千代": "chiyo",
    "远野十夜": "toya",
    "苍": "ao",
    "日生光線": "hinase",
    "桐島七葵": "kirishima",
    "遠野十夜": "toya",
    "蒼": "ao",
}

BOOKISH_FINE_NAVIGATION_ROUTE_LABEL = {
    "hinase": "日生光",
    "kirishima": "桐岛七葵",
    "chiyo": "千代",
    "toya": "远野十夜",
    "ao": "苍",
}

BOOKISH_ZHCN_DIVIDER_SPECS = [
    {"file": "dividers/00_story.md", "title": "正文", "before": "reading_order/00_name.md"},
    {"file": "dividers/01_prologue.md", "title": "序章", "before": "reading_order/01_prologue.md"},
    {"file": "dividers/02_chapter1.md", "title": "一章", "before": "reading_order/02_chapter1.md"},
    {"file": "dividers/03_chapter2.md", "title": "二章", "before": "reading_order/03_chapter2.md"},
    {"file": "dividers/04_chapter3.md", "title": "三章", "before": "reading_order/04_chapter3.md"},
    {"file": "dividers/05_natsuko.md", "title": "夏帆", "before": "reading_order/05_natsuko.md"},
    {"file": "dividers/06_chapter4.md", "title": "四章", "before": "reading_order/06_chapter4_to_hinase_branch.md"},
    {"file": "dividers/07_hinase.md", "title": "日生光线", "before": "reading_order/07_hinase_chapter4_branch.md"},
    {"file": "dividers/08_chapter5.md", "title": "五章", "before": "reading_order/10_chapter5_to_kirichiyo_branch.md"},
    {"file": "dividers/09_kirishima.md", "title": "桐岛七葵线", "before": "reading_order/11_kirishima_chapter5_branch.md"},
    {"file": "dividers/10_chiyo.md", "title": "千代线", "before": "reading_order/13_chiyo_chapter5_branch.md"},
    {"file": "dividers/11_chapter6.md", "title": "六章", "before": "reading_order/17_chapter6.md"},
    {"file": "dividers/12_kuro.md", "title": "黑之章", "before": "reading_order/18_kuro.md"},
    {"file": "dividers/13_ao.md", "title": "苍之章", "before": "reading_order/19_ao.md"},
    {"file": "dividers/14_atogaki.md", "title": "后记", "before": "reading_order/20_atogaki.md"},
    {"file": "dividers/15_appendix.md", "title": "附录", "before": BOOKISH_ENDINGS_AND_RECOVERY_FILE},
]

BOOKISH_ZHCN_TOC_TITLES: dict[str, str | None] = {
    BOOKISH_ZHCN_READER_MANUAL_FILE: "序言",
    BOOKISH_ZHCN_BOOK_TOC_FILE: "目录",
    "reading_order/00_name.md": "名字",
    "reading_order/00_hajimari_gate.md": "开端",
    "reading_order/00_hajimari.md": None,
    "reading_order/01_prologue.md": "序章",
    "reading_order/02_chapter1.md": "一章",
    "reading_order/03_chapter2.md": "二章",
    "reading_order/04_chapter3.md": "三章",
    "reading_order/05_natsuko.md": "夏帆",
    "reading_order/06_chapter4_to_hinase_branch.md": "四章",
    "reading_order/07_hinase_chapter4_branch.md": "日生光线",
    "reading_order/08_hinase.md": None,
    "reading_order/09_chapter4_after_hinase_branch.md": None,
    "reading_order/10_chapter5_to_kirichiyo_branch.md": "五章",
    "reading_order/11_kirishima_chapter5_branch.md": "桐岛七葵线",
    "reading_order/12_kirishima.md": None,
    "reading_order/13_chiyo_chapter5_branch.md": "千代线",
    "reading_order/14_chiyo_kirishima_branch.md": None,
    "reading_order/15_chiyo.md": None,
    "reading_order/16_chapter5_after_kirichiyo_branch.md": None,
    "reading_order/17_chapter6.md": "六章",
    "reading_order/18_kuro.md": "黑之章",
    "reading_order/19_ao.md": "苍之章",
    "reading_order/20_atogaki.md": "后记",
    BOOKISH_ENDINGS_AND_RECOVERY_FILE: "附录：结局与回收",
    BOOKISH_INTERNAL_STORIES_FILE: "附录：内部故事",
}

BOOKISH_ZHCN_BOOK_TOC_ITEMS = [
    ("名字", "reading_order/00_name.md"),
    ("开端", "reading_order/00_hajimari_gate.md"),
    ("序章", "reading_order/01_prologue.md"),
    ("一章", "reading_order/02_chapter1.md"),
    ("二章", "reading_order/03_chapter2.md"),
    ("三章", "reading_order/04_chapter3.md"),
    ("夏帆", "reading_order/05_natsuko.md"),
    ("四章", "reading_order/06_chapter4_to_hinase_branch.md"),
    ("日生光线", "reading_order/07_hinase_chapter4_branch.md"),
    ("五章", "reading_order/10_chapter5_to_kirichiyo_branch.md"),
    ("桐岛七葵线", "reading_order/11_kirishima_chapter5_branch.md"),
    ("千代线", "reading_order/13_chiyo_chapter5_branch.md"),
    ("六章", "reading_order/17_chapter6.md"),
    ("黑之章", "reading_order/18_kuro.md"),
    ("苍之章", "reading_order/19_ao.md"),
    ("后记", "reading_order/20_atogaki.md"),
    ("附录：结局与回收", BOOKISH_ENDINGS_AND_RECOVERY_FILE),
    ("附录：内部故事", BOOKISH_INTERNAL_STORIES_FILE),
]


def bookish_navigation_lines(source_file: str) -> list[str]:
    entries = BOOKISH_READER_NAVIGATION_LINKS.get(source_file, [])
    lines: list[str] = []
    for prefix, label, target in entries:
        href = bookish_xhtml_filename(target).removeprefix("text/")
        lines.append(f"> {prefix}[{label}]({href})")
    return lines


def bookish_fine_navigation_route_keys(label: str | None, active_route_keys: list[str]) -> set[str]:
    if not label or label in {"全员共通", "全員共通"}:
        return set(active_route_keys)
    keys: set[str] = set()
    for part in label.split("・"):
        key = BOOKISH_FINE_NAVIGATION_LABEL_TO_ROUTE.get(part.strip())
        if key and key in active_route_keys:
            keys.add(key)
    return keys


def bookish_fine_navigation_label(route_keys: list[str]) -> str:
    labels = [BOOKISH_FINE_NAVIGATION_ROUTE_LABEL.get(route_key, route_key) for route_key in route_keys]
    return "・".join(labels)


def split_markdown_segments(lines: list[str]) -> list[list[str]]:
    segments: list[list[str]] = [[]]
    for line in lines:
        if line.strip() == "---":
            segments.append([])
        else:
            segments[-1].append(line)
    return segments


def markdown_segment_heading_label(segment: list[str]) -> str | None:
    for line in segment:
        if line.startswith("## "):
            return line[3:].strip()
    return None


def insert_markdown_anchor(segment: list[str], anchor: str) -> None:
    anchor_line = f"<!-- anchor: {anchor} -->"
    if anchor_line in segment:
        return
    insert_at = 0
    if segment and segment[0].startswith("# "):
        insert_at = 1
        if len(segment) > insert_at and not segment[insert_at].strip():
            insert_at += 1
    segment.insert(insert_at, anchor_line)
    if len(segment) > insert_at + 1 and segment[insert_at + 1].strip():
        segment.insert(insert_at + 1, "")


def apply_bookish_fine_navigation(path: Path, source_file: str) -> None:
    active_route_keys = BOOKISH_FINE_NAVIGATION_ACTIVE_ROUTES.get(source_file)
    if not active_route_keys:
        return

    original_lines = path.read_text(encoding="utf-8").splitlines()
    segments = split_markdown_segments(original_lines)
    block_infos: list[dict[str, Any]] = []

    for segment_index, segment in enumerate(segments):
        if not any(line.strip() for line in segment):
            continue
        label = markdown_segment_heading_label(segment)
        route_keys = bookish_fine_navigation_route_keys(label, active_route_keys)
        if not route_keys:
            continue
        block_infos.append(
            {
                "segment_index": segment_index,
                "route_keys": route_keys,
                "anchor": f"route-block-{segment_index + 1:03d}",
            }
        )

    if len(block_infos) < 2:
        return

    appended_by_segment: dict[int, list[str]] = defaultdict(list)
    for block_position, block in enumerate(block_infos):
        grouped_targets: dict[int, list[str]] = defaultdict(list)
        for route_key in active_route_keys:
            if route_key not in block["route_keys"]:
                continue
            target_position: int | None = None
            for next_position in range(block_position + 1, len(block_infos)):
                if route_key in block_infos[next_position]["route_keys"]:
                    target_position = next_position
                    break
            if target_position is None or target_position == block_position + 1:
                continue
            grouped_targets[target_position].append(route_key)

        for target_position, route_keys in grouped_targets.items():
            target = block_infos[target_position]
            label = bookish_fine_navigation_label(route_keys)
            appended_by_segment[block["segment_index"]].append(
                f"> 沿{label}线继续：[下一段](#{target['anchor']})"
            )

    if not appended_by_segment:
        return

    for block in block_infos:
        insert_markdown_anchor(segments[block["segment_index"]], block["anchor"])

    for segment_index, navigation_lines in appended_by_segment.items():
        segment = segments[segment_index]
        while segment and not segment[-1].strip():
            segment.pop()
        if segment:
            segment.append("")
        segment.extend(navigation_lines)

    output_lines: list[str] = []
    for index, segment in enumerate(segments):
        if index:
            while output_lines and not output_lines[-1].strip():
                output_lines.pop()
            output_lines.extend(["", "---", ""])
        output_lines.extend(segment)
    path.write_text("\n".join(output_lines).rstrip() + "\n", encoding="utf-8")


def append_bookish_navigation(path: Path, source_file: str) -> None:
    lines = bookish_navigation_lines(source_file)
    if not lines:
        return
    original = path.read_text(encoding="utf-8").rstrip()
    path.write_text(f"{original}\n\n---\n\n" + "\n".join(lines) + "\n", encoding="utf-8")


def write_zhcn_divider_files(base_dir: Path = BOOKISH_ZHCN_DIR) -> None:
    for spec in BOOKISH_ZHCN_DIVIDER_SPECS:
        path = base_dir / spec["file"]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"# {spec['title']}\n", encoding="utf-8")


def build_zhcn_epub_source_files(
    reading_order_files: list[str],
    appendix_files: list[str],
) -> tuple[list[str], dict[str, str | None]]:
    source_files = bookish_epub_source_files(reading_order_files, appendix_files)
    divider_before = {spec["before"]: spec["file"] for spec in BOOKISH_ZHCN_DIVIDER_SPECS}
    with_dividers: list[str] = []
    for source_file in source_files:
        divider_file = divider_before.get(source_file)
        if divider_file:
            with_dividers.append(divider_file)
        with_dividers.append(source_file)
    toc_titles = dict(BOOKISH_ZHCN_TOC_TITLES)
    for spec in BOOKISH_ZHCN_DIVIDER_SPECS:
        toc_titles[spec["file"]] = None
    return with_dividers, toc_titles


def render_zhcn_book_toc() -> list[str]:
    lines = ["# 目录", ""]
    for label, source_file in BOOKISH_ZHCN_BOOK_TOC_ITEMS:
        href = bookish_xhtml_filename(source_file).removeprefix("text/")
        lines.append(f"- [{label}]({href})")
    return lines


def write_zhcn_book_toc(path: Path = BOOKISH_ZHCN_DIR / BOOKISH_ZHCN_BOOK_TOC_FILE) -> None:
    path.write_text("\n".join(render_zhcn_book_toc()).rstrip() + "\n", encoding="utf-8")


def write_bookish_markdown_file(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def copy_bookish_markdown_file(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")


def write_bookish_reading_order_files(
    data: dict[str, Any],
    route_plan: dict[str, Any],
    output_dir: Path = BOOKISH_DIR,
    translator: BookishTranslator | None = None,
) -> list[str]:
    reading_dir = output_dir / BOOKISH_READING_ORDER_DIRNAME
    written: list[str] = []

    def finalize_reading_order_file(target_name: str) -> None:
        if translator:
            source_file = f"{BOOKISH_READING_ORDER_DIRNAME}/{target_name}"
            apply_bookish_fine_navigation(reading_dir / target_name, source_file)
            append_bookish_navigation(reading_dir / target_name, source_file)
        written.append(f"{BOOKISH_READING_ORDER_DIRNAME}/{target_name}")

    def add_generated(target_file: str, lines: list[str]) -> None:
        write_bookish_markdown_file(reading_dir / target_file, lines)
        finalize_reading_order_file(target_file)

    def add_copy(source_file: str, target_file: str | None = None) -> None:
        target_name = target_file or source_file
        copy_bookish_markdown_file(output_dir / source_file, reading_dir / target_name)
        finalize_reading_order_file(target_name)

    def add_blocks(target_file: str, title: str, blocks: list[dict[str, Any]]) -> None:
        write_bookish_markdown_file(reading_dir / target_file, bookish_blocks_to_markdown_lines(title, blocks, translator))
        finalize_reading_order_file(target_file)

    def add_hajimari_split() -> None:
        name_title = "# 名字" if translator else "# 名前"
        name_body = render_bookish_name_setup(data)
        if translator:
            name_body = translator.translate_lines(name_body, "prologue/name.txt")
        add_generated("00_name.md", [name_title, "", *name_body])

        if translator:
            gate_lines = ["# 开端", "", f"> 注：{zhcn_reader_note('hajimari_gate')}"]
            hajimari_lines = ["# 开端", "", f"> 注：{zhcn_reader_note('hajimari_unlocked')}", ""]
        else:
            gate_lines = [
                "# はじまり",
                "",
                "> 注：はじまり（十夜と紗夜の外出会話）はクリア後に表示される解放場面です。このまま読むことも、序章へ進むこともできます。",
            ]
            hajimari_lines = [
                "# はじまり",
                "",
                "> 注：はじまり（十夜と紗夜の外出会話）はクリア後に表示される解放場面です。",
                "",
            ]
        add_generated("00_hajimari_gate.md", gate_lines)

        hajimari_body = render_bookish_hajimari_body(data)
        if translator:
            hajimari_body = translator.translate_lines(hajimari_body, "prologue/hajimari.txt")
        hajimari_lines.extend(
            hajimari_body
            if hajimari_body
            else [
                f"_{zhcn_reader_note('empty_main_text')}_"
                if translator
                else "_この場面には抽出できる本文がありません。_"
            ]
        )
        add_generated("00_hajimari.md", hajimari_lines)

    add_hajimari_split()

    for source_file in [
        "01_prologue.md",
        "02_chapter1.md",
        "03_chapter2.md",
        "04_chapter3.md",
        "05_natsuko.md",
    ]:
        add_copy(source_file)

    chapter4_blocks = build_bookish_chapter_section_blocks(
        data,
        route_plan,
        "四章",
        BOOKISH_CHAPTER_ROUTE_KEYS["四章"],
    )
    add_blocks(
        "06_chapter4_to_hinase_branch.md",
        "四章（日生分岐まで）",
        filtered_bookish_blocks(chapter4_blocks, scene_max=131),
    )
    add_blocks(
        "07_hinase_chapter4_branch.md",
        "日生（四章分岐）",
        filtered_bookish_blocks(chapter4_blocks, scene_min=132, scene_max=142, active_route_keys=["hinase"]),
    )
    add_copy("07_hinase.md", "08_hinase.md")
    add_blocks(
        "09_chapter4_after_hinase_branch.md",
        "四章（日生分岐後）",
        filtered_bookish_blocks(
            chapter4_blocks,
            scene_min=132,
            active_route_keys=["kirishima", "chiyo", "toya", "ao"],
        ),
    )

    chapter5_blocks = build_bookish_chapter_section_blocks(
        data,
        route_plan,
        "五章",
        BOOKISH_CHAPTER_ROUTE_KEYS["五章"],
    )
    add_blocks(
        "10_chapter5_to_kirichiyo_branch.md",
        "五章（桐島・千代分岐まで）",
        filtered_bookish_blocks(chapter5_blocks, scene_max=231),
    )
    add_blocks(
        "11_kirishima_chapter5_branch.md",
        "桐島（五章分岐）",
        filtered_bookish_blocks(chapter5_blocks, scene_min=232, scene_max=235, active_route_keys=["kirishima"]),
    )
    add_copy("09_kirishima.md", "12_kirishima.md")
    add_blocks(
        "13_chiyo_chapter5_branch.md",
        "千代（五章分岐）",
        filtered_bookish_blocks(chapter5_blocks, scene_min=232, scene_max=235, active_route_keys=["chiyo"]),
    )

    chiyo_kirishima_blocks = build_bookish_chapter_section_blocks(
        data,
        route_plan,
        "桐島",
        ["chiyo"],
    )
    add_blocks(
        "14_chiyo_kirishima_branch.md",
        "千代（桐島分岐）",
        filtered_bookish_blocks(chiyo_kirishima_blocks, active_route_keys=["chiyo"]),
    )
    add_copy("10_chiyo.md", "15_chiyo.md")
    add_blocks(
        "16_chapter5_after_kirichiyo_branch.md",
        "五章（桐島・千代分岐後）",
        filtered_bookish_blocks(chapter5_blocks, scene_min=232, active_route_keys=["toya", "ao"]),
    )

    for source_file, target_file in [
        ("11_chapter6.md", "17_chapter6.md"),
        ("12_kuro.md", "18_kuro.md"),
        ("13_ao.md", "19_ao.md"),
        ("14_atogaki.md", "20_atogaki.md"),
    ]:
        add_copy(source_file, target_file)

    return written


def write_bookish_chapter_files(
    data: dict[str, Any],
    route_plan: dict[str, Any],
    output_dir: Path = BOOKISH_DIR,
    translator: BookishTranslator | None = None,
) -> list[str]:
    sections_by_index = {section["section_index"]: section for section in data["full_disasm"]}
    source_file_by_scene = build_bookish_scene_source_files(data)
    scenes_by_chapter: dict[str, list[dict[str, Any]]] = {}
    for scene in data["scene_annotations"]:
        scenes_by_chapter.setdefault(scene["chapter"], []).append(scene)

    selection_lookup = bookish_selection_lookup(route_plan)
    plan_norms_lookup = bookish_plan_norms_by_route(route_plan)
    route_kind = {route["key"]: route["kind"] for route in route_plan.get("routes", [])}
    rendered_cache: dict[tuple[str, int], list[str]] = {}

    def body_signature(body: list[str]) -> str:
        return "\n".join(line.rstrip() for line in body).strip()

    def render_scene(scene: dict[str, Any], route_key: str) -> list[str]:
        cache_key = (route_key, scene["scene_index"])
        if cache_key in rendered_cache:
            return rendered_cache[cache_key]
        if is_bookish_main_omitted_scene(scene) or route_kind.get(route_key) == "bad":
            rendered_cache[cache_key] = []
            return []
        section = sections_by_index.get(scene["section_index"])
        if not section:
            rendered_cache[cache_key] = []
            return []
        rendered = bookish_scene_body_lines(
            section["records"],
            scene["scene_index"],
            route_key,
            selection_lookup.get(route_key, {}),
            plan_norms_lookup.get(route_key, set()),
        )
        rendered_cache[cache_key] = rendered
        return rendered

    def add_scene(
        sections: list[dict[str, Any]],
        label: str | None,
        body: list[str],
        scene: dict[str, Any],
    ) -> None:
        if body_signature(body):
            sections.append(
                {
                    "label": label,
                    "body": body,
                    "scene_index": scene["scene_index"],
                    "source_file": source_file_by_scene.get(scene["scene_index"]),
                }
            )

    def build_sections_for_chapter(
        chapter: str,
        route_keys: list[str],
        scenes: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        sections: list[dict[str, Any]] = []

        for scene in sorted(scenes, key=lambda item: item["scene_index"]):
            if scene["scene_index"] <= BOOKISH_CANONICAL_COMMON_SCENE_CUTOFFS.get(chapter, 0):
                scene_route_keys = ["hinase"]
            else:
                scene_route_keys = route_keys
            primary_keys = [key for key in scene_route_keys if key in BOOKISH_PRIMARY_ROUTE_KEYS]
            appendix_keys = [
                key for key in scene_route_keys if key not in BOOKISH_PRIMARY_ROUTE_KEYS and route_kind.get(key) != "bad"
            ]
            scene_signatures: set[str] = set()
            if len(primary_keys) > 1:
                variants: dict[str, dict[str, Any]] = {}
                for route_key in primary_keys:
                    body = render_scene(scene, route_key)
                    signature = body_signature(body)
                    if not signature:
                        continue
                    entry = variants.setdefault(signature, {"route_keys": [], "body": body})
                    entry["route_keys"].append(route_key)
                if not variants:
                    continue
                if len(variants) == 1:
                    signature, only = next(iter(variants.items()))
                    label = "全員共通" if set(only["route_keys"]) == set(primary_keys) else route_variant_label(only["route_keys"])
                    add_scene(sections, label, only["body"], scene)
                    scene_signatures.add(signature)
                else:
                    for signature, variant in variants.items():
                        add_scene(sections, route_variant_label(variant["route_keys"]), variant["body"], scene)
                        scene_signatures.add(signature)
            elif len(primary_keys) == 1:
                label = None if len(scene_route_keys) == 1 else BOOKISH_ROUTE_NAMES.get(primary_keys[0], primary_keys[0])
                body = render_scene(scene, primary_keys[0])
                signature = body_signature(body)
                add_scene(sections, label, body, scene)
                if signature:
                    scene_signatures.add(signature)

            for route_key in appendix_keys:
                label = BOOKISH_ROUTE_NAMES.get(route_key, route_key)
                body = render_scene(scene, route_key)
                signature = body_signature(body)
                if signature and signature not in scene_signatures:
                    add_scene(sections, label, body, scene)
                    scene_signatures.add(signature)

        return sections

    written: list[str] = []
    for spec in BOOKISH_CHAPTER_FILES:
        chapter = spec["chapter"]
        route_keys = BOOKISH_CHAPTER_ROUTE_KEYS.get(chapter, BOOKISH_PRIMARY_ROUTE_KEYS)
        scenes = scenes_by_chapter.get(chapter, [])
        section_blocks = [] if chapter == "はじまり" else build_sections_for_chapter(chapter, route_keys, scenes)

        lines: list[str] = []
        if chapter == "はじまり":
            lines.extend(["# 名字" if translator else "# 名前", ""])
            name_lines = render_bookish_name_setup(data)
            if translator:
                name_lines = translator.translate_lines(name_lines, "prologue/name.txt")
            lines.extend(name_lines)
            lines.extend(["", "---", "", "# 开端" if translator else "# はじまり", ""])
            if translator:
                lines.append(f"> 注：{zhcn_reader_note('hajimari_unlocked')}")
            else:
                lines.append("> 注：はじまり（十夜と紗夜の外出会話）はクリア後に表示される解放場面です。")
            lines.append("")
            hajimari_body = render_bookish_hajimari_body(data)
            if translator:
                hajimari_body = translator.translate_lines(hajimari_body, "prologue/hajimari.txt")
            lines.extend(
                hajimari_body
                if hajimari_body
                else [
                    f"_{zhcn_reader_note('empty_main_text')}_"
                    if translator
                    else "_この場面には抽出できる本文がありません。_"
                ]
            )
        else:
            title = translate_bookish_heading(spec["title"]) if translator else spec["title"]
            lines.extend([f"# {title}", ""])

        if chapter in {"夏帆", "六章"}:
            if translator:
                lines.append(f"> 注：{zhcn_reader_note('moved_to_appendix')}")
            else:
                lines.append(
                    f"> 注：この章に属する回収 / bad / other end 内容は `{BOOKISH_ENDINGS_AND_RECOVERY_FILE}` に移動しています。"
                )
            lines.append("")

        if chapter == "はじまり":
            pass
        elif not section_blocks:
            lines.append(
                f"_{zhcn_reader_note('empty_main_text')}_"
                if translator
                else "_この章では、現在の bookish 方針で表示する本文はありません。_"
            )
        else:
            previous_label: str | None = None
            wrote_body = False
            for block in section_blocks:
                label = block["label"]
                if wrote_body:
                    lines.extend(["", "---", ""])

                if label:
                    if label != previous_label:
                        if lines and lines[-1]:
                            lines.append("")
                        lines.append(f"## {translate_bookish_heading(label) if translator else label}")
                        lines.append("")
                elif lines and lines[-1]:
                    lines.append("")

                body = block["body"]
                if translator:
                    body = translator.translate_lines(body, block.get("source_file"))
                lines.extend(body)
                previous_label = label
                wrote_body = True

        output_path = output_dir / spec["file"]
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
        written.append(spec["file"])

    return written


def bookish_epub_source_files(chapter_files: list[str], appendix_files: list[str]) -> list[str]:
    ordered = list(chapter_files)
    for item in [BOOKISH_ENDINGS_AND_RECOVERY_FILE, BOOKISH_INTERNAL_STORIES_FILE]:
        if item in appendix_files and item not in ordered:
            ordered.append(item)
    for item in appendix_files:
        if item not in ordered:
            ordered.append(item)
    return ordered


def bookish_markdown_title(markdown: str, fallback: str) -> str:
    for line in markdown.splitlines():
        if line.startswith("# "):
            return strip_interactive_markers(line[2:].strip()) or fallback
    return fallback


def bookish_xhtml_filename(source_file: str) -> str:
    stem = source_file.removesuffix(".md").replace("/", "_")
    return f"text/{stem}.xhtml"


def epub_escape(value: str) -> str:
    return html.escape(value, quote=True)


def markdown_inline_to_xhtml(text: str) -> str:
    parts = re.split(r"(`[^`\n]+`|\*\*[^*\n]+\*\*|\[[^\]\n]+\]\([^) \n]+\))", text)
    rendered: list[str] = []
    for part in parts:
        if not part:
            continue
        if part.startswith("`") and part.endswith("`"):
            rendered.append(f"<code>{epub_escape(part[1:-1])}</code>")
        elif part.startswith("**") and part.endswith("**"):
            rendered.append(f"<strong>{epub_escape(part[2:-2])}</strong>")
        elif link_match := re.fullmatch(r"\[([^\]\n]+)\]\(([^) \n]+)\)", part):
            label, href = link_match.groups()
            rendered.append(f'<a href="{epub_escape(href)}">{epub_escape(label)}</a>')
        else:
            rendered.append(epub_escape(part))
    return "".join(rendered)


def epub_blockquote_class(text: str) -> str:
    if text.startswith("選択："):
        return "choice"
    if text.startswith(("继续阅读：", "返回主线：", "跳至：", "也可跳至：", "沿")):
        return "navigation"
    return "note"


def markdown_to_epub_xhtml(
    markdown: str,
    title: str,
    language: str = BOOKISH_EPUB_LANGUAGE,
    body_class: str | None = None,
) -> str:
    body: list[str] = []
    heading_counts: Counter[str] = Counter()
    in_unordered_list = False
    last_visible_block_was_navigation = False

    def close_unordered_list() -> None:
        nonlocal in_unordered_list
        if in_unordered_list:
            body.append("</ul>")
            in_unordered_list = False

    def heading_id(raw: str) -> str:
        base = re.sub(r"[^0-9A-Za-z_-]+", "-", raw).strip("-") or "section"
        heading_counts[base] += 1
        suffix = "" if heading_counts[base] == 1 else f"-{heading_counts[base]}"
        return f"{base}{suffix}"

    for raw_line in markdown.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped:
            close_unordered_list()
            body.append("")
            continue
        if stripped == "---":
            close_unordered_list()
            if last_visible_block_was_navigation:
                body.append('<hr class="scene-break scene-page-break" />')
            else:
                body.append('<hr class="scene-break" />')
            last_visible_block_was_navigation = False
            continue
        anchor_match = re.fullmatch(r"<!--\s*anchor:\s*([0-9A-Za-z_-]+)\s*-->", stripped)
        if anchor_match:
            close_unordered_list()
            body.append(f'<span id="{epub_escape(anchor_match.group(1))}" class="route-anchor"></span>')
            continue
        heading_match = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading_match:
            close_unordered_list()
            level = min(len(heading_match.group(1)), 6)
            text = heading_match.group(2).strip()
            body.append(
                f'<h{level} id="{heading_id(strip_interactive_markers(text))}">'
                f"{markdown_inline_to_xhtml(text)}</h{level}>"
            )
            last_visible_block_was_navigation = False
            continue
        if stripped.startswith("- "):
            if not in_unordered_list:
                body.append("<ul>")
                in_unordered_list = True
            body.append(f"<li>{markdown_inline_to_xhtml(stripped[2:].strip())}</li>")
            last_visible_block_was_navigation = False
            continue
        if line.startswith("> "):
            close_unordered_list()
            text = line[2:].strip()
            block_class = epub_blockquote_class(text)
            body.append(f'<blockquote class="{block_class}"><p>{markdown_inline_to_xhtml(text)}</p></blockquote>')
            last_visible_block_was_navigation = block_class == "navigation"
            continue
        if stripped.startswith("_") and stripped.endswith("_") and len(stripped) > 2:
            close_unordered_list()
            body.append(f'<p class="meta"><em>{markdown_inline_to_xhtml(stripped[1:-1])}</em></p>')
            last_visible_block_was_navigation = False
            continue
        close_unordered_list()
        body.append(f"<p>{markdown_inline_to_xhtml(line)}</p>")
        last_visible_block_was_navigation = False
    close_unordered_list()

    return "\n".join(
        [
            '<?xml version="1.0" encoding="utf-8"?>',
            '<!DOCTYPE html>',
            f'<html xmlns="http://www.w3.org/1999/xhtml" lang="{language}" xml:lang="{language}">',
            "<head>",
            '  <meta charset="utf-8" />',
            f"  <title>{epub_escape(title)}</title>",
            '  <link rel="stylesheet" type="text/css" href="../styles/bookish.css" />',
            "</head>",
            f'<body class="{epub_escape(body_class)}">' if body_class else "<body>",
            *body,
            "</body>",
            "</html>",
            "",
        ]
    )


def write_bookish_complete_markdown(
    base_dir: Path,
    source_files: list[str],
    output_path: Path,
    title: str,
) -> None:
    lines: list[str] = [
        f"# {title}",
        "",
        "_EPUB-ready complete Markdown generated from bookish reading-order files._",
        "",
    ]
    for index, source_file in enumerate(source_files):
        source_path = base_dir / source_file
        if not source_path.exists():
            continue
        if index:
            lines.extend(["", "---", ""])
        lines.append(f"<!-- source: {source_file} -->")
        lines.append("")
        lines.extend(source_path.read_text(encoding="utf-8").splitlines())
    output_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_epub_container(epub_dir: Path) -> None:
    meta_inf = epub_dir / "META-INF"
    meta_inf.mkdir(parents=True, exist_ok=True)
    (epub_dir / "mimetype").write_text("application/epub+zip", encoding="utf-8")
    (meta_inf / "container.xml").write_text(
        "\n".join(
            [
                '<?xml version="1.0" encoding="utf-8"?>',
                '<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">',
                '  <rootfiles>',
                '    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml" />',
                '  </rootfiles>',
                '</container>',
                "",
            ]
        ),
        encoding="utf-8",
    )


def write_epub_styles(epub_dir: Path) -> None:
    styles_dir = epub_dir / "OEBPS" / "styles"
    styles_dir.mkdir(parents=True, exist_ok=True)
    (styles_dir / "bookish.css").write_text(
        "\n".join(
            [
                "body {",
                "  font-family: serif;",
                "  line-height: 1.75;",
                "  margin: 5%;",
                "}",
                "h1, h2, h3 {",
                "  line-height: 1.35;",
                "  page-break-after: avoid;",
                "}",
                "p {",
                "  margin: 0 0 0.65em 0;",
                "}",
                "blockquote {",
                "  border-left: 0.25em solid #777;",
                "  margin: 1em 0;",
                "  padding: 0.2em 0 0.2em 1em;",
                "}",
                "blockquote.choice {",
                "  border-left-color: #444;",
                "  font-weight: bold;",
                "}",
                "blockquote.note, p.meta {",
                "  color: #555;",
                "}",
                "blockquote.navigation {",
                "  border-left-color: #888;",
                "  color: #333;",
                "  page-break-inside: avoid;",
                "}",
                "blockquote.navigation a {",
                "  font-weight: 700;",
                "}",
                "hr.scene-break {",
                "  border: 0;",
                "  border-top: 1px solid #aaa;",
                "  margin: 1.6em 0;",
                "}",
                "hr.scene-page-break {",
                "  border: 0;",
                "  height: 0;",
                "  margin: 0;",
                "  page-break-after: always;",
                "  break-after: page;",
                "}",
                "strong {",
                "  font-weight: 700;",
                "}",
                "code {",
                "  font-family: monospace;",
                "}",
                ".cover {",
                "  margin: 0;",
                "  padding: 0;",
                "  text-align: center;",
                "}",
                ".cover img {",
                "  max-width: 100%;",
                "  max-height: 100vh;",
                "}",
                ".divider-page {",
                "  display: flex;",
                "  min-height: 80vh;",
                "  align-items: center;",
                "  justify-content: center;",
                "  text-align: center;",
                "}",
                ".divider-page h1 {",
                "  margin-top: 35vh;",
                "  font-size: 1.8em;",
                "  font-weight: 400;",
                "}",
                "",
            ]
        ),
        encoding="utf-8",
    )


def write_epub_cover_page(epub_dir: Path, cover_image_href: str, title: str, language: str) -> str:
    href = "text/cover.xhtml"
    image_src = "../" + cover_image_href
    (epub_dir / "OEBPS" / href).write_text(
        "\n".join(
            [
                '<?xml version="1.0" encoding="utf-8"?>',
                '<!DOCTYPE html>',
                f'<html xmlns="http://www.w3.org/1999/xhtml" lang="{language}" xml:lang="{language}">',
                "<head>",
                '  <meta charset="utf-8" />',
                f"  <title>{epub_escape(title)} 封面</title>",
                '  <link rel="stylesheet" type="text/css" href="../styles/bookish.css" />',
                "</head>",
                '<body class="cover">',
                f'  <img src="{epub_escape(image_src)}" alt="{epub_escape(title)} 封面" />',
                "</body>",
                "</html>",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return href


def write_epub_nav(epub_dir: Path, items: list[dict[str, str]], title: str, language: str) -> None:
    nav_items = "\n".join(
        f'      <li><a href="{epub_escape(item["href"])}">{epub_escape(item["title"])}</a></li>' for item in items
    )
    (epub_dir / "OEBPS" / "nav.xhtml").write_text(
        "\n".join(
            [
                '<?xml version="1.0" encoding="utf-8"?>',
                '<!DOCTYPE html>',
                f'<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="{language}" xml:lang="{language}">',
                "<head>",
                '  <meta charset="utf-8" />',
                f"  <title>{epub_escape(title)} Navigation</title>",
                '  <link rel="stylesheet" type="text/css" href="styles/bookish.css" />',
                "</head>",
                "<body>",
                '  <nav epub:type="toc" id="toc">',
                "    <h1>目次</h1>",
                "    <ol>",
                nav_items,
                "    </ol>",
                "  </nav>",
                "</body>",
                "</html>",
                "",
            ]
        ),
        encoding="utf-8",
    )


def write_epub_ncx(epub_dir: Path, items: list[dict[str, str]], identifier: str, title: str) -> None:
    nav_points: list[str] = []
    for index, item in enumerate(items, start=1):
        nav_points.extend(
            [
                f'    <navPoint id="navPoint-{index}" playOrder="{index}">',
                f'      <navLabel><text>{epub_escape(item["title"])}</text></navLabel>',
                f'      <content src="{epub_escape(item["href"])}" />',
                "    </navPoint>",
            ]
        )
    (epub_dir / "OEBPS" / "toc.ncx").write_text(
        "\n".join(
            [
                '<?xml version="1.0" encoding="utf-8"?>',
                '<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">',
                "  <head>",
                f'    <meta name="dtb:uid" content="{epub_escape(identifier)}" />',
                '    <meta name="dtb:depth" content="1" />',
                '    <meta name="dtb:totalPageCount" content="0" />',
                '    <meta name="dtb:maxPageNumber" content="0" />',
                "  </head>",
                f"  <docTitle><text>{epub_escape(title)}</text></docTitle>",
                "  <navMap>",
                *nav_points,
                "  </navMap>",
                "</ncx>",
                "",
            ]
        ),
        encoding="utf-8",
    )


def write_epub_opf(
    epub_dir: Path,
    items: list[dict[str, str]],
    identifier: str,
    modified: str,
    title: str,
    language: str,
    author: str,
    cover_image_href: str | None = None,
    cover_page_href: str | None = None,
) -> None:
    metadata_lines = [
        f'    <dc:identifier id="book-id">{epub_escape(identifier)}</dc:identifier>',
        f"    <dc:title>{epub_escape(title)}</dc:title>",
        f"    <dc:language>{language}</dc:language>",
        f"    <dc:creator>{epub_escape(author)}</dc:creator>",
        f'    <meta property="dcterms:modified">{epub_escape(modified)}</meta>',
    ]
    if cover_image_href:
        metadata_lines.append('    <meta name="cover" content="cover-image" />')

    manifest_lines = [
        '    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav" />',
        '    <item id="toc" href="toc.ncx" media-type="application/x-dtbncx+xml" />',
        '    <item id="style" href="styles/bookish.css" media-type="text/css" />',
    ]
    spine_lines = []
    if cover_image_href:
        manifest_lines.append(
            f'    <item id="cover-image" href="{epub_escape(cover_image_href)}" media-type="image/jpeg" properties="cover-image" />'
        )
    if cover_page_href:
        manifest_lines.append(
            f'    <item id="cover-page" href="{epub_escape(cover_page_href)}" media-type="application/xhtml+xml" />'
        )
        spine_lines.append('    <itemref idref="cover-page" />')

    for index, item in enumerate(items, start=1):
        item_id = f"chapter-{index}"
        manifest_lines.append(
            f'    <item id="{item_id}" href="{epub_escape(item["href"])}" media-type="application/xhtml+xml" />'
        )
        spine_lines.append(f'    <itemref idref="{item_id}" />')

    (epub_dir / "OEBPS" / "content.opf").write_text(
        "\n".join(
            [
                '<?xml version="1.0" encoding="utf-8"?>',
                '<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="book-id">',
                "  <metadata xmlns:dc=\"http://purl.org/dc/elements/1.1/\">",
                *metadata_lines,
                "  </metadata>",
                "  <manifest>",
                *manifest_lines,
                "  </manifest>",
                '  <spine toc="toc">',
                *spine_lines,
                "  </spine>",
                "</package>",
                "",
            ]
        ),
        encoding="utf-8",
    )


def write_epub_zip(epub_dir: Path, epub_path: Path) -> None:
    with zipfile.ZipFile(epub_path, "w") as archive:
        archive.write(epub_dir / "mimetype", "mimetype", compress_type=zipfile.ZIP_STORED)
        for path in sorted(epub_dir.rglob("*")):
            if path.is_dir() or path.name == "mimetype":
                continue
            archive.write(path, path.relative_to(epub_dir).as_posix(), compress_type=zipfile.ZIP_DEFLATED)


def write_bookish_epub(
    data: dict[str, Any],
    source_files: list[str],
    *,
    base_dir: Path = BOOKISH_DIR,
    epub_dir: Path = BOOKISH_EPUB_DIR,
    epub_file: Path = BOOKISH_EPUB_FILE,
    complete_markdown: Path = BOOKISH_COMPLETE_MD,
    title: str = BOOKISH_EPUB_TITLE,
    language: str = BOOKISH_EPUB_LANGUAGE,
    author: str = BOOKISH_EPUB_AUTHOR,
    identifier_suffix: str = "bookish-complete",
    frontmatter_files: list[str] | None = None,
    cover_image: Path | None = None,
    toc_titles: dict[str, str | None] | None = None,
) -> dict[str, Any]:
    frontmatter_files = frontmatter_files or []
    toc_titles = toc_titles or {}
    all_source_files = [*frontmatter_files, *source_files]
    write_bookish_complete_markdown(base_dir, all_source_files, complete_markdown, title)

    write_epub_container(epub_dir)
    write_epub_styles(epub_dir)
    text_dir = epub_dir / "OEBPS" / "text"
    text_dir.mkdir(parents=True, exist_ok=True)
    for old_xhtml in text_dir.glob("*.xhtml"):
        old_xhtml.unlink()

    items: list[dict[str, str]] = []
    for source_file in all_source_files:
        source_path = base_dir / source_file
        if not source_path.exists():
            continue
        markdown = source_path.read_text(encoding="utf-8")
        item_title = bookish_markdown_title(markdown, source_file)
        href = bookish_xhtml_filename(source_file)
        body_class = "divider-page" if source_file.startswith("dividers/") else None
        (epub_dir / "OEBPS" / href).write_text(
            markdown_to_epub_xhtml(markdown, item_title, language, body_class),
            encoding="utf-8",
        )
        nav_title = toc_titles[source_file] if source_file in toc_titles else item_title
        item = {"source": source_file, "href": href, "title": item_title}
        if nav_title:
            item["nav_title"] = nav_title
        items.append(item)

    cover_image_href: str | None = None
    cover_page_href: str | None = None
    if cover_image and cover_image.exists():
        images_dir = epub_dir / "OEBPS" / "images"
        images_dir.mkdir(parents=True, exist_ok=True)
        cover_target = images_dir / "cover.jpg"
        shutil.copyfile(cover_image, cover_target)
        cover_image_href = "images/cover.jpg"
        cover_page_href = write_epub_cover_page(epub_dir, cover_image_href, title, language)

    identifier = f"urn:sha256:{data['meta']['sha256']}:{identifier_suffix}"
    modified = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    nav_items = [{"href": item["href"], "title": item["nav_title"]} for item in items if item.get("nav_title")]
    write_epub_nav(epub_dir, nav_items, title, language)
    write_epub_ncx(epub_dir, nav_items, identifier, title)
    write_epub_opf(epub_dir, items, identifier, modified, title, language, author, cover_image_href, cover_page_href)
    write_epub_zip(epub_dir, epub_file)

    return {
        "title": title,
        "language": language,
        "source_files": all_source_files,
        "frontmatter_files": frontmatter_files,
        "cover_image": str((epub_dir / "OEBPS" / cover_image_href).relative_to(base_dir)).replace("\\", "/")
        if cover_image_href
        else None,
        "xhtml_items": len(items),
        "complete_markdown": complete_markdown.relative_to(base_dir).as_posix()
        if complete_markdown.is_relative_to(base_dir)
        else str(complete_markdown.relative_to(ROOT)),
        "source_dir": epub_dir.relative_to(base_dir).as_posix()
        if epub_dir.is_relative_to(base_dir)
        else str(epub_dir.relative_to(ROOT)),
        "epub_file": epub_file.relative_to(base_dir).as_posix()
        if epub_file.is_relative_to(base_dir)
        else str(epub_file.relative_to(ROOT)),
    }


AUDIT_KANA_RE = re.compile(r"[ぁ-んァ-ン]")


def audit_line_kind(line: str) -> str:
    stripped = line.strip()
    if not stripped:
        return "blank"
    if stripped == "---":
        return "hr"
    if re.match(r"^#{1,6}\s+", stripped):
        return "heading"
    if stripped.startswith("> 選択：") or stripped.startswith("> 选择："):
        return "choice"
    if stripped.startswith("> "):
        return "note"
    if stripped.startswith("_") and stripped.endswith("_"):
        return "meta"
    if re.match(r"^[^:：]{1,24}[:：]\s*", stripped):
        return "speaker"
    if re.match(r"^[^「『、。，,.]{1,12}[「『]", stripped):
        return "speaker"
    return "text"


def audit_line_speaker(line: str) -> str | None:
    stripped = line.strip()
    match = re.match(r"^([^:：]{1,24})[:：]\s*", stripped)
    if match:
        return match.group(1).strip()
    match = re.match(r"^([^「『、。，,.]{1,12})[「『]", stripped)
    return match.group(1).strip() if match else None


def audit_norm(line: str) -> str:
    return re.sub(r"[\s\u3000]+", "", strip_interactive_markers(line.strip()))


def write_translation_alignment_audit(
    jp_dir: Path,
    zh_dir: Path,
    relative_files: list[str],
) -> dict[str, Any]:
    BOOKISH_ZHCN_AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    issues: list[dict[str, Any]] = []
    compared_files = 0
    compared_lines = 0

    for relative_file in relative_files:
        jp_path = jp_dir / relative_file
        zh_path = zh_dir / relative_file
        if not jp_path.exists() or not zh_path.exists():
            issues.append(
                {
                    "file": relative_file,
                    "line": None,
                    "kind": "missing_file",
                    "jp": "" if not jp_path.exists() else str(jp_path.relative_to(ROOT)),
                    "zh": "" if not zh_path.exists() else str(zh_path.relative_to(ROOT)),
                }
            )
            continue

        compared_files += 1
        jp_lines = jp_path.read_text(encoding="utf-8").splitlines()
        zh_lines = zh_path.read_text(encoding="utf-8").splitlines()
        if len(jp_lines) != len(zh_lines):
            issues.append(
                {
                    "file": relative_file,
                    "line": None,
                    "kind": "line_count_mismatch",
                    "jp_line_count": len(jp_lines),
                    "zh_line_count": len(zh_lines),
                }
            )

        for index in range(max(len(jp_lines), len(zh_lines))):
            jp_line = jp_lines[index] if index < len(jp_lines) else ""
            zh_line = zh_lines[index] if index < len(zh_lines) else ""
            line_no = index + 1
            compared_lines += 1
            jp_kind = audit_line_kind(jp_line)
            zh_kind = audit_line_kind(zh_line)
            stripped_zh = zh_line.strip()
            stripped_jp = jp_line.strip()

            if jp_kind != zh_kind and jp_kind not in {"text", "speaker"} and zh_kind not in {"text", "speaker"}:
                issues.append(
                    {
                        "file": relative_file,
                        "line": line_no,
                        "kind": "structure_mismatch",
                        "jp_kind": jp_kind,
                        "zh_kind": zh_kind,
                        "jp": stripped_jp,
                        "zh": stripped_zh,
                    }
                )

            if "**" in zh_line or INTERACTIVE_BOLD_RE.search(zh_line):
                issues.append(
                    {
                        "file": relative_file,
                        "line": line_no,
                        "kind": "bold_marker_left",
                        "jp": stripped_jp,
                        "zh": stripped_zh,
                    }
                )

            if INTERACTIVE_TERM_RE.search(jp_line) or INTERACTIVE_TERM_RE.search(zh_line):
                issues.append(
                    {
                        "file": relative_file,
                        "line": line_no,
                        "kind": "interactive_marker_left",
                        "jp": stripped_jp,
                        "zh": stripped_zh,
                    }
                )

            if stripped_zh and AUDIT_KANA_RE.search(stripped_zh):
                issues.append(
                    {
                        "file": relative_file,
                        "line": line_no,
                        "kind": "japanese_kana_in_translation",
                        "jp": stripped_jp,
                        "zh": stripped_zh,
                    }
                )

            if stripped_jp and audit_norm(stripped_jp) == audit_norm(stripped_zh) and AUDIT_KANA_RE.search(stripped_jp):
                issues.append(
                    {
                        "file": relative_file,
                        "line": line_no,
                        "kind": "unchanged_japanese_line",
                        "jp": stripped_jp,
                        "zh": stripped_zh,
                    }
                )

            jp_speaker = audit_line_speaker(jp_line)
            zh_speaker = audit_line_speaker(zh_line)
            if bool(jp_speaker) != bool(zh_speaker):
                issues.append(
                    {
                        "file": relative_file,
                        "line": line_no,
                        "kind": "speaker_shape_mismatch",
                        "jp": stripped_jp,
                        "zh": stripped_zh,
                    }
                )

            jp_len = len(audit_norm(stripped_jp))
            zh_len = len(audit_norm(stripped_zh))
            if jp_kind in {"text", "speaker"} and zh_kind in {"text", "speaker"} and jp_len >= 18 and zh_len:
                ratio = zh_len / jp_len
                if ratio < 0.18 or ratio > 3.2:
                    issues.append(
                        {
                            "file": relative_file,
                            "line": line_no,
                            "kind": "length_ratio_outlier",
                            "ratio": round(ratio, 3),
                            "jp": stripped_jp,
                            "zh": stripped_zh,
                        }
                    )

    counts = Counter(issue["kind"] for issue in issues)
    report = {
        "compared_files": compared_files,
        "compared_lines": compared_lines,
        "issue_count": len(issues),
        "issue_counts": dict(sorted(counts.items())),
        "issues": issues,
    }
    write_json(BOOKISH_ZHCN_AUDIT_DIR / "translation_alignment_audit.json", report)

    lines = [
        "# Translation Alignment Audit",
        "",
        "This is a mechanical locator for likely translation alignment problems.",
        "It does not prove every listed line is wrong; it narrows the review queue.",
        "",
        f"- Compared files: {compared_files}",
        f"- Compared lines: {compared_lines}",
        f"- Issues: {len(issues)}",
        "",
        "## Issue Counts",
        "",
        "| Kind | Count |",
        "|---|---:|",
    ]
    for kind, count in sorted(counts.items()):
        lines.append(f"| `{kind}` | {count} |")
    lines.extend(["", "## First Issues", ""])
    for issue in issues[:300]:
        location = issue["file"] if issue.get("line") is None else f"{issue['file']}:{issue['line']}"
        lines.append(f"### `{location}` `{issue['kind']}`")
        lines.append("")
        if "ratio" in issue:
            lines.append(f"- Ratio: {issue['ratio']}")
        if issue.get("jp"):
            lines.append(f"- JP: {issue['jp']}")
        if issue.get("zh"):
            lines.append(f"- ZH: {issue['zh']}")
        lines.append("")
    (BOOKISH_ZHCN_AUDIT_DIR / "translation_alignment_audit.md").write_text(
        "\n".join(lines).rstrip() + "\n",
        encoding="utf-8",
    )
    return {
        "directory": BOOKISH_ZHCN_AUDIT_DIR.relative_to(BOOKISH_ZHCN_DIR).as_posix(),
        "json": (BOOKISH_ZHCN_AUDIT_DIR / "translation_alignment_audit.json").relative_to(BOOKISH_ZHCN_DIR).as_posix(),
        "markdown": (BOOKISH_ZHCN_AUDIT_DIR / "translation_alignment_audit.md").relative_to(BOOKISH_ZHCN_DIR).as_posix(),
        "issue_count": len(issues),
        "issue_counts": dict(sorted(counts.items())),
    }


def write_bookish_outputs(data: dict[str, Any]) -> None:
    source_dir = BOOKISH_DIR / "_source"
    source_dir.mkdir(parents=True, exist_ok=True)
    entries = build_bookish_scene_entries(data)
    route_plan = build_bookish_route_plan(data)
    chapter_files = write_bookish_chapter_files(data, route_plan)
    appendix_files = write_bookish_appendix_files(data, route_plan)
    translator = BookishTranslator()
    zhcn_chapter_files = write_bookish_chapter_files(data, route_plan, BOOKISH_ZHCN_DIR, translator)
    zhcn_appendix_files = write_bookish_appendix_files(data, route_plan, BOOKISH_ZHCN_DIR, translator)
    reading_order_files = write_bookish_reading_order_files(data, route_plan)
    zhcn_reading_order_files = write_bookish_reading_order_files(data, route_plan, BOOKISH_ZHCN_DIR, translator)
    epub_source_files = bookish_epub_source_files(reading_order_files, appendix_files)
    write_zhcn_divider_files()
    write_zhcn_book_toc()
    zhcn_epub_source_files, zhcn_toc_titles = build_zhcn_epub_source_files(zhcn_reading_order_files, zhcn_appendix_files)
    audit_relative_files = unique_ordered(
        [
            *chapter_files,
            *appendix_files,
        ]
    )
    translation_audit = write_translation_alignment_audit(BOOKISH_DIR, BOOKISH_ZHCN_DIR, audit_relative_files)

    write_json(source_dir / "scenes_default.json", entries)
    write_bookish_archive_order(source_dir / "archive_order_default.md", entries)
    write_json(BOOKISH_DIR / "route_plan.json", route_plan)
    epub_outputs = write_bookish_epub(data, epub_source_files)
    zhcn_epub_outputs = write_bookish_epub(
        data,
        zhcn_epub_source_files,
        base_dir=BOOKISH_ZHCN_DIR,
        epub_dir=BOOKISH_ZHCN_EPUB_DIR,
        epub_file=BOOKISH_ZHCN_EPUB_FILE,
        complete_markdown=BOOKISH_ZHCN_COMPLETE_MD,
        title=BOOKISH_ZHCN_EPUB_TITLE,
        language=BOOKISH_ZHCN_EPUB_LANGUAGE,
        identifier_suffix="bookish-complete-zhcn",
        frontmatter_files=[BOOKISH_ZHCN_BOOK_TOC_FILE, BOOKISH_ZHCN_READER_MANUAL_FILE],
        cover_image=BOOKISH_ZHCN_COVER_IMAGE,
        toc_titles=zhcn_toc_titles,
    )
    write_bookish_readme(BOOKISH_DIR / "README.md", data, entries, route_plan, appendix_files)
    write_json(
        BOOKISH_DIR / "manifest.json",
        {
            "source": data["meta"]["source"],
            "sha256": data["meta"]["sha256"],
            "scene_count": len(entries),
            "protagonist": {
                "speaker": PROTAGONIST_FULL_NAME,
                "placeholder_value": PROTAGONIST_NAME,
            },
            "name_normalization": {
                "player_speaker_rewritten": True,
                "format_placeholder_rewritten": True,
                "adjacent_duplicate_format_variants_folded": True,
            },
            "source_files": {
                "scenes_default_json": "_source/scenes_default.json",
                "archive_order_default_md": "_source/archive_order_default.md",
                "route_plan_json": "route_plan.json",
                "appendix_internal_stories_md": "appendix/internal_stories.md",
                "appendix_endings_and_recovery_md": BOOKISH_ENDINGS_AND_RECOVERY_FILE,
                "complete_epub_markdown": BOOKISH_COMPLETE_MD.relative_to(BOOKISH_DIR).as_posix(),
                "reading_order_dir": BOOKISH_READING_ORDER_DIRNAME,
            },
            "epub": epub_outputs,
            "ladder_status": "generated_draft",
            "file_structure": "original_chapter_count",
            "chapter_files": chapter_file_specs_for_manifest(),
            "generated_chapter_files": chapter_files,
            "reading_order_files": reading_order_files,
            "appendix_files": appendix_files,
        },
    )
    BOOKISH_ZHCN_DIR.mkdir(parents=True, exist_ok=True)
    write_json(BOOKISH_ZHCN_DIR / "route_plan.json", route_plan)
    write_bookish_zhcn_readme(BOOKISH_ZHCN_DIR / "README.md", data, route_plan, translator, zhcn_appendix_files)
    write_json(
        BOOKISH_ZHCN_DIR / "manifest.json",
        {
            "source": data["meta"]["source"],
            "sha256": data["meta"]["sha256"],
            "structure_source": "bookish",
            "translation_source": {
                "authoritative_epub": str(BOOKISH_JA_ZH_EPUB_FILE.relative_to(ROOT)),
                "authoritative_epub_pairs": translator.stats["authoritative_epub_pairs"],
                "processed": str(PROCESSED_V2_DIR.relative_to(ROOT)),
                "translated": str(TRANSLATED_PROCESSED_V2_DIR.relative_to(ROOT)),
                "modified_ja_zh": str(MODIFIED_JA_ZH_DIR.relative_to(ROOT)),
                "json": "Json/v0.1.0",
                "loaded_source_files": translator.stats["source_files"],
                "loaded_line_pairs": translator.stats["paired_lines"],
                "missing_translated_files": translator.stats["missing_translated_files"],
            },
            "file_structure": "original_chapter_count",
            "chapter_files": chapter_file_specs_for_manifest(),
            "generated_chapter_files": zhcn_chapter_files,
            "reading_order_files": zhcn_reading_order_files,
            "appendix_files": zhcn_appendix_files,
            "epub": zhcn_epub_outputs,
            "audit": translation_audit,
        },
    )


def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)
    data = build_outputs()
    write_json(OUT_DIR / "arc_structure.json", {k: data[k] for k in ("meta", "sections", "scene_script_order")})
    write_json(OUT_DIR / "scene_table.json", data["scene_table"])
    write_json(OUT_DIR / "choice_edges.json", data["choice_edges"])
    write_json(OUT_DIR / "local_jumps.json", data["local_jumps"])
    write_json(OUT_DIR / "variable_semantics.json", data["variable_semantics"])
    write_json(OUT_DIR / "route_controller_calls.json", data["route_controller_calls"])
    write_json(OUT_DIR / "route_logic.json", data["route_logic"])
    write_json(OUT_DIR / "inferred_routes.json", data["inferred_routes"])
    write_json(OUT_DIR / "inferred_choice_edges.json", data["inferred_choice_edges"])
    write_json(OUT_DIR / "scene_annotations.json", data["scene_annotations"])
    write_json(OUT_DIR / "choice_crosscheck.json", data["choice_crosscheck"])
    write_json(OUT_DIR / "scene_graph.json", data["scene_graph"])
    write_json(OUT_DIR / "disasm.json", data["full_disasm"])
    write_report(OUT_DIR / "arc_inspect_report.md", data)
    write_route_paths(OUT_DIR / "route_paths.md", data["route_controller_calls"])
    write_route_logic(OUT_DIR / "route_logic.md", data["route_logic"])
    write_scene_annotations(OUT_DIR / "scene_annotations.md", data["scene_annotations"])
    write_script_annotated(OUT_DIR / "script_annotated.md", data)
    write_bookish_outputs(data)
    print(f"Parsed {data['meta']['section_count']} sections")
    print(f"Mapped {data['meta']['mapped_scene_scripts']} scene scripts")
    print(f"Choice edges: {len(data['choice_edges'])}")
    print(f"Route controller calls: {len(data['route_controller_calls'])}")
    print(f"Route condition blocks: {len(data['route_logic']['branch_blocks'])}")
    print(f"Route unresolved jumps: {len(data['route_logic']['unresolved_jumps'])}")
    print(f"Scene annotations: {len(data['scene_annotations'])}")
    print(f"Scene annotations with inferred route context: {data['meta']['scene_annotations_inferred_route']}")
    print(f"Inferred choice edges: {data['meta']['inferred_choice_edges']}")
    print(f"Bookish source written to: {BOOKISH_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
