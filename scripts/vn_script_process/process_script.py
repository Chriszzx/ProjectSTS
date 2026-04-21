#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VN Script Processor for ProjectSTS (Shinigami to Shoujo)

Processes raw split_output files from the VN engine dump into clean,
structured script files suitable for translation.

Processing pipeline (on raw lines, preserving empty lines initially):
  1. Remove title lines (シナリオタイトル)
  2. Namespace merge (character name + dialogue → single line)
     - Also joins multi-line dialogues broken by NAME placeholders
  3. Merge NAME duplicate pairs (insert canonical name 紗夜)
  4. Mark unnamed dialogue (canonical protagonist full-name speaker prefix)
  5. Mark choice branches (### prefix for alternate choices)
  6. Clean up (remove empty lines, trailing whitespace)
"""

import os
import sys
import re
import json
import argparse
from typing import List, Set, Tuple, Optional


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PROTAGONIST_NAME = "紗夜"
UNNAMED_DIALOGUE_SPEAKER = "遠野　紗夜"
CHOICE_BRANCH_MARKER = "###"
JOIN_MARK = "\ufff0"
NAME_JOIN_MARK = "\ufff1"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CHARACTER_FILE = os.path.join(SCRIPT_DIR, "special_character.txt")
DEFAULT_MAPPING_FILE = os.path.join(SCRIPT_DIR, "chapter_mapping.json")

# Particles / honorific suffixes that indicate a NAME was removed before them
NAME_INDICATORS = [
    "ちゃん", "さん", "くん", "君", "様",
    "は", "が", "を", "の", "に", "も", "と", "で", "へ",
    "って", "だ", "、",
]

HONORIFIC_INDICATORS = ["ちゃん", "さん", "くん", "君", "様"]
PUNCTUATION_CHARS = "「……、。！？　 『』（）()"
LEADING_NAME_INDICATORS = [
    "ちゃん", "さん", "くん", "君", "様",
    "は", "が", "を", "の", "に", "も", "と", "で", "へ",
    "って", "だ",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_character_names(filepath: str) -> Set[str]:
    """Load character names from the lookup table file."""
    names: Set[str] = set()
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            name = line.rstrip("\n")
            if name:
                names.add(name)
    return names


def load_chapter_mapping(filepath: str) -> dict:
    """Load chapter mapping configuration."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def read_lines(filepath: str) -> List[str]:
    """Read file and return lines with trailing newlines stripped."""
    with open(filepath, "r", encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f]


def write_lines(filepath: str, lines: List[str]) -> None:
    """Write lines to file."""
    os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")


def is_char_name(line: str, char_names: Set[str]) -> bool:
    """Check if a stripped line matches a character name."""
    return line.strip() in char_names and line.strip() != ""


def is_name_fragment(text: str) -> bool:
    """
    Check if text looks like it was broken by a NAME placeholder.

    Checks:
    1. Starts with a particle/honorific (は、が、ちゃん etc.)
    2. After stripping leading punctuation, starts with an indicator
    3. Contains a NAME indicator right after a punctuation mark (、。 etc.)
       where a name would be inserted, e.g. 「あれ、ちゃんじゃないか」
    """
    if not text:
        return False
    if NAME_JOIN_MARK in text:
        return True
    # Direct check: starts with indicator
    for indicator in NAME_INDICATORS:
        if text.startswith(indicator):
            return True
    # Check after stripping leading punctuation (……、「 etc.)
    stripped = text.lstrip("「……、。！？　 " + JOIN_MARK + NAME_JOIN_MARK)
    if stripped != text and stripped:
        for indicator in NAME_INDICATORS:
            if stripped.startswith(indicator):
                return True
    # Check for honorific suffixes after punctuation in the middle
    # e.g. 「あれ、ちゃんじゃないか」 — only check honorifics, not particles
    # (particles like は、が are too common to trigger false positives)
    honorifics = ["ちゃん", "さん", "くん", "君", "様"]
    for hon in honorifics:
        for punct in ["、", "，", "　", " "]:
            if punct + hon in text:
                return True
    return False


def _is_clear_name_junction(text: str) -> bool:
    """
    Check if a continuation line in a multi-line dialogue clearly indicates
    a NAME junction point (where the protagonist name should be inserted).

    This step is intentionally conservative. Multi-line joins should only
    insert the protagonist name for unmistakable honorific-start fragments like:
    - 「あれ、
      ちゃんじゃないか」

    Particle-start continuations such as:
    - 「今度の物語は、
      死神
      を主人公にしようと思ってるんだ」

    are ambiguous during line-join time and must be left untouched here.
    Those cases are resolved later by duplicate-pair detection instead.
    """
    if not text:
        return False

    return any(text.startswith(hon) for hon in HONORIFIC_INDICATORS)


def _find_name_insertion_index(text: str) -> Optional[int]:
    """
    Find the most likely insertion point for the protagonist name.

    The raw dump can break NAME placeholders in several ways:
    - は俺の世界で...                -> insert at start
    - ……は夜が好きかい？            -> insert after leading punctuation
    - で、に意見を聞こうと思って      -> insert before the second particle
    - 多分が思っているような         -> insert before が
    - 一番初めにに見せるよ           -> insert between the two に
    - あれ、ちゃんじゃないか         -> insert before ちゃん

    This helper scores all plausible indicator positions and picks the
    strongest one instead of blindly prepending the name.
    """
    if not text:
        return None

    mark_idx = text.find(NAME_JOIN_MARK)
    if mark_idx != -1:
        return mark_idx

    candidates = []

    for indicator in sorted(NAME_INDICATORS, key=len, reverse=True):
        start = 0
        while True:
            idx = text.find(indicator, start)
            if idx == -1:
                break

            before = text[idx - 1] if idx > 0 else ""
            after_idx = idx + len(indicator)
            after = text[after_idx] if after_idx < len(text) else ""

            score = 0

            if indicator in HONORIFIC_INDICATORS:
                if idx == 0:
                    # If the fragment itself starts with an honorific and the next
                    # char is real content, the missing name belongs at the start.
                    # Example: ちゃんじゃないか -> 紗夜ちゃんじゃないか
                    score = 115 if not (after and after in PUNCTUATION_CHARS) else 40
                elif before in PUNCTUATION_CHARS or before in "，, ":
                    score = 110
                else:
                    score = 90
            else:
                if idx == 0:
                    # Strongly prefer a true leading particle fragment like:
                    # は俺の世界で... -> 紗夜は俺の世界で...
                    # but avoid cases like で、に意見を... where the first token is
                    # just a carried-over conjunction before the actual gap.
                    score = 115 if not (after and after in PUNCTUATION_CHARS) else 40
                elif before in PUNCTUATION_CHARS or before in "，, ":
                    score = 105
                elif before in "はがをのにもとでへだ":
                    score = 102
                elif before and before not in PUNCTUATION_CHARS:
                    score = 88

                if after and after in "、。！？　 」』）)":
                    score -= 25

            if score > 0:
                candidates.append((score, idx))

            start = idx + 1

    if not candidates:
        return None

    candidates.sort(key=lambda item: (-item[0], item[1]))
    return candidates[0][1]


def _starts_with_name_indicator(text: str) -> bool:
    """Return True if a continuation line starts with a likely NAME indicator."""
    return any(text.startswith(ind) for ind in LEADING_NAME_INDICATORS)


def _next_nonempty_line(lines: List[str], start: int) -> str:
    """Return the next non-empty stripped line from start, or empty string."""
    i = start
    while i < len(lines):
        text = lines[i].strip()
        if text:
            return text
        i += 1
    return ""


def _looks_like_speaker_dialogue_start(text: str) -> bool:
    """
    Return True if a line following a speaker label looks like actual dialogue.

    This is stricter than generic NAME-fragment detection. It is used to decide
    whether a token that matches a character-name entry should interrupt an
    in-progress multi-line join. For example:
    - `男子生徒` + `「あ、遠野さん！...」` -> True (real speaker line)
    - `侍女` + `お嬢様、何をして...」` -> True (bare dialogue fragment)
    - `死神` + `を主人公にしよう...」` -> False (ordinary continuation)
    """
    if not text:
        return False
    if text.startswith("「") or text.startswith("『"):
        return True
    if _is_clear_name_junction(text):
        return True
    if text.endswith(("」", "』")):
        particle_starts = [ind for ind in LEADING_NAME_INDICATORS if ind not in HONORIFIC_INDICATORS]
        if any(text.startswith(ind) for ind in particle_starts):
            return False
        return True
    return False


def extract_char_prefix(line: str, char_names: Set[str]) -> Optional[Tuple[str, str]]:
    """
    Extract (character_name, rest) from a merged line like 角色名「台词」.
    Returns None if no character prefix found.

    Only matches when the rest starts with "「", ensuring the line is actual
    dialogue (after namespace merge) rather than choice text or narration
    that merely starts with a character name (e.g. "兄に事情を話す").
    """
    for name in sorted(char_names, key=len, reverse=True):
        if line.startswith(name) and len(line) > len(name):
            rest = line[len(name):]
            if rest.startswith("「"):
                return (name, rest)
    return None


# ---------------------------------------------------------------------------
# Step 1: Remove title lines
# ---------------------------------------------------------------------------

def step_remove_titles(lines: List[str]) -> List[str]:
    """Remove lines containing シナリオタイトル."""
    return [l for l in lines if "シナリオタイトル" not in l]


# ---------------------------------------------------------------------------
# Step 2: Namespace merge + multi-line join
# ---------------------------------------------------------------------------

def step_namespace_merge(lines: List[str], char_names: Set[str]) -> List[str]:
    """
    Merge character name lines with their following dialogue/content.

    Works on raw lines (including empty lines). Handles:
    1. CharName → (skip empty) → 「dialogue」 → merge to CharName「dialogue」
    2. CharName → (skip empty) → fragment (no 「) → merge to CharName「fragment
    3. CharName → (skip empty) → CharName → keep first standalone, process second
    4. Multi-line dialogues: if merged result doesn't end with 」,
       keep joining subsequent lines until closing 」 is found
    """
    result: List[str] = []
    i = 0

    while i < len(lines):
        line = lines[i].rstrip()

        # Skip empty lines
        if not line:
            i += 1
            continue

        # Check if current line is a character name
        if is_char_name(line, char_names):
            char_name = line.strip()

            # Find next non-empty line
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1

            if j >= len(lines):
                # No more content — standalone char name
                result.append(char_name)
                i = j
                continue

            next_line = lines[j].strip()

            # Next non-empty is also a char name
            if is_char_name(next_line, char_names):
                # First name is standalone (sprite display or NAME call)
                result.append(char_name)
                i = j  # Process the next char name in next iteration
                continue

            # Merge char name + content
            if next_line.startswith("「"):
                merged = char_name + next_line
                j += 1

                # Multi-line dialogue: if incomplete (no closing 」),
                # join subsequent lines. If continuation is a clear
                # NAME-split fragment, insert protagonist name at junction.
                if not merged.endswith("」"):
                    first_continuation = True
                    while j < len(lines):
                        cont = lines[j].strip()
                        if not cont:
                            j += 1
                            continue
                        if is_char_name(cont, char_names):
                            nxt = _next_nonempty_line(lines, j + 1)
                            if _looks_like_speaker_dialogue_start(nxt):
                                break
                        if cont.startswith("「"):
                            break
                        if cont.startswith("『"):
                            break
                        # Only insert NAME for clear name fragments:
                        # honorific suffixes or particle + closing bracket
                        # that clearly indicate a name was here
                        if first_continuation and _is_clear_name_junction(cont):
                            merged += PROTAGONIST_NAME + cont
                        elif first_continuation and _starts_with_name_indicator(cont):
                            merged += NAME_JOIN_MARK + cont
                        else:
                            merged += JOIN_MARK + cont
                        j += 1
                        first_continuation = False
                        if merged.endswith("」"):
                            break

                result.append(merged)
                i = j
            elif next_line.endswith("」") or is_name_fragment(next_line):
                # NAME-broken fragment or dialogue continuation without 「
                # DON'T insert protagonist name here — leave the raw fragment
                # so the dup detector can find exact pairs later
                merged = char_name + "「" + next_line
                j += 1

                # Continue joining if still incomplete
                if not merged.endswith("」"):
                    first_continuation = True
                    while j < len(lines):
                        cont = lines[j].strip()
                        if not cont:
                            j += 1
                            continue
                        if is_char_name(cont, char_names):
                            nxt = _next_nonempty_line(lines, j + 1)
                            if _looks_like_speaker_dialogue_start(nxt):
                                break
                        if cont.startswith("「"):
                            break
                        if cont.startswith("『"):
                            break
                        if first_continuation and _starts_with_name_indicator(cont):
                            merged += NAME_JOIN_MARK + cont
                        else:
                            merged += JOIN_MARK + cont
                        j += 1
                        first_continuation = False
                        if merged.endswith("」"):
                            break

                result.append(merged)
                i = j
            else:
                # Next line is narration — char name is standalone (sprite display)
                result.append(char_name)
                i = j  # Don't skip j, process it next
        else:
            result.append(line)
            i += 1

    return result


# ---------------------------------------------------------------------------
# Step 3: Merge NAME duplicate pairs
# ---------------------------------------------------------------------------

def step_merge_name_duplicates(lines: List[str], char_names: Set[str]) -> List[str]:
    """
    Detect and merge NAME-variant duplicate lines.

    After namespace merge, NAME variants appear as consecutive pairs:
    1. Exact dup: two identical lines with a char prefix whose dialogue
       contains a NAME gap → keep one copy, insert 紗夜
    2. Near dup: same char prefix, one has NAME gap and the other is
       the generic alternative → keep the NAME version, insert 紗夜, drop other
    """
    result: List[str] = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # --- Exact consecutive duplicate ---
        if i + 1 < len(lines) and lines[i + 1] == line:
            # Count all consecutive copies
            j = i + 1
            while j < len(lines) and lines[j] == line:
                j += 1

            # Try to insert protagonist name
            parsed = extract_char_prefix(line, char_names)
            if parsed:
                char_name, rest = parsed
                inner = rest[1:] if rest.startswith("「") else rest
                # Only insert if protagonist name isn't already in the line
                # (multi-line join may have already inserted it)
                if PROTAGONIST_NAME in inner:
                    result.append(line)
                elif is_name_fragment(inner):
                    result.append(char_name + "「" + _insert_protagonist_name(inner))
                else:
                    result.append(line)
            elif is_char_name(line, char_names):
                # Standalone char name duplicated — char calling protagonist
                result.append(line.strip() + "「" + PROTAGONIST_NAME + "」")
            else:
                result.append(line)
            i = j
            continue

        # --- Near duplicate (same char, NAME variant) ---
        # Only match when the two lines are actually variants of each other
        # (same content except for the NAME gap), NOT just any two consecutive
        # lines by the same speaker.
        if i + 1 < len(lines):
            parsed1 = extract_char_prefix(line, char_names)
            parsed2 = extract_char_prefix(lines[i + 1], char_names)
            if parsed1 and parsed2 and parsed1[0] == parsed2[0]:
                char_name = parsed1[0]
                inner1 = parsed1[1][1:] if parsed1[1].startswith("「") else parsed1[1]
                inner2 = parsed2[1][1:] if parsed2[1].startswith("「") else parsed2[1]

                frag1 = is_name_fragment(inner1)
                frag2 = is_name_fragment(inner2)

                # Both must be fragments, or one is a fragment and the other
                # is the generic version. Verify similarity: the non-NAME
                # portion should be substantially the same.
                if _are_name_variant_pair(inner1, inner2) and (
                    frag1 or frag2 or
                    (PROTAGONIST_NAME in inner1 and PROTAGONIST_NAME not in inner2) or
                    (PROTAGONIST_NAME in inner2 and PROTAGONIST_NAME not in inner1)
                ):
                    # Pick the version with the fragment, insert name
                    if frag1 and PROTAGONIST_NAME not in inner1:
                        result.append(char_name + "「" + _insert_protagonist_name(inner1))
                    elif frag2 and PROTAGONIST_NAME not in inner2:
                        result.append(char_name + "「" + _insert_protagonist_name(inner2))
                    elif PROTAGONIST_NAME in inner1 and PROTAGONIST_NAME not in inner2:
                        result.append(line)
                    elif PROTAGONIST_NAME in inner2 and PROTAGONIST_NAME not in inner1:
                        result.append(lines[i + 1])
                    else:
                        # Name already inserted by multi-line join
                        result.append(line)
                    i += 2
                    continue

        result.append(line)
        i += 1

    return result


def _are_name_variant_pair(inner1: str, inner2: str) -> bool:
    """
    Check if two dialogue inner texts are NAME variants of each other.

    True NAME variants differ only in the NAME slot. The rest of the content
    should be identical or nearly identical. For example:
    - 「は俺の世界で…」 vs 「は俺の世界で…」 (exact dup)
    - 「紗夜ちゃんじゃないか…」 vs 「こんなところで…」 (different content = NAME alt pair)
    - 「分かってるよ」 vs 「は俺の世界で…」 (completely different = NOT variants)

    Strategy: strip leading NAME indicators/punct from both, then check if
    the remaining content shares significant overlap.
    """
    # If they're identical, definitely a pair
    if inner1 == inner2:
        return True

    def strip_name_prefix(text: str) -> str:
        """Strip the NAME gap prefix to get the 'core' content."""
        s = text
        # Strip leading punct
        s = s.lstrip("「……、。！？　 ")
        # Strip leading NAME indicator
        for ind in sorted(NAME_INDICATORS, key=len, reverse=True):
            if s.startswith(ind):
                s = s[len(ind):]
                break
        return s.strip()

    core1 = strip_name_prefix(inner1)
    core2 = strip_name_prefix(inner2)

    # After stripping NAME prefix, the cores should be identical or
    # at least share the ending (the part after NAME is the same)
    if core1 == core2:
        return True

    # Check suffix overlap: if the endings match significantly, they're
    # likely NAME variants (same sentence, different NAME slot content)
    min_len = min(len(core1), len(core2))
    if min_len > 3:
        match_len = 0
        for c1, c2 in zip(reversed(core1), reversed(core2)):
            if c1 == c2:
                match_len += 1
            else:
                break
        if match_len >= min_len * 0.4:
            return True

    # Check common prefix + common suffix pattern:
    # 「あれ、ちゃんじゃないか。どうしたのかな？」 vs
    # 「あれ、こんなところで。どうしたのかな？」
    # Common prefix = 「あれ、, common suffix = どうしたのかな？」
    # The middle part differs due to NAME
    prefix_len = 0
    for c1, c2 in zip(inner1, inner2):
        if c1 == c2:
            prefix_len += 1
        else:
            break
    suffix_len = 0
    for c1, c2 in zip(reversed(inner1), reversed(inner2)):
        if c1 == c2:
            suffix_len += 1
        else:
            break
    total_common = prefix_len + suffix_len
    max_len = max(len(inner1), len(inner2))
    if max_len > 0 and total_common >= max_len * 0.5:
        return True

    return False


def _insert_protagonist_name(text: str) -> str:
    """
    Insert PROTAGONIST_NAME at the NAME gap position in a dialogue string.

    The NAME gap appears as a missing subject before a particle:
    - 「は台词」 → 「紗夜は台词」
    - 「……は台词」 → 「……紗夜は台词」
    - 「、先に帰って」 → 「紗夜、先に帰って」
    - 「ちゃんの台词」 → 「紗夜ちゃんの台词」
    """
    if not text:
        return text

    if NAME_JOIN_MARK in text:
        return text.replace(NAME_JOIN_MARK, PROTAGONIST_NAME, 1).replace(JOIN_MARK, "")

    idx = _find_name_insertion_index(text)
    if idx is None:
        return PROTAGONIST_NAME + text.replace(JOIN_MARK, "")

    return (text[:idx] + PROTAGONIST_NAME + text[idx:]).replace(JOIN_MARK, "").replace(NAME_JOIN_MARK, "")


def step_remove_empty_lines(lines: List[str]) -> List[str]:
    """Remove empty lines while preserving internal join markers."""
    return [l.rstrip() for l in lines if l.strip()]


def _merge_name_pair(
    line1: str, line2: str, char_name: str, char_names: Set[str]
) -> str:
    """
    Merge a NAME-variant pair into a single line with 紗夜 inserted.
    """
    parsed1 = extract_char_prefix(line1, char_names)
    parsed2 = extract_char_prefix(line2, char_names)

    if not parsed1 or not parsed2:
        return line1

    rest1 = parsed1[1]
    rest2 = parsed2[1]

    inner1 = rest1[1:] if rest1.startswith("「") else rest1
    inner2 = rest2[1:] if rest2.startswith("「") else rest2

    # Determine which version has the NAME gap
    if is_name_fragment(inner1):
        return char_name + "「" + _insert_protagonist_name(inner1)
    elif is_name_fragment(inner2):
        return char_name + "「" + _insert_protagonist_name(inner2)
    else:
        # Exact dup or can't determine — just return line1
        return line1


# ---------------------------------------------------------------------------
# Step 4: Handle standalone char names (NAME call → 角色名「紗夜」)
# ---------------------------------------------------------------------------

def step_resolve_standalone_names(lines: List[str], char_names: Set[str]) -> List[str]:
    """
    Resolve standalone character names that remain after namespace merge.

    A standalone char name (no dialogue attached) typically means the
    character was calling the protagonist by name (which was blank in
    the raw dump). Convert these to: 角色名「紗夜」

    Exception: if the next line is narration (no 「), the char name is
    just a sprite display marker — keep it standalone.
    """
    result: List[str] = []

    for i, line in enumerate(lines):
        if is_char_name(line, char_names):
            # Check if next non-empty line gives context
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1

            if j < len(lines):
                next_line = lines[j].strip()
                # If next line is narration (no char prefix, not dialogue)
                # then this is just a sprite display — keep standalone
                if (not next_line.startswith("「") and
                    not is_char_name(next_line, char_names) and
                    not extract_char_prefix(next_line, char_names)):
                    result.append(line)
                    continue

            # Otherwise, this char was calling the protagonist's name
            result.append(line.strip() + "「" + PROTAGONIST_NAME + "」")
        else:
            result.append(line)

    return result


# ---------------------------------------------------------------------------
# Step 5: Mark unnamed dialogue
# ---------------------------------------------------------------------------

def step_mark_unnamed_dialogue(lines: List[str], char_names: Set[str]) -> List[str]:
    """
    Mark dialogue lines that have no speaker prefix.

    Lines starting with 「 (and optionally ending with 」) that don't
    already have a character name prefix get the canonical protagonist
    full-name speaker prefix.

    Result: 遠野　紗夜「台词」
    """
    result: List[str] = []

    for line in lines:
        if line.startswith("「"):
            result.append(UNNAMED_DIALOGUE_SPEAKER + line)
        else:
            result.append(line)

    return result


# ---------------------------------------------------------------------------
# Step 6: Mark choice branches
# ---------------------------------------------------------------------------

def step_mark_choices(lines: List[str]) -> List[str]:
    """
    Mark choice branch options.

    Choice options appear as lines wrapped in 『...』.
    When multiple consecutive choice lines appear, the first is kept as-is,
    subsequent ones get the ### prefix.
    """
    result: List[str] = []
    i = 0

    while i < len(lines):
        line = lines[i]

        if line.startswith("『") and line.endswith("』"):
            choices = [line]
            j = i + 1
            while j < len(lines) and lines[j].startswith("『") and lines[j].endswith("』"):
                choices.append(lines[j])
                j += 1

            result.append(choices[0])
            for c in choices[1:]:
                result.append(CHOICE_BRANCH_MARKER + c)
            i = j
        else:
            result.append(line)
            i += 1

    return result


# ---------------------------------------------------------------------------
# Step 6b: Fix NAME-break artifacts in non-dialogue and dialogue text
# ---------------------------------------------------------------------------

# Particles that indicate a NAME was removed right before them
_NAME_PARTICLES = ("は", "が", "を", "の", "に", "も", "と", "で", "へ", "だ", "って")
_HONORIFIC_STARTS = ("ちゃん", "さん", "くん", "君", "様")

# The protagonist last name that appears at break points
_LAST_NAME = "遠野"
_FULL_NAME = "遠野" + PROTAGONIST_NAME  # 遠野紗夜


def _line_ends_with_lastname(text: str) -> bool:
    """Check if a line ends with the protagonist's last name 遠野.
    Matches both standalone 遠野 and 遠野 inside dialogue text."""
    stripped = text.rstrip()
    if not stripped.endswith(_LAST_NAME):
        return False
    # Ensure 遠野 is at the very end (not followed by other chars)
    after_idx = stripped.rfind(_LAST_NAME) + len(_LAST_NAME)
    if after_idx < len(stripped):
        return False
    return True


def _line_starts_with_name_particle(text: str) -> bool:
    """Check if a line starts with a particle or honorific that indicates
    a NAME was removed before it."""
    if not text:
        return False
    for ind in sorted(list(_NAME_PARTICLES) + list(_HONORIFIC_STARTS), key=len, reverse=True):
        if text.startswith(ind):
            return True
    return False


def _is_in_dialogue(line: str, in_dialogue_flag: bool) -> bool:
    """Track whether we're inside a 「」 dialogue block."""
    # Simple heuristic: count open/close brackets
    opens = line.count("「")
    closes = line.count("」")
    return in_dialogue_flag  # Use the tracking flag passed in


def step_fix_name_breaks(lines: List[str]) -> List[str]:
    """
    Fix text broken by NAME-placeholder removal.

    Handles four patterns:
    1. Line ending with 遠野 + next line starting with particle/honorific
       → merge, inserting 紗夜 at the junction
    2. Line ending with 遠野 + next line is a clear continuation
       → merge, inserting 紗夜
    3. Duplicate consecutive line pairs (NAME + generic variant)
       → deduplicate, inserting 紗夜
    4. Dialogue containing unclosed 遠野 inside 「」
       → merge continuation lines, inserting 紗夜
    """
    if not lines:
        return lines

    # First pass: fix duplicate pairs (Pattern B / Rule 3)
    lines = _fix_duplicate_pairs(lines)

    # Second pass: fix 遠野 breaks (Patterns A, C, D / Rules 1, 2, 4)
    lines = _fix_lastname_breaks(lines)

    return lines


def _fix_duplicate_pairs(lines: List[str]) -> List[str]:
    """Remove consecutive duplicate line pairs, keeping one with 紗夜 inserted
    at NAME gap points."""
    result: List[str] = []
    i = 0
    while i < len(lines):
        if i + 1 < len(lines) and lines[i] == lines[i + 1]:
            # Found a duplicate pair — merge by inserting 紗夜 at NAME gaps
            merged = _insert_name_in_line(lines[i])
            result.append(merged)
            i += 2
        else:
            result.append(lines[i])
            i += 1
    return result


def _insert_name_in_line(line: str) -> str:
    """Insert 紗夜 after 遠野 at NAME gap points in a line."""
    if _LAST_NAME not in line:
        return line

    # Don't insert if 紗夜 already follows 遠野
    full = _LAST_NAME + PROTAGONIST_NAME
    if full in line:
        return line

    # Find 遠野 that is NOT part of a speaker prefix (遠野　紗夜「)
    # and NOT already followed by 紗夜
    result = []
    i = 0
    while i < len(line):
        if line[i:i + len(_LAST_NAME)] == _LAST_NAME:
            # Check what follows 遠野
            after = i + len(_LAST_NAME)
            # Skip if this is a speaker prefix (遠野　紗夜)
            if after < len(line) and line[after:after + len(PROTAGONIST_NAME)] == PROTAGONIST_NAME:
                result.append(line[i:i + len(_LAST_NAME) + len(PROTAGONIST_NAME)])
                i += len(_LAST_NAME) + len(PROTAGONIST_NAME)
                continue
            # Skip if inside 『』and followed by 』 (name placeholder)
            if after < len(line) and line[after] == "』":
                result.append(_LAST_NAME + PROTAGONIST_NAME)
                i += len(_LAST_NAME)
                continue
            # Skip if followed by a space + 紗夜 (already has the name)
            if after < len(line) and line[after] in ("　", " ") and \
               after + 1 < len(line) and line[after + 1:after + 1 + len(PROTAGONIST_NAME)] == PROTAGONIST_NAME:
                result.append(line[i:i + len(_LAST_NAME) + 1 + len(PROTAGONIST_NAME)])
                i += len(_LAST_NAME) + 1 + len(PROTAGONIST_NAME)
                continue
            # Insert 紗夜 after 遠野
            result.append(_LAST_NAME + PROTAGONIST_NAME)
            i += len(_LAST_NAME)
        else:
            result.append(line[i])
            i += 1

    return "".join(result)


def _fix_lastname_breaks(lines: List[str]) -> List[str]:
    """Fix lines ending with 遠野 by joining with the next line and inserting 紗夜.
    Also fixes unclosed dialogue from NAME removal inside dialogue text."""
    result: List[str] = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Check if this line ends with 遠野 (Pattern A/C/D)
        if _line_ends_with_lastname(line) and i + 1 < len(lines):
            next_line = lines[i + 1]

            # Pattern C: next line starts with a particle or honorific
            if _line_starts_with_name_particle(next_line):
                merged = line + PROTAGONIST_NAME + next_line
                result.append(merged)
                i += 2
                continue

            # Pattern A: next line is a clear continuation
            if _is_continuation(next_line, line):
                merged = line + PROTAGONIST_NAME + next_line
                result.append(merged)
                i += 2
                continue

            # Pattern D: inside dialogue (line has 「 but no 」)
            if _has_unclosed_dialogue(line):
                merged = line + PROTAGONIST_NAME + next_line
                result.append(merged)
                i += 2
                continue

        # Pattern E: unclosed dialogue with NAME-break inside
        # e.g. 遠野　十夜「おはよう、 \n (next independent line)
        # Also: 遠野　紗夜「あ、はい。遠野 \n と申します。」
        if _has_unclosed_dialogue(line) and i + 1 < len(lines):
            next_line = lines[i + 1]
            dialogue_inner = _extract_unclosed_dialogue_inner(line)
            if dialogue_inner and (
                dialogue_inner.endswith(("、", "……", "…", "，")) or
                dialogue_inner.endswith(_LAST_NAME)
            ):
                # Priority 1: if next line is a new speaker, close this dialogue
                if _is_new_speaker_line(next_line):
                    result.append(line + PROTAGONIST_NAME + "」")
                    result.append(next_line)
                    i += 2
                    continue
                # Priority 2: next line is the NAME continuation (starts with 」 or particle)
                if next_line.startswith("」") or \
                   (next_line.endswith("」") and not _is_new_speaker_line(next_line)) or \
                   (_line_starts_with_name_particle(next_line) and not _is_new_speaker_line(next_line)):
                    merged = line + PROTAGONIST_NAME + next_line
                    result.append(merged)
                    i += 2
                    continue

        result.append(line)
        i += 1

    return result


def _extract_unclosed_dialogue_inner(line: str) -> Optional[str]:
    """Extract the inner text of an unclosed dialogue.
    Returns None if line doesn't have an unclosed dialogue."""
    if not _has_unclosed_dialogue(line):
        return None
    # Find the last 「 that doesn't have a matching 」
    last_open = line.rfind("「")
    if last_open == -1:
        return None
    return line[last_open + 1:]


def _looks_like_name_continuation(line: str) -> bool:
    """Check if a line looks like it continues after a NAME placeholder
    within dialogue."""
    if not line:
        return False
    # Starts with a particle after the name slot
    if _line_starts_with_name_particle(line):
        return True
    # Starts with closing bracket
    if line.startswith("」"):
        return True
    # Short continuation that ends with 」
    if line.endswith("」") and len(line) <= 15:
        return True
    return False


def _is_new_speaker_line(line: str) -> bool:
    """Check if a line starts a new speaker's dialogue."""
    if not line:
        return False
    # Starts with a character name pattern followed by 「
    if "「" in line:
        prefix = line[:line.index("「")]
        if len(prefix) >= 2 and not prefix.startswith("「"):
            return True
    # Starts with 「 (unnamed dialogue)
    if line.startswith("「"):
        return True
    return False


def _is_continuation(next_line: str, current_line: str) -> bool:
    """Determine if next_line is a continuation of current_line
    (i.e. not a new sentence or independent content)."""
    if not next_line:
        return False

    # Starts with a particle-like continuation
    if _line_starts_with_name_particle(next_line):
        return True

    # Starts with lowercase hiragana that connects to previous (like の, で)
    first_char = next_line[0]
    if first_char in "ののにとでへが":
        return True

    # Starts with a closing bracket continuation like 』 or ）
    if next_line.startswith(("』", "）", ")")):
        return True

    # Next line starts with a verb/particle that clearly continues
    # e.g. の場合～, です, と申します
    if next_line.startswith("の"):
        return True

    return False


def _has_unclosed_dialogue(line: str) -> bool:
    """Check if a line has an unclosed 「 (i.e. 「 count > 」 count)."""
    opens = line.count("「")
    closes = line.count("」")
    return opens > closes


# ---------------------------------------------------------------------------
# Step 7: Clean up
# ---------------------------------------------------------------------------

def step_cleanup(lines: List[str]) -> List[str]:
    """Remove empty lines and trailing whitespace."""
    return [
        l.replace(JOIN_MARK, "").replace(NAME_JOIN_MARK, "").rstrip()
        for l in lines
        if l.strip()
    ]


# ---------------------------------------------------------------------------
# Main processing pipeline
# ---------------------------------------------------------------------------

def process_file(filepath: str, char_names: Set[str]) -> List[str]:
    """Run the full processing pipeline on a single file."""
    lines = read_lines(filepath)

    # Step 1: Remove title lines
    lines = step_remove_titles(lines)

    # Step 2: Namespace merge (works on raw lines including empties)
    lines = step_namespace_merge(lines, char_names)

    # Remove empty lines before duplicate detection
    lines = step_remove_empty_lines(lines)

    # Step 3: Merge NAME duplicate pairs
    lines = step_merge_name_duplicates(lines, char_names)

    # Step 4: Resolve standalone character names
    lines = step_resolve_standalone_names(lines, char_names)

    # Step 5: Mark unnamed dialogue with protagonist full-name speaker prefix
    lines = step_mark_unnamed_dialogue(lines, char_names)

    # Step 6: Mark choice branches
    lines = step_mark_choices(lines)

    # Step 6b: Fix NAME-break artifacts
    lines = step_fix_name_breaks(lines)

    # Step 7: Final cleanup
    lines = step_cleanup(lines)

    return lines


# ---------------------------------------------------------------------------
# Output mapping
# ---------------------------------------------------------------------------

def get_output_path(
    split_number: int, mapping: dict, output_base: str
) -> Optional[str]:
    """
    Determine the output file path for a given split_output number.
    """
    for entry in mapping["mappings"]:
        start, end = entry["range"]
        if start <= split_number <= end:
            directory = entry["directory"]
            naming = entry["naming"]
            n = split_number - start + 1

            if "{n}" in naming:
                filename = naming.replace("{n}", str(n))
            else:
                filename = naming

            return os.path.join(output_base, directory, filename)

    return None


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Process VN script files for ProjectSTS translation"
    )
    parser.add_argument(
        "--input", "-i", required=True,
        help="Input: a single split_output file or the split_output directory"
    )
    parser.add_argument(
        "--output", "-o", default="stdout",
        help="Output: 'stdout', a directory path, or a file path. Default: stdout"
    )
    parser.add_argument(
        "--characters", "-c", default=DEFAULT_CHARACTER_FILE,
        help=f"Path to character names file. Default: {DEFAULT_CHARACTER_FILE}"
    )
    parser.add_argument(
        "--mapping", "-m", default=DEFAULT_MAPPING_FILE,
        help=f"Path to chapter mapping JSON. Default: {DEFAULT_MAPPING_FILE}"
    )
    parser.add_argument(
        "--range", "-r", default=None,
        help="Process only split numbers in range, e.g. '10-55' or '10'"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Show what would be done without writing files"
    )

    args = parser.parse_args()

    # Load character names
    char_names = load_character_names(args.characters)
    if not char_names:
        print("Error: No character names loaded.", file=sys.stderr)
        sys.exit(1)
    print(f"Loaded {len(char_names)} character names.", file=sys.stderr)

    # Single file mode
    if os.path.isfile(args.input):
        lines = process_file(args.input, char_names)
        if args.output == "stdout":
            for line in lines:
                print(line)
        else:
            write_lines(args.output, lines)
            print(f"Written to: {args.output}", file=sys.stderr)
        return

    # Directory mode
    if not os.path.isdir(args.input):
        print(f"Error: '{args.input}' is not a file or directory.", file=sys.stderr)
        sys.exit(1)

    mapping = load_chapter_mapping(args.mapping)

    range_start, range_end = 1, 999
    if args.range:
        parts = args.range.split("-")
        range_start = int(parts[0])
        range_end = int(parts[-1])

    files = []
    for f in os.listdir(args.input):
        if not f.endswith(".txt"):
            continue
        match = re.match(r"split_output_(\d+)\.txt$", f)
        if match:
            num = int(match.group(1))
            if range_start <= num <= range_end:
                files.append((num, os.path.join(args.input, f)))

    files.sort(key=lambda x: x[0])

    if not files:
        print("No matching split_output files found.", file=sys.stderr)
        sys.exit(1)

    print(f"Processing {len(files)} files (range {files[0][0]}-{files[-1][0]})...",
          file=sys.stderr)

    output_base = args.output if args.output != "stdout" else "."

    for num, filepath in files:
        output_path = get_output_path(num, mapping, output_base)
        if output_path is None:
            print(f"  Warning: No mapping for split_output_{num}, skipping.",
                  file=sys.stderr)
            continue

        if args.dry_run:
            print(f"  split_output_{num}.txt → {output_path}")
            continue

        lines = process_file(filepath, char_names)
        write_lines(output_path, lines)
        print(f"  split_output_{num}.txt → {output_path}", file=sys.stderr)

    print("Processing complete!", file=sys.stderr)


if __name__ == "__main__":
    main()
