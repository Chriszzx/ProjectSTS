# SCRDATA.ARC Inspection Report

## Summary

- Source: `SCRDATA.ARC`
- SHA-256: `7244f1047d4f58f6960926d0c83b3d8397edfbafe9e3984ea073f26cd86ac680`
- Size: 6819840 bytes
- SCR sections: 471
- Scenario title sections: 441
- Scene scripts mapped: 441
- Parse reasons: `{'zeros': 6, 'term': 465}`

## Scene Coverage

| Chapter | Scenes |
|---|---:|
| はじまり | 1 |
| 序章 | 7 |
| 一章 | 46 |
| 二章 | 26 |
| 三章 | 45 |
| 夏帆 | 1 |
| 四章 | 62 |
| 日生 | 41 |
| 五章 | 48 |
| 桐島 | 48 |
| 千代 | 5 |
| 六章 | 10 |
| 黒の章 | 37 |
| 蒼の章 | 63 |
| あとがき | 1 |

## Choice Coverage

- Select menus: 265
- User-visible choice menus: 156
- Internal branch marker menus: 109
- Select options total: 565
- User-visible choice options: 344
- Internal branch marker options: 221
- Scenes with choices: 146
- Local jumps: 550
- Route controller calls mapped: 290
- Route condition blocks decoded: 27
- Route unresolved jumps: 6
- Scene annotations with route context: 289
- Scene annotations with inferred route context: 152
- Scene annotations using scene order only: 0
- Variable assignment writes decoded: 47750
- Inferred route edges: 149
- Inferred choice edges: 1

## Choice Cross-Check

- ARC user-visible options: 344 total / 230 unique
- choices_map_v3_1 options: 438 total / 268 unique
- In choices_map but not ARC user choices: 45
- In ARC user choices but not choices_map: 7

## Outputs

- `arc_structure.json`: section summaries and global metadata
- `scene_table.json`: mapped scene list with labels, choices, and local jumps
- `choice_edges.json`: option text to local target label mapping
- `variable_semantics.json`: decoded variable writes linked back to choice options when possible
- `scene_graph.json`: graph edges with confidence labels
- `inferred_routes.json`: inferred route contexts for unresolved controller targets
- `inferred_choice_edges.json`: inferred cross-scene choice target fixes
- `scene_annotations.json`: per-scene annotation draft for localization context
- `scene_annotations.md`: compact per-scene annotation table
- `route_paths.md`: route-controller calls grouped by label, including decoded conditions
- `route_logic.json`: structured route-controller conditions, calls, jumps, and graph edges
- `script_annotated.md`: full script draft with scene-level route/condition headers
- `choice_crosscheck.json`: ARC choices vs choices_map_v3_1 comparison
- `disasm.json`: full record dump including unknown opcode payload hex
