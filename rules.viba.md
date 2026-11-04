# 规则集

## 需求背景

规则与违规是同一种东西：一条规则被违反就是一条违规，所以只保留一个和类型 `Violation`，它的每个变体就是一条规则，变体自己带一个叶子类型，叶子类型里写清这条规则的判定标准。规则不能再写成一句话挂在提示里，每条规则必须有独立的类型，类型里有依据、检查方法与判定方式。示例：`root_background_changed` 与旧规则集里的 `readme_background_frozen` 是同一条规则，合并后只剩 `readme_background_frozen` 一个变体；它带的 `ReadmeBackgroundFrozen` 里写着冻结文本与逐字比对的检查方法。根 README 的 `Check` 返回本类型的违规清单，所以这篇有 public。

## public.viba

```bash public
import rules.types as rules
import rules.apis as rules_api

Violation = rules.Violation
CheckViolations = rules_api.CheckViolations
```

## types.viba

`Violation` 的每个变体对应一条规则，载荷是该规则自己的类型；每个叶子类型有四个字段：规则原文、依据、检查方法、判定方式。规则集把每条规则写成带载荷的变体。

```bash types
Violation =
  Oneof
  | $readme_background_frozen (ReadmeBackgroundFrozen * { README 需求背景冻结，新经验写进别的文档 })
  | $external_only_public (ExternalOnlyPublic * { 外部只依赖 public，types/apis 是内部实现 })
  | $five_sections (FiveSections * { 每篇必须有 需求背景/public/types/基本操作/apis 五段 })
  | $background_states_input_and_ops (BackgroundStatesInputAndOps * { 根需求背景写输入与操作类别，不写阅读顺序 })
  | $root_api_is_real_operation (RootApiIsRealOperation * { 根 api 必须是真操作，不是 Read/List })
  | $explicit_dependencies (ExplicitDependencies * { 大 api 依赖小 api 写成显式参数 })
  | $dependencies_after_hint (DependenciesAfterHint * { 依赖参数放在 HINT_BLOCK 之后 })
  | $dep_tag_and_api_type (DepTagAndApiType * { 依赖参数带 tag，类型写被依赖的 api })
  | $dep_hint_explains_service (DepHintExplainsService * { 依赖提示写交回什么、拿它做什么 })
  | $hint_folded (HintFolded * { 函数提示块一律折行 })
  | $orphan_is_unreachable (OrphanIsUnreachable * { 孤立=从根 public 不可达，不凭感觉 })
  | $delete_all_file_kinds (DeleteAllFileKinds * { 删除不分文件类型，同一可达性判据 })
  | $generated_follows_source (GeneratedFollowsSource * { 生成物跟源头走，删后重查冗余 })
  | $sum_with_payload (SumWithPayload * { 和类型是带载荷的原语，不是标签集合 })
  | $no_record_plus_kind (NoRecordPlusKind * { 禁止记录+kind 枚举 })
  | $variant_names_problem (VariantNamesProblem * { 变体名是情况/问题，不是话题 })
  | $type_name_says_content (TypeNameSaysContent * { 类型名说清内容（装违规叫 Violation） })
  | $polarity_consistent (PolarityConsistent * { 类型名与变体名正负一致 })
  | $tag_form_consistent (TagFormConsistent * { 变体标签形态统一：问题/术语/动作 })
  | $payload_form_consistent (PayloadFormConsistent * { 载荷类型名也要同形态 })
  | $name_triple_consistent (NameTripleConsistent * { 文件名/需求背景/public 三处一致 })
  | $public_covers_chain (PublicCoversChain * { public 必须覆盖需求全链路 })
  | $virtual_edge_before_delete (VirtualEdgeBeforeDelete * { 删前先查说明里提到但代码没引用 })
  | $fix_whole_class (FixWholeClass * { 点名一处要按同一判据改完整类 })
  | $rename_is_semantic (RenameIsSemantic * { 改名不是字符串替换，形态一起升级 })
  | $background_names_public (BackgroundNamesPublic * { 每篇背景收尾写根 README 从这里取什么 })
  | $inner_sum_for_failures (InnerSumForFailures * { 同一语义位置的失败收进内层和类型 })
  | $principle_into_kb (PrincipleIntoKb * { 用户讲清的原则必须落进知识库并附示例 })
  | $six_checks_per_round (SixChecksPerRound * { 每轮固定跑解析/加载/闭包/环/旧名/三者 })
  | $verified_before_done (VerifiedBeforeDone * { 没跑完验证不宣布完成、不推送 })
  | $graph_before_delete (GraphBeforeDelete * { 概念图先于删除，闭包只发现够不到 })
  | $hint_adds_information (HintAddsInformation * { 说明要有新信息：删掉信息量不减即废话 })
  | $violation_attribution (ViolationAttribution * { 违规要归因到原则+位置+内容 })
  | $rule_before_action (RuleBeforeAction * { 规则先于动作，先写判据再动手 })
  | $fixed_structure (FixedStructure * { 结构固定、入口唯一 })
  | $interface_answers_need (InterfaceAnswersNeed * { 接口要对得起输入与需求 })
  | $design_phase_spec_only (DesignPhaseSpecOnly * { 设计阶段只留规范，删除即检验 })
  | $pure_enum_allowed (PureEnumAllowed * { 纯字符串枚举只在确实无数据时允许 })
  | $define_new_words (DefineNewWords * { 自造词第一次出现必须当场解释 })
  | $scolding_is_requirement (ScoldingIsRequirement * { 训斥即需求：摘原话反推痛恨再成规则 })
  | $public_only_own_names (PublicOnlyOwnNames * { public 只导出本文档内部的 types 与 apis，不转发别的文档的名字 })
  | $text_reviewed_by_subagent (TextReviewedBySubagent * { 交付自然语言前起独立 subagent 审查：不得过分口语，尽量用标准术语，读起来不能拗口 })


ReadmeBackgroundFrozen =
  Object
  * $statement (str * { README 需求背景冻结，新经验写进别的文档 })
  * $evidence (str * { 原话：一定要冻结，不能改 })
  * $check (str * { 与冻结文本逐字比对 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
ExternalOnlyPublic =
  Object
  * $statement (str * { 外部只依赖 public，types/apis 是内部实现 })
  * $evidence (str * { 原话：外部只能依赖 public })
  * $check (str * { 跨文档 import 以 .public 结尾 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
FiveSections =
  Object
  * $statement (str * { 每篇必须有 需求背景/public/types/基本操作/apis 五段 })
  * $evidence (str * { 原话：必须有 public/types/apis 等章节 })
  * $check (str * { 抽 ## 章节比对 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
BackgroundStatesInputAndOps =
  Object
  * $statement (str * { 根需求背景写输入与操作类别，不写阅读顺序 })
  * $evidence (str * { 原话：总输入应是 repo_path；操作两类 })
  * $check (str * { 背景能抄出输入与操作 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
RootApiIsRealOperation =
  Object
  * $statement (str * { 根 api 必须是真操作，不是 Read/List })
  * $evidence (str * { 原话：对外 api 竟然只是 read })
  * $check (str * { 根 public 操作能独立执行并产出结果 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
ExplicitDependencies =
  Object
  * $statement (str * { 大 api 依赖小 api 写成显式参数 })
  * $evidence (str * { 原话：A <- B <- {...} <- FooBar })
  * $check (str * { 签名里有对应依赖参数 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
DependenciesAfterHint =
  Object
  * $statement (str * { 依赖参数放在 HINT_BLOCK 之后 })
  * $evidence (str * { 原话：小 api 要放到 HINT 之后 })
  * $check (str * { 提示块前的参数不含 _api. })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
DepTagAndApiType =
  Object
  * $statement (str * { 依赖参数带 tag，类型写被依赖的 api })
  * $evidence (str * { 原话：给 Measure 带个展位的 tag })
  * $check (str * { 匹配 <- $tag (X.Api * {...}) })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
DepHintExplainsService =
  Object
  * $statement (str * { 依赖提示写交回什么、拿它做什么 })
  * $evidence (str * { 原话：这一句话有点像废话 })
  * $check (str * { 提示含返回与用途，无“依赖 X：” })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
HintFolded =
  Object
  * $statement (str * { 函数提示块一律折行 })
  * $evidence (str * { 原话：无论长短都要折行 })
  * $check (str * { 正则 ^  <- \{ .+ \}$ })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
OrphanIsUnreachable =
  Object
  * $statement (str * { 孤立=从根 public 不可达，不凭感觉 })
  * $evidence (str * { 原话：只要没人使用就是孤立 })
  * $check (str * { 从根 public BFS 差集 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
DeleteAllFileKinds =
  Object
  * $statement (str * { 删除不分文件类型，同一可达性判据 })
  * $evidence (str * { 原话：不限于 python 文件 })
  * $check (str * { 每类文件回答谁依赖它 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
GeneratedFollowsSource =
  Object
  * $statement (str * { 生成物跟源头走，删后重查冗余 })
  * $evidence (str * { 原话：json_schema 重新生成了吗 })
  * $check (str * { 定义集合-函数=应有 schema })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
SumWithPayload =
  Object
  * $statement (str * { 和类型是带载荷的原语，不是标签集合 })
  * $evidence (str * { 原话：这个错大发了 })
  * $check (str * { 遍历 Oneof，看变体有无载荷 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
NoRecordPlusKind =
  Object
  * $statement (str * { 禁止记录+kind 枚举 })
  * $evidence (str * { 原话：替代继承/Oneof })
  * $check (str * { 搜 $kind + 纯字符串枚举 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
VariantNamesProblem =
  Object
  * $statement (str * { 变体名是情况/问题，不是话题 })
  * $evidence (str * { 原话：一个叫需求的 Rule })
  * $check (str * { 代入“这条报的是___” })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
TypeNameSaysContent =
  Object
  * $statement (str * { 类型名说清内容（装违规叫 Violation） })
  * $evidence (str * { 原话：这哪是 Lesson 啊 })
  * $check (str * { 读类型名与变体是否同类 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
PolarityConsistent =
  Object
  * $statement (str * { 类型名与变体名正负一致 })
  * $evidence (str * { 原话：否则要么都是负面的 })
  * $check (str * { 标 positive/negative 比对 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
TagFormConsistent =
  Object
  * $statement (str * { 变体标签形态统一：问题/术语/动作 })
  * $evidence (str * { 原话：inline_hint 只是名词 })
  * $check (str * { 逐标签归三类 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
PayloadFormConsistent =
  Object
  * $statement (str * { 载荷类型名也要同形态 })
  * $evidence (str * { 原话：不只是 tag })
  * $check (str * { 逐 <tag,payload> 比对 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
NameTripleConsistent =
  Object
  * $statement (str * { 文件名/需求背景/public 三处一致 })
  * $evidence (str * { 原话：信息量一定要一致 })
  * $check (str * { 文件名关键词∈背景；public=背景声明 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
PublicCoversChain =
  Object
  * $statement (str * { public 必须覆盖需求全链路 })
  * $evidence (str * { 原话：怎么构建一条样本 })
  * $check (str * { 需求操作逐个查可达 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
VirtualEdgeBeforeDelete =
  Object
  * $statement (str * { 删前先查说明里提到但代码没引用 })
  * $evidence (str * { 原话：想想概念之间的引用关系 })
  * $check (str * { mention vs reference 清单 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
FixWholeClass =
  Object
  * $statement (str * { 点名一处要按同一判据改完整类 })
  * $evidence (str * { 原话：不能我说一句你只做一句 })
  * $check (str * { 列同类命中并逐项勾销 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
RenameIsSemantic =
  Object
  * $statement (str * { 改名不是字符串替换，形态一起升级 })
  * $evidence (str * { 原话：就改了个名字 })
  * $check (str * { 改名后问形态/载荷/引用 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
BackgroundNamesPublic =
  Object
  * $statement (str * { 每篇背景收尾写根 README 从这里取什么 })
  * $evidence (str * { 九篇都补过这句 })
  * $check (str * { 背景清单=public 导出行 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
InnerSumForFailures =
  Object
  * $statement (str * { 同一语义位置的失败收进内层和类型 })
  * $evidence (str * { 点赞 Mismatch })
  * $check (str * { 外层变体数不变、内层增加 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
PrincipleIntoKb =
  Object
  * $statement (str * { 用户讲清的原则必须落进知识库并附示例 })
  * $evidence (str * { 原话：显然要写到 design-by-viba })
  * $check (str * { 知识库有篇讲它并带本次例子 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
SixChecksPerRound =
  Object
  * $statement (str * { 每轮固定跑解析/加载/闭包/环/旧名/三者 })
  * $evidence (str * { goal 要求反复审查 })
  * $check (str * { 贴六项数字 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
VerifiedBeforeDone =
  Object
  * $statement (str * { 没跑完验证不宣布完成、不推送 })
  * $evidence (str * { 原话：json_schema 重新生成了吗 })
  * $check (str * { 完成附命令与输出 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
GraphBeforeDelete =
  Object
  * $statement (str * { 概念图先于删除，闭包只发现够不到 })
  * $evidence (str * { SampleConfigBase 被误删 })
  * $check (str * { 删前查虚边再删 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
HintAddsInformation =
  Object
  * $statement (str * { 说明要有新信息：删掉信息量不减即废话 })
  * $evidence (str * { 原话：有点像废话 })
  * $check (str * { 删掉说明问信息量 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
ViolationAttribution =
  Object
  * $statement (str * { 违规要归因到原则+位置+内容 })
  * $evidence (str * { 原话：清晰指出违反原则 })
  * $check (str * { Violation 三要素 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
RuleBeforeAction =
  Object
  * $statement (str * { 规则先于动作，先写判据再动手 })
  * $evidence (str * { 先有规则才有后续删除 })
  * $check (str * { 动作前有可复核判据 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
FixedStructure =
  Object
  * $statement (str * { 结构固定、入口唯一 })
  * $evidence (str * { 五段+唯一根 })
  * $check (str * { 结构检查 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
InterfaceAnswersNeed =
  Object
  * $statement (str * { 接口要对得起输入与需求 })
  * $evidence (str * { Read 被否定 })
  * $check (str * { 接口对应输入与操作 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
DesignPhaseSpecOnly =
  Object
  * $statement (str * { 设计阶段只留规范，删除即检验 })
  * $evidence (str * { 删代码/生成物/样例 })
  * $check (str * { 可达性判据 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
PureEnumAllowed =
  Object
  * $statement (str * { 纯字符串枚举只在确实无数据时允许 })
  * $evidence (str * { Polarity/TagForm 未被骂 })
  * $check (str * { 检查变体是否本应有数据 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
DefineNewWords =
  Object
  * $statement (str * { 自造词第一次出现必须当场解释 })
  * $evidence (str * { AGENTS.md 禁词规定 })
  * $check (str * { 生僻词同段有定义 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
ScoldingIsRequirement =
  Object
  * $statement (str * { 训斥即需求：摘原话反推痛恨再成规则 })
  * $evidence (str * { 这句话本身也是经验 })
  * $check (str * { 复盘含原话与规则 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
PublicOnlyOwnNames =
  Object
  * $statement (str * { public 只导出本文档内部的 types 与 apis，不转发别的文档的名字 })
  * $evidence (str * { 这也是规则 })
  * $check (str * { 每个导出行的来源模块都属于本文档 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
TextReviewedBySubagent =
  Object
  * $statement (str * { 交付自然语言前起独立 subagent 审查：不得过分口语，尽量用标准术语，读起来不能拗口 })
  * $evidence (str * { 这条规则也是铁律 })
  * $check (str * { 交付前有审查记录，覆盖口语、术语、拗口 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
Finding =
  Object
  * $rule (Violation * { 违反的是哪一条规则 })
  * $where (Position * { 在哪个文件的哪一行、哪个名字 })
  * $evidence (str * { 查到的具体内容 })

Position =
  Object
  * $doc (str * { 文件路径 })
  * $line (int * { 行号 })
  * $name (str * { 名字或章节 })
```

## 基本操作

只有一个操作：按规则检查。给出仓库路径，逐条规则检查，交回违规清单；每条违规带上规则叶子类型与位置。

## apis.viba

```bash apis
import rules.types as rules

CheckViolations =
     list[rules.Finding]
  <- $repo (str * { 仓库路径：里面是一组 .viba.md 文档 })
  <- $rules (list[rules.Violation] * { 这次要执行的规则；从规则集里取 })
  <- {
    按规则检查：对每条规则执行它的 $check，不符合的记成一条 Finding，带上规则、位置与证据；返回违规清单
  }
```
