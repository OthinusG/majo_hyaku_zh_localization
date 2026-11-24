# 魔女与百骑兵（PS3 BLJS-10160 1.40 合并版）全量交付说明

日期：2026-11-24  
数据来源：日版 1.00 ISO + 官方 1.10 / 1.20 / 1.30 / 1.40 补丁合并最新数据

---

## 一、交付目录总览

| 文件 / 目录 | 说明 | 数量 / 规模 |
|---|---|---|
| `魔女与百骑兵_全量中日对照文本.json` | **主翻译用全量中日对照 JSON**（UTF-8，已过滤开发内部备注与调试日志，附官方内置英文参考 `en`） | **18,005 条**（0 乱码） |
| `魔女与百骑兵_中日对照文本.json` | 与上表完全一致的同步副本（已替换旧版残缺污染文件） | **18,005 条** |
| `魔女与百骑兵_全量中日对照文本.csv` | Excel 可直接打开的 UTF-8-BOM 表格版（列含 `id / source / file / ver / type / speaker_or_field / voice / jp / zh / en_ref`） | **18,005 行** |
| `魔女与百骑兵_开发内部与调试文本_参考.json` | 开发者内部注释/测试占位/Lua 调试打印（`FlagDatabase.dat`、`DemoList.dat`、`EffectList.dat`、`Relic.dat` 占位、`FieldHouseNPC` 未使用槽、Lua `print`/调试工具等），通常无需翻译 | **6,190 条** |
| `图片/` | 全量游戏图片 PNG（已修复 DXT3/BC2 Alpha 解码并统一正立翻转），按用途分 5 类并附 `image_manifest.json` | **2,605 张**（0 失败） |
| 视频 | **经全盘核查确认：本游戏不含任何预渲染视频文件**（详见第四节） | **0 个** |

---

## 二、主翻译 JSON 结构与字段说明

```json
{
  "meta": { "... 版本、总条数、分来源统计 ..." },
  "entries": [
    {
      "id": "DemoText.dat#00267",
      "source": "DAT | EBOOT_140.elf | LUA | TROPHY.TRP | PARAM.SFO",
      "file": "DemoText.dat",
      "ver": "SDAT_130",
      "row": 267,
      "rid": 20534,
      "speaker": "アルレッキーノ",
      "voice": "sc01_arurekkino05",
      "type": "text | speaker | placeholder",
      "jp": "沼の魔女リカ様の執事にして\nお目付け役の誠実かつ\n忠実なシモベでございます。",
      "zh": "",
      "en": "I am the butler and faithful servant...",
      "loc": { "... 精确回灌坐标（勿改动）..." }
    }
  ]
}
```

### 主翻译文本分来源统计（18,005 条）
- **主线与过场剧情 `DemoText.dat`**（1.30/1.40 最新 10,642 行全量）：**10,632 条**对白 + **259 条**去重说话人名（`DemoText_Speakers`）
- **据点与城镇 NPC 对白 `FieldHouseNPC.dat`**：**1,588 条**（已剔除 534 条 `未使用`）
- **核心 UI / 系统 / 商店 / 地图事件 `GameString.dat`**：**1,119 条**
- **角色 / 敌人 / BOSS 名称 `CharacterStatus.dat`**：**516 条**
- **其余 26 张游戏 `.dat` 文本表**（`CharacterRaceText` 836、`RandomName` 568、`WitchToken` 497、`ShopSkill` 448、`ItemBase` 402、`PillarList` 330、`FieldHouse` 170、`MapInfo` 74、`ItemFlavor` 64、`ShopLvUpPrize` 41、`MapEvaluation` 33、`AreaInfo` 31、`ShopList` 31、`MapBonusList` 20、`Petition` 20、`ItemTitleB` 20、`ItemTitleA` 19、`ItemAbility` 18、`Notorious` 12、`ItemGroupName` 11、`AptitudeEquip` 6、`FieldHouseArea` 3、`FieldHouseBlock` 3、`CharacterInfo` 2、`FieldHouseWitch` 2）：**3,723 条**
- **程序硬编码 UI / 商店 / 状态 / 存档提示 `EBOOT_140.elf`**：**123 条**
- **奖杯与光盘标题 `TROPHY.TRP (TROP.SFM)` + `PARAM.SFO`**：**99 条**（48 奖杯名+说明+集合标题+光盘名）
- **Lua 实机运行时字符串**：**8 条**（1.40 已将绝大部分弹窗迁移至 `GameString.dat`；关键实机项为第 13 章结局 `episode13_demo.lua#L7945` 硬编码说话人 `"メタリカ"`）
- 其中 **14,276 条（79.3%）** 已自动关联官方内置英文（`*Eng.dat`）作 `en` 译文参考。

### 翻译注意事项
1. 字符串中的 `\n` 为字幕/提示换行符，请原样保留（`DemoText.dat` 字幕最多 3 行，切勿多加换行）。
2. 控制码与占位符（如 `%s`、`%d`、`%ld`、`%02d` 等）必须原样保留且不得改变顺序。
3. `type = "placeholder"` 为加密/乱码风演出占位符号串（如 `＆＃＄％●▼……？`），保持原样即可。
4. 说话人 `"？？？"` 为剧情伏笔，保留原样；`voice` 与 `loc` 为语音及回灌定位字段，请勿改动。
5. 常用译名参考：`メタリカ`＝梅塔莉卡（官英 Metallia）、`百騎兵`＝百骑兵、`アルレッキーノ`＝阿尔雷奇诺、`ビスコ`＝比丝可、`ヴァンダーカンマー`＝游荡商人、`カルマ`＝业值、`ファセット`＝百骑兵形态（Facet）、`トーチカ`＝战术火炬（Tochka）。

---

## 三、图片提取说明（`图片/`，共 2,605 张 PNG）

已基于 1.40/1.30/1.20 更新包优先、1.00 ISO Joliet 未截断原名兜底提取全部唯一纹理（去除 121 张完全重复纹理），并修复了旧工程将 **776 张 DXT3（BC2）纹理误用 BC3/DXT5 算法解码** 导致透明通道损坏的 Bug。所有 PSSG 纹理均已垂直翻转为正立方向（回灌时需垂直翻回自底向上再编码）。

- `图片/01_UI界面与菜单/`：**222 张**（主菜单、窗口、按钮、地图、商店、系统图标、ED 制作人员表等——需改字的美术资源主要在此目录）
- `图片/02_角色立绘/`：**357 张**（角色立绘与表情差分）
- `图片/03_字库图集/`：**3 张**（`FONTSCENARIO` 剧情字库 2048×2048 图集、`FONTTOCHKA` 数字/伤害图集）
- `图片/04_系统图标与奖杯/`：**69 张**（ISO 系统 `ICON/PIC/SYSDATA` 20 张 + `TROPHY.TRP` 奖杯图标 49 张）
- `图片/05_3D模型与场景纹理/`：**1,954 张**（角色/武器/敌人/地形/特效贴图）
- `图片/image_manifest.json`：完整清单（含每张图的源 PSSG、原纹理名、宽高、DXT/像素格式与来源版本）。

---

## 四、视频核查结论（确认无预渲染视频）

已对以下全部数据范围做完整文件名及二进制魔数扫描（`PAMF / CRID(USM) / BIK / SFD / MPEG / RIFF`）：
1. 日版 1.00 ISO 全部 **10,483** 个文件（Joliet 目录树，总计 2,974.6 MB，仅含 PSSG/HKX/DAT/PNG/CGFPO/CGVPO/ACB/AWB/SFB/SFO/TRP/BIN/SDAT/ACF/PUP）→ **0 个视频文件**。
2. 官方 1.10 / 1.20 / 1.30 / 1.40 四个 PKG 补丁包全部文件 → **0 个视频文件**。
3. 1.10 / 1.20 / 1.30 / 1.40 解密 SDAT 内全部 **12,938** 个 CPK 条目（含全部压缩与未压缩条目）→ **0 处视频魔数命中**。

结论：本作的开场、剧情过场与通关制作人员表（`ED_EASY_STAFFROLL.PSSG` 等）均由 PhyreEngine + Lua + 2D/3D PSSG + CRI AWB 音轨实时演算，**游戏本体与升级补丁中不存在任何视频文件**。
