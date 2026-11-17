"""增强规则判读（对照实验的 B 版，也是无 API 时的回退）。

判断顺序（先排除、后认定）：
  缩写 → 释义 → 法规引用 → 行业门槛 → 计划/申报中 → 培训/简历 → 客户服务
  → 方法/标准引用 → 本企业持证（动词 / 证书表 / 资质清单） → 备案提及 → 转人工
所有窗口都截在句号内，避免被相邻句子带偏。
"""

from __future__ import annotations

import re

from .judge_types import CERT_ID, Judgment, squash

ABBREV = re.compile(r"SFT|微调|优化方式|偏好优化|DirectPreference|运维理念|平台融入|多种运维")
DEFINITION = re.compile(
    r"释义|是指|即软件|即能力成熟度|认证指|[A-Z]{2,}[\d\-]*指|）指|级指|的统称|"
    r"共有五个等级|分为5级|分为五个等级|共分五个等级|五个层次|从低等级|"
    r"是衡量|由美国|创立的一套|国际通用标准|主要用于|规格最高|是中国自主研发的一套"
)
REGULATION = re.compile(
    r"规定了|以下简称|配套立法|监管环境|征求意见稿|制度作出|实施规则|出台|应当|数据来源于|"
    r"出境标准合同|数据出境安全评估|出境活动条件|认证体系，确保国家|"
    r"《[^》]{2,40}(规定|办法|条例|规则|指南|法|意见|公告|指引|准则)》"
)
INDUSTRY = re.compile(
    r"资质壁垒|行业壁垒|技术壁垒|需要取得|门槛|需求不断增加|越来越多的应用|行业要求|要求等保|可满足|共\d+款"
)
STD_SETTING = re.compile(r"主持和参与|参与制定|参编|标准的制定")
PENDING = re.compile(
    r"(?<!模)拟(申请|开展|取得|通过|申报)|计划|将开展|未来将|正在申请|正在推进|"
    r"筹备|争取|申报|申请中|评审中|流程中|正在备案|建设工作"
)
DONE = re.compile(r"已(取得|获得|通过)|获得|取得|成功通过|荣获")
TRAINING = re.compile(r"培训|宣贯|课程|学习地图")
BIO = re.compile(r"出生|国籍|学历|任职于|曾任|现任|管理师")
CUSTOMER = re.compile(
    r"认证咨询|认证评估咨询|评估咨询|提供认证|咨询服务|帮助客户|协助客户|为客户提供|"
    r"协助企业|帮助企业|一站式协助|服务客户|授权培训|培训服务|适配要求|满足企业对|"
    r"辅助企业|助力企业"
)
CUSTOMER_STRONG = re.compile(
    r"协助企业|帮助企业|认证咨询|评估咨询|一站式协助|咨询服务|授权培训|培训服务|适配要求|满足企业对"
)
METHOD_LEFT = re.compile(r"融合|遵循|遵从|依照|按照|根据|参照|基于|依据|围绕|运用|贯彻")
METHOD_RIGHT = re.compile(r"^[^。]{0,40}?(等模型|模型、方法|方法的|理念|框架|知识体系|的要求|体系的基础上|标准，结合|标准规范)")
HOLD = re.compile(
    r"取得|获得|获评|荣获|通过了|已通过|成功通过|顺利通过|持有|拥有|具备|具有|保持|设有|设立了|"
    r"达到[^，。；]{0,40}(等级|级)|"
    r"完成[^，。；]{0,60}(备案|认证|评估|年审|审核)|"
    r"通过[^，。；]{0,60}(认证|评估|评审|备案|审核|测评|评测|复评|复审)"
)
COMPANY_HOLD = re.compile(r"(公司|本公司|我司|集团|子公司)[^，。；]{0,24}(取得|获得|通过|完成|持有|拥有|具备)")
CERT_WORD = re.compile(r"证书|认证|资质|评估|备案|等级|体系|[一二三四五12345]级|数据保护官")
CERT_TABLE = re.compile(r"有效期|发证日期|发证机构|颁发|认证有限公司|认证中心|\d{4}年\d{1,2}月\d{1,2}日\d{4}年")
QUAL_LIST = re.compile(r"等(多项|一系列|系列|各类)?(行业)?(资质|认证|证书|体系认证|资格认证|标准体系认证|权威资质)")


def _j(label: str, conf: float, cite: str, reason: str, needs: bool = False) -> Judgment:
    return Judgment(label, conf, cite, reason, needs, "rules")


def _parts(flat: str, kw: str, n: int) -> tuple[str, str]:
    """关键词左右各 n 字，截在句号内。"""
    i = flat.find(kw)
    if i < 0:
        return "", ""
    left = flat[max(0, i - n): i]
    left = left[left.rfind("。") + 1:]
    right = flat[i + len(kw): i + len(kw) + n]
    j = right.find("。")
    return left, (right[:j] if j >= 0 else right)


def judge_rules(text: str, keyword: str, item: str) -> Judgment:
    flat = squash(text)
    kw = squash(keyword)
    l56, r56 = _parts(flat, kw, 56)
    l36, r36 = _parts(flat, kw, 36)
    l20, r20 = _parts(flat, kw, 20)
    lclause, _ = _parts(flat, kw, 240)
    span, mid, near = l56 + kw + r56, l36 + kw + r36, l20 + kw + r20
    cite = span or flat[:112]

    if kw in {"DPO", "CMMI", "ITIL", "DCMM"} and ABBREV.search(span):
        return _j("abbreviation", 0.9, cite, "缩写出现在算法/运维方法语境，不是治理岗位或企业资质。")
    if (DEFINITION.search(mid) or "释义" in span) and not COMPANY_HOLD.search(mid):
        return _j("definition", 0.85, cite, "出现在释义或概念介绍中，不是本企业的持证陈述。")
    if REGULATION.search(mid) and not COMPANY_HOLD.search(mid):
        return _j("regulation_cite", 0.85, cite, "法规或政策引用，不是本企业已落实的措施。")
    if INDUSTRY.search(mid) and not COMPANY_HOLD.search(mid):
        return _j("industry_context", 0.8, cite, "描述行业门槛、市场需求或产品可满足的要求，不是本企业持证。")
    if STD_SETTING.search(near) and not HOLD.search(near):
        return _j("industry_context", 0.75, cite, "参与标准制定，不等于本企业取得该认证。")
    if (PENDING.search(mid) or PENDING.search(lclause)) and not DONE.search(mid) and not DONE.search(lclause):
        return _j("future", 0.8, cite, "计划、申报或建设中，尚未完成。")
    if BIO.search(near):
        return _j("irrelevant_context", 0.8, cite, "人物简历或个人资格，不是企业治理证据。")
    if TRAINING.search(near) and not HOLD.search(near):
        return _j("training", 0.8, cite, "员工培训内容，不是企业已取得的认证。")
    if CUSTOMER.search(span):
        if CUSTOMER_STRONG.search(span) or not (HOLD.search(span) or HOLD.search(lclause)):
            return _j("customer_service", 0.85, cite, "主体是面向客户的服务或培训，不是本企业自身资质。")
    method = METHOD_LEFT.search(l20) or METHOD_RIGHT.search(r56)
    if method and not HOLD.search(lclause) and not HOLD.search(l20 + kw):
        return _j("method_reference", 0.75, cite, "按某标准或方法论开展工作，未声称取得第三方认证。")
    if HOLD.search(span) and CERT_WORD.search(span):
        return _j("held_claim", 0.75, cite, "声称本企业（或子公司）取得认证/资质，需核对证书编号。")
    if CERT_TABLE.search(span) or CERT_ID.search(span):
        return _j("held_claim", 0.7, cite, "出现在证书清单（编号/有效期/发证机构）中，按本企业持证处理。")
    if HOLD.search(lclause) and CERT_WORD.search(span):
        return _j("held_claim", 0.65, cite, "资质清单的一项，句首动词为取得/通过类，需核对证书编号。")
    if QUAL_LIST.search(r56):
        return _j("held_claim", 0.6, cite, "列在本企业「等资质/认证」清单中，需核对证书编号。")
    if item.startswith("M") and "备案" in kw:
        return _j("filing_mention", 0.7, cite, "提及完成备案，研究模式下不据此认定已核实。")
    return _j("unclear", 0.4, cite, "规则无法确定主体或时态，转人工。", True)
