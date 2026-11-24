# 《魔女与百骑兵》简体中文汉化工程

基于 PS3 日版 `BLJS-10160` 1.00 光盘与官方 1.10–1.40 更新合并数据。文本已归档，可开始翻译。初始工作稿的 `zh` 全部留空。

## 目录与入口

| 路径 | 用途 |
|---|---|
| [`data/source/`](data/source/) | 日文基准 JSON，含日文 `jp`、可用的官方英文 `en` 和回灌坐标 `loc` |
| [`data/translation/`](data/translation/) | 中文工作稿，只填写 `entries[].zh` |
| [`data/reference/`](data/reference/) | 开发内部和调试文本，供上下文核对 |
| [`tables/`](tables/) | 初始 UTF-8 BOM 对照 CSV，以及后续校对用 CSV/TSV |
| [`analysis/`](analysis/) | [术语表](analysis/glossary.md)和后续校对分析 |
| [`scripts/`](scripts/) | Python 3 标准库结构校验 |
| [`docs/`](docs/) | [原始交付说明](docs/翻译说明_README.md)，保留提取过程与资产记录 |
| `tmp/` | 本地临时文件 |

## 已核实的文本范围

| 来源 | 条目 |
|---|---:|
| `DemoText.dat` 剧情文本（含 16 条演出占位） | 10,632 |
| `DemoText.dat` 去重说话人名 | 259 |
| `FieldHouseNPC.dat` 据点及城镇 NPC | 1,588 |
| `GameString.dat` UI 与系统 | 1,119 |
| `CharacterStatus.dat` 角色及敌人名称 | 516 |
| 其余 25 张 DAT 文本表 | 3,661 |
| `EBOOT_140.elf` 硬编码文本 | 123 |
| `TROP.SFM` 奖杯与 `PARAM.SFO` 光盘标题 | 99 |
| Lua 运行时字符串 | 8 |
| **合计** | **18,005** |

主语料有 14,276 条附带官方英文参考。另有 6,190 条内部与调试参考。原说明对其余 DAT 表的统计以本页实测值为准。

## 翻译与验收

1. 在[工程计划](localization_project_plan.md)选定批次，使用序号区间和首末 ID 定位。按[术语表](analysis/glossary.md)统一用词，以日文和上下文为准，参考 `en`。
2. 仅编辑工作稿的 `zh`。保留源文换行、制表符和格式占位符的数量及顺序。剧情字幕最多 3 行，`placeholder` 条目将 `jp` 原样写入 `zh`。`？？？` 说话人标记、语音、引擎坐标及其他元数据保持原样。
3. 在根目录运行 `python3 scripts/verify_alignment.py`。校对并通过结构校验后，勾选批次并更新[修改索引](localization_modification_index.md)。所有 `zh` 填写完毕后，再运行 `python3 scripts/verify_alignment.py --require-complete`。

CSV 为初始快照，便于在表格工具中查阅。`speaker_or_field` 依次取 JSON 的 `speaker`、`field` 或 `context`，`en_ref` 对应 `en`。翻译和校验以工作 JSON 为准。

## 资产与回灌

原交付说明报告了 2,605 张 PNG、`image_manifest.json` 和无预渲染视频的扫描结果。本地仅收到文本与交付说明。图片、字库、游戏文件、回灌工具和实机验收目前待补，资产详情见[原始交付说明](docs/翻译说明_README.md)。

工程流程参考 [Grisaia 汉化仓库](https://github.com/OthinusG/grisaia_zh_localization/tree/9c9cd3578a62af60b6fdff12f6f138d07d386abc)。
