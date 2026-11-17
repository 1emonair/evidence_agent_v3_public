# 软通动力 证据核验工单

模式：research。硬锁：不改冻结分数，不改相对因子，不输出拒保或事故结论。
本次新入审批队列：1 张。

## 冻结画像

- ABRI-T 67.4，T5，等权档 L5
- O 56.77（4 个年度均值），S 75.0，红旗 0，EVC 7.81
- 备案展示：无（不参与计分）

## 复查卡（原记 L2，共 6 张）

### 2021 D3 · DCMM → 披露但未核实

- 卡号：`CNINFO_1213110008:D3:DCMM`
- 引用：务十强”、“2021年度IT智能服务领军企业”、“2021年十佳云原生先锋实践”、“工信部电子联合会2021年度DCMM十佳案例”等奖项，获得可信云MSP卓越级认证、华为云MSP技术认证、阿里云原生合作伙伴、阿里云MSP&能力中心认
- 判读：held_claim（语义=算，编号=无），声称本企业（或子公司）取得认证/资质，需核对证书编号。
- 后端：rules，置信度 0.75；工具：judge:held_claim/rules/0.75 → expand_context→held_claim/rules → find_cert_id:False
- 第二章审计：verdict=POS，counts_as_L2=1
- 补件：请提供数据管理认证的证书编号、主体和有效期。

### 2021 O1 · ISO20000 → 待人工

- 卡号：`CNINFO_1213110008:O1:ISO20000`
- 引用：了质量ISO9001、信息安全ISO27001、环境ISO14000、职业健康安全ISO45001、信息技术服务ISO20000等体系五标合一的一体化管理机制
- 判读：unclear（语义=待人工，编号=无），规则无法确定主体或时态，转人工。
- 后端：rules，置信度 0.40；工具：judge:unclear/rules/0.40 → expand_context→unclear/rules → find_cert_id:False → compare_years:[]
- 第二章审计：verdict=BARE，counts_as_L2=0
- 补件：请提供运维或服务管理体系证书编号、主体和有效期。

### 2021 A4 · CMMI → 不支持

- 卡号：`CNINFO_1213110008:A4:CMMI`
- 引用：CMMI共有五个等级，分别标志着软件企业能力成熟度的五个层次
- 判读：definition（语义=不算，编号=无），出现在释义或概念介绍中，不是本企业的持证陈述。
- 后端：rules，置信度 0.85；工具：judge:definition/rules/0.85 → expand_context→definition/rules → same_doc_search:无其他支持
- 第二章审计：verdict=POS，counts_as_L2=1
- 补件：请提供认证证书编号、获证主体、有效期和覆盖范围。

### 2022 D3 · DCMM → 披露但未核实

- 卡号：`CNINFO_1216589974:D3:DCMM`
- 引用：报告期内，软通动力通过DevOps持续交付标准3级评估，成功入选DCMM年度十佳案例，获评全国信标委大数据标准工作组制定的《数据管理能力成熟度评估模型》(DCMM)“稳健级(三级)”，
- 判读：held_claim（语义=算，编号=无），声称本企业（或子公司）取得认证/资质，需核对证书编号。
- 后端：rules，置信度 0.75；工具：judge:held_claim/rules/0.75 → expand_context→held_claim/rules → find_cert_id:False
- 第二章审计：verdict=POS，counts_as_L2=1
- 补件：请提供数据管理认证的证书编号、主体和有效期。

### 2022 A4 · CMMI → 不支持

- 卡号：`CNINFO_1216589974:A4:CMMI`
- 引用：CMMI共有五个等级，分别标志着软件企业能力成熟度的五个层次
- 判读：definition（语义=不算，编号=无），出现在释义或概念介绍中，不是本企业的持证陈述。
- 后端：rules，置信度 0.85；工具：judge:definition/rules/0.85 → expand_context→definition/rules → same_doc_search:无其他支持
- 第二章审计：verdict=POS，counts_as_L2=1
- 补件：请提供认证证书编号、获证主体、有效期和覆盖范围。

### 2023 A4 · 等保三级 → 披露但未核实

- 卡号：`CNINFO_1219867433:A4:等保三级`
- 引用：入规模同比实现高速增长；业务创新进展方面，司库产品完成了业务场景全覆盖，初步实现从自动化向智能化的提升，产品取得等保三级认证，司库云T6Cloud完成了票据系统升级版本、数据国资报送、应收账款管理等功能，银企通TbCloud产品，重
- 判读：held_claim（语义=算，编号=无），声称本企业（或子公司）取得认证/资质，需核对证书编号。
- 后端：rules，置信度 0.75；工具：judge:held_claim/rules/0.75 → find_cert_id:False
- 第二章审计：verdict=POS，counts_as_L2=1
- 补件：请提供认证证书编号、获证主体、有效期和覆盖范围。

## 升级卡（漏检复查，共 0 张）

AI 段落语料中未发现词表外的持证或备案写法。

## 情景列（只读，不回写）

| 口径 | O′ | 红旗′ | 翻转 | 降级格 | 升级格 |
|---|---|---|---|---|---|
| 冻结 | 56.77 | 0 | - | - | - |
| strict（主） | 59.9 | 0 | +0 | 2 | 0 |
| loose（稳健性） | 61.46 | 0 | +0 | 5 | 0 |
| strict + 待定升级全采纳（上界） | 59.9 | 0 | +0 | 2 | 0 |

strict：同格全部卡不支持才降 L0。loose：另把无已核实的未核实格降 L1b。待人工的格子两档都不动。升级只采纳人工 accept 的卡。

## 复核建议

部分原记 L2 的命中不构成本企业证据，已出补件项。 有卡片待人工确认，已写入审批队列。 本 Agent 不改冻结分数、相对因子和承保结论。
