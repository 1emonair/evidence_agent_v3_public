# 东软集团 证据核验工单

模式：research。硬锁：不改冻结分数，不改相对因子，不输出拒保或事故结论。
本次新入审批队列：3 张。

## 冻结画像

- ABRI-T 28.04，T4，等权档 L3
- O 69.17（5 个年度均值），S 58.0，红旗 0，EVC 12.5
- 备案展示：无（不参与计分）

## 复查卡（原记 L2，共 12 张）

### 2020 O1 · ITIL → 不支持

- 卡号：`CNINFO_1209858138:O1:ITIL`
- 引用：6、质量管理优势东软基于ISO9001质量管理标准，融合CMMI、A-SPICE、RUP、Lean、Agile、ITIL、PCMM等模型、方法的先进理念，对公司的质量体系进行持续的升级和完善，先后通过了DNV、BSI、QAI、CQC
- 判读：method_reference（语义=不算，编号=无），按某标准或方法论开展工作，未声称取得第三方认证。
- 后端：rules，置信度 0.75；工具：judge:method_reference/rules/0.75 → expand_context→method_reference/rules → same_doc_search:无其他支持
- 第二章审计：verdict=POS，counts_as_L2=1
- 补件：请提供运维或服务管理体系证书编号、主体和有效期。

### 2020 A4 · CMMI → 披露但未核实

- 卡号：`CNINFO_1209858138:A4:CMMI`
- 引用：行业情况说明东软集团于1991年成立，于1996年上市，是中国第一家上市的软件企业，也是中国第一家通过CMM5、CMMI5认证和PCMMLevel5评估的软件企业
- 判读：held_claim（语义=算，编号=无），声称本企业（或子公司）取得认证/资质，需核对证书编号。
- 后端：rules，置信度 0.75；工具：judge:held_claim/rules/0.75 → expand_context→held_claim/rules → find_cert_id:False
- 第二章审计：verdict=POS，counts_as_L2=1
- 补件：请提供认证证书编号、获证主体、有效期和覆盖范围。

### 2021 O1 · ITIL → 不支持

- 卡号：`CNINFO_1213224036:O1:ITIL`
- 引用：6、质量管理优势东软基于ISO9001质量管理标准，融合CMMI、A-SPICE、RUP、Lean、Agile、ITIL、PCMM等模型、方法的先进理念，对公司的质量体系进行持续的升级和完善，先后通过了DNV、BSI、QAI、CQC
- 判读：method_reference（语义=不算，编号=无），按某标准或方法论开展工作，未声称取得第三方认证。
- 后端：rules，置信度 0.75；工具：judge:method_reference/rules/0.75 → expand_context→method_reference/rules → same_doc_search:无其他支持
- 第二章审计：verdict=POS，counts_as_L2=1
- 补件：请提供运维或服务管理体系证书编号、主体和有效期。

### 2021 A4 · CMMI → 待人工

- 卡号：`CNINFO_1213224036:A4:CMMI`
- 引用：6、质量管理优势东软基于ISO9001质量管理标准，融合CMMI、A-SPICE、RUP、Lean、Agile、ITIL、PCMM等模型、方法的先进理念，对公司的质量体系进行持
- 判读：method_reference（语义=不算，编号=无），按某标准或方法论开展工作，未声称取得第三方认证。 但 [2020, 2024] 年同一关键词有持证陈述，可能仍在有效期内，不自动降级。
- 后端：rules，置信度 0.75；工具：judge:method_reference/rules/0.75 → expand_context→method_reference/rules → same_doc_search:无其他支持 → compare_years→[2020, 2024]有持证陈述
- 第二章审计：verdict=POS，counts_as_L2=1
- 补件：请提供认证证书编号、获证主体、有效期和覆盖范围。

### 2022 O1 · ITIL → 不支持

- 卡号：`CNINFO_1216427790:O1:ITIL`
- 引用：6、质量管理优势东软基于ISO9001质量管理标准，融合CMMI、A-SPICE、RUP、Lean、Agile、ITIL、PCMM等模型、方法的先进理念，对公司的质量体系进行持续的升级和完善，先后通过了DNV、BSI、QAI、CQC
- 判读：method_reference（语义=不算，编号=无），按某标准或方法论开展工作，未声称取得第三方认证。
- 后端：rules，置信度 0.75；工具：judge:method_reference/rules/0.75 → expand_context→method_reference/rules → same_doc_search:无其他支持
- 第二章审计：verdict=POS，counts_as_L2=1
- 补件：请提供运维或服务管理体系证书编号、主体和有效期。

### 2022 A4 · CMMI → 待人工

- 卡号：`CNINFO_1216427790:A4:CMMI`
- 引用：6、质量管理优势东软基于ISO9001质量管理标准，融合CMMI、A-SPICE、RUP、Lean、Agile、ITIL、PCMM等模型、方法的先进理念，对公司的质量体系进行持
- 判读：method_reference（语义=不算，编号=无），按某标准或方法论开展工作，未声称取得第三方认证。 但 [2020, 2024] 年同一关键词有持证陈述，可能仍在有效期内，不自动降级。
- 后端：rules，置信度 0.75；工具：judge:method_reference/rules/0.75 → expand_context→method_reference/rules → same_doc_search:无其他支持 → compare_years→[2020, 2024]有持证陈述
- 第二章审计：verdict=POS，counts_as_L2=1
- 补件：请提供认证证书编号、获证主体、有效期和覆盖范围。

### 2023 D3 · DCMM → 披露但未核实

- 卡号：`CNINFO_1219773391:D3:DCMM`
- 引用：从资质结果看，2023年，公司通过国家数据管理能力成熟度（DCMM）四级认证，数据管理和应用的成熟度达到量化管理级水平，标志着东软已具备目前乙方企业(数据运营商)获取到的最高等级
- 判读：held_claim（语义=算，编号=无），声称本企业（或子公司）取得认证/资质，需核对证书编号。
- 后端：rules，置信度 0.75；工具：judge:held_claim/rules/0.75 → expand_context→held_claim/rules → find_cert_id:False
- 第二章审计：verdict=POS，counts_as_L2=1
- 补件：请提供数据管理认证的证书编号、主体和有效期。

### 2023 O1 · ITIL → 不支持

- 卡号：`CNINFO_1219773391:O1:ITIL`
- 引用：基于ISO9001质量管理标准，融合CMMI、TMMI、DCMM、A-SPICE、RUP、Lean、Agile、ITIL、PCMM等模型、方法的先进理念，对公司的质量体系进行持续的升级和完善，先后通过了DNV、BSI、QAI、CQC
- 判读：method_reference（语义=不算，编号=无），按某标准或方法论开展工作，未声称取得第三方认证。
- 后端：rules，置信度 0.75；工具：judge:method_reference/rules/0.75 → expand_context→method_reference/rules → same_doc_search:无其他支持
- 第二章审计：verdict=POS，counts_as_L2=1
- 补件：请提供运维或服务管理体系证书编号、主体和有效期。

### 2023 A4 · CMMI → 待人工

- 卡号：`CNINFO_1219773391:A4:CMMI`
- 引用：23/211东软集团股份有限公司2023年年度报告6、质量管理优势东软基于ISO9001质量管理标准，融合CMMI、TMMI、DCMM、A-SPICE、RUP、Lean、Agile、ITIL、PCMM等模型、方法的先进理念，对
- 判读：method_reference（语义=不算，编号=无），按某标准或方法论开展工作，未声称取得第三方认证。 但 [2020, 2024] 年同一关键词有持证陈述，可能仍在有效期内，不自动降级。
- 后端：rules，置信度 0.75；工具：judge:method_reference/rules/0.75 → expand_context→method_reference/rules → same_doc_search:无其他支持 → compare_years→[2020, 2024]有持证陈述
- 第二章审计：verdict=POS，counts_as_L2=1
- 补件：请提供认证证书编号、获证主体、有效期和覆盖范围。

### 2024 D3 · DCMM → 披露但未核实

- 卡号：`CNINFO_1223383841:D3:DCMM`
- 引用：2023年，公司通过国家数据管理能力成熟度（DCMM）四级认证和国产化信息系统集成和服务能力等级评估-优秀级(LS4)
- 判读：held_claim（语义=算，编号=无），声称本企业（或子公司）取得认证/资质，需核对证书编号。
- 后端：rules，置信度 0.75；工具：judge:held_claim/rules/0.75 → expand_context→held_claim/rules → find_cert_id:False
- 第二章审计：verdict=POS，counts_as_L2=1
- 补件：请提供数据管理认证的证书编号、主体和有效期。

### 2024 O1 · ITIL → 不支持

- 卡号：`CNINFO_1223383841:O1:ITIL`
- 引用：基于ISO9001质量管理标准，融合CMMI、TMMI、DCMM、A-SPICE、RUP、Lean、Agile、ITIL、PCMM等模型、方法的先进理念，对公司的质量体系进行持续的升级和完善，先后通过了DNV、BSI、QAI、CQC
- 判读：method_reference（语义=不算，编号=无），按某标准或方法论开展工作，未声称取得第三方认证。
- 后端：rules，置信度 0.75；工具：judge:method_reference/rules/0.75 → expand_context→method_reference/rules → same_doc_search:无其他支持
- 第二章审计：verdict=BARE，counts_as_L2=0
- 补件：请提供运维或服务管理体系证书编号、主体和有效期。

### 2024 A4 · CMMI → 披露但未核实

- 卡号：`CNINFO_1223383841:A4:CMMI`
- 引用：6、质量管理优势东软基于ISO9001质量管理标准，融合CMMI、TMMI、DCMM、A-SPICE、RUP、Lean、Agile、ITIL、PCMM等模型、方法的先进理念，对
- 判读：method_reference（语义=不算，编号=无），命中句本身不成立（method_reference）；同一年报他处支持（held_claim），该格不降级。
- 后端：rules，置信度 0.75；工具：judge:method_reference/rules/0.75 → expand_context→method_reference/rules → same_doc_search→held_claim
- 同一年报他处支持：2022年，东软通过CMMIV2.0的5级评估和TMMI的5级评估
- 第二章审计：verdict=BARE，counts_as_L2=0
- 补件：请提供认证证书编号、获证主体、有效期和覆盖范围。

## 升级卡（漏检复查，共 0 张）

AI 段落语料中未发现词表外的持证或备案写法。

## 情景列（只读，不回写）

| 口径 | O′ | 红旗′ | 翻转 | 降级格 | 升级格 |
|---|---|---|---|---|---|
| 冻结 | 69.17 | 0 | - | - | - |
| strict（主） | 75.42 | 0 | +0 | 5 | 0 |
| loose（稳健性） | 77.08 | 0 | +0 | 9 | 0 |
| strict + 待定升级全采纳（上界） | 75.42 | 0 | +0 | 5 | 0 |

strict：同格全部卡不支持才降 L0。loose：另把无已核实的未核实格降 L1b。待人工的格子两档都不动。升级只采纳人工 accept 的卡。

## 复核建议

部分原记 L2 的命中不构成本企业证据，已出补件项。 有卡片待人工确认，已写入审批队列。 本 Agent 不改冻结分数、相对因子和承保结论。
