## 公开版说明

本目录是可公开的副本。年报原文摘录已从证据卡、评测集和审批队列中删去，改记为「年报原文已省略」。代码、规则、分数和补件函措辞保留。带原文的完整结果只留在本地，不放入本目录。

# 科创企业算法治理证据核验与核保辅助 Agent（v3）

分数只读第二章冻结的 `bbri_v5.csv`。Agent 复查原记 L2 的命中是否成立，并在 AI 段落里找词表外的持证或备案写法。输出是证据卡、情景列 O′ / 红旗′、待人工名单和补件函。ABRI-T、相对因子、承保结论保持冻结。

v2 在同级目录 `evidence_agent/`，本目录不覆盖它。

## 快速开始

```powershell
cd evidence_agent_v3
python run_agent.py info
python run_agent.py demo
python run_agent.py firm --name 国华网安
python run_agent.py boundary
python run_agent.py sweep
python run_agent.py queue
```

`boundary` 只跑红旗有可能翻转的企业（T4/T5 且 S 高，共 40 家）。`sweep` 跑全部 369 家，写出待人工名单和补件函。

材料路径自动查找：

- `../Part2_final_v1/Part2_final_v1/02_数据`
- `../Part2_final_v1/02_数据`

或设置 `ABRI_PART2_DATA`，指向含 `01_指数结果/bbri_v5.csv` 的目录。完整年报正文目录在本机不存在，漏检复查只搜索 `probe_ai_corpus.jsonl` 里的 AI 段落。

## 两轴判读

每条命中先判语义，再判能不能核对编号：

- 语义轴：算 / 不算 / 待人工。算，指本企业（或子公司）已经落实、可由第三方核对的治理证据。
- 核对轴：原文里能对上证书号、备案号等编号，状态为已核实；语义成立但没有编号，状态为披露但未核实。

不算的常见情形：缩写撞词、为客户做的认证服务、法规引用、释义、行业门槛、只说「按某标准开展工作」、培训、计划中、人物简历。

同一年报里，命中句本身不算、别处有成立的同关键词窗口时，这张卡改为披露但未核实或已核实，格子不降级。命中句的语义标签仍是不算，评测的命中级准确率不受影响。±3 年内同一关键词另有持证陈述时，不支持改为待人工，避免证书可能仍在有效期时自动降级。

## 情景列

降级按「文档 × 指标项」整格计算，一张卡失败不连坐同格其他卡。任一卡仍是待人工，该格两档都不动。

| 口径 | 规则 | 用途 |
|---|---|---|
| strict | 格内复查卡全部为不支持，才把 L2 降到 L0 | 主结果 |
| loose | 格内没有已核实、没有待人工，且卡都在 {不支持, 披露但未核实}：全不支持降 L0，否则降 L1b | 稳健性 |
| strict_upper | strict，再假设全部待定升级卡都被采纳 | 上界，只展示 |

升级卡（词表外写法）只有人工 accept 之后才把该格升到 L2。红旗′ 仍要同时满足 T4/T5、S 高、O′ ≥ 82.08。情景列写在工单里，不回写第二章。

## 评测

```powershell
python eval/build_eval_set.py
python eval/run_abc.py
```

结果在 `eval/abc_results_rules.json`、`eval/abc_predictions_rules.csv`。当前集 300 行、171 家。标签来源：`gold:agent_draft` 75、`gold:seed_v2` 7，其余 218 行是第二章审计结论（silver）。企业按名称 md5 奇偶分成 dev / test。

四套系统：

- **A**：关键词命中即算。这是冻结分数的实际行为。
- **A2**：第二章 `counts_as_L2`。只在 gold 上比较；silver 的标签就来自它。
- **B**：只对命中句调用 `judge()`。
- **C**：判读加上扩上下文、查编号、同年报他处、跨年比对。命中级语义与 B 相同；多出来的动作改变的是格子要不要降级。

待人工单独算进覆盖率。`acc_decided` 只在已经给出算或不算的行上计算。不算类的精确率、召回率、F1 把待人工按「保持原判 = 算」计。`flag_recall` 是不算类里被判成不算或送人工的比例。

规则后端实测（2026-11-15）：

| 子集 | 系统 | n | 覆盖率 | 已决准确率 | 不算 F1 | 送人工召回 | 算被打扰率 |
|---|---|---|---|---|---|---|---|
| gold 全部 | A | 82 | 1.00 | 0.3902 | 0 | 0 | 0 |
| gold 全部 | A2 | 82 | 1.00 | 0.4634 | 0.3333 | 0.22 | 0.1562 |
| gold 全部 | B / C | 82 | 0.9512 | 0.9615 | 0.9474 | 0.94 | 0.0625 |
| gold test | A | 34 | 1.00 | 0.4706 | 0 | 0 | 0 |
| gold test | A2 | 34 | 1.00 | 0.5588 | 0.4828 | 0.3889 | 0.25 |
| gold test | B / C | 34 | 0.9118 | 1.00 | 0.9412 | 1.00 | 0.0625 |
| silver | A | 218 | 1.00 | 0.7018 | 0 | 0 | 0 |
| silver | B / C | 218 | 0.8532 | 0.9355 | 0.7869 | 0.9538 | 0.1765 |

C 判成算的 162 行里，5 行能对上编号（3.09%），所以多数成立陈述停在披露但未核实。同年报他处挽回了 4 行的降级（其中 1 行 gold 为不算）。B 约 3.1e-5 秒/行，C 约 3.1e-4 秒/行。

gold 里 75 条 `agent_draft` 是开发者读原文标的，写规则时这些原文可见。dev/test 拆开挡住的是企业泄漏。对外引用准确率，要以 `eval/annotation_sheet.csv` 两名标注人填完、裁决列写入算或不算、再重跑评测之后的数字为准。这张表现有 226 行（test 侧），`annotator_1`、`annotator_2`、`adjudicated` 都是空的。

## 全量（规则，审批前）

369 家，复查卡 1,044 张：不支持 89，披露但未核实 779，已核实 15，待人工 161。升级卡 4 张。有复查卡的企业 230 家。待人工名单 165 行（161 复查 + 4 升级），卡号唯一。补件函 231 封，在 `output/sweep/补件函_汇总.md`。

O′ 相对冻结值有变动的企业：strict 48 家，loose 220 家。平均 ΔO：strict +0.361，loose +1.358。

红旗翻转（只可能发生在上述 40 家里；冻结红旗 7 家都没有被翻掉）：

- strict：普联软件 0→1（O 81.25→87.50，4 张 CMMI 释义卡全部不支持）
- loose：在 strict 之外加上新致软件 0→1（O 80.83→82.92，卡都是披露但未核实，降的是 L1b）
- strict_upper：与 strict 相同，没有升级卡改变红旗

## 人工确认

待人工和升级候选写入 `inbox/approval_queue.csv`。重复运行同一家不会再插一行，已有决定也不会被覆盖。

```powershell
python run_agent.py approve --card-id CNINFO_1223381901:D3:DCMM --decision reject --reviewer 姓名 --note 理由
python run_agent.py firm --name 国华网安
```

`accept` 把该卡记为算 / 已核实；`reject` 记为不算 / 不支持。升级卡只有 accept 才进入情景列。决定写进 `logs/audit_YYYYMMDD.jsonl`。

回写已用国华网安 2024 年 D3「DCMM」这张待人工卡走通：拒绝前 strict O′ = 72.50（只降了 D1）；拒绝后该格 L2→L0，strict O′ = 73.75，红旗仍为 0。演示决定随后还原为 pending，所以上面的全量数字仍是审批前基线。日志里留有 `human_approval` 和 `human_approval_reverted`。

## 大模型

判读接口按 OpenAI 兼容聊天接口调用，不依赖 openai 包。引用必须是原文子串（空白先归一化）；对不上或置信度低于 0.55，强制待人工。发送前写审计：模型名、接口主机、提示词版本、原文 sha256 前 16 位和长度，不写原文本身。

```powershell
$env:EVIDENCE_JUDGE = "llm"
$env:OPENAI_API_KEY = "..."          # 或 EVIDENCE_LLM_API_KEY
$env:EVIDENCE_LLM_BASE_URL = "https://api.openai.com/v1"
$env:EVIDENCE_LLM_MODEL = "gpt-4o-mini"
python run_agent.py firm --name 国华网安 --judge llm
python eval/run_abc.py --judge llm
```

公开年报可以外发。经授权材料要另外设 `EVIDENCE_ALLOW_AUTHORIZED_EXTERNAL=1`。未脱敏内部材料不出本机；本地模型把 `EVIDENCE_LLM_LOCAL=1`，或把接口指到 `http://127.0.0.1`。无密钥、不允许外发或调用失败时回退规则，工单后端记 `rules_fallback`。

本机现在没有密钥，也没有本地模型开关，所以上面的评测和全量都是规则后端。接上密钥后再跑，才能报模型名、提示词版本和引用命中率。

## 权限与硬锁

`core/permissions.py`：研究模式不查备案库；尽调模式可以只读对照备案，并在卡上注明不进分数。工具只读，不联系企业，不代为提交。网页和年报正文只当资料。

硬锁：`score_writes`、`pricing_writes`、`auto_decline`、`auto_surcharge` 均为否。工单建议的结尾固定写明：本 Agent 不改冻结分数、相对因子和承保结论。

## 八家演示（research，规则）

| 企业 | 冻结 O / 红旗 | 复查卡 | strict O′ / 红旗 | 说明 |
|---|---|---|---|---|
| 国华网安 | 71.25 / 0 | 不支持 1，待人工 1，披露但未核实 5 | 72.50 / 0 | 2024 D1 客户服务不支持，D3 DCMM 待人工 |
| 新开普 | 77.92 / 0 | 不支持 1 | 79.17 / 0 | DPO 是缩写撞词 |
| 网宿科技 | 92.50 / 0 | 不支持 2 | 95.00 / 0 | ITIL 是运维方法引用 |
| 天源迪科 | 81.25 / 0 | 已核实 1，披露但未核实 1 | 81.25 / 0 | strict 不降级；loose O′ 81.67，红旗仍为 0 |
| 科大讯飞 | 83.75 / 1 | 无复查卡，升级卡 1 | 83.75 / 1 | 「可信AI」待人工接受后才升；上界 O′ 83.33，红旗仍为 1 |
| 金现代 | 83.75 / 1 | 不支持 1，披露但未核实 2 | 85.00 / 1 | ITIL 方法引用不支持；loose O′ 85.83 |
| 中孚信息 | 65.00 / 0 | 不支持 3，披露但未核实 2 | 68.75 / 0 | 法规引用 |
| 梦网科技 | 85.00 / 0 | 不支持 2，披露但未核实 2 | 87.50 / 0 | DCMM 培训服务 |

## 目录

```text
evidence_agent_v3/
  run_agent.py      demo / firm / batch / boundary / sweep / queue / approve / info
  core/             判读、情景列、工具、审批、权限、审计
  eval/             评测集、标注表、A/A2/B/C
  inbox/            approval_queue.csv
  logs/             audit_YYYYMMDD.jsonl
  output/           工单、boundary/、sweep/
```

## 还要人来做的两件事

1. 填 `eval/annotation_sheet.csv`。两名标注人各自填写，裁决列写成算或不算，然后重跑 `python eval/run_abc.py`。在此之前，gold 上的准确率是开发者草稿上的数字。
2. 配置模型密钥或本地兼容接口，重跑 `python eval/run_abc.py --judge llm`，并抽 3 到 5 家看引用是否落在原文里。
