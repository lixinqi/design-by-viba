# 规则集

## 需求背景

规则必须落到文件里，Check 与评审才能共用同一份清单，而不是每次靠记忆复述。这份规则集收 41 条：26 条来自用户原话，8 条由事件归纳，7 条为元规则；查漏新增的 48 条暂不采纳，等出现新的证据再逐条讨论。示例：`A14` 要求变体带载荷、`A19` 要求标签形态统一，这两条都不是口号，`Check` 能按它们报出违规。根 README 从这里取 `RuleId` 与 `List`，所以这篇有 public。

## public.viba

```bash public
import rules.types as rules
import rules.apis as rules_api

RuleId = rules.RuleId
List = rules_api.List
```

## types.viba

规则是固定词汇，每条规则一个取值；标签用英文短名，说明里写规则本身、依据与检查方法。规则集本体只记哪些规则被采纳。

```bash types
RuleId =
  Oneof
  | "readme_background_frozen" * { README 需求背景冻结，新经验写进别的文档；依据：原话：一定要冻结，不能改；检查：与冻结文本逐字比对 }
  | "external_only_public" * { 外部只依赖 public，types/apis 是内部实现；依据：原话：外部只能依赖 public；检查：跨文档 import 以 .public 结尾 }
  | "five_sections" * { 每篇必须有 需求背景/public/types/基本操作/apis 五段；依据：原话：必须有 public/types/apis 等章节；检查：抽 ## 章节比对 }
  | "background_states_input_and_ops" * { 根需求背景写输入与操作类别，不写阅读顺序；依据：原话：总输入应是 repo_path；操作两类；检查：背景能抄出输入与操作 }
  | "root_api_is_real_operation" * { 根 api 必须是真操作，不是 Read/List；依据：原话：对外 api 竟然只是 read；检查：根 public 操作能独立执行并产出结果 }
  | "explicit_dependencies" * { 大 api 依赖小 api 写成显式参数；依据：原话：A <- B <- {...} <- FooBar；检查：签名里有对应依赖参数 }
  | "dependencies_after_hint" * { 依赖参数放在 HINT_BLOCK 之后；依据：原话：小 api 要放到 HINT 之后；检查：提示块前的参数不含 _api. }
  | "dep_tag_and_api_type" * { 依赖参数带 tag，类型写被依赖的 api；依据：原话：给 Measure 带个展位的 tag；检查：匹配 <- $tag (X.Api * {...}) }
  | "dep_hint_explains_service" * { 依赖提示写交回什么、拿它做什么；依据：原话：这一句话有点像废话；检查：提示含返回与用途，无“依赖 X：” }
  | "hint_folded" * { 函数提示块一律折行；依据：原话：无论长短都要折行；检查：正则 ^  <- \{ .+ \}$ }
  | "orphan_is_unreachable" * { 孤立=从根 public 不可达，不凭感觉；依据：原话：只要没人使用就是孤立；检查：从根 public BFS 差集 }
  | "delete_all_file_kinds" * { 删除不分文件类型，同一可达性判据；依据：原话：不限于 python 文件；检查：每类文件回答谁依赖它 }
  | "generated_follows_source" * { 生成物跟源头走，删后重查冗余；依据：原话：json_schema 重新生成了吗；检查：定义集合-函数=应有 schema }
  | "sum_with_payload" * { 和类型是带载荷的原语，不是标签集合；依据：原话：这个错大发了；检查：遍历 Oneof，看变体有无载荷 }
  | "no_record_plus_kind" * { 禁止记录+kind 枚举；依据：原话：替代继承/Oneof；检查：搜 $kind + 纯字符串枚举 }
  | "variant_names_problem" * { 变体名是情况/问题，不是话题；依据：原话：一个叫需求的 Rule；检查：代入「这条违规说的是___」 }
  | "type_name_says_content" * { 类型名说清内容（装违规叫 Violation）；依据：原话：这哪是 Lesson 啊；检查：读类型名与变体是否同类 }
  | "polarity_consistent" * { 类型名与变体名正负一致；依据：原话：否则要么都是负面的；检查：标 positive/negative 比对 }
  | "tag_form_consistent" * { 变体标签形态统一：问题/术语/动作；依据：原话：inline_hint 只是名词；检查：逐标签归三类 }
  | "payload_form_consistent" * { 载荷类型名也要同形态；依据：原话：不只是 tag；检查：逐 <tag,payload> 比对 }
  | "name_triple_consistent" * { 文件名/需求背景/public 三处一致；依据：原话：信息量一定要一致；检查：文件名关键词∈背景；public=背景声明 }
  | "public_covers_chain" * { public 必须覆盖需求全链路；依据：原话：怎么构建一条样本；检查：需求操作逐个查可达 }
  | "virtual_edge_before_delete" * { 删前先查说明里提到但代码没引用；依据：原话：想想概念之间的引用关系；检查：mention vs reference 清单 }
  | "fix_whole_class" * { 点名一处要按同一判据改完整类；依据：原话：不能我说一句你只做一句；检查：列同类命中并逐项勾销 }
  | "rename_is_semantic" * { 改名不是字符串替换，形态一起升级；依据：原话：就改了个名字；检查：改名后问形态/载荷/引用 }
  | "background_names_public" * { 每篇背景收尾写根 README 从这里取什么；依据：九篇都补过这句；检查：背景清单=public 导出行 }
  | "inner_sum_for_failures" * { 同一语义位置的失败收进内层和类型；依据：点赞 Mismatch；检查：外层变体数不变、内层增加 }
  | "principle_into_kb" * { 用户讲清的原则必须落进知识库并附示例；依据：原话：显然要写到 design-by-viba；检查：知识库有篇讲它并带本次例子 }
  | "six_checks_per_round" * { 每轮固定跑解析/加载/闭包/环/旧名/三者；依据：goal 要求反复审查；检查：贴六项数字 }
  | "verified_before_done" * { 没跑完验证不宣布完成、不推送；依据：原话：json_schema 重新生成了吗；检查：完成附命令与输出 }
  | "graph_before_delete" * { 概念图先于删除，闭包只发现够不到；依据：SampleConfigBase 被误删；检查：删前查虚边再删 }
  | "hint_adds_information" * { 说明要有新信息：删掉信息量不减即废话；依据：原话：有点像废话；检查：删掉说明问信息量 }
  | "violation_attribution" * { 违规要归因到原则+位置+内容；依据：原话：清晰指出违反原则；检查：Violation 三要素 }
  | "rule_before_action" * { 规则先于动作，先写判据再动手；依据：先有规则才有后续删除；检查：动作前有可复核判据 }
  | "fixed_structure" * { 结构固定、入口唯一；依据：五段+唯一根；检查：结构检查 }
  | "interface_answers_need" * { 接口要对得起输入与需求；依据：Read 被否定；检查：接口对应输入与操作 }
  | "design_phase_spec_only" * { 设计阶段只留规范，删除即检验；依据：删代码/生成物/样例；检查：可达性判据 }
  | "pure_enum_allowed" * { 纯字符串枚举只在确实无数据时允许；依据：Polarity/TagForm 未被骂；检查：检查变体是否本应有数据 }
  | "define_new_words" * { 自造词第一次出现必须当场解释；依据：AGENTS.md 禁词规定；检查：生僻词同段有定义 }
  | "text_reviewed_by_subagent" * { 交付自然语言前起独立 subagent 审查：不得过分口语，尽量用标准术语，读起来不能拗口；依据：这条规则也是铁律；检查：交付前有审查记录，且审查项覆盖口语、术语、拗口 }
  | "scolding_is_requirement" * { 训斥即需求：摘原话反推痛恨再成规则；依据：这句话本身也是经验；检查：复盘含原话与规则 }
  | "natural_language_reviewed" * { 自然语言描述要过独立审查：不得过分口语，尽量用标准术语，一定不能拗口；依据：这条是铁律；检查：另起一个审查者通读全部说明文字，逐条改掉拗口处 }

RuleBook =
  Object
  * $accepted (list[RuleId] * { 已采纳的规则；共 41 条 })
  * $rejected (int * { 未采纳的条数；查漏新增的 48 条暂不进入规则集 })
```

## 基本操作

只有一个操作：列规则。交回规则集里已采纳的 41 条，以及未采纳的条数。

## apis.viba

```bash apis
import rules.types as rules

List =
     rules.RuleBook
  <- $accepted (list[rules.RuleId] * { 已采纳的规则，按 A01 到 A41 的顺序 })
  <- {
    列规则：把已采纳的 41 条按顺序交回，并交回未采纳的条数；规则集只收有证据的条目，新条目要等出现新证据
  }
```
