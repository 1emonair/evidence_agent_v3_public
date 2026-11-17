# 普联软件 证据核验工单

模式：research。硬锁：不改冻结分数，不改相对因子，不输出拒保或事故结论。
本次新入审批队列：0 张。

## 冻结画像

- ABRI-T 30.88，T4，等权档 L3
- O 81.25（4 个年度均值），S 40.0，红旗 0，EVC 0.0
- 备案展示：无（不参与计分）

## 复查卡（原记 L2，共 4 张）

### 2021 A4 · CMMI → 不支持

- 卡号：`CNINFO_1212752922:A4:CMMI`
- 引用：该平台提供可视化和集成化开发模式，是公司目前的主流研发平台CMMI指软件能力成熟度模型集成（CapabilityMaturityModelIntegration）XBRL指可扩展
- 判读：definition（语义=不算，编号=无），出现在释义或概念介绍中，不是本企业的持证陈述。
- 后端：rules，置信度 0.85；工具：judge:definition/rules/0.85 → expand_context→definition/rules → same_doc_search:无其他支持
- 第二章审计：verdict=DEF，counts_as_L2=0
- 补件：请提供认证证书编号、获证主体、有效期和覆盖范围。

### 2022 A4 · CMMI → 不支持

- 卡号：`CNINFO_1216413635:A4:CMMI`
- 引用：该平台提供可视化和集成化开发模式，是公司目前的主流研发平台CMMI指软件能力成熟度模型集成（CapabilityMaturityModelIntegration）XBRL指可扩展
- 判读：definition（语义=不算，编号=无），出现在释义或概念介绍中，不是本企业的持证陈述。
- 后端：rules，置信度 0.85；工具：judge:definition/rules/0.85 → expand_context→definition/rules → same_doc_search:无其他支持
- 第二章审计：verdict=DEF，counts_as_L2=0
- 补件：请提供认证证书编号、获证主体、有效期和覆盖范围。

### 2023 A4 · CMMI → 不支持

- 卡号：`CNINFO_1219598562:A4:CMMI`
- 引用：该平台提供可视化和集成化开发模式，是公司目前的主流研发平台CMMI指软件能力成熟度模型集成（CapabilityMaturityModelIntegration）XBRL指可扩展
- 判读：definition（语义=不算，编号=无），出现在释义或概念介绍中，不是本企业的持证陈述。
- 后端：rules，置信度 0.85；工具：judge:definition/rules/0.85 → expand_context→definition/rules → same_doc_search:无其他支持
- 第二章审计：verdict=DEF，counts_as_L2=0
- 补件：请提供认证证书编号、获证主体、有效期和覆盖范围。

### 2024 A4 · CMMI → 不支持

- 卡号：`CNINFO_1222972153:A4:CMMI`
- 引用：该平台提供可视化和集成化开发模式，是公司目前的主流研发平台CMMI指软件能力成熟度模型集成（CapabilityMaturityModelIntegration）XBRL指可扩展
- 判读：definition（语义=不算，编号=无），出现在释义或概念介绍中，不是本企业的持证陈述。
- 后端：rules，置信度 0.85；工具：judge:definition/rules/0.85 → expand_context→definition/rules → same_doc_search:无其他支持
- 第二章审计：verdict=DEF，counts_as_L2=0
- 补件：请提供认证证书编号、获证主体、有效期和覆盖范围。

## 升级卡（漏检复查，共 0 张）

AI 段落语料中未发现词表外的持证或备案写法。

## 情景列（只读，不回写）

| 口径 | O′ | 红旗′ | 翻转 | 降级格 | 升级格 |
|---|---|---|---|---|---|
| 冻结 | 81.25 | 0 | - | - | - |
| strict（主） | 87.5 | 1 | +1 | 4 | 0 |
| loose（稳健性） | 87.5 | 1 | +1 | 4 | 0 |
| strict + 待定升级全采纳（上界） | 87.5 | 1 | +1 | 4 | 0 |

strict：同格全部卡不支持才降 L0。loose：另把无已核实的未核实格降 L1b。待人工的格子两档都不动。升级只采纳人工 accept 的卡。

## 复核建议

strict 情景红旗 0→1，转人工复核 O 的证据基础。 部分原记 L2 的命中不构成本企业证据，已出补件项。 本 Agent 不改冻结分数、相对因子和承保结论。
