# 《魔女与百骑兵》汉化工程计划

目标是完成 PS3 日版 BLJS-10160 1.40 合并版的 18,005 条玩家可见文本汉化，并保留回灌所需的条目结构。6,190 条开发内部与调试文本留作参考。

## 约束与验收

- 每批最多 1,000 条。保留 ID、顺序、字段与源文。批次范围使用主 JSON 的 1-based 条目序号（两端含），以首末 ID 交叉定位。
- 采用原表顺序切分剧情。已知的语音前缀仅供定位，存在无语音条目，不能用来直接判断章节边界。
- 验收时核对原意、角色语气、术语与界面上下文。结构校验通过后更新修改索引和本计划。最终文本验收要求所有条目 `zh` 填写完毕。
- 回灌风险包括原位字符串空间、字库缺字和 UI 溢出。资产与工具齐备后按 M6 确认实机结果。

## M0 — 工程基建

- [x] 归档并验证原始数据，建立工作稿、术语表、修改索引、批次清单及结构校验。原始数据哈希保持一致，49 个批次完整覆盖 18,005 条。

## M1 — 角色名与系统 UI

- [x] **M1-01** CharacterStatus.dat，序号 876–1391（516 条），`CharacterStatus.dat#00000.c1` → `CharacterStatus.dat#00515.c1`
- [x] **M1-02** DemoText.dat（说话人），序号 1392–1650（259 条），`DemoText_Speakers#0001` → `DemoText_Speakers#0259`
- [x] **M1-03** GameString.dat，序号 14049–15048（1000 条），`GameString.dat#00000.c1` → `GameString.dat#01621.c1`
- [x] **M1-04** GameString.dat，序号 15049–15167（119 条），`GameString.dat#01623.c1` → `GameString.dat#01786.c1`

## M2 — 主线与过场对白

- [x] **M2-01** DemoText.dat，序号 1651–2650（1000 条），`DemoText.dat#00000` → `DemoText.dat#00999`
- [x] **M2-02** DemoText.dat，序号 2651–3650（1000 条），`DemoText.dat#01000` → `DemoText.dat#01999`
- [x] **M2-03** DemoText.dat，序号 3651–4650（1000 条），`DemoText.dat#02000` → `DemoText.dat#02999`
- [x] **M2-04** DemoText.dat，序号 4651–5650（1000 条），`DemoText.dat#03000` → `DemoText.dat#03999`
- [x] **M2-05** DemoText.dat，序号 5651–6650（1000 条），`DemoText.dat#04000` → `DemoText.dat#04999`
- [x] **M2-06** DemoText.dat，序号 6651–7650（1000 条），`DemoText.dat#05000` → `DemoText.dat#05999`
- [x] **M2-07** DemoText.dat，序号 7651–8650（1000 条），`DemoText.dat#06000` → `DemoText.dat#06999`
- [x] **M2-08** DemoText.dat，序号 8651–9650（1000 条），`DemoText.dat#07000` → `DemoText.dat#07999`
- [x] **M2-09** DemoText.dat，序号 9651–10650（1000 条），`DemoText.dat#08000` → `DemoText.dat#08999`
- [x] **M2-10** DemoText.dat，序号 10651–11650（1000 条），`DemoText.dat#09000` → `DemoText.dat#09999`
- [x] **M2-11** DemoText.dat，序号 11651–12282（632 条），`DemoText.dat#10000` → `DemoText.dat#10641`

## M3 — 据点 NPC 与其他 DAT 文本

- [x] **M3-01** AptitudeEquip.dat，序号 1–6（6 条），`AptitudeEquip.dat#00000.c1` → `AptitudeEquip.dat#00005.c1`
- [x] **M3-02** AreaInfo.dat，序号 7–37（31 条），`AreaInfo.dat#00000.name` → `AreaInfo.dat#00015.description`
- [x] **M3-03** CharacterInfo.dat，序号 38–39（2 条），`CharacterInfo.dat#00000.c1` → `CharacterInfo.dat#00001.c1`
- [x] **M3-04** CharacterRaceText.dat，序号 40–875（836 条），`CharacterRaceText.dat#00001.c1` → `CharacterRaceText.dat#00038.c22`
- [x] **M3-05** FieldHouse.dat，序号 12283–12452（170 条），`FieldHouse.dat#00000.c1` → `FieldHouse.dat#00169.c1`
- [x] **M3-06** FieldHouseArea.dat，序号 12453–12455（3 条），`FieldHouseArea.dat#00000.c1` → `FieldHouseArea.dat#00002.c1`
- [x] **M3-07** FieldHouseBlock.dat，序号 12456–12458（3 条），`FieldHouseBlock.dat#00000.c1` → `FieldHouseBlock.dat#00002.c1`
- [x] **M3-08** FieldHouseNPC.dat，序号 12459–13458（1000 条），`FieldHouseNPC.dat#00000.npc_name` → `FieldHouseNPC.dat#00168.line_normal`
- [x] **M3-09** FieldHouseNPC.dat，序号 13459–14046（588 条），`FieldHouseNPC.dat#00168.line_angry1` → `FieldHouseNPC.dat#00267.line_raid2`
- [x] **M3-10** FieldHouseWitch.dat，序号 14047–14048（2 条），`FieldHouseWitch.dat#00000.c1` → `FieldHouseWitch.dat#00001.c1`
- [x] **M3-11** ItemAbility.dat，序号 15168–15185（18 条），`ItemAbility.dat#00000.c1` → `ItemAbility.dat#00017.c1`
- [x] **M3-12** ItemBase.dat，序号 15186–15587（402 条），`ItemBase.dat#00000.name` → `ItemBase.dat#00200.description`
- [x] **M3-13** ItemFlavor.dat，序号 15588–15651（64 条），`ItemFlavor.dat#00000.name` → `ItemFlavor.dat#00031.description`
- [x] **M3-14** ItemGroupName.dat，序号 15652–15662（11 条），`ItemGroupName.dat#00000.c1` → `ItemGroupName.dat#00010.c1`
- [x] **M3-15** ItemTitleA.dat，序号 15663–15681（19 条），`ItemTitleA.dat#00000.c1` → `ItemTitleA.dat#00018.c1`
- [x] **M3-16** ItemTitleB.dat，序号 15682–15701（20 条），`ItemTitleB.dat#00000.c1` → `ItemTitleB.dat#00019.c1`
- [x] **M3-17** MapBonusList.dat，序号 15702–15721（20 条），`MapBonusList.dat#00000.name` → `MapBonusList.dat#00012.name`
- [x] **M3-18** MapEvaluation.dat，序号 15722–15754（33 条），`MapEvaluation.dat#00000.c1` → `MapEvaluation.dat#00032.c1`
- [x] **M3-19** MapInfo.dat，序号 15755–15828（74 条），`MapInfo.dat#00001.name` → `MapInfo.dat#00037.description`
- [x] **M3-20** Notorious.dat，序号 15829–15840（12 条），`Notorious.dat#00000.c1` → `Notorious.dat#00011.c1`
- [x] **M3-21** Petition.dat，序号 15841–15860（20 条），`Petition.dat#00000.title` → `Petition.dat#00009.description`
- [x] **M3-22** PillarList.dat，序号 15861–16190（330 条），`PillarList.dat#00000.name` → `PillarList.dat#00164.description`
- [x] **M3-23** RandomName.dat，序号 16191–16758（568 条），`RandomName.dat#00000.name_male` → `RandomName.dat#00283.name_female`
- [x] **M3-24** ShopList.dat，序号 16759–16789（31 条），`ShopList.dat#00000.c1` → `ShopList.dat#00030.c1`
- [x] **M3-25** ShopLvUpPrize.dat，序号 16790–16830（41 条），`ShopLvUpPrize.dat#00000.c4` → `ShopLvUpPrize.dat#00086.c10`
- [x] **M3-26** ShopSkill.dat，序号 16831–17278（448 条），`ShopSkill.dat#00000.name` → `ShopSkill.dat#00223.description`
- [x] **M3-27** WitchToken.dat，序号 17279–17775（497 条），`WitchToken.dat#00000.c1` → `WitchToken.dat#00496.c1`

## M4 — 程序、Lua、奖杯与光盘标题

- [x] **M4-01** EBOOT_140.elf，序号 17776–17898（123 条），`EBOOT_140.elf#0x0E1D8C0` → `EBOOT_140.elf#0x0E60DB8`
- [x] **M4-02** Game/Demo/episodeLoad.lua，序号 17899–17899（1 条），`Game/Demo/episodeLoad.lua#L0036_2` → `Game/Demo/episodeLoad.lua#L0036_2`
- [x] **M4-03** Game/Demo/mainquest/demo9999_0000.lua，序号 17900–17904（5 条），`Game/Demo/mainquest/demo9999_0000.lua#L0455_1` → `Game/Demo/mainquest/demo9999_0000.lua#L0459_5`
- [x] **M4-04** Game/Demo/mainquest/episode13_demo.lua，序号 17905–17905（1 条），`Game/Demo/mainquest/episode13_demo.lua#L7945_1` → `Game/Demo/mainquest/episode13_demo.lua#L7945_1`
- [x] **M4-05** Map/mapScrLoad.lua，序号 17906–17906（1 条），`Map/mapScrLoad.lua#L0053_2` → `Map/mapScrLoad.lua#L0053_2`
- [ ] **M4-06** PARAM.SFO，序号 17907–17907（1 条），`PARAM.SFO#TITLE` → `PARAM.SFO#TITLE`
- [ ] **M4-07** TROP.SFM，序号 17908–18005（98 条），`TROPHY.TRP#title-name` → `TROPHY.TRP#047_detail`

## M5 — 全量文本验收

- [ ] 运行 `python3 scripts/verify_alignment.py --require-complete`，核对术语跨表一致性、16 条演出占位及修改索引。

## M6 — 回灌与实机验收

- [ ] 补齐图像、字库、回灌工具和目标版本游戏文件，核对实际资源清单与回灌坐标。
- [ ] 校验文本回灌、字库覆盖和 UI 显示，抽测剧情字幕、语音对应及菜单、奖杯、Lua 运行时文本。
