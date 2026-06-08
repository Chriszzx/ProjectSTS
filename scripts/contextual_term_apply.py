#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply context-sensitive terminology corrections for 言葉 and 本物/偽物."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ZH_DIR = ROOT / "bookish_zhcn" / "reading_order"
DEFAULT_OUT_DIR = ROOT / "_audit" / "translation_experiment" / "corrections"
DEFAULT_ROUND_ID = "terminology_round_002_honmono_kotoba"


@dataclass(frozen=True)
class ContextRule:
    rule_id: str
    title: str
    replacements: tuple[tuple[str, str], ...]
    judgment: str

    def apply(self, text: str) -> str:
        updated = text
        for before, after in self.replacements:
            updated = updated.replace(before, after)
        return updated

    def matches(self, text: str) -> bool:
        return any(before in text for before, _ in self.replacements)


@dataclass(frozen=True)
class Change:
    rule_id: str
    title: str
    file: str
    line: int
    before: str
    after: str
    llm_judgment: str
    human_status: str = "applied-auto-contextual"

    def to_dict(self) -> dict[str, object]:
        return {
            "rule_id": self.rule_id,
            "title": self.title,
            "file": self.file,
            "line": self.line,
            "before": self.before,
            "after": self.after,
            "llm_judgment": self.llm_judgment,
            "human_status": self.human_status,
        }


@dataclass(frozen=True)
class ReviewFinding:
    rule_id: str
    title: str
    file: str
    line: int
    line_text: str
    llm_judgment: str
    human_status: str = "pending"

    def to_dict(self) -> dict[str, object]:
        return {
            "rule_id": self.rule_id,
            "title": self.title,
            "file": self.file,
            "line": self.line,
            "line_text": self.line_text,
            "llm_judgment": self.llm_judgment,
            "human_status": self.human_status,
        }


RULES: list[ContextRule] = [
    ContextRule(
        rule_id="kotoba-theme-beautiful-words",
        title="言葉主题词：美しい言葉 -> 美丽/最美的话语",
        replacements=(
            ("世界上最美妙语言", "世界上最美妙的话语"),
            ("世界上最美妙的语言", "世界上最美妙的话语"),
            ("世界最美妙的语言", "世界最美妙的话语"),
            ("世上最美妙的语言", "世上最美妙的话语"),
            ("世上最美妙的言语", "世上最美妙的话语"),
            ("这个世上最美的语言", "这个世上最美的话语"),
            ("这个世界最美的语言", "这个世界最美的话语"),
            ("世界上最美的语言", "世界上最美的话语"),
            ("世界最美的语言", "世界最美的话语"),
            ("世上最美的语言", "世上最美的话语"),
            ("这世上最美的言语", "这世上最美的话语"),
            ("最美妙言语", "最美妙的话语"),
            ("最美妙语言", "最美妙的话语"),
            ("最美妙的言语", "最美妙的话语"),
            ("最美妙的语言", "最美妙的话语"),
            ("最美的言语", "最美的话语"),
            ("最美的语言", "最美的话语"),
            ("美丽的言语", "美丽的话语"),
            ("美丽的语言", "美丽的话语"),
            ("美妙的言语", "美妙的话语"),
            ("美妙的语言", "美妙的话语"),
            ("美好的语言", "美好的话语"),
            ("美丽语言", "美丽话语"),
            ("美好语言", "美好话语"),
            ("这样的语言", "这样的话语"),
        ),
        judgment=(
            "`美しい言葉 / 世界で一番美しい言葉` 是全书主题词，"
            "这里不是实际语言系统；中文用“话语”比“语言/言语”更自然，也保留诗性。"
        ),
    ),
    ContextRule(
        rule_id="kotoba-world-coloring-scene",
        title="言葉约定场景：世界を彩る言葉",
        replacements=(
            ("远野纱夜: 「是语言」", "远野纱夜: 「是话语」"),
            ("苍: 「语言？」", "苍: 「话语？」"),
            ("想寻找给这个世界增添色彩的语言", "想寻找给这个世界增添色彩的话语"),
            ("来寻找给这个世界增添色彩的语言吧", "来寻找给这个世界增添色彩的话语吧"),
            ("描绘这景色的语言", "描绘这景色的词语"),
            ("超出我现在能想到的语言", "超出我现在能想到的词语"),
            ("那些美丽的语言", "那些美丽的话语"),
            ("没有语言的话，故事就不会诞生吧", "没有话语的话，故事就不会诞生吧"),
            ("苍: 「了解语言」", "苍: 「了解话语」"),
            ("好吧。我和你一起寻找语言", "好吧。我和你一起寻找话语"),
            ("你之前说想要寻找语言", "你之前说想要寻找话语"),
            ("难道这件事，会和了解语言有关吗", "难道这件事，会和了解话语有关吗"),
            ("关于语言的事，我不清楚", "关于话语的事，我不清楚"),
            ("说过要和你一起寻找语言", "说过要和你一起寻找话语"),
            ("了解语言。比想象中要麻烦", "了解话语。比想象中要麻烦"),
        ),
        judgment=(
            "山丘约定场景中的 `言葉` 指能描绘世界、使故事诞生的表达，"
            "不是外语或语言系统；叙述中可按语境用“话语/词语”。"
        ),
    ),
    ContextRule(
        rule_id="kotoba-flower-language",
        title="花相关言葉：花言葉/花に言葉を込める",
        replacements=(
            ("苍: 「然后，在某个时候，人们开始赋予花语言」", "苍: 「然后，在某个时候，人们开始把话语寄托在花上」"),
            ("花语言", "花语"),
        ),
        judgment=(
            "`花言葉` 固定为“花语”；`花に言葉を込める` 在中文里译为"
            "“把话语寄托在花上”更顺，也能接住下一句“花语”。"
        ),
    ),
    ContextRule(
        rule_id="kotoba-speech-register",
        title="言语书面腔：按上下文改为话语/话",
        replacements=(
            ("我忘了言语，也忘了自己原本想做什么。", "我忘了该说什么，也忘了自己原本想做什么。"),
            ("向苍道谢的不仅是言语，也是我的真心。", "向苍道谢的不只是话语，也是我的真心。"),
            ("爱的言语甜腻，", "爱的话语甜腻，"),
            ("十夜哥给了我言语。", "十夜哥给了我话语。"),
            ("他会给我想要的言语。", "他会给我想要的话语。"),
            ("哥哥总是能给我想要的言语。", "哥哥总是能给我想要的话语。"),
            ("这份情感和语言", "这份情感和话语"),
            ("言语会伤人。", "话语会伤人。"),
            ("言语会惑人。", "话语会迷惑人。"),
            ("能够表达自我的言语很方便。", "能够表达自我的话语很方便。"),
            ("漂亮的言语", "漂亮的话语"),
            ("伤害人的言语", "伤人的话语"),
            ("我和你，在寻找言语", "我和你，在寻找话语"),
            ("相信言语", "相信话语"),
            ("光是用言语安慰", "光是用话语安慰"),
            ("诅咒般的言语", "诅咒般的话语"),
            ("停留在言语上的谢礼", "停留在话语上的谢礼"),
            ("不用言语也达成共识", "不用话语也达成共识"),
        ),
        judgment=(
            "这些句子里的 `言葉` 是发话、安慰、伤人或表达；“言语”偏书面，"
            "按中文自然度改为“话语/话”。"
        ),
    ),
    ContextRule(
        rule_id="kotoba-lexical-word-context",
        title="言葉词汇语境：词语/各种话语",
        replacements=(
            ("我收集了语言。但是，找不到能够匹配这份挂心的词汇。", "我收集了词语。但是，找不到能够匹配这份挂心的词汇。"),
            ("从一开始就不存在那样的语言。", "从一开始就不存在那样的词语。"),
            ("远野纱夜教会了我语言。", "远野纱夜教会了我词语。"),
            ("教会了我认识语言。", "教会了我认识词语。"),
            ("所有遇到的人都教会了我语言", "所有遇到的人都教会了我各种话语"),
            ("那些语言，即使与我追寻的不同，也各自是美丽的话语", "那些话语，即使与我追寻的不同，也各自美丽"),
            ("收集其他许多语言就无法明白的语言", "收集其他许多话语就无法明白的话语"),
        ),
        judgment=(
            "这些句子紧邻“词汇/每学会一个词/旅途中收集”等线索，`言葉` "
            "不是语言系统；按中文语义分别用“词语”或“话语”。"
        ),
    ),
    ContextRule(
        rule_id="kotoba-depth-title",
        title="Depth副标题：深层之语",
        replacements=(
            ("Depth（深层中的言语）", "Depth（深层之语）"),
            ("Depth（深层的言叶）", "Depth（深层之语）"),
            ("Depth（深层之言）", "Depth（深层之语）"),
        ),
        judgment="系统提示中的 `Depth` 副标题需要固定，统一为较自然且不生硬的“深层之语”。",
    ),
    ContextRule(
        rule_id="honmono-attributive-hinase",
        title="本物/偽物修饰人名：正牌/冒牌",
        replacements=(
            ("真正的『日生前辈』", "正牌的『日生前辈』"),
            ("真正的『日生光』", "正牌的『日生光』"),
            ("真正的『日生光", "正牌的『日生光"),
            ("假的『日生光』", "冒牌的『日生光』"),
            ("真正的‘日生光’", "正牌的‘日生光’"),
            ("假货‘日生光’", "冒牌的‘日生光’"),
            ("冒牌货『日生光』", "冒牌的『日生光』"),
            ("冒牌货『日生光", "冒牌的『日生光"),
            ("冒牌货日生君", "冒牌日生君"),
            ("『赝品的日生光』", "『冒牌的日生光』"),
            ("『真品的日生光』", "『正牌的日生光』"),
        ),
        judgment=(
            "用户确认“正牌/冒牌”适合修饰身份/人名；这里都是日生身份轴的修饰语，"
            "替换后避免“真品/赝品/假货+人名”的物品感。"
        ),
    ),
    ContextRule(
        rule_id="honmono-nisemono-legacy-object",
        title="人物身份轴：去除真品/赝品物品感",
        replacements=(
            ("找出那个真品和冒牌货的区别", "找出正牌和冒牌货的区别"),
            ("哪个是真品哪个是赝品", "哪个是正牌哪个是冒牌"),
            ("真品也好赝品也好", "正牌也好冒牌也好"),
            ("真品和赝品的区别", "正牌和冒牌的区别"),
            ("『真品』和『赝品』", "『正牌』和『冒牌』"),
            ("真品的日生光", "正牌的日生光"),
            ("赝品的日生光", "冒牌的日生光"),
        ),
        judgment=(
            "“真品/赝品”用于人物身份不自然；日生身份轴中改成“正牌/冒牌”"
            "或保留“冒牌货”更符合中文口语。"
        ),
    ),
    ContextRule(
        rule_id="honmono-noun-register",
        title="本物/偽物名词位：本人/冒牌货",
        replacements=(
            ("作为本尊，却不肯出现在假货面前", "作为本人，却不肯出现在冒牌货面前"),
            ("那个冒牌货才是本尊", "那个冒牌货才是本人"),
            ("是『本尊』吗", "是『本人』吗"),
            ("我是『本尊』啊", "我是『本人』啊"),
            ("因为本尊和冒牌货", "因为本人和冒牌货"),
            ("本尊和冒牌货", "本人和冒牌货"),
            ("没接触过本尊的人", "没接触过本人的人"),
            ("希望我们能找到『日生光』是假货的证据", "希望我们能找到『日生光』是冒牌货的证据"),
            ("证明假货是假货的证据", "证明冒牌货就是冒牌货的证据"),
            ("真货和假货的区别", "正牌和冒牌的区别"),
            ("不会弄错真货和假货吧", "不会把正牌和冒牌弄错吧"),
            ("存在真货和假货两个日生光", "存在正牌和冒牌两个日生光"),
            ("对面那个假货深信不疑", "对面那个冒牌货深信不疑"),
            ("作为假货的你", "作为冒牌货的你"),
        ),
        judgment=(
            "独立名词位不硬套“正牌/冒牌”：严肃身份确认用“本人”，"
            "明确 impostor 用“冒牌货”；成对比较时用“正牌/冒牌”作为标签。"
        ),
    ),
    ContextRule(
        rule_id="honmono-family-context",
        title="非日生身份轴：母亲真伪",
        replacements=(
            ("真正的母亲变成了赝品，而赝品的母亲变成了真正的母亲", "真正的母亲成了假的母亲，而假的母亲成了真正的母亲"),
        ),
        judgment="亲缘/童话语境不能用鉴定物品的“赝品”；保留真/假的残酷倒置即可。",
    ),
]


REVIEW_PATTERNS: tuple[tuple[str, str, re.Pattern[str], str], ...] = (
    (
        "kotoba-remaining-review",
        "言葉剩余人工判断",
        re.compile(r"语言|言语|话语|言叶|花之语言|花语|词语"),
        "剩余项需继续区分主题话语、实际语言系统、单个词、故事台词和 UI 标题。",
    ),
    (
        "honmono-remaining-review",
        "本物/偽物剩余人工判断",
        re.compile(r"正牌|冒牌|本尊|正主|真货|假货|真品|赝品|真正的日生|真正的『日生|真正的‘日生|日生[^。！？\n]*本人|本人[^。！？\n]*日生"),
        "剩余项需看说话人语气：正牌/冒牌只作修饰或成对标签，名词位按本人、正主、真货、冒牌货等判断。",
    ),
)


def relative_path(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path)


def clean_dialogue_terminal_periods(text: str) -> str:
    return text.replace("。」", "」")


def apply_contextual_terms(
    files: Iterable[Path] | None = None,
    *,
    zh_dir: Path = DEFAULT_ZH_DIR,
    root: Path = ROOT,
) -> list[Change]:
    paths = sorted(files) if files is not None else sorted(zh_dir.glob("*.md"))
    changes: list[Change] = []
    for path in paths:
        lines = path.read_text(encoding="utf-8").splitlines()
        for index, line in enumerate(lines):
            current = line
            for rule in RULES:
                if not rule.matches(current):
                    continue
                updated = rule.apply(current)
                if updated == current:
                    continue
                changes.append(
                    Change(
                        rule_id=rule.rule_id,
                        title=rule.title,
                        file=relative_path(path, root),
                        line=index + 1,
                        before=current,
                        after=updated,
                        llm_judgment=rule.judgment,
                    )
                )
                current = updated
            lines[index] = clean_dialogue_terminal_periods(current)
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    changes.sort(key=lambda item: (item.file, item.line, item.rule_id))
    return changes


def collect_review_findings(
    files: Iterable[Path] | None = None,
    *,
    zh_dir: Path = DEFAULT_ZH_DIR,
    root: Path = ROOT,
    limit_per_rule: int = 260,
) -> list[ReviewFinding]:
    paths = sorted(files) if files is not None else sorted(zh_dir.glob("*.md"))
    findings: list[ReviewFinding] = []
    counts: dict[str, int] = {}
    for path in paths:
        for index, line in enumerate(path.read_text(encoding="utf-8").splitlines()):
            for rule_id, title, pattern, judgment in REVIEW_PATTERNS:
                if counts.get(rule_id, 0) >= limit_per_rule:
                    continue
                if not pattern.search(line):
                    continue
                findings.append(
                    ReviewFinding(
                        rule_id=rule_id,
                        title=title,
                        file=relative_path(path, root),
                        line=index + 1,
                        line_text=line,
                        llm_judgment=judgment,
                    )
                )
                counts[rule_id] = counts.get(rule_id, 0) + 1
    findings.sort(key=lambda item: (item.rule_id, item.file, item.line))
    return findings


def write_jsonl(path: Path, items: Iterable[Change | ReviewFinding]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for item in items:
            handle.write(json.dumps(item.to_dict(), ensure_ascii=False) + "\n")


def count_by_rule(items: Iterable[Change | ReviewFinding]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in items:
        counts[item.rule_id] = counts.get(item.rule_id, 0) + 1
    return dict(sorted(counts.items()))


def render_report(round_id: str, changes: list[Change], findings: list[ReviewFinding]) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    change_counts = count_by_rule(changes)
    finding_counts = count_by_rule(findings)
    lines = [
        f"# 上下文术语修正记录：{round_id}",
        "",
        f"> 生成时间：{now}",
        "> 范围：`bookish_zhcn/reading_order/*.md`",
        "> 原则：只修正 `言葉` 与 `本物/偽物` 中可由局部上下文稳定判断的 legacy 译法；剩余项进入人工审核。",
        "",
        "## 本轮状态",
        "",
        f"- 自动上下文修正：{len(changes)}",
        f"- 人工候选：{len(findings)}",
        "",
        "## 自动规则统计",
        "",
    ]
    for rule in RULES:
        lines.extend(
            [
                f"### {rule.rule_id}",
                "",
                f"- 说明：{rule.title}",
                f"- 初判：{rule.judgment}",
                f"- 本轮应用：{change_counts.get(rule.rule_id, 0)}",
                "",
            ]
        )

    lines.extend(["## 人工候选统计", ""])
    for rule_id, title, _, judgment in REVIEW_PATTERNS:
        lines.extend(
            [
                f"### {rule_id}",
                "",
                f"- 说明：{title}",
                f"- 初判：{judgment}",
                f"- 本轮候选：{finding_counts.get(rule_id, 0)}",
                "",
            ]
        )

    lines.extend(["## 自动修正明细", ""])
    if changes:
        for change in changes:
            lines.extend(
                [
                    f"- `{change.file}:{change.line}` `{change.rule_id}`",
                    f"  - before: {change.before}",
                    f"  - after: {change.after}",
                ]
            )
    else:
        lines.append("- 本轮没有自动修正。")

    lines.extend(["", "## 人工候选样例", ""])
    if findings:
        for finding in findings[:180]:
            lines.extend(
                [
                    f"- `{finding.file}:{finding.line}` `{finding.rule_id}`",
                    f"  - text: {finding.line_text}",
                ]
            )
        if len(findings) > 180:
            lines.append(f"- 其余 {len(findings) - 180} 条见 `*.review.jsonl`。")
    else:
        lines.append("- 本轮没有人工候选。")

    lines.extend(["", "## 人工审核说明", ""])
    lines.append("- `*.operations.jsonl` 记录自动上下文修正，可逐条验收或回滚。")
    lines.append("- `*.review.jsonl` 记录尚需人工或 LLM 精判的剩余候选。")
    lines.append("")
    return "\n".join(lines)


def write_outputs(
    round_id: str,
    changes: list[Change],
    findings: list[ReviewFinding],
    out_dir: Path,
) -> dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    report = out_dir / f"{round_id}.md"
    operations = out_dir / f"{round_id}.operations.jsonl"
    review = out_dir / f"{round_id}.review.jsonl"
    report.write_text(render_report(round_id, changes, findings), encoding="utf-8")
    write_jsonl(operations, changes)
    write_jsonl(review, findings)
    return {"report": report, "operations": operations, "review": review}


def command_apply(args: argparse.Namespace) -> int:
    root = Path(args.root)
    zh_dir = Path(args.zh_dir)
    files = sorted(zh_dir.glob("*.md"))
    changes = apply_contextual_terms(files, zh_dir=zh_dir, root=root)
    findings = collect_review_findings(files, zh_dir=zh_dir, root=root, limit_per_rule=args.review_limit)
    outputs = write_outputs(args.round_id, changes, findings, Path(args.out_dir))
    print(f"contextual changes: {len(changes)}")
    print(f"review findings: {len(findings)}")
    print(f"report: {outputs['report']}")
    print(f"operations: {outputs['operations']}")
    print(f"review: {outputs['review']}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=str(ROOT))
    parser.add_argument("--zh-dir", default=str(DEFAULT_ZH_DIR))
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR))
    parser.add_argument("--round-id", default=DEFAULT_ROUND_ID)
    parser.add_argument("--review-limit", type=int, default=260)
    subparsers = parser.add_subparsers(dest="command", required=True)
    apply = subparsers.add_parser("apply", help="Apply contextual corrections.")
    apply.set_defaults(func=command_apply)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
