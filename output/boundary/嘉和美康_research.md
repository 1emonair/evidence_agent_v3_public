# 嘉和美康 证据核验工单

模式：research。硬锁：不改冻结分数，不改相对因子，不输出拒保或事故结论。
本次新入审批队列：11 张。

## 冻结画像

- ABRI-T 47.06，T5，等权档 L4
- O 63.02（4 个年度均值），S 100.0，红旗 0，EVC 18.75
- 备案展示：无（不参与计分）

## 复查卡（原记 L2，共 12 张）

### 2021 O1 · ISO20000 → 待人工

- 卡号：`CNINFO_1213087068:O1:ISO20000`
- 引用：公司先后通过ISO9001、ISO13485医疗器械质量管理体系、ISO20000信息技术服务管理体系、ISO22301业务连续性管理体系、ISO27001信息安全管理体系、ISO27017云安
- 判读：unclear（语义=待人工，编号=无），规则无法确定主体或时态，转人工。
- 后端：rules，置信度 0.40；工具：judge:unclear/rules/0.40 → expand_context→unclear/rules → find_cert_id:False → compare_years:[2022, 2023, 2024]
- 第二章审计：verdict=POS，counts_as_L2=1
- 补件：请提供运维或服务管理体系证书编号、主体和有效期。

### 2021 O4 · 业务连续性管理体系 → 披露但未核实

- 卡号：`CNINFO_1213087068:O4:业务连续性管理体系`
- 引用：2021年，公司通过了ISO22301业务连续性管理体系、ISO27017云安全管理体系、ISO27018公有云个人信息保护管理体系、ISO27701隐私信息管理体系、
- 判读：held_claim（语义=算，编号=无），声称本企业（或子公司）取得认证/资质，需核对证书编号。
- 后端：rules，置信度 0.75；工具：judge:held_claim/rules/0.75 → find_cert_id:False
- 第二章审计：verdict=POS，counts_as_L2=1
- 补件：请提供回滚或业务连续性安排的证明。

### 2021 A4 · ISO27001 → 待人工

- 卡号：`CNINFO_1213087068:A4:ISO27001`
- 引用：ISO13485医疗器械质量管理体系、ISO20000信息技术服务管理体系、ISO22301业务连续性管理体系、ISO27001信息安全管理体系、ISO27017云安全管理体系、ISO27018公有云个人信息保护管理体系、ISO27701隐
- 判读：unclear（语义=待人工，编号=无），规则无法确定主体或时态，转人工。
- 后端：rules，置信度 0.40；工具：judge:unclear/rules/0.40 → expand_context→unclear/rules → find_cert_id:False → compare_years:[2022, 2023, 2024]
- 第二章审计：verdict=POS，counts_as_L2=1
- 补件：请提供认证证书编号、获证主体、有效期和覆盖范围。

### 2022 O1 · ISO20000 → 待人工

- 卡号：`CNINFO_1216671112:O1:ISO20000`
- 引用：公司先后通过ISO9001质量管理体系、ISO13485医疗器械质量管理体系、ISO20000信息技术服务管理体系、ISO22301业务连续性管理体系、ISO27001信息安全管理体系、ISO27017云安
- 判读：unclear（语义=待人工，编号=无），规则无法确定主体或时态，转人工。
- 后端：rules，置信度 0.40；工具：judge:unclear/rules/0.40 → expand_context→unclear/rules → find_cert_id:False → compare_years:[2021, 2023, 2024]
- 第二章审计：verdict=POS，counts_as_L2=1
- 补件：请提供运维或服务管理体系证书编号、主体和有效期。

### 2022 O4 · 业务连续性管理体系 → 待人工

- 卡号：`CNINFO_1216671112:O4:业务连续性管理体系`
- 引用：001质量管理体系、ISO13485医疗器械质量管理体系、ISO20000信息技术服务管理体系、ISO22301业务连续性管理体系、ISO27001信息安全管理体系、ISO27017云安2022年年度报告42/250全管理体系、ISO2701
- 判读：unclear（语义=待人工，编号=无），规则无法确定主体或时态，转人工。
- 后端：rules，置信度 0.40；工具：judge:unclear/rules/0.40 → expand_context→unclear/rules → find_cert_id:False → compare_years:[2021, 2023, 2024]
- 第二章审计：verdict=POS，counts_as_L2=1
- 补件：请提供回滚或业务连续性安排的证明。

### 2022 A4 · ISO27001 → 待人工

- 卡号：`CNINFO_1216671112:A4:ISO27001`
- 引用：ISO13485医疗器械质量管理体系、ISO20000信息技术服务管理体系、ISO22301业务连续性管理体系、ISO27001信息安全管理体系、ISO27017云安2022年年度报告42/250全管理体系、ISO27018公有云个人信息保
- 判读：unclear（语义=待人工，编号=无），规则无法确定主体或时态，转人工。
- 后端：rules，置信度 0.40；工具：judge:unclear/rules/0.40 → expand_context→unclear/rules → find_cert_id:False → compare_years:[2021, 2023, 2024]
- 第二章审计：verdict=POS，counts_as_L2=1
- 补件：请提供认证证书编号、获证主体、有效期和覆盖范围。

### 2023 O1 · ISO20000 → 待人工

- 卡号：`CNINFO_1219885439:O1:ISO20000`
- 引用：公司先后通过ISO9001质量管理体系、ISO13485医疗器械质量管理体系、ISO20000信息技术服务管理体系、ISO22301业务连续性管理体系、ISO27001信息安全管理体系、ISO27017云安
- 判读：unclear（语义=待人工，编号=无），规则无法确定主体或时态，转人工。
- 后端：rules，置信度 0.40；工具：judge:unclear/rules/0.40 → expand_context→unclear/rules → find_cert_id:False → compare_years:[2021, 2022, 2024]
- 第二章审计：verdict=POS，counts_as_L2=1
- 补件：请提供运维或服务管理体系证书编号、主体和有效期。

### 2023 O4 · 业务连续性管理体系 → 待人工

- 卡号：`CNINFO_1219885439:O4:业务连续性管理体系`
- 引用：001质量管理体系、ISO13485医疗器械质量管理体系、ISO20000信息技术服务管理体系、ISO22301业务连续性管理体系、ISO27001信息安全管理体系、ISO27017云安全管理体系、ISO27018公有云个人信息保护管理体系、
- 判读：unclear（语义=待人工，编号=无），规则无法确定主体或时态，转人工。
- 后端：rules，置信度 0.40；工具：judge:unclear/rules/0.40 → expand_context→unclear/rules → find_cert_id:False → compare_years:[2021, 2022, 2024]
- 第二章审计：verdict=POS，counts_as_L2=1
- 补件：请提供回滚或业务连续性安排的证明。

### 2023 A4 · ISO27001 → 待人工

- 卡号：`CNINFO_1219885439:A4:ISO27001`
- 引用：ISO13485医疗器械质量管理体系、ISO20000信息技术服务管理体系、ISO22301业务连续性管理体系、ISO27001信息安全管理体系、ISO27017云安全管理体系、ISO27018公有云个人信息保护管理体系、ISO27701隐
- 判读：unclear（语义=待人工，编号=无），规则无法确定主体或时态，转人工。
- 后端：rules，置信度 0.40；工具：judge:unclear/rules/0.40 → expand_context→unclear/rules → find_cert_id:False → compare_years:[2021, 2022, 2024]
- 第二章审计：verdict=POS，counts_as_L2=1
- 补件：请提供认证证书编号、获证主体、有效期和覆盖范围。

### 2024 O1 · ISO20000 → 待人工

- 卡号：`CNINFO_1223427496:O1:ISO20000`
- 引用：公司先后通过ISO9001质量管理体系、ISO13485医疗器械质量管理体系、ISO20000信息技术服务管理体系、ISO22301业务连续性管理体系、ISO27001信息安全管理体系、ISO27017云安
- 判读：unclear（语义=待人工，编号=无），规则无法确定主体或时态，转人工。
- 后端：rules，置信度 0.40；工具：judge:unclear/rules/0.40 → expand_context→unclear/rules → find_cert_id:False → compare_years:[2021, 2022, 2023]
- 第二章审计：verdict=POS，counts_as_L2=1
- 补件：请提供运维或服务管理体系证书编号、主体和有效期。

### 2024 O4 · 业务连续性管理体系 → 待人工

- 卡号：`CNINFO_1223427496:O4:业务连续性管理体系`
- 引用：001质量管理体系、ISO13485医疗器械质量管理体系、ISO20000信息技术服务管理体系、ISO22301业务连续性管理体系、ISO27001信息安全管理体系、ISO27017云安全管理体系、ISO27018公有云个人信息保护管理体系、
- 判读：unclear（语义=待人工，编号=无），规则无法确定主体或时态，转人工。
- 后端：rules，置信度 0.40；工具：judge:unclear/rules/0.40 → expand_context→unclear/rules → find_cert_id:False → compare_years:[2021, 2022, 2023]
- 第二章审计：verdict=POS，counts_as_L2=1
- 补件：请提供回滚或业务连续性安排的证明。

### 2024 A4 · ISO27001 → 待人工

- 卡号：`CNINFO_1223427496:A4:ISO27001`
- 引用：ISO13485医疗器械质量管理体系、ISO20000信息技术服务管理体系、ISO22301业务连续性管理体系、ISO27001信息安全管理体系、ISO27017云安全管理体系、ISO27018公有云个人信息保护管理体系、ISO27701隐
- 判读：unclear（语义=待人工，编号=无），规则无法确定主体或时态，转人工。
- 后端：rules，置信度 0.40；工具：judge:unclear/rules/0.40 → expand_context→unclear/rules → find_cert_id:False → compare_years:[2021, 2022, 2023]
- 第二章审计：verdict=POS，counts_as_L2=1
- 补件：请提供认证证书编号、获证主体、有效期和覆盖范围。

## 升级卡（漏检复查，共 0 张）

AI 段落语料中未发现词表外的持证或备案写法。

## 情景列（只读，不回写）

| 口径 | O′ | 红旗′ | 翻转 | 降级格 | 升级格 |
|---|---|---|---|---|---|
| 冻结 | 63.02 | 0 | - | - | - |
| strict（主） | 63.02 | 0 | +0 | 0 | 0 |
| loose（稳健性） | 63.54 | 0 | +0 | 1 | 0 |
| strict + 待定升级全采纳（上界） | 63.02 | 0 | +0 | 0 | 0 |

strict：同格全部卡不支持才降 L0。loose：另把无已核实的未核实格降 L1b。待人工的格子两档都不动。升级只采纳人工 accept 的卡。

## 复核建议

有卡片待人工确认，已写入审批队列。 本 Agent 不改冻结分数、相对因子和承保结论。
