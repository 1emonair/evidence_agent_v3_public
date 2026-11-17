# 罗普特 证据核验工单

模式：research。硬锁：不改冻结分数，不改相对因子，不输出拒保或事故结论。
本次新入审批队列：1 张。

## 冻结画像

- ABRI-T 70.0，T5，等权档 L5
- O 58.75（5 个年度均值），S 58.0，红旗 0，EVC 6.25
- 备案展示：有（不参与计分）

## 复查卡（原记 L2，共 5 张）

### 2020 A4 · CMMI → 披露但未核实

- 卡号：`CNINFO_1209728766:A4:CMMI`
- 引用：:2013）、质量管理体系认证（GB/T19001-2016/ISO9001:2015）等系列认证，并已初审通过CMMI5认证
- 判读：held_claim（语义=算，编号=无），声称本企业（或子公司）取得认证/资质，需核对证书编号。
- 后端：rules，置信度 0.75；工具：judge:held_claim/rules/0.75 → expand_context→held_claim/rules → find_cert_id:False
- 第二章审计：verdict=POS，counts_as_L2=1
- 补件：请提供认证证书编号、获证主体、有效期和覆盖范围。

### 2021 A4 · CMMI → 披露但未核实

- 卡号：`CNINFO_1212959432:A4:CMMI`
- 引用：7001:2013）、质量管理体系认证（GB/T19001-2016/ISO9001:2015）等系列认证，通过CMMI认证最高级-CMMI五级认证
- 判读：held_claim（语义=算，编号=无），声称本企业（或子公司）取得认证/资质，需核对证书编号。
- 后端：rules，置信度 0.75；工具：judge:held_claim/rules/0.75 → expand_context→held_claim/rules → find_cert_id:False
- 第二章审计：verdict=POS，counts_as_L2=1
- 补件：请提供认证证书编号、获证主体、有效期和覆盖范围。

### 2022 A4 · CMMI → 披露但未核实

- 卡号：`CNINFO_1216355644:A4:CMMI`
- 引用：(ISO9001:2015)、商品售后服务评价体系(GB/T27922-2011)等系列认证，持有软件开发成熟度CMMI五级证书
- 判读：held_claim（语义=算，编号=无），声称本企业（或子公司）取得认证/资质，需核对证书编号。
- 后端：rules，置信度 0.75；工具：judge:held_claim/rules/0.75 → expand_context→held_claim/rules → find_cert_id:False
- 第二章审计：verdict=POS，counts_as_L2=1
- 补件：请提供认证证书编号、获证主体、有效期和覆盖范围。

### 2023 A4 · CMMI → 披露但未核实

- 卡号：`CNINFO_1219741721:A4:CMMI`
- 引用：(ISO9001:2015)、商品售后服务评价体系(GB/T27922-2011)等系列认证，持有软件开发成熟度CMMI五级证书
- 判读：held_claim（语义=算，编号=无），声称本企业（或子公司）取得认证/资质，需核对证书编号。
- 后端：rules，置信度 0.75；工具：judge:held_claim/rules/0.75 → expand_context→held_claim/rules → find_cert_id:False
- 第二章审计：verdict=POS，counts_as_L2=1
- 补件：请提供认证证书编号、获证主体、有效期和覆盖范围。

### 2024 A4 · CMMI → 披露但未核实

- 卡号：`CNINFO_1223221327:A4:CMMI`
- 引用：等前沿技术研发，强化国产化技术突破，全年新增发明专利27项、软件著作权32项，累计知识产权达528项，并重新通过CMMI5认证及ITSS运维三级认证，构建AI算法训练推理一体化平台，技术模块复用率超50%
- 判读：held_claim（语义=算，编号=无），声称本企业（或子公司）取得认证/资质，需核对证书编号。
- 后端：rules，置信度 0.75；工具：judge:held_claim/rules/0.75 → expand_context→held_claim/rules → find_cert_id:False
- 第二章审计：verdict=POS，counts_as_L2=1
- 补件：请提供认证证书编号、获证主体、有效期和覆盖范围。

## 升级卡（漏检复查，共 1 张）

### 2024 O1 · ITSS → 升级候选（漏检复查，冻结层级 L1b）

- 卡号：`CNINFO_1223221327:O1:recall:ITSS`
- 引用：强化国产化技术突破，全年新增发明专利27项、软件著作权32项，累计知识产权达528项，并重新通过CMMI5认证及ITSS运维三（二）夯实产品和运营，深化业务布局在人工智能技术变革推动各行各业转型升级的大环境下，公司面向人工智能算力、
- 判读：held_claim（语义=算，编号=无），词表外写法命中，判读为本企业持证/已备案；需人工确认后才升 L2。声称本企业（或子公司）取得认证/资质，需核对证书编号。
- 后端：rules，置信度 0.75；工具：recall_search:ITSS → judge:held_claim/rules → find_cert_id:False
- 补件：请提供运维或服务管理体系证书编号、主体和有效期。

## 情景列（只读，不回写）

| 口径 | O′ | 红旗′ | 翻转 | 降级格 | 升级格 |
|---|---|---|---|---|---|
| 冻结 | 58.75 | 0 | - | - | - |
| strict（主） | 58.75 | 0 | +0 | 0 | 0 |
| loose（稳健性） | 60.83 | 0 | +0 | 5 | 0 |
| strict + 待定升级全采纳（上界） | 58.33 | 0 | +0 | 0 | 1 |

strict：同格全部卡不支持才降 L0。loose：另把无已核实的未核实格降 L1b。待人工的格子两档都不动。升级只采纳人工 accept 的卡。

## 复核建议

有卡片待人工确认，已写入审批队列。 本 Agent 不改冻结分数、相对因子和承保结论。
