# Route Logic

- Section: `453`
- Calls: 290
- Structured edges: 292
- Branch blocks: 27
- Unresolved jumps: 6

## Unresolved Jumps

| Label | Line | Target | Conditions |
|---|---:|---|---|
| CHAPTER_START | 89 | `ROOT_6` | 不满足：章节入口选择：序章/开端<br>不满足：章节入口选择：一章<br>不满足：章节入口选择：二章<br>不满足：章节入口选择：三章<br>不满足：章节入口选择：四章<br>不满足：章节入口选择：五章<br>章节入口选择：六章 |
| CHAPTER_START | 93 | `ROOT_KURO` | 不满足：章节入口选择：序章/开端<br>不满足：章节入口选择：一章<br>不满足：章节入口选择：二章<br>不满足：章节入口选择：三章<br>不满足：章节入口选择：四章<br>不满足：章节入口选择：五章<br>不满足：章节入口选择：六章<br>章节入口选择：黒の章 |
| CHAPTER_START | 97 | `ROOT_AO` | 不满足：章节入口选择：序章/开端<br>不满足：章节入口选择：一章<br>不满足：章节入口选择：二章<br>不满足：章节入口选择：三章<br>不满足：章节入口选择：四章<br>不满足：章节入口选择：五章<br>不满足：章节入口选择：六章<br>不满足：章节入口选择：黒の章<br>章节入口选择：蒼の章 |
| CHAPTER_START | 101 | `ROOT_EPILOGUE` | 不满足：章节入口选择：序章/开端<br>不满足：章节入口选择：一章<br>不满足：章节入口选择：二章<br>不满足：章节入口选择：三章<br>不满足：章节入口选择：四章<br>不满足：章节入口选择：五章<br>不满足：章节入口选择：六章<br>不满足：章节入口选择：黒の章<br>不满足：章节入口选择：蒼の章<br>章节入口选择：あとがき |
| ROOT_4 | 309 | `hina` | 选择「日生と付き合う」（4-16.scr / シナリオタイトル【四章-16】） |
| ROOT_5 | 432 | `ROOT_6` | - |

## Branch Blocks

| Label | Line | Condition |
|---|---:|---|
| CHAPTER_START | 58 | var_01b0 == 0 |
| CHAPTER_START | 64 | 章节入口选择：序章/开端 |
| CHAPTER_START | 68 | 章节入口选择：一章 |
| CHAPTER_START | 72 | 章节入口选择：二章 |
| CHAPTER_START | 76 | 章节入口选择：三章 |
| CHAPTER_START | 80 | 章节入口选择：四章 |
| CHAPTER_START | 84 | 章节入口选择：五章 |
| CHAPTER_START | 88 | 章节入口选择：六章 |
| CHAPTER_START | 92 | 章节入口选择：黒の章 |
| CHAPTER_START | 96 | 章节入口选择：蒼の章 |
| CHAPTER_START | 100 | 章节入口选择：あとがき |
| ROOT_OP | 109 | var_823c == 1 |
| ROOT_1 | 138 | 选择「学校に残る」（1-14.scr / シナリオタイトル【一章-14】） |
| ROOT_1 | 147 | 选择「承知しない」（1-16.scr / シナリオタイトル【一章-16-1】） |
| ROOT_1 | 170 | 不满足：选择「兄に事情を話さない」（1-34.scr / シナリオタイトル【一章-34】） |
| ROOT_1 | 176 | 选择「兄に事情を話さない」（1-34.scr / シナリオタイトル【一章-34】） |
| ROOT_1 | 188 | ((var_0340 == 11) OR (var_0340 == 44)) OR (var_0340 == 45) |
| ROOT_1 | 191 | var_0344 == 73 |
| ROOT_2 | 212 | 选择「ルイス」（2-11.scr / シナリオタイトル【二章-11】） |
| ROOT_3 | 279 | 满足内部分岐「【分岐１：追加シーン有り】」（3-42.scr / シナリオタイトル【三章-42】） |
| ROOT_4 | 308 | 选择「日生と付き合う」（4-16.scr / シナリオタイトル【四章-16】） |
| ROOT_4 | 323 | 选择「頼む」（4-27.scr / シナリオタイトル【四章-27】） |
| ROOT_4 | 342 | 选择「夏帆にお弁当作りを頼む」（3-15.scr / シナリオタイトル【三章-15】） |
| ROOT_5 | 375 | 满足内部分岐「【分岐２：桐島攻略可能】」（5-04.scr / シナリオタイトル【五章-04】） |
| ROOT_5 | 382 | 选择「外に出かけない」（5-08.scr / シナリオタイトル【五章-08】） |
| ROOT_5 | 388 | 选择「臥待堂に行く」（5-08.scr / シナリオタイトル【五章-08】） |
| nana | 479 | 满足内部分岐「【分岐２：好感度千代】」（nana5-45.scr / シナリオタイトル【桐島-37】） |

## Structured Edges

| From | To | Label | Confidence | Conditions |
|---|---|---|---|---|
| `op-00.scr` | `op-01.scr` | ROOT_OP | medium-high | - |
| `op-01.scr` | `op-02.scr` | ROOT_OP | medium-high | - |
| `op-02.scr` | `op-03.scr` | ROOT_OP | medium-high | - |
| `op-03.scr` | `op-04.scr` | ROOT_OP | medium-high | - |
| `op-04.scr` | `op-05.scr` | ROOT_OP | medium-high | - |
| `op-05.scr` | `op-06.scr` | ROOT_OP | medium-high | - |
| `op-06.scr` | `op-07.scr` | ROOT_OP | medium-high | - |
| `1-01.scr` | `1-02.scr` | ROOT_1 | medium-high | - |
| `1-02.scr` | `1-03.scr` | ROOT_1 | medium-high | - |
| `1-03.scr` | `1-04.scr` | ROOT_1 | medium-high | - |
| `1-04.scr` | `1-05.scr` | ROOT_1 | medium-high | - |
| `1-05.scr` | `1-06.scr` | ROOT_1 | medium-high | - |
| `1-06.scr` | `1-07.scr` | ROOT_1 | medium-high | - |
| `1-07.scr` | `1-08.scr` | ROOT_1 | medium-high | - |
| `1-08.scr` | `1-09.scr` | ROOT_1 | medium-high | - |
| `1-09.scr` | `1-10.scr` | ROOT_1 | medium-high | - |
| `1-10.scr` | `1-11.scr` | ROOT_1 | medium-high | - |
| `1-11.scr` | `1-12.scr` | ROOT_1 | medium-high | - |
| `1-12.scr` | `1-13.scr` | ROOT_1 | medium-high | - |
| `1-13.scr` | `1-14.scr` | ROOT_1 | medium-high | - |
| `1-14.scr` | `1-15a.scr` | ROOT_1 | medium-high | 选择「学校に残る」（1-14.scr / シナリオタイトル【一章-14】） |
| `1-14.scr` | `1-15b.scr` | ROOT_1 | medium-high | 不满足：选择「学校に残る」（1-14.scr / シナリオタイトル【一章-14】） |
| `1-15a.scr` | `1-16.scr` | ROOT_1 | medium-high | - |
| `1-15b.scr` | `1-16.scr` | ROOT_1 | medium-high | - |
| `1-16.scr` | `1-bad.scr` | ROOT_1 | medium-high | 选择「承知しない」（1-16.scr / シナリオタイトル【一章-16-1】） |
| `1-bad.scr` | `1-16b.scr` | ROOT_1 | low | - |
| `1-16.scr` | `1-16b.scr` | ROOT_1 | medium-high | - |
| `1-16b.scr` | `1-17.scr` | ROOT_1 | medium-high | - |
| `1-17.scr` | `1-18.scr` | ROOT_1 | medium-high | - |
| `1-18.scr` | `1-19.scr` | ROOT_1 | medium-high | - |
| `1-19.scr` | `1-20.scr` | ROOT_1 | medium-high | - |
| `1-20.scr` | `1-21.scr` | ROOT_1 | medium-high | - |
| `1-21.scr` | `1-22.scr` | ROOT_1 | medium-high | - |
| `1-22.scr` | `1-23.scr` | ROOT_1 | medium-high | - |
| `1-23.scr` | `1-24.scr` | ROOT_1 | medium-high | - |
| `1-24.scr` | `1-25.scr` | ROOT_1 | medium-high | - |
| `1-25.scr` | `1-26.scr` | ROOT_1 | medium-high | - |
| `1-26.scr` | `1-27.scr` | ROOT_1 | medium-high | - |
| `1-27.scr` | `1-28.scr` | ROOT_1 | medium-high | - |
| `1-28.scr` | `1-29.scr` | ROOT_1 | medium-high | - |
| `1-29.scr` | `1-30.scr` | ROOT_1 | medium-high | - |
| `1-30.scr` | `1-31.scr` | ROOT_1 | medium-high | - |
| `1-31.scr` | `1-32.scr` | ROOT_1 | medium-high | - |
| `1-32.scr` | `1-33.scr` | ROOT_1 | medium-high | - |
| `1-33.scr` | `1-34.scr` | ROOT_1 | medium-high | - |
| `1-34.scr` | `1-35.scr` | ROOT_1 | medium-high | 不满足：选择「兄に事情を話さない」（1-34.scr / シナリオタイトル【一章-34】） |
| `1-35.scr` | `1-36.scr` | ROOT_1 | medium-high | - |
| `1-34.scr` | `1-36.scr` | ROOT_1 | medium-high | - |
| `1-36.scr` | `1-bad.scr` | ROOT_1 | medium-high | 选择「兄に事情を話さない」（1-34.scr / シナリオタイトル【一章-34】） |
| `1-bad.scr` | `1-37.scr` | ROOT_1 | low | - |
| `1-36.scr` | `1-37.scr` | ROOT_1 | medium-high | - |
| `1-37.scr` | `1-38.scr` | ROOT_1 | medium-high | - |
| `1-38.scr` | `1-39.scr` | ROOT_1 | medium-high | - |
| `1-39.scr` | `1-40.scr` | ROOT_1 | medium-high | - |
| `1-40.scr` | `1-41.scr` | ROOT_1 | medium-high | - |
| `1-41.scr` | `1-42EP.scr` | ROOT_1 | medium-high | - |
| `1-42EP.scr` | `1-43EP.scr` | ROOT_1 | medium-high | ((var_0340 == 11) OR (var_0340 == 44)) OR (var_0340 == 45)<br>var_0344 == 73 |
| `2-01.scr` | `2-02.scr` | ROOT_2 | medium-high | - |
| `2-02.scr` | `2-03.scr` | ROOT_2 | medium-high | - |
| `2-03.scr` | `2-04.scr` | ROOT_2 | medium-high | - |
| `2-04.scr` | `2-04b.scr` | ROOT_2 | medium-high | - |
| `2-04b.scr` | `2-04c.scr` | ROOT_2 | medium-high | - |
| `2-04c.scr` | `2-05.scr` | ROOT_2 | medium-high | - |
| `2-05.scr` | `2-06.scr` | ROOT_2 | medium-high | - |
| `2-06.scr` | `2-07.scr` | ROOT_2 | medium-high | - |
| `2-07.scr` | `2-08.scr` | ROOT_2 | medium-high | - |
| `2-08.scr` | `2-09.scr` | ROOT_2 | medium-high | - |
| `2-09.scr` | `2-10.scr` | ROOT_2 | medium-high | - |
| `2-10.scr` | `2-11.scr` | ROOT_2 | medium-high | - |
| `2-11.scr` | `2-12.scr` | ROOT_2 | medium-high | 选择「ルイス」（2-11.scr / シナリオタイトル【二章-11】） |
| `2-11.scr` | `2-12b.scr` | ROOT_2 | medium-high | 不满足：选择「ルイス」（2-11.scr / シナリオタイトル【二章-11】） |
| `2-12b.scr` | `2-12c.scr` | ROOT_2 | medium-high | 不满足：选择「ルイス」（2-11.scr / シナリオタイトル【二章-11】） |
| `2-12.scr` | `2-13.scr` | ROOT_2 | medium-high | - |
| `2-12c.scr` | `2-13.scr` | ROOT_2 | medium-high | - |
| `2-13.scr` | `2-14.scr` | ROOT_2 | medium-high | - |
| `2-14.scr` | `2-15.scr` | ROOT_2 | medium-high | - |
| `2-15.scr` | `2-16.scr` | ROOT_2 | medium-high | - |
| `2-16.scr` | `2-17.scr` | ROOT_2 | medium-high | - |
| `2-17.scr` | `2-18.scr` | ROOT_2 | medium-high | - |
| `2-18.scr` | `2-19.scr` | ROOT_2 | medium-high | - |
| `2-19.scr` | `2-20.scr` | ROOT_2 | medium-high | - |
| `2-20.scr` | `2-21.scr` | ROOT_2 | medium-high | - |
| `2-21.scr` | `2-22.scr` | ROOT_2 | medium-high | - |
| `3-01.scr` | `3-02.scr` | ROOT_3 | medium-high | - |
| `3-02.scr` | `3-03.scr` | ROOT_3 | medium-high | - |
| `3-03.scr` | `3-04.scr` | ROOT_3 | medium-high | - |
| `3-04.scr` | `3-05.scr` | ROOT_3 | medium-high | - |
| `3-05.scr` | `3-06.scr` | ROOT_3 | medium-high | - |
| `3-06.scr` | `3-07.scr` | ROOT_3 | medium-high | - |
| `3-07.scr` | `3-08.scr` | ROOT_3 | medium-high | - |
| `3-08.scr` | `3-09.scr` | ROOT_3 | medium-high | - |
| `3-09.scr` | `3-10.scr` | ROOT_3 | medium-high | - |
| `3-10.scr` | `3-11.scr` | ROOT_3 | medium-high | - |
| `3-11.scr` | `3-12.scr` | ROOT_3 | medium-high | - |
| `3-12.scr` | `3-13.scr` | ROOT_3 | medium-high | - |
| `3-13.scr` | `3-14.scr` | ROOT_3 | medium-high | - |
| `3-14.scr` | `3-15.scr` | ROOT_3 | medium-high | - |
| `3-15.scr` | `3-16.scr` | ROOT_3 | medium-high | - |
| `3-16.scr` | `3-17.scr` | ROOT_3 | medium-high | - |
| `3-17.scr` | `3-18.scr` | ROOT_3 | medium-high | - |
| `3-18.scr` | `3-19.scr` | ROOT_3 | medium-high | - |
| `3-19.scr` | `3-20.scr` | ROOT_3 | medium-high | - |
| `3-20.scr` | `3-21.scr` | ROOT_3 | medium-high | - |
| `3-21.scr` | `3-22.scr` | ROOT_3 | medium-high | - |
| `3-22.scr` | `3-23.scr` | ROOT_3 | medium-high | - |
| `3-23.scr` | `3-24.scr` | ROOT_3 | medium-high | - |
| `3-24.scr` | `3-25.scr` | ROOT_3 | medium-high | - |
| `3-25.scr` | `3-26.scr` | ROOT_3 | medium-high | - |
| `3-26.scr` | `3-27.scr` | ROOT_3 | medium-high | - |
| `3-27.scr` | `3-28.scr` | ROOT_3 | medium-high | - |
| `3-28.scr` | `3-29.scr` | ROOT_3 | medium-high | - |
| `3-29.scr` | `3-30.scr` | ROOT_3 | medium-high | - |
| `3-30.scr` | `3-31.scr` | ROOT_3 | medium-high | - |
| `3-31.scr` | `3-32.scr` | ROOT_3 | medium-high | - |
| `3-32.scr` | `3-32b.scr` | ROOT_3 | medium-high | - |
| `3-32b.scr` | `3-33.scr` | ROOT_3 | medium-high | - |
| `3-33.scr` | `3-34.scr` | ROOT_3 | medium-high | - |
| `3-34.scr` | `3-35.scr` | ROOT_3 | medium-high | - |
| `3-35.scr` | `3-36.scr` | ROOT_3 | medium-high | - |
| `3-36.scr` | `3-37.scr` | ROOT_3 | medium-high | - |
| `3-37.scr` | `3-38a.scr` | ROOT_3 | medium-high | - |
| `3-38a.scr` | `3-38b.scr` | ROOT_3 | medium-high | - |
| `3-38b.scr` | `3-39.scr` | ROOT_3 | medium-high | - |
| `3-39.scr` | `3-40.scr` | ROOT_3 | medium-high | - |
| `3-40.scr` | `3-41.scr` | ROOT_3 | medium-high | - |
| `3-41.scr` | `3-42.scr` | ROOT_3 | medium-high | - |
| `3-42.scr` | `3-45EP.scr` | ROOT_3 | medium-high | 满足内部分岐「【分岐１：追加シーン有り】」（3-42.scr / シナリオタイトル【三章-42】） |
| `3-42.scr` | `3-44EP.scr` | ROOT_3 | medium-high | 不满足：满足内部分岐「【分岐１：追加シーン有り】」（3-42.scr / シナリオタイトル【三章-42】） |
| `4-01.scr` | `4-02.scr` | ROOT_4 | medium-high | - |
| `4-02.scr` | `4-03.scr` | ROOT_4 | medium-high | - |
| `4-03.scr` | `4-04.scr` | ROOT_4 | medium-high | - |
| `4-04.scr` | `4-05.scr` | ROOT_4 | medium-high | - |
| `4-05.scr` | `4-06.scr` | ROOT_4 | medium-high | - |
| `4-06.scr` | `4-07.scr` | ROOT_4 | medium-high | - |
| `4-07.scr` | `4-08.scr` | ROOT_4 | medium-high | - |
| `4-08.scr` | `4-09.scr` | ROOT_4 | medium-high | - |
| `4-09.scr` | `4-10.scr` | ROOT_4 | medium-high | - |
| `4-10.scr` | `4-11.scr` | ROOT_4 | medium-high | - |
| `4-11.scr` | `4-12.scr` | ROOT_4 | medium-high | - |
| `4-12.scr` | `4-13.scr` | ROOT_4 | medium-high | - |
| `4-13.scr` | `4-14.scr` | ROOT_4 | medium-high | - |
| `4-14.scr` | `4-15.scr` | ROOT_4 | medium-high | - |
| `4-15.scr` | `4-16.scr` | ROOT_4 | medium-high | - |
| `4-16.scr` | `4-17.scr` | ROOT_4 | medium-high | - |
| `4-17.scr` | `4-18.scr` | ROOT_4 | medium-high | - |
| `4-18.scr` | `4-19.scr` | ROOT_4 | medium-high | - |
| `4-19.scr` | `4-20.scr` | ROOT_4 | medium-high | - |
| `4-20.scr` | `4-21.scr` | ROOT_4 | medium-high | - |
| `4-21.scr` | `4-22.scr` | ROOT_4 | medium-high | - |
| `4-22.scr` | `4-23.scr` | ROOT_4 | medium-high | - |
| `4-23.scr` | `4-24.scr` | ROOT_4 | medium-high | - |
| `4-24.scr` | `4-25.scr` | ROOT_4 | medium-high | - |
| `4-25.scr` | `4-26.scr` | ROOT_4 | medium-high | - |
| `4-26.scr` | `4-27.scr` | ROOT_4 | medium-high | - |
| `4-27.scr` | `4-28.scr` | ROOT_4 | medium-high | 选择「頼む」（4-27.scr / シナリオタイトル【四章-27】） |
| `4-28.scr` | `4-28a.scr` | ROOT_4 | medium-high | 选择「頼む」（4-27.scr / シナリオタイトル【四章-27】） |
| `4-28a.scr` | `4-29a.scr` | ROOT_4 | medium-high | 选择「頼む」（4-27.scr / シナリオタイトル【四章-27】） |
| `4-29a.scr` | `4-30a.scr` | ROOT_4 | medium-high | 选择「頼む」（4-27.scr / シナリオタイトル【四章-27】） |
| `4-27.scr` | `4-29.scr` | ROOT_4 | medium-high | 不满足：选择「頼む」（4-27.scr / シナリオタイトル【四章-27】） |
| `4-29.scr` | `4-30.scr` | ROOT_4 | medium-high | 不满足：选择「頼む」（4-27.scr / シナリオタイトル【四章-27】） |
| `4-30a.scr` | `4-31.scr` | ROOT_4 | medium-high | - |
| `4-30.scr` | `4-31.scr` | ROOT_4 | medium-high | - |
| `4-31.scr` | `4-32.scr` | ROOT_4 | medium-high | - |
| `4-32.scr` | `4-33.scr` | ROOT_4 | medium-high | - |
| `4-33.scr` | `4-34.scr` | ROOT_4 | medium-high | - |
| `4-34.scr` | `4-35.scr` | ROOT_4 | medium-high | - |
| `4-35.scr` | `4-36.scr` | ROOT_4 | medium-high | - |
| `4-36.scr` | `4-37.scr` | ROOT_4 | medium-high | - |
| `4-37.scr` | `4-37b.scr` | ROOT_4 | medium-high | 选择「夏帆にお弁当作りを頼む」（3-15.scr / シナリオタイトル【三章-15】） |
| `4-37b.scr` | `4-38.scr` | ROOT_4 | medium-high | - |
| `4-37.scr` | `4-38.scr` | ROOT_4 | medium-high | - |
| `4-38.scr` | `4-39.scr` | ROOT_4 | medium-high | - |
| `4-39.scr` | `4-40.scr` | ROOT_4 | medium-high | - |
| `4-40.scr` | `4-40b.scr` | ROOT_4 | medium-high | - |
| `4-40b.scr` | `4-41.scr` | ROOT_4 | medium-high | - |
| `4-41.scr` | `4-42.scr` | ROOT_4 | medium-high | - |
| `4-42.scr` | `4-43.scr` | ROOT_4 | medium-high | - |
| `4-43.scr` | `4-44.scr` | ROOT_4 | medium-high | - |
| `4-44.scr` | `4-45.scr` | ROOT_4 | medium-high | - |
| `4-45.scr` | `4-45b.scr` | ROOT_4 | medium-high | - |
| `4-45b.scr` | `4-46.scr` | ROOT_4 | medium-high | - |
| `4-46.scr` | `4-47.scr` | ROOT_4 | medium-high | - |
| `4-47.scr` | `4-48.scr` | ROOT_4 | medium-high | - |
| `4-48.scr` | `4-49.scr` | ROOT_4 | medium-high | - |
| `4-49.scr` | `4-50.scr` | ROOT_4 | medium-high | - |
| `4-50.scr` | `4-51.scr` | ROOT_4 | medium-high | - |
| `4-51.scr` | `4-52.scr` | ROOT_4 | medium-high | - |
| `4-52.scr` | `4-53.scr` | ROOT_4 | medium-high | - |
| `4-53.scr` | `4-54.scr` | ROOT_4 | medium-high | - |
| `4-54.scr` | `4-55.scr` | ROOT_4 | medium-high | - |
| `4-55.scr` | `4-56ep.scr` | ROOT_4 | medium-high | - |
| `5-01.scr` | `5-02.scr` | ROOT_5 | medium-high | - |
| `5-02.scr` | `5-03.scr` | ROOT_5 | medium-high | - |
| `5-03.scr` | `5-04.scr` | ROOT_5 | medium-high | - |
| `5-04.scr` | `5-05a.scr` | ROOT_5 | medium-high | 满足内部分岐「【分岐２：桐島攻略可能】」（5-04.scr / シナリオタイトル【五章-04】） |
| `5-05a.scr` | `5-06.scr` | ROOT_5 | medium-high | - |
| `5-04.scr` | `5-06.scr` | ROOT_5 | medium-high | - |
| `5-06.scr` | `5-07.scr` | ROOT_5 | medium-high | - |
| `5-07.scr` | `5-08.scr` | ROOT_5 | medium-high | - |
| `5-08.scr` | `ani5-09.scr` | ROOT_5 | medium-high | 选择「外に出かけない」（5-08.scr / シナリオタイトル【五章-08】） |
| `ani5-09.scr` | `ani5-10.scr` | ROOT_5 | medium-high | 选择「外に出かけない」（5-08.scr / シナリオタイトル【五章-08】） |
| `ani5-10.scr` | `ani5-11.scr` | ROOT_5 | medium-high | 选择「外に出かけない」（5-08.scr / シナリオタイトル【五章-08】） |
| `5-08.scr` | `ao5-09.scr` | ROOT_5 | medium-high | 不满足：选择「外に出かけない」（5-08.scr / シナリオタイトル【五章-08】）<br>选择「臥待堂に行く」（5-08.scr / シナリオタイトル【五章-08】） |
| `ao5-09.scr` | `ao5-10.scr` | ROOT_5 | medium-high | 不满足：选择「外に出かけない」（5-08.scr / シナリオタイトル【五章-08】）<br>选择「臥待堂に行く」（5-08.scr / シナリオタイトル【五章-08】） |
| `ao5-10.scr` | `ao5-11.scr` | ROOT_5 | medium-high | 不满足：选择「外に出かけない」（5-08.scr / シナリオタイトル【五章-08】）<br>选择「臥待堂に行く」（5-08.scr / シナリオタイトル【五章-08】） |
| `ao5-11.scr` | `ao5-12.scr` | ROOT_5 | medium-high | 不满足：选择「外に出かけない」（5-08.scr / シナリオタイトル【五章-08】）<br>选择「臥待堂に行く」（5-08.scr / シナリオタイトル【五章-08】） |
| `ao5-12.scr` | `ao5-13.scr` | ROOT_5 | medium-high | 不满足：选择「外に出かけない」（5-08.scr / シナリオタイトル【五章-08】）<br>选择「臥待堂に行く」（5-08.scr / シナリオタイトル【五章-08】） |
| `ani5-11.scr` | `comm5-14.scr` | ROOT_5 | medium-high | - |
| `ao5-13.scr` | `comm5-14.scr` | ROOT_5 | medium-high | - |
| `comm5-14.scr` | `comm5-15.scr` | ROOT_5 | medium-high | - |
| `comm5-15.scr` | `comm5-16.scr` | ROOT_5 | medium-high | - |
| `comm5-16.scr` | `comm5-17.scr` | ROOT_5 | medium-high | - |
| `comm5-17.scr` | `comm5-18.scr` | ROOT_5 | medium-high | - |
| `comm5-18.scr` | `comm5-19.scr` | ROOT_5 | medium-high | - |
| `comm5-19.scr` | `comm5-20.scr` | ROOT_5 | medium-high | - |
| `comm5-20.scr` | `comm5-21.scr` | ROOT_5 | medium-high | - |
| `comm5-21.scr` | `comm5-22.scr` | ROOT_5 | medium-high | - |
| `comm5-22.scr` | `comm5-23.scr` | ROOT_5 | medium-high | - |
| `comm5-23.scr` | `comm5-24.scr` | ROOT_5 | medium-high | - |
| `comm5-24.scr` | `comm5-25.scr` | ROOT_5 | medium-high | - |
| `comm5-25.scr` | `comm5-26.scr` | ROOT_5 | medium-high | - |
| `comm5-26.scr` | `comm5-27.scr` | ROOT_5 | medium-high | - |
| `comm5-27.scr` | `comm5-28.scr` | ROOT_5 | medium-high | - |
| `comm5-28.scr` | `comm5-29.scr` | ROOT_5 | medium-high | - |
| `comm5-29.scr` | `comm5-30.scr` | ROOT_5 | medium-high | - |
| `comm5-30.scr` | `comm5-31.scr` | ROOT_5 | medium-high | - |
| `comm5-31.scr` | `comm5-32.scr` | ROOT_5 | medium-high | - |
| `comm5-32.scr` | `comm5-33.scr` | ROOT_5 | medium-high | - |
| `comm5-33.scr` | `comm5-34.scr` | ROOT_5 | medium-high | - |
| `comm5-34.scr` | `comm5-35.scr` | ROOT_5 | medium-high | - |
| `comm5-35.scr` | `comm5-36.scr` | ROOT_5 | medium-high | - |
| `comm5-36.scr` | `comm5-37.scr` | ROOT_5 | medium-high | - |
| `comm5-37.scr` | `comm5-38.scr` | ROOT_5 | medium-high | - |
| `comm5-38.scr` | `comm5-39.scr` | ROOT_5 | medium-high | - |
| `comm5-39.scr` | `comm5-40.scr` | ROOT_5 | medium-high | - |
| `comm5-40.scr` | `comm5-41.scr` | ROOT_5 | medium-high | - |
| `comm5-41.scr` | `comm5-42.scr` | ROOT_5 | medium-high | - |
| `comm5-42.scr` | `comm5-43.scr` | ROOT_5 | medium-high | - |
| `comm5-43.scr` | `comm5-44.scr` | ROOT_5 | medium-high | - |
| `comm5-44.scr` | `comm5-45ed.scr` | ROOT_5 | medium-high | - |
| `nana5-09.scr` | `nana5-10.scr` | nana | medium-high | - |
| `nana5-10.scr` | `nana5-11.scr` | nana | medium-high | - |
| `nana5-11.scr` | `nana5-12.scr` | nana | medium-high | - |
| `nana5-12.scr` | `nana5-13.scr` | nana | medium-high | - |
| `nana5-13.scr` | `nana5-14.scr` | nana | medium-high | - |
| `nana5-14.scr` | `nana5-15.scr` | nana | medium-high | - |
| `nana5-15.scr` | `nana5-16.scr` | nana | medium-high | - |
| `nana5-16.scr` | `nana5-17.scr` | nana | medium-high | - |
| `nana5-17.scr` | `nana5-18.scr` | nana | medium-high | - |
| `nana5-18.scr` | `nana5-19.scr` | nana | medium-high | - |
| `nana5-19.scr` | `nana5-20.scr` | nana | medium-high | - |
| `nana5-20.scr` | `nana5-21.scr` | nana | medium-high | - |
| `nana5-21.scr` | `nana5-22.scr` | nana | medium-high | - |
| `nana5-22.scr` | `nana5-23.scr` | nana | medium-high | - |
| `nana5-23.scr` | `nana5-24.scr` | nana | medium-high | - |
| `nana5-24.scr` | `nana5-25.scr` | nana | medium-high | - |
| `nana5-25.scr` | `nana5-26.scr` | nana | medium-high | - |
| `nana5-26.scr` | `nana5-27.scr` | nana | medium-high | - |
| `nana5-27.scr` | `nana5-28.scr` | nana | medium-high | - |
| `nana5-28.scr` | `nana5-29.scr` | nana | medium-high | - |
| `nana5-29.scr` | `nana5-30.scr` | nana | medium-high | - |
| `nana5-30.scr` | `nana5-31.scr` | nana | medium-high | - |
| `nana5-31.scr` | `nana5-32.scr` | nana | medium-high | - |
| `nana5-32.scr` | `nana5-33.scr` | nana | medium-high | - |
| `nana5-33.scr` | `nana5-34.scr` | nana | medium-high | - |
| `nana5-34.scr` | `nana5-35.scr` | nana | medium-high | - |
| `nana5-35.scr` | `nana5-36.scr` | nana | medium-high | - |
| `nana5-36.scr` | `nana5-37.scr` | nana | medium-high | - |
| `nana5-37.scr` | `nana5-38.scr` | nana | medium-high | - |
| `nana5-38.scr` | `nana5-39.scr` | nana | medium-high | - |
| `nana5-39.scr` | `nana5-40.scr` | nana | medium-high | - |
| `nana5-40.scr` | `nana5-41.scr` | nana | medium-high | - |
| `nana5-41.scr` | `nana5-42.scr` | nana | medium-high | - |
| `nana5-42.scr` | `nana5-43.scr` | nana | medium-high | - |
| `nana5-43.scr` | `nana5-44.scr` | nana | medium-high | - |
| `nana5-44.scr` | `nana5-45.scr` | nana | medium-high | - |
| `nana5-45.scr` | `nana5-46.scr` | nana | medium-high | - |
| `nana5-46.scr` | `nana5-47.scr` | nana | medium-high | - |
| `nana5-47.scr` | `nana5-48.scr` | nana | medium-high | - |
| `nana5-48.scr` | `nana5-49.scr` | nana | medium-high | - |
| `nana5-49.scr` | `nana5-50.scr` | nana | medium-high | - |
| `nana5-50.scr` | `tiyo5-51.scr` | nana | medium-high | 满足内部分岐「【分岐２：好感度千代】」（nana5-45.scr / シナリオタイトル【桐島-37】） |
| `tiyo5-51.scr` | `tiyo5-52.scr` | nana | medium-high | 满足内部分岐「【分岐２：好感度千代】」（nana5-45.scr / シナリオタイトル【桐島-37】） |
| `tiyo5-52.scr` | `tiyo5-53.scr` | nana | medium-high | 满足内部分岐「【分岐２：好感度千代】」（nana5-45.scr / シナリオタイトル【桐島-37】） |
| `tiyo5-53.scr` | `tiyo5-54.scr` | nana | medium-high | 满足内部分岐「【分岐２：好感度千代】」（nana5-45.scr / シナリオタイトル【桐島-37】） |
| `tiyo5-54.scr` | `tiyoＥＰ.scr` | nana | medium-high | 满足内部分岐「【分岐２：好感度千代】」（nana5-45.scr / シナリオタイトル【桐島-37】） |
| `nana5-50.scr` | `nana5-51.scr` | nana | medium-high | 不满足：满足内部分岐「【分岐２：好感度千代】」（nana5-45.scr / シナリオタイトル【桐島-37】） |
| `nana5-51.scr` | `nana5-52.scr` | nana | medium-high | 不满足：满足内部分岐「【分岐２：好感度千代】」（nana5-45.scr / シナリオタイトル【桐島-37】） |
| `nana5-52.scr` | `nana5-53.scr` | nana | medium-high | 不满足：满足内部分岐「【分岐２：好感度千代】」（nana5-45.scr / シナリオタイトル【桐島-37】） |
| `nana5-53.scr` | `nana5-54.scr` | nana | medium-high | 不满足：满足内部分岐「【分岐２：好感度千代】」（nana5-45.scr / シナリオタイトル【桐島-37】） |
| `nana5-54.scr` | `nana5-55.scr` | nana | medium-high | 不满足：满足内部分岐「【分岐２：好感度千代】」（nana5-45.scr / シナリオタイトル【桐島-37】） |
| `nana5-55.scr` | `nanaＥＰ.scr` | nana | medium-high | 不满足：满足内部分岐「【分岐２：好感度千代】」（nana5-45.scr / シナリオタイトル【桐島-37】） |
