#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Final extraction: scene/choice/branch structure from SCRDATA.ARC.txt.

Matches known choices from choices_map_v3_1.md against the raw script,
maps them to scenes and branch context, and cross-references with
choices.txt for consequence annotations.

Outputs:
  - final_structure.json
  - final_summary.md
"""

import json
import re
import os
import sys
from collections import defaultdict
from typing import List, Dict, Set, Tuple, Optional


# ═══════════════════════════════════════════════════════════════════════════
# File loading
# ═══════════════════════════════════════════════════════════════════════════

def load_raw_lines(path: str) -> List[dict]:
    """Parse SCRDATA.ARC.txt (UTF-16LE) into structured dicts."""
    lines = []
    with open(path, 'r', encoding='utf-16-le') as f:
        for raw in f:
            line = raw.rstrip('\n').rstrip('\r')
            if not line.strip():
                continue
            if line.startswith('\ufeff'):
                line = line[1:]
            parts = line.split(',', 2)
            if len(parts) < 3:
                continue
            lines.append({
                'addr': parts[0].strip(),
                'addr_int': int(parts[0].strip(), 16),
                'num': parts[1].strip(),
                'content': parts[2],
            })
    return lines


def load_known_choices(choices_map_path: str) -> Set[str]:
    """Extract choice texts from choices_map_v3_1.md."""
    choices = set()
    with open(choices_map_path, 'r', encoding='utf-8') as f:
        for line in f:
            m = re.match(r'^\s*\d+\.\s+(.+?)$', line.rstrip())
            if m:
                ct = m.group(1).strip().strip('『』')
                if ct and len(ct) < 50:
                    choices.add(ct)
    return choices


def load_choices_txt(path: str) -> dict:
    """
    Parse choices.txt into structured route data.
    Returns:
      {
        'routes': {'日生光': {'choices': [...], 'annotations': {...}}, ...},
        'branch_points': [{'name': '全員共通SAVE', 'choices': [...]}, ...],
      }
    """
    result = {'routes': {}, 'annotations': {}}
    current_route = None
    current_branch = None
    
    with open(path, 'r', encoding='utf-8') as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line:
                continue
            
            # Branch point marker
            if line.startswith('♪♪♪'):
                current_branch = line.strip('♪').strip()
                if current_branch not in result:
                    result[current_branch] = []
                current_route = None
                continue
            
            # Annotation line
            if line.startswith('※'):
                # ※「choice_text」→consequence
                m = re.match(r'※「(.+?)」→(.+)', line)
                if m:
                    result['annotations'][m.group(1)] = m.group(2)
                continue
            
            # Chapter/route header (no numbers, no special chars)
            if re.match(r'^[^\d※♪『]+$', line) and len(line) <= 20:
                current_route = line
                if current_route not in result['routes']:
                    result['routes'][current_route] = []
                continue
            
            # Choice line
            if current_route:
                result['routes'][current_route].append(line.strip('『』'))
            elif current_branch:
                result[current_branch].append(line.strip('『』'))
    
    return result


def load_chapter_mapping(path: str) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


# ═══════════════════════════════════════════════════════════════════════════
# Main extraction
# ═══════════════════════════════════════════════════════════════════════════

def extract(raw_path: str, choices_map_path: str, choices_txt_path: str,
            mapping_path: str) -> dict:
    
    # Load data
    raw_lines = load_raw_lines(raw_path)
    known_choices = load_known_choices(choices_map_path)
    choices_data = load_choices_txt(choices_txt_path)
    mapping = load_chapter_mapping(mapping_path)
    
    # Helper: map scene index (1-based) to file path
    def scene_to_file(idx: int) -> str:
        for m in mapping['mappings']:
            r = m['range']
            if r[0] <= idx <= r[1]:
                n = idx - r[0] + 1
                return f"{m['directory']}/{m['naming'].replace('{n}', str(n))}"
        return 'unknown'
    
    # Build content lookup: for fast choice matching
    # Also index content -> line indices
    content_to_indices = defaultdict(list)
    for i, line in enumerate(raw_lines):
        content = line['content']
        content_to_indices[content].append(i)
    
    # --- Step 1: Find scene boundaries ---
    scenes = []
    for i, line in enumerate(raw_lines):
        m = re.match(r'シナリオタイトル【(.+?)】?$', line['content'])
        if m:
            chapter_name = m.group(1).rstrip('】').strip()
            scenes.append({
                'index': len(scenes) + 1,
                'line_idx': i,
                'addr': line['addr'],
                'addr_int': line['addr_int'],
                'chapter': chapter_name,
            })
    
    # --- Step 2: Find branch markers ---
    branch_markers = []
    for i, line in enumerate(raw_lines):
        m = re.match(r'【分岐(\d+)：?(.*?)】', line['content'])
        if m:
            branch_markers.append({
                'line_idx': i,
                'addr': line['addr'],
                'addr_int': line['addr_int'],
                'num': m.group(1),
                'condition': m.group(2),
            })
    
    # --- Step 3: Find known choices in raw ---
    choice_hits = []  # (line_idx, choice_text)
    for i, line in enumerate(raw_lines):
        content = line['content']
        # Exact match
        if content in known_choices:
            choice_hits.append((i, content, 'exact'))
        elif content.startswith('『') and content.endswith('』'):
            inner = content[1:-1]
            if inner in known_choices:
                choice_hits.append((i, inner, 'wrapped'))
    
    # --- Step 4: Group consecutive choices ---
    choice_idx_set = {h[0] for h in choice_hits}
    choice_at_idx = {h[0]: h[1] for h in choice_hits}
    
    choice_groups = []
    i = 0
    while i < len(raw_lines):
        if i in choice_idx_set:
            start = i
            group_opts = []
            j = i
            while j < len(raw_lines) and j in choice_idx_set:
                group_opts.append({
                    'text': choice_at_idx[j],
                    'line_idx': j,
                    'addr': raw_lines[j]['addr'],
                    'addr_int': raw_lines[j]['addr_int'],
                })
                j += 1
            
            if len(group_opts) >= 2:
                # Find which scene this belongs to
                scene_idx = None
                for s_idx, s in enumerate(scenes):
                    if s_idx + 1 < len(scenes):
                        if s['line_idx'] <= start < scenes[s_idx + 1]['line_idx']:
                            scene_idx = s['index']
                            break
                    else:
                        if s['line_idx'] <= start:
                            scene_idx = s['index']
                
                # Find active branch markers at this point
                active_branches = []
                for bm in branch_markers:
                    if bm['line_idx'] < start:
                        # Check if there's a scene boundary between this branch and here
                        scene_reset = False
                        for s in scenes:
                            if bm['line_idx'] < s['line_idx'] <= start:
                                scene_reset = True
                                break
                        if not scene_reset:
                            active_branches.append({
                                'num': bm['num'],
                                'condition': bm['condition'],
                                'addr': bm['addr'],
                            })
                    elif bm['line_idx'] >= start:
                        break
                
                # Look up annotations
                annotations = {}
                for opt in group_opts:
                    if opt['text'] in choices_data.get('annotations', {}):
                        annotations[opt['text']] = choices_data['annotations'][opt['text']]
                
                # Get context (text before and after the choice)
                context_before = []
                for k in range(max(0, start - 5), start):
                    ctx = raw_lines[k]['content']
                    if 'シナリオタイトル' not in ctx and '【分岐' not in ctx:
                        context_before.append(ctx)
                
                # Find what follows the choice group (continuation for option 1)
                # The line after the group typically is dialogue or narration
                continuation_start = j
                continuation_lines = []
                for k in range(j, min(j + 30, len(raw_lines))):
                    ctx = raw_lines[k]['content']
                    if 'シナリオタイトル' in ctx:
                        break
                    if k in choice_idx_set:
                        break  # Hit another choice group
                    continuation_lines.append({
                        'line_idx': k,
                        'content': ctx,
                        'addr': raw_lines[k]['addr'],
                    })
                
                # Determine which route(s) this choice belongs to
                routes = []
                for route_name, route_choices in choices_data.get('routes', {}).items():
                    for opt in group_opts:
                        if opt['text'] in route_choices:
                            routes.append(route_name)
                            break
                
                choice_groups.append({
                    'id': len(choice_groups) + 1,
                    'scene': scene_idx,
                    'file': scene_to_file(scene_idx) if scene_idx else None,
                    'line_start': start,
                    'line_end': j - 1,
                    'num_options': len(group_opts),
                    'options': group_opts,
                    'active_branches': active_branches,
                    'routes': list(set(routes)),
                    'annotations': annotations,
                    'context_before': context_before[-3:],  # Last 3 lines
                    'continuation': {
                        'start_line': continuation_start,
                        'lines': continuation_lines[:10],  # First 10 lines
                    },
                })
            
            i = j
        else:
            i += 1
    
    # --- Step 5: Build scene summaries ---
    scene_summaries = []
    for s_idx, scene in enumerate(scenes):
        start = scene['line_idx']
        end = scenes[s_idx + 1]['line_idx'] if s_idx + 1 < len(scenes) else len(raw_lines)
        
        # Count elements
        branch_count = sum(1 for bm in branch_markers if start <= bm['line_idx'] < end)
        choice_count = sum(1 for cg in choice_groups if start <= cg['line_start'] < end)
        text_lines = end - start
        
        # Get branches in this scene
        scene_branches = [bm for bm in branch_markers if start <= bm['line_idx'] < end]
        
        # Get choice groups in this scene
        scene_choices = [cg for cg in choice_groups if start <= cg['line_start'] < end]
        
        scene_summaries.append({
            'index': scene['index'],
            'chapter': scene['chapter'],
            'file': scene_to_file(scene['index']),
            'addr': scene['addr'],
            'line_start': start,
            'line_end': end,
            'total_lines': text_lines,
            'branch_markers': scene_branches,
            'choice_groups': scene_choices,
        })
    
    # --- Step 6: Build statistics ---
    # Per-chapter stats
    chapter_stats = defaultdict(lambda: {'scenes': 0, 'branches': 0, 'choices': 0})
    for ss in scene_summaries:
        ch = ss['chapter']
        chapter_stats[ch]['scenes'] += 1
        chapter_stats[ch]['branches'] += len(ss['branch_markers'])
        chapter_stats[ch]['choices'] += len(ss['choice_groups'])
    
    # Unfound choices
    found_choice_texts = set()
    for cg in choice_groups:
        for opt in cg['options']:
            found_choice_texts.add(opt['text'])
    unfound = known_choices - found_choice_texts
    
    # Branch condition catalog
    branch_catalog = defaultdict(int)
    for bm in branch_markers:
        cond = f"分岐{bm['num']}" + (f":{bm['condition']}" if bm['condition'] else "")
        branch_catalog[cond] += 1
    
    return {
        'meta': {
            'source': 'SCRDATA.ARC.txt',
            'total_raw_lines': len(raw_lines),
            'total_scenes': len(scenes),
            'total_branch_markers': len(branch_markers),
            'total_choice_groups': len(choice_groups),
            'known_choices_total': len(known_choices),
            'found_choices': len(found_choice_texts),
            'unfound_choices': sorted(unfound),
        },
        'chapter_stats': dict(chapter_stats),
        'branch_catalog': dict(branch_catalog),
        'annotations': choices_data.get('annotations', {}),
        'scene_summaries': scene_summaries,
        'choice_groups': choice_groups,
        'branch_markers': branch_markers,
    }


# ═══════════════════════════════════════════════════════════════════════════
# Summary report
# ═══════════════════════════════════════════════════════════════════════════

def generate_summary(data: dict) -> str:
    lines = []
    meta = data['meta']
    
    lines.append('# SCRDATA.ARC.txt 分支结构提取报告')
    lines.append('')
    lines.append('## 总览')
    lines.append('')
    lines.append(f'| 项目 | 数值 |')
    lines.append(f'|------|------|')
    lines.append(f'| 原始行数 | {meta["total_raw_lines"]} |')
    lines.append(f'| 场景数 | {meta["total_scenes"]} |')
    lines.append(f'| 分支标记数 | {meta["total_branch_markers"]} |')
    lines.append(f'| 选项组数 | {meta["total_choice_groups"]} |')
    lines.append(f'| 已知选项数 | {meta["known_choices_total"]} |')
    lines.append(f'| 在源文件中找到 | {meta["found_choices"]} |')
    lines.append(f'| 未找到 | {len(meta["unfound_choices"])} |')
    lines.append('')
    
    if meta['unfound_choices']:
        lines.append('### 未找到的选项')
        lines.append('')
        lines.append('这些选项在 choices_map 中存在但在原始脚本中未直接找到（可能是角色名/视角选择/文字变体）：')
        lines.append('')
        for u in meta['unfound_choices']:
            lines.append(f'- `{u}`')
        lines.append('')
    
    # Chapter stats
    lines.append('## 章节统计')
    lines.append('')
    lines.append('| 章节 | 场景数 | 分支标记 | 选项组 |')
    lines.append('|------|--------|----------|--------|')
    for ch in sorted(data['chapter_stats'].keys()):
        st = data['chapter_stats'][ch]
        lines.append(f'| {ch} | {st["scenes"]} | {st["branches"]} | {st["choices"]} |')
    lines.append('')
    
    # Branch catalog
    lines.append('## 分支条件目录')
    lines.append('')
    lines.append('| 条件 | 出现次数 |')
    lines.append('|------|----------|')
    for cond, count in sorted(data['branch_catalog'].items(), key=lambda x: -x[1]):
        lines.append(f'| {cond} | {count} |')
    lines.append('')
    
    # Choice groups summary
    lines.append('## 选项组详情')
    lines.append('')
    
    for cg in data['choice_groups']:
        scene_info = f"场景{cg['scene']}" if cg['scene'] else "未知场景"
        opts = ' | '.join(o['text'] for o in cg['options'])
        branches = ', '.join(f"分岐{b['num']}:{b['condition']}" for b in cg['active_branches']) or '无'
        routes = ', '.join(cg['routes']) if cg['routes'] else '未标注'
        anno = ', '.join(f'「{k}」→{v}' for k, v in cg['annotations'].items()) if cg['annotations'] else '无'
        
        lines.append(f'### #{cg["id"]} {scene_info} [{branches}]')
        lines.append(f'- **选项**: {opts}')
        lines.append(f'- **路线**: {routes}')
        lines.append(f'- **后果标注**: {anno}')
        
        # Context
        if cg['context_before']:
            lines.append(f'- **前文**:')
            for ctx in cg['context_before']:
                lines.append(f'  > {ctx[:80]}')
        
        # Continuation start
        cont = cg['continuation']
        if cont['lines']:
            lines.append(f'- **后续文本** (从行{cont["start_line"]}开始):')
            for cl in cont['lines'][:5]:
                prefix = '  - ' if '「' in cl['content'] else '  - '
                lines.append(f'{prefix}{cl["content"][:100]}')
        
        lines.append('')
    
    # Scene summary
    lines.append('## 场景分支索引')
    lines.append('')
    lines.append('| 场景 | 章节 | 分支条件 | 选项组 |')
    lines.append('|------|------|----------|--------|')
    for ss in data['scene_summaries']:
        branches = ', '.join(f"分岐{b['num']}:{b['condition']}" for b in ss['branch_markers']) or '-'
        choices = str(len(ss['choice_groups'])) if ss['choice_groups'] else '-'
        if ss['branch_markers'] or ss['choice_groups']:
            lines.append(f'| {ss["index"]} | {ss["chapter"]} | {branches} | {choices} |')
    lines.append('')
    
    return '\n'.join(lines)


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    raw_path = os.path.join(project_root, 'SCRDATA.ARC.txt')
    choices_map_path = os.path.join(project_root, 'choices_map_v3_1.md')
    choices_txt_path = os.path.join(project_root, 'choices.txt')
    mapping_path = os.path.join(project_root, 'scripts', 'vn_script_process', 'chapter_mapping.json')
    
    for p in [raw_path, choices_map_path, choices_txt_path]:
        if not os.path.exists(p):
            print(f"ERR: {p} not found")
            sys.exit(1)
    
    print("Extracting...")
    data = extract(raw_path, choices_map_path, choices_txt_path, mapping_path)
    
    # Save JSON
    out_json = os.path.join(script_dir, 'final_structure.json')
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  -> {out_json}")
    
    # Save summary
    out_md = os.path.join(script_dir, 'final_summary.md')
    summary = generate_summary(data)
    with open(out_md, 'w', encoding='utf-8') as f:
        f.write(summary)
    print(f"  -> {out_md}")
    
    # Quick summary
    m = data['meta']
    print(f"\nDone. {m['total_scenes']} scenes, {m['total_branch_markers']} branches, "
          f"{m['total_choice_groups']} choice groups.")
    print(f"Found {m['found_choices']}/{m['known_choices_total']} known choices in raw script.")
    if m['unfound_choices']:
        print(f"Unfound ({len(m['unfound_choices'])}): {', '.join(m['unfound_choices'])}")
    
    # Stats
    scenes_with_branches = sum(1 for ss in data['scene_summaries'] if ss['branch_markers'])
    scenes_with_choices = sum(1 for ss in data['scene_summaries'] if ss['choice_groups'])
    print(f"Scenes with branches: {scenes_with_branches}")
    print(f"Scenes with choices: {scenes_with_choices}")


if __name__ == '__main__':
    main()
