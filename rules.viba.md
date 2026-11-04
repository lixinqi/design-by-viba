# 规则集

## 需求背景

一条规则就是一个类型：规则集只保留一个和类型 `Rule`，它的每个变体就是一条规则，变体自己带一个叶子类型，叶子类型里写清这条规则的判定标准。规则被违反时，`CheckViolations` 交回 `Finding`（规则、位置、证据），而不是另造一个违规类型。规则不能再写成一句话挂在提示里，每条规则必须有独立的类型，类型里有依据、检查方法与判定方式。示例：旧规则集里叫 `root_background_changed` 的那条并进了 `readme_background_frozen`；它带的 `ReadmeBackgroundFrozen` 里写着冻结文本与逐字比对的检查方法。根 README 的 `Check` 依赖本篇的 `CheckViolations`，所以这篇有 public。

## public.viba

```bash public
import rules.types as rules
import rules.apis as rules_api

Finding = rules.Finding
CheckViolations = rules_api.CheckViolations
```

## types.viba

`Rule` 的每个变体对应一条规则，载荷是该规则自己的类型；每个叶子类型有四个字段：规则原文、依据、检查方法、判定方式。规则集把每条规则写成带载荷的变体。

```bash types
Rule =
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


  | $change_boundary (ChangeBoundary * { 只改任务范围内、且先声明范围的对象；越界先确认 })
  | $target_before_edit (TargetBeforeEdit * { 改之前确认目标文件唯一，改后核对 diff 没有动错 })
  | $function_scope (FunctionScope * { 函数只用它的参数与返回值表达语义，不替调用方保管知识 })
  | $third_person_readable (ThirdPersonReadable * { 术语首次出现给定义，不假设读者看过当前对话 })
  | $no_change_log (NoChangeLog * { 文档写现在是什么，变更写进提交信息 })
  | $section_matches_heading (SectionMatchesHeading * { 每节内容只回答本节标题 })
  | $docs_name_only_public (DocsNameOnlyPublic * { 文档只提 public 里的名字，不暴露内部 api })
  | $explain_hard_parts (ExplainHardParts * { 难点先铺垫，必要时附录，不假设读者自会 })
  | $public_api_general (PublicApiGeneral * { 对外 api 不耦合内部实现细节 })
  | $no_time_bound_content (NoTimeBoundContent * { 不写“今天”“本次”“当前对话”，只写适用条件 })
  | $small_functions (SmallFunctions * { 函数短，圈复杂度受控，短 if 也计入 })

  | $rule_has_examples (RuleHasExamples * { 每条规则必须有正例与反例 })

ReadmeBackgroundFrozen =
  Object
  * $statement (str * { README 需求背景冻结，新经验写进别的文档 })
  * $evidence (str * { 原话：一定要冻结，不能改 })
  * $check (str * { 与冻结文本逐字比对 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/ReadmeBackgroundFrozen/positive }
  * { 反例见 examples/ReadmeBackgroundFrozen/negative }

ExternalOnlyPublic =
  Object
  * $statement (str * { 外部只依赖 public，types/apis 是内部实现 })
  * $evidence (str * { 原话：外部只能依赖 public })
  * $check (str * { 跨文档 import 以 .public 结尾 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/ExternalOnlyPublic/positive }
  * { 反例见 examples/ExternalOnlyPublic/negative }

FiveSections =
  Object
  * $statement (str * { 每篇必须有 需求背景/public/types/基本操作/apis 五段 })
  * $evidence (str * { 原话：必须有 public/types/apis 等章节 })
  * $check (str * { 抽 ## 章节比对 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/FiveSections/positive }
  * { 反例见 examples/FiveSections/negative }

BackgroundStatesInputAndOps =
  Object
  * $statement (str * { 根需求背景写输入与操作类别，不写阅读顺序 })
  * $evidence (str * { 原话：总输入应是 repo_path；操作两类 })
  * $check (str * { 背景能抄出输入与操作 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/BackgroundStatesInputAndOps/positive }
  * { 反例见 examples/BackgroundStatesInputAndOps/negative }

RootApiIsRealOperation =
  Object
  * $statement (str * { 根 api 必须是真操作，不是 Read/List })
  * $evidence (str * { 原话：对外 api 竟然只是 read })
  * $check (str * { 根 public 操作能独立执行并产出结果 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/RootApiIsRealOperation/positive }
  * { 反例见 examples/RootApiIsRealOperation/negative }

ExplicitDependencies =
  Object
  * $statement (str * { 大 api 依赖小 api 写成显式参数 })
  * $evidence (str * { 原话：A <- B <- {...} <- FooBar })
  * $check (str * { 签名里有对应依赖参数 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/ExplicitDependencies/positive }
  * { 反例见 examples/ExplicitDependencies/negative }

DependenciesAfterHint =
  Object
  * $statement (str * { 依赖参数放在 HINT_BLOCK 之后 })
  * $evidence (str * { 原话：小 api 要放到 HINT 之后 })
  * $check (str * { 提示块前的参数不含 _api. })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/DependenciesAfterHint/positive }
  * { 反例见 examples/DependenciesAfterHint/negative }

DepTagAndApiType =
  Object
  * $statement (str * { 依赖参数带 tag，类型写被依赖的 api })
  * $evidence (str * { 原话：给 Measure 带个展位的 tag })
  * $check (str * { 匹配 <- $tag (X.Api * {...}) })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/DepTagAndApiType/positive }
  * { 反例见 examples/DepTagAndApiType/negative }

DepHintExplainsService =
  Object
  * $statement (str * { 依赖提示写交回什么、拿它做什么 })
  * $evidence (str * { 原话：这一句话有点像废话 })
  * $check (str * { 提示含返回与用途，无“依赖 X：” })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/DepHintExplainsService/positive }
  * { 反例见 examples/DepHintExplainsService/negative }

HintFolded =
  Object
  * $statement (str * { 函数提示块一律折行 })
  * $evidence (str * { 原话：无论长短都要折行 })
  * $check (str * { 正则 ^  <- \{ .+ \}$ })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/HintFolded/positive }
  * { 反例见 examples/HintFolded/negative }

OrphanIsUnreachable =
  Object
  * $statement (str * { 孤立=从根 public 不可达，不凭感觉 })
  * $evidence (str * { 原话：只要没人使用就是孤立 })
  * $check (str * { 从根 public BFS 差集 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/OrphanIsUnreachable/positive }
  * { 反例见 examples/OrphanIsUnreachable/negative }

DeleteAllFileKinds =
  Object
  * $statement (str * { 删除不分文件类型，同一可达性判据 })
  * $evidence (str * { 原话：不限于 python 文件 })
  * $check (str * { 每类文件回答谁依赖它 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/DeleteAllFileKinds/positive }
  * { 反例见 examples/DeleteAllFileKinds/negative }

GeneratedFollowsSource =
  Object
  * $statement (str * { 生成物跟源头走，删后重查冗余 })
  * $evidence (str * { 原话：json_schema 重新生成了吗 })
  * $check (str * { 定义集合-函数=应有 schema })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/GeneratedFollowsSource/positive }
  * { 反例见 examples/GeneratedFollowsSource/negative }

SumWithPayload =
  Object
  * $statement (str * { 和类型是带载荷的原语，不是标签集合 })
  * $evidence (str * { 原话：这个错大发了 })
  * $check (str * { 遍历 Oneof，看变体有无载荷 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/SumWithPayload/positive }
  * { 反例见 examples/SumWithPayload/negative }

NoRecordPlusKind =
  Object
  * $statement (str * { 禁止记录+kind 枚举 })
  * $evidence (str * { 原话：替代继承/Oneof })
  * $check (str * { 搜 $kind + 纯字符串枚举 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/NoRecordPlusKind/positive }
  * { 反例见 examples/NoRecordPlusKind/negative }

VariantNamesProblem =
  Object
  * $statement (str * { 变体名是情况/问题，不是话题 })
  * $evidence (str * { 原话：一个叫需求的 Rule })
  * $check (str * { 代入“这条报的是___” })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/VariantNamesProblem/positive }
  * { 反例见 examples/VariantNamesProblem/negative }

TypeNameSaysContent =
  Object
  * $statement (str * { 类型名说清内容（装违规叫 Violation） })
  * $evidence (str * { 原话：这哪是 Lesson 啊 })
  * $check (str * { 读类型名与变体是否同类 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/TypeNameSaysContent/positive }
  * { 反例见 examples/TypeNameSaysContent/negative }

PolarityConsistent =
  Object
  * $statement (str * { 类型名与变体名正负一致 })
  * $evidence (str * { 原话：否则要么都是负面的 })
  * $check (str * { 标 positive/negative 比对 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/PolarityConsistent/positive }
  * { 反例见 examples/PolarityConsistent/negative }

TagFormConsistent =
  Object
  * $statement (str * { 变体标签形态统一：问题/术语/动作 })
  * $evidence (str * { 原话：inline_hint 只是名词 })
  * $check (str * { 逐标签归三类 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/TagFormConsistent/positive }
  * { 反例见 examples/TagFormConsistent/negative }

PayloadFormConsistent =
  Object
  * $statement (str * { 载荷类型名也要同形态 })
  * $evidence (str * { 原话：不只是 tag })
  * $check (str * { 逐 <tag,payload> 比对 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/PayloadFormConsistent/positive }
  * { 反例见 examples/PayloadFormConsistent/negative }

NameTripleConsistent =
  Object
  * $statement (str * { 文件名/需求背景/public 三处一致 })
  * $evidence (str * { 原话：信息量一定要一致 })
  * $check (str * { 文件名关键词∈背景；public=背景声明 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/NameTripleConsistent/positive }
  * { 反例见 examples/NameTripleConsistent/negative }

PublicCoversChain =
  Object
  * $statement (str * { public 必须覆盖需求全链路 })
  * $evidence (str * { 原话：怎么构建一条样本 })
  * $check (str * { 需求操作逐个查可达 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/PublicCoversChain/positive }
  * { 反例见 examples/PublicCoversChain/negative }

VirtualEdgeBeforeDelete =
  Object
  * $statement (str * { 删前先查说明里提到但代码没引用 })
  * $evidence (str * { 原话：想想概念之间的引用关系 })
  * $check (str * { mention vs reference 清单 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/VirtualEdgeBeforeDelete/positive }
  * { 反例见 examples/VirtualEdgeBeforeDelete/negative }

FixWholeClass =
  Object
  * $statement (str * { 点名一处要按同一判据改完整类 })
  * $evidence (str * { 原话：不能我说一句你只做一句 })
  * $check (str * { 列同类命中并逐项勾销 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/FixWholeClass/positive }
  * { 反例见 examples/FixWholeClass/negative }

RenameIsSemantic =
  Object
  * $statement (str * { 改名不是字符串替换，形态一起升级 })
  * $evidence (str * { 原话：就改了个名字 })
  * $check (str * { 改名后问形态/载荷/引用 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/RenameIsSemantic/positive }
  * { 反例见 examples/RenameIsSemantic/negative }

BackgroundNamesPublic =
  Object
  * $statement (str * { 每篇背景收尾写根 README 从这里取什么 })
  * $evidence (str * { 九篇都补过这句 })
  * $check (str * { 背景清单=public 导出行 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/BackgroundNamesPublic/positive }
  * { 反例见 examples/BackgroundNamesPublic/negative }

InnerSumForFailures =
  Object
  * $statement (str * { 同一语义位置的失败收进内层和类型 })
  * $evidence (str * { 点赞 Mismatch })
  * $check (str * { 外层变体数不变、内层增加 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/InnerSumForFailures/positive }
  * { 反例见 examples/InnerSumForFailures/negative }

PrincipleIntoKb =
  Object
  * $statement (str * { 用户讲清的原则必须落进知识库并附示例 })
  * $evidence (str * { 原话：显然要写到 design-by-viba })
  * $check (str * { 知识库有篇讲它并带本次例子 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/PrincipleIntoKb/positive }
  * { 反例见 examples/PrincipleIntoKb/negative }

SixChecksPerRound =
  Object
  * $statement (str * { 每轮固定跑解析/加载/闭包/环/旧名/三者 })
  * $evidence (str * { goal 要求反复审查 })
  * $check (str * { 贴六项数字 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/SixChecksPerRound/positive }
  * { 反例见 examples/SixChecksPerRound/negative }

VerifiedBeforeDone =
  Object
  * $statement (str * { 没跑完验证不宣布完成、不推送 })
  * $evidence (str * { 原话：json_schema 重新生成了吗 })
  * $check (str * { 完成附命令与输出 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/VerifiedBeforeDone/positive }
  * { 反例见 examples/VerifiedBeforeDone/negative }

GraphBeforeDelete =
  Object
  * $statement (str * { 概念图先于删除，闭包只发现够不到 })
  * $evidence (str * { SampleConfigBase 被误删 })
  * $check (str * { 删前查虚边再删 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/GraphBeforeDelete/positive }
  * { 反例见 examples/GraphBeforeDelete/negative }

HintAddsInformation =
  Object
  * $statement (str * { 说明要有新信息：删掉信息量不减即废话 })
  * $evidence (str * { 原话：有点像废话 })
  * $check (str * { 删掉说明问信息量 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/HintAddsInformation/positive }
  * { 反例见 examples/HintAddsInformation/negative }

ViolationAttribution =
  Object
  * $statement (str * { 违规要归因到原则+位置+内容 })
  * $evidence (str * { 原话：清晰指出违反原则 })
  * $check (str * { 违规要归因到规则、位置与内容 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/ViolationAttribution/positive }
  * { 反例见 examples/ViolationAttribution/negative }

RuleBeforeAction =
  Object
  * $statement (str * { 规则先于动作，先写判据再动手 })
  * $evidence (str * { 先有规则才有后续删除 })
  * $check (str * { 动作前有可复核判据 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/RuleBeforeAction/positive }
  * { 反例见 examples/RuleBeforeAction/negative }

FixedStructure =
  Object
  * $statement (str * { 结构固定、入口唯一 })
  * $evidence (str * { 五段+唯一根 })
  * $check (str * { 结构检查 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/FixedStructure/positive }
  * { 反例见 examples/FixedStructure/negative }

InterfaceAnswersNeed =
  Object
  * $statement (str * { 接口要对得起输入与需求 })
  * $evidence (str * { Read 被否定 })
  * $check (str * { 接口对应输入与操作 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/InterfaceAnswersNeed/positive }
  * { 反例见 examples/InterfaceAnswersNeed/negative }

DesignPhaseSpecOnly =
  Object
  * $statement (str * { 设计阶段只留规范，删除即检验 })
  * $evidence (str * { 删代码/生成物/样例 })
  * $check (str * { 可达性判据 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/DesignPhaseSpecOnly/positive }
  * { 反例见 examples/DesignPhaseSpecOnly/negative }

PureEnumAllowed =
  Object
  * $statement (str * { 纯字符串枚举只在确实无数据时允许 })
  * $evidence (str * { 没有数据的取值没有被纠正过 })
  * $check (str * { 检查变体是否本应有数据 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/PureEnumAllowed/positive }
  * { 反例见 examples/PureEnumAllowed/negative }

DefineNewWords =
  Object
  * $statement (str * { 自造词第一次出现必须当场解释 })
  * $evidence (str * { AGENTS.md 禁词规定 })
  * $check (str * { 生僻词同段有定义 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/DefineNewWords/positive }
  * { 反例见 examples/DefineNewWords/negative }

ScoldingIsRequirement =
  Object
  * $statement (str * { 训斥即需求：摘原话反推痛恨再成规则 })
  * $evidence (str * { 这句话本身也是经验 })
  * $check (str * { 复盘含原话与规则 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/ScoldingIsRequirement/positive }
  * { 反例见 examples/ScoldingIsRequirement/negative }

PublicOnlyOwnNames =
  Object
  * $statement (str * { public 只导出本文档内部的 types 与 apis，不转发别的文档的名字 })
  * $evidence (str * { 这也是规则 })
  * $check (str * { 每个导出行的来源模块都属于本文档 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/PublicOnlyOwnNames/positive }
  * { 反例见 examples/PublicOnlyOwnNames/negative }

TextReviewedBySubagent =
  Object
  * $statement (str * { 交付自然语言前起独立 subagent 审查：不得过分口语，尽量用标准术语，读起来不能拗口 })
  * $evidence (str * { 这条规则也是铁律 })
  * $check (str * { 交付前有审查记录，覆盖口语、术语、拗口 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/TextReviewedBySubagent/positive }
  * { 反例见 examples/TextReviewedBySubagent/negative }


ChangeBoundary =
  Object
  * $statement (str * { 只改任务范围内、且先声明范围的对象；越界先确认 })
  * $evidence (str * { 三方评审一致：没有边界感与超出任务范围同源 })
  * $check (str * { 对照任务范围与改动清单，越界项未获确认即违规 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/ChangeBoundary/positive }
  * { 反例见 examples/ChangeBoundary/negative }

TargetBeforeEdit =
  Object
  * $statement (str * { 改之前确认目标文件唯一，改后核对 diff 没有动错 })
  * $evidence (str * { 改错文件不会被任何现有检查发现 })
  * $check (str * { 改前列出目标路径并确认唯一，改后 diff 逐文件核对 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/TargetBeforeEdit/positive }
  * { 反例见 examples/TargetBeforeEdit/negative }

FunctionScope =
  Object
  * $statement (str * { 函数只用它的参数与返回值表达语义，不替调用方保管知识 })
  * $evidence (str * { 依赖规则只约束调用写法，不约束函数掌握的知识 })
  * $check (str * { 检查函数体是否使用了参数与返回值之外的状态或约定 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/FunctionScope/positive }
  * { 反例见 examples/FunctionScope/negative }

ThirdPersonReadable =
  Object
  * $statement (str * { 术语首次出现给定义，不假设读者看过当前对话 })
  * $evidence (str * { 自造词规则只管生词，不管对读者的假设 })
  * $check (str * { 把文档交给未参与对话的读者，术语与指代必须能读懂 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/ThirdPersonReadable/positive }
  * { 反例见 examples/ThirdPersonReadable/negative }

NoChangeLog =
  Object
  * $statement (str * { 文档写现在是什么，变更写进提交信息 })
  * $evidence (str * { 说明信息量规则管不到整篇写成变更史 })
  * $check (str * { 搜索“本次”“改为”“新增”这类变更叙述，出现在正文即违规 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/NoChangeLog/positive }
  * { 反例见 examples/NoChangeLog/negative }

SectionMatchesHeading =
  Object
  * $statement (str * { 每节内容只回答本节标题 })
  * $evidence (str * { 结构规则只查章节名与顺序，不查内容是否对题 })
  * $check (str * { 逐节读首句与末句，是否在回答本节标题 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/SectionMatchesHeading/positive }
  * { 反例见 examples/SectionMatchesHeading/negative }

DocsNameOnlyPublic =
  Object
  * $statement (str * { 文档只提 public 里的名字，不暴露内部 api })
  * $evidence (str * { 外部只依赖 public 管 import，管不到正文提到内部 api })
  * $check (str * { 扫描文档正文中出现的名字，是否都能在目标文档的 public 找到 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/DocsNameOnlyPublic/positive }
  * { 反例见 examples/DocsNameOnlyPublic/negative }

ExplainHardParts =
  Object
  * $statement (str * { 难点先铺垫，必要时附录，不假设读者自会 })
  * $evidence (str * { 现有规则没有铺垫或附录的要求 })
  * $check (str * { 找出首次出现的新概念，检查前文是否给出定义或例子 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/ExplainHardParts/positive }
  * { 反例见 examples/ExplainHardParts/negative }

PublicApiGeneral =
  Object
  * $statement (str * { 对外 api 不耦合内部实现细节 })
  * $evidence (str * { 接口对得起需求只管方向，不管是否耦合内部 })
  * $check (str * { 检查 public api 的参数与返回是否引用了内部类型或内部约定 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/PublicApiGeneral/positive }
  * { 反例见 examples/PublicApiGeneral/negative }

NoTimeBoundContent =
  Object
  * $statement (str * { 不写“今天”“本次”“当前对话”，只写适用条件 })
  * $evidence (str * { 现有条款不管与时刻、受众耦合的内容 })
  * $check (str * { 搜索时间词与对话指代，命中即改为适用条件 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/NoTimeBoundContent/positive }
  * { 反例见 examples/NoTimeBoundContent/negative }

SmallFunctions =
  Object
  * $statement (str * { 函数短，圈复杂度受控，短 if 也计入 })
  * $evidence (str * { 规则集没有函数长度与圈复杂度的约束 })
  * $check (str * { 统计分支数与行数，超过阈值即违规 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/SmallFunctions/positive }
  * { 反例见 examples/SmallFunctions/negative }

RuleHasExamples =
  Object
  * $statement (str * { 每条规则必须有正例与反例 })
  * $evidence (str * { 规则要有明确示例，这也是规则 })
  * $check (str * { 检查每个规则类型是否带正例与反例的路径 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/RuleHasExamples/positive }
  * { 反例见 examples/RuleHasExamples/negative }

Finding =
  Object
  * $rule (Rule * { 违反的是哪一条规则 })
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
  <- $rules (list[rules.Rule] * { 这次要执行的规则；从规则集里取 })
  <- {
    按规则检查：对每条规则执行它的 $check，不符合的记成一条 Finding，带上规则、位置与证据；返回违规清单
  }
```
