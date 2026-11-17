# 山大地纬 证据核验工单

模式：research。硬锁：不改冻结分数，不改相对因子，不输出拒保或事故结论。
本次新入审批队列：3 张。

## 冻结画像

- ABRI-T 50.0，T5，等权档 L5
- O 67.92（5 个年度均值），S 54.0，红旗 0，EVC 8.75
- 备案展示：有（不参与计分）

## 复查卡（原记 L2，共 7 张）

### 2020 D3 · DCMM → 披露但未核实

- 卡号：`CNINFO_1209820675:D3:DCMM`
- 引用：二级）、CCRC-信息系统安全集成（二级）、CCRC-信息系统安全运维（二级）、CCRC-软件安全开发（二级）、DCMM-数据管理能力成熟度（三级）、知识产权管理体系等系列认证，推行全面质量控制管理，持续提升产品质量；公司注重知识产
- 判读：held_claim（语义=算，编号=无），列在本企业「等资质/认证」清单中，需核对证书编号。
- 后端：rules，置信度 0.60；工具：judge:held_claim/rules/0.60 → expand_context→held_claim/rules → find_cert_id:False
- 第二章审计：verdict=POS，counts_as_L2=1
- 补件：请提供数据管理认证的证书编号、主体和有效期。

### 2020 A4 · CMMI → 待人工

- 卡号：`CNINFO_1209820675:A4:CMMI`
- 引用：4.产品安全保障情况√适用□不适用公司产品以自主研发软件为主，建立了严谨有效的管理规范和流程体系，通过CMMI5、ITSS-信息技术服务标准成熟度(二级）、CCRC-信息系统安全集成（二级）、CCRC-信息系统安全运维（二
- 判读：unclear（语义=待人工，编号=无），规则无法确定主体或时态，转人工。
- 后端：rules，置信度 0.40；工具：judge:unclear/rules/0.40 → expand_context→unclear/rules → find_cert_id:False → compare_years:[2021, 2022, 2024]
- 第二章审计：verdict=POS，counts_as_L2=1
- 补件：请提供认证证书编号、获证主体、有效期和覆盖范围。

### 2021 D3 · DCMM → 披露但未核实

- 卡号：`CNINFO_1212899410:D3:DCMM`
- 引用：二级）、CCRC-信息系统安全集成（二级）、CCRC-信息系统安全运维（二级）、CCRC-软件安全开发（二级）、DCMM-数据管理能力成熟度（三级）、CCRC-应急处理（三级）、知识产权管理体系等系列认证，推行全面质量控制管理，持续
- 判读：held_claim（语义=算，编号=无），列在本企业「等资质/认证」清单中，需核对证书编号。
- 后端：rules，置信度 0.60；工具：judge:held_claim/rules/0.60 → expand_context→held_claim/rules → find_cert_id:False
- 第二章审计：verdict=POS，counts_as_L2=1
- 补件：请提供数据管理认证的证书编号、主体和有效期。

### 2021 A4 · CMMI → 待人工

- 卡号：`CNINFO_1212899410:A4:CMMI`
- 引用：产品安全保障情况公司以客户为中心，不断优化产品性能，提高和稳定产品质量，建立了严谨有效的管理规范和流程体系，通过CMMI5、ITSS-信息技术服务标准成熟度(二级）、CCRC-信息系统安全集成（二级）、CCRC-信息系统安全运维（二
- 判读：unclear（语义=待人工，编号=无），规则无法确定主体或时态，转人工。
- 后端：rules，置信度 0.40；工具：judge:unclear/rules/0.40 → expand_context→unclear/rules → find_cert_id:False → compare_years:[2020, 2022, 2024]
- 第二章审计：verdict=POS，counts_as_L2=1
- 补件：请提供认证证书编号、获证主体、有效期和覆盖范围。

### 2022 D3 · DCMM → 披露但未核实

- 卡号：`CNINFO_1216406643:D3:DCMM`
- 引用：二级）、CCRC-信息系统安全集成（二级）、CCRC-信息系统安全运维（二级）、CCRC-软件安全开发（二级）、DCMM-数据管理能力成熟度（三级）、CCRC-应急处理（三级）、知识产权管理体系等系列认证，推行全面质量控制管理，持续
- 判读：held_claim（语义=算，编号=无），列在本企业「等资质/认证」清单中，需核对证书编号。
- 后端：rules，置信度 0.60；工具：judge:held_claim/rules/0.60 → expand_context→held_claim/rules → find_cert_id:False
- 第二章审计：verdict=POS，counts_as_L2=1
- 补件：请提供数据管理认证的证书编号、主体和有效期。

### 2022 A4 · CMMI → 待人工

- 卡号：`CNINFO_1216406643:A4:CMMI`
- 引用：产品安全保障情况公司以客户为中心，不断优化产品性能，提高和稳定产品质量，建立了严谨有效的管理规范和流程体系，通过CMMI5、ITSS-信息技术服务标准成熟度(二级）、CCRC-信息系统安全集成（二级）、CCRC-信息系统安全运维（二
- 判读：unclear（语义=待人工，编号=无），规则无法确定主体或时态，转人工。
- 后端：rules，置信度 0.40；工具：judge:unclear/rules/0.40 → expand_context→unclear/rules → find_cert_id:False → compare_years:[2020, 2021, 2024]
- 第二章审计：verdict=POS，counts_as_L2=1
- 补件：请提供认证证书编号、获证主体、有效期和覆盖范围。

### 2024 A4 · CMMI → 披露但未核实

- 卡号：`CNINFO_1223072333:A4:CMMI`
- 引用：产品安全保障情况公司以客户为中心，不断优化产品性能，提高和稳定产品质量，建立了严谨有效的管理规范和流程体系，通过CMMI5、CS-信息系统建设和服务能力优秀级（四级）、LS-国产化信息系统集成和服务能力等级(四级)等系列认证，推行全
- 判读：held_claim（语义=算，编号=无），声称本企业（或子公司）取得认证/资质，需核对证书编号。
- 后端：rules，置信度 0.75；工具：judge:held_claim/rules/0.75 → expand_context→held_claim/rules → find_cert_id:False
- 第二章审计：verdict=POS，counts_as_L2=1
- 补件：请提供认证证书编号、获证主体、有效期和覆盖范围。

## 升级卡（漏检复查，共 0 张）

AI 段落语料中未发现词表外的持证或备案写法。

## 情景列（只读，不回写）

| 口径 | O′ | 红旗′ | 翻转 | 降级格 | 升级格 |
|---|---|---|---|---|---|
| 冻结 | 67.92 | 0 | - | - | - |
| strict（主） | 67.92 | 0 | +0 | 0 | 0 |
| loose（稳健性） | 69.58 | 0 | +0 | 4 | 0 |
| strict + 待定升级全采纳（上界） | 67.92 | 0 | +0 | 0 | 0 |

strict：同格全部卡不支持才降 L0。loose：另把无已核实的未核实格降 L1b。待人工的格子两档都不动。升级只采纳人工 accept 的卡。

## 复核建议

有卡片待人工确认，已写入审批队列。 本 Agent 不改冻结分数、相对因子和承保结论。
