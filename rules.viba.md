# 规则集

## 需求背景

一条规则就是一个类型：规则集只保留一个和类型 `Rule`，它的每个变体就是一条规则，变体自己带一个叶子类型，叶子类型里写清这条规则的判定标准。规则被违反时，`CheckViolations` 交回 `Finding`（规则、位置、证据），而不是另造一个违规类型。规则不能再写成一句话挂在提示里，每条规则必须有独立的类型，类型里有依据、检查方法与判定方式。规则由谁判也落在结构上：每个叶子类型带一个 `tagged[__type__, Object]` 成员，用定义自己的名字做 tag，判定表才能按结构认出是哪一条规则；没有这个 tag，五十五个叶子就是同一个类型。谁判一条规则由 `must_judged_by_agent[规则类型]` 回答：默认 true，交给 agent 判；`$check` 能落到结构上的规则在 `must_judged_by_agent_impl` 里列成 false，由程序判。示例：旧规则集里叫 `root_background_changed` 的那条并进了 `readme_background_frozen`；它带的 `ReadmeBackgroundFrozen` 里写着冻结文本与逐字比对的检查方法。根 README 的 `Check` 依赖本篇的 `CheckViolations`，所以这篇有 public。

## public.viba

```viba public
import rules.types as rules
import rules.apis as rules_api

Finding = rules.Finding
CheckViolations = rules_api.CheckViolations
```

## types.viba

`Rule` 的每个变体对应一条规则，变体后面是这条规则自己的类型；每个叶子类型有四个字段：规则原文、依据、检查方法、判定方式。规则集把每条规则写成一个变体，变体后面跟着这条规则的类型。叶子都带一个 `tagged[__type__, Object]` 成员：tag 是这条规则自己的名字，判定表按它认规则。

```viba types
Rule =
  Oneof
  | $readme_background_frozen (ReadmeBackgroundFrozen * { 根 README 的需求背景一旦定稿就冻结，新的经验写进别的文档；冻结时的文本记在 requirement.viba.md 的 FrozenRootBackground 里，当前正文必须与它逐字一致，不一致就报违规。 })
  | $external_only_public (ExternalOnlyPublic * { 一篇文档要用另一篇文档的名字，只能 import 对方的 public；跨文档 import 的模块名必须以 .public 结尾，直接 import types 或 apis 就报违规。模块文档与泛型目录没有 public，不查。 })
  | $five_sections (FiveSections * { 每篇设计文档必须有 需求背景、public.viba、types.viba、基本操作、apis.viba 五段，顺序固定；多出来的节放在末尾 })
  | $background_states_input_and_ops (BackgroundStatesInputAndOps * { 根 README 的需求背景要写清输入是什么、操作分几类，不写“先读哪篇、后读哪篇”的阅读顺序；读者只读背景就能写出输入与操作。 })
  | $root_api_is_real_operation (RootApiIsRealOperation * { 根 README 的 public 导出的必须是能独立执行、交回结果的操作，不能只是 Read、List 这类读文件或列目录的名字；每个根操作都要能独立跑完并交回结果。 })
  | $explicit_dependencies (ExplicitDependencies * { 一个操作要调用另一个操作时，依赖必须写成签名里的参数；只在提示块里说“用它”不算，调用方从签名上看不出这条依赖。 })
  | $dependencies_after_hint (DependenciesAfterHint * { 函数签名里，提示块之前只放输入参数；依赖另一个操作而传进来的参数要放在提示块之后。提示块之前出现依赖参数就报违规。 })
  | $dep_tag_and_api_type (DepTagAndApiType * { 依赖参数要有自己的 tag，类型写成被依赖文档 public 里的操作名；写成字符串或内部类型就报违规，调用方看不出依赖的是哪个操作。 })
  | $dep_hint_explains_service (DepHintExplainsService * { 依赖参数的提示要写清这个操作交回什么、拿它做什么，不能只写“依赖 X：”再重复一遍名字。 })
  | $hint_folded (HintFolded * { 函数的提示块一律折行：起始标记、提示内容、结束标记各占一行，再短的提示也不写成一行。 })
  | $orphan_is_unreachable (OrphanIsUnreachable * { 孤立不是“看起来没人用”，而是从根 README 的 public 出发、沿字段类型与参数类型走不到的定义；只在说明文字里被提到，不算走到。 })
  | $delete_all_file_kinds (DeleteAllFileKinds * { 删除时不看文件类型：文档、生成物、脚本、数据都用同一条判据——从根 README 的 public 出发走不走得到；只按 .viba.md 一种文件判就报违规。 })
  | $generated_follows_source (GeneratedFollowsSource * { 生成物必须跟源头一致：对象定义改了要重新生成 schema，字段集合与生成物对不上就报违规；删改之后还要重查有没有多余的生成物。 })
  | $variant_carries_type (VariantCarriesType * { 和类型的每个变体后面都要跟一个类型，把这一种情况的数据带上；只写标签、或标签后面跟空括号，都算没有类型。 })
  | $no_record_plus_kind (NoRecordPlusKind * { 不要用一个记录加一个 $kind 字段来表示状态；状态要写成和类型，每种情况一个变体，各带自己的数据。 })
  | $variant_names_problem (VariantNamesProblem * { 变体名要写这一种情况或这个问题，不是写话题；把它填进“这条报的是___”要读得通。 })
  | $type_name_says_content (TypeNameSaysContent * { 类型名要说清里面装的是什么：装违规的类型叫 Violation，不叫 Lesson；名字与内容对不上，读的人猜不到它的用途。 })
  | $polarity_consistent (PolarityConsistent * { 类型名与变体名的正负要一致：类型名是正面说法，变体名也得是正面说法；否则两者一起改用负面说法，不能一正一负。 })
  | $tag_form_consistent (TagFormConsistent * { 同一个和类型里的标签形态要统一：要么全是对问题的描述，要么全是术语名词，要么全是动作动词，不能混着写。 })
  | $variant_type_form_consistent (VariantTypeFormConsistent * { 变体标签后面的类型名，要和标签同一个形态：标签是术语，类型名也是术语；标签是问题描述，类型名也得是问题描述。 })
  | $name_triple_consistent (NameTripleConsistent * { 文件名、需求背景、public 三处要说同一件事，信息量一致：文件名的关键词出现在需求背景里，public 的导出行与背景声明的操作对得上。 })
  | $public_covers_chain (PublicCoversChain * { public 必须覆盖需求的全链路：需求背景里点到的每个操作，都要能从根 README 的 public 出发走到；留在内部 apis 里没导出，就报违规。 })
  | $virtual_edge_before_delete (VirtualEdgeBeforeDelete * { 删一个名字之前，先查说明文字里有没有提到它：真引用（字段类型或参数类型里出现，闭包走得到）与提及（只在说明里出现）要分开列；只有提及的名字也要补成真引用或保留，不能直接删。 })
  | $fix_whole_class (FixWholeClass * { 用户点出一处问题时，要按同一条判据把整类问题都找出来：先列出所有同类命中，再逐项改完，不能只改被点到的那一处。 })
  | $rename_is_semantic (RenameIsSemantic * { 改名不是字符串替换：旧名字对应的类型名、提示文字与所有引用要一起升级，改成新名字该有的说法；只替换名字、其余照旧就报违规。 })
  | $background_names_public (BackgroundNamesPublic * { 每篇文档的需求背景收尾要写清：根 README 从这里取哪些名字；这句话要与本文档 public 的导出行对得上，对不上就报违规。 })
  | $inner_sum_for_failures (InnerSumForFailures * { 同一个语义位置的多种失败，要收进内层的和类型里：外层和类型的变体数不变，内层按失败的种类增加，不要把所有失败平铺在外层。 })
  | $principle_into_kb (PrincipleIntoKb * { 用户讲清的一条原则，必须落进知识库，不能只留在对话里：写成一条规则类型，写清原文、依据、检查方法，并附正例与反例。 })
  | $six_checks_per_round (SixChecksPerRound * { 每一轮固定跑六项检查：解析、加载、闭包、环、旧名，以及文件名、需求背景、public 三者一致；报告里要贴出这六项的数字，不能只说“检查过了”。 })
  | $verified_before_done (VerifiedBeforeDone * { 验证没跑完，不宣布完成、不推送；宣布完成时要附上跑过的命令与输出，让别人能复核。 })
  | $graph_before_delete (GraphBeforeDelete * { 删之前先把概念图画出来：闭包只告诉你哪些名字够不到，不告诉你该不该删；还要查说明文字里的提及，确认没有漏掉的引用再删。 })
  | $hint_adds_information (HintAddsInformation * { 说明要有新信息：把它删掉，读者得到的信息不能减少；删掉也不缺什么，这句话就是废话。 })
  | $violation_attribution (ViolationAttribution * { 每条违规都要能归因到三样：违反的是哪条规则、在哪个文件的哪一行、证据原文是什么；缺一样就报违规。 })
  | $rule_before_action (RuleBeforeAction * { 规则先于动作：动手之前先把可复核的判据写下来，再按判据做事；判据没有写进规则文档，就报违规。 })
  | $fixed_structure (FixedStructure * { 结构固定、入口唯一：根 README 是唯一的入口，每篇设计文档的五节顺序固定，不能多出第二个入口。 })
  | $interface_answers_need (InterfaceAnswersNeed * { 接口要对得起输入与需求：参数要对应需求背景写的输入，返回值要交回需求要的结果；交回文件路径这类答非所问的结果，就报违规。 })
  | $design_phase_spec_only (DesignPhaseSpecOnly * { 设计阶段只留规范：实现代码、生成的 schema、样例数据都按同一条可达性判据删掉；从根 README 的 public 出发走不到的文件留在仓库里，就报违规。 })
  | $pure_enum_allowed (PureEnumAllowed * { 纯字符串枚举只允许用在确实没有数据的取值上；这个取值本来要带失败原因、数量这类数据，却只写成标签，就报违规。 })
  | $define_new_words (DefineNewWords * { 自造词或生僻词第一次出现时，要在同一段里当场解释它指什么；不解释就直接用，读者读不懂，就报违规。 })
  | $scolding_is_requirement (ScoldingIsRequirement * { 用户训斥的话也是需求：把原话逐字摘进规则的依据里，从原话反推出规则，单独成一条，不能只记一句转述。 })
  | $public_only_own_names (PublicOnlyOwnNames * { public 只导出本文档 types 与 apis 里的名字：每个导出行只能来自本文档的模块，把别的文档的名字转发出来，就报违规。 })
  | $text_reviewed_by_subagent (TextReviewedBySubagent * { 交付自然语言之前，要起一个独立的 subagent 审查文字：不得过分口语，尽量用标准术语，读起来不能拗口；审查者、发现与判定要留下记录。 })


  | $change_boundary (ChangeBoundary * { 只改任务范围内、并且事先声明过范围的对象：先对照任务范围与改动清单，越界的改动要先确认；没有确认的越界项就算违规。 })
  | $target_before_edit (TargetBeforeEdit * { 改之前先确认目标文件唯一：有同名文件就列全路径；改完再逐文件核对 diff，看有没有动错。 })
  | $function_scope (FunctionScope * { 函数只用它的参数与返回值表达语义，不替调用方保管知识：不读参数与返回值之外的状态，也不让调用方传入它本可以自己判断的约定，例如“是不是最后一项”。 })
  | $third_person_readable (ThirdPersonReadable * { 文档要写给没看过这段对话的人：术语第一次出现就给定义，“上一轮”“刚才”这类指代要换成具体定义，不能假设读者知道上下文。 })
  | $no_change_log (NoChangeLog * { 文档只写现在是什么，变更写进提交信息：正文出现“本次”“改为”“新增”这类变更叙述，就报违规。 })
  | $section_matches_heading (SectionMatchesHeading * { 每一节只回答本节标题问的事：基本操作列步骤，types 写字段，限制说明各归其位，不塞进别的节。 })
  | $section_detail_consistent (SectionDetailConsistent * { 同一篇文档里各章节的详略要一致：不能一节一句话带过，另一节讲到实现细节；差得太远的章节要报出来。 })
  | $docs_name_only_public (DocsNameOnlyPublic * { 文档正文只提对方 public 里的名字，不暴露内部 api：正文提到内部 api 就报违规，读者会以为那是可用的接口。 })
  | $explain_hard_parts (ExplainHardParts * { 难点要先铺垫：首次出现的新概念先给定义或例子，读不懂的推导放进附录，不假设读者自己会。 })
  | $public_api_general (PublicApiGeneral * { 对外 api 不耦合内部实现细节：参数与返回值不引用内部类型，也不要求调用方知道内部的存储布局或约定。 })
  | $no_time_bound_content (NoTimeBoundContent * { 文档不写“今天”“本次”“当前对话”这类与时刻或对话绑定的内容，只写适用条件；命中时间词或对话指代就报违规。 })
  | $small_functions (SmallFunctions * { 函数要短，圈复杂度受控，短的 if 也计入分支数；分支多、行数长的函数要报出来。 })

  | $rule_has_examples (RuleHasExamples * { 每条规则都要有正例与反例：规则类型末尾两行提示各给一条路径，路径指向真实存在的示例仓库，缺一条就报违规。 })

ReadmeBackgroundFrozen =
    tagged[__type__, Object]
  * $statement (str * { 根 README 的需求背景一旦定稿就冻结，新的经验写进别的文档；冻结时的文本记在 requirement.viba.md 的 FrozenRootBackground 里，当前正文必须与它逐字一致，不一致就报违规。 })
  * $evidence (str * { 原话：一定要冻结，不能改 })
  * $check (str * { 读 `README.viba.md` 需求背景的正文，与 `requirement.viba.md` 里 `FrozenRootBackground` 的冻结文本逐字比对；不一致即违规。 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/ReadmeBackgroundFrozen/positive }
  * { 反例见 examples/ReadmeBackgroundFrozen/negative }

ExternalOnlyPublic =
    tagged[__type__, Object]
  * $statement (str * { 一篇文档要用另一篇文档的名字，只能 import 对方的 public；跨文档 import 的模块名必须以 .public 结尾，直接 import types 或 apis 就报违规。模块文档与泛型目录没有 public，不查。 })
  * $evidence (str * { 原话：外部只能依赖 public })
  * $check (str * { 读每篇设计文档代码块里的 `import` 行；目标模块不属于本文档时，模块名必须以 `.public` 结尾，否则违规；模块文档与泛型目录不查。 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/ExternalOnlyPublic/positive }
  * { 反例见 examples/ExternalOnlyPublic/negative }

FiveSections =
    tagged[__type__, Object]
  * $statement (str * { 每篇设计文档必须有 需求背景、public.viba、types.viba、基本操作、apis.viba 五段，顺序固定；多出来的节放在末尾 })
  * $evidence (str * { 原话：必须有 public/types/apis 等章节 })
  * $check (str * { 读每篇设计文档的 `##` 章节名，按 需求背景、public.viba、types.viba、基本操作、apis.viba 的顺序逐项比对；少一节或顺序不同即违规；多出来的节只许放在末尾，放在五段中间也违规；模块文档不查 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/FiveSections/positive }
  * { 反例见 examples/FiveSections/negative }

BackgroundStatesInputAndOps =
    tagged[__type__, Object]
  * $statement (str * { 根 README 的需求背景要写清输入是什么、操作分几类，不写“先读哪篇、后读哪篇”的阅读顺序；读者只读背景就能写出输入与操作。 })
  * $evidence (str * { 原话：总输入应是 repo_path；操作两类 })
  * $check (str * { 背景能抄出输入与操作 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/BackgroundStatesInputAndOps/positive }
  * { 反例见 examples/BackgroundStatesInputAndOps/negative }

RootApiIsRealOperation =
    tagged[__type__, Object]
  * $statement (str * { 根 README 的 public 导出的必须是能独立执行、交回结果的操作，不能只是 Read、List 这类读文件或列目录的名字；每个根操作都要能独立跑完并交回结果。 })
  * $evidence (str * { 原话：对外 api 竟然只是 read })
  * $check (str * { 根 public 操作能独立执行并产出结果 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/RootApiIsRealOperation/positive }
  * { 反例见 examples/RootApiIsRealOperation/negative }

ExplicitDependencies =
    tagged[__type__, Object]
  * $statement (str * { 一个操作要调用另一个操作时，依赖必须写成签名里的参数；只在提示块里说“用它”不算，调用方从签名上看不出这条依赖。 })
  * $evidence (str * { 原话：A <- B <- {...} <- FooBar })
  * $check (str * { 签名里有对应依赖参数 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/ExplicitDependencies/positive }
  * { 反例见 examples/ExplicitDependencies/negative }

DependenciesAfterHint =
    tagged[__type__, Object]
  * $statement (str * { 函数签名里，提示块之前只放输入参数；依赖另一个操作而传进来的参数要放在提示块之后。提示块之前出现依赖参数就报违规。 })
  * $evidence (str * { 原话：小 api 要放到 HINT 之后 })
  * $check (str * { 读每个函数定义的参数顺序：提示块 `<- { ... }` 之前只能是输入参数，之后才允许依赖参数（类型来自另一篇文档的操作）；提示块之前出现依赖参数即违规。 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/DependenciesAfterHint/positive }
  * { 反例见 examples/DependenciesAfterHint/negative }

DepTagAndApiType =
    tagged[__type__, Object]
  * $statement (str * { 依赖参数要有自己的 tag，类型写成被依赖文档 public 里的操作名；写成字符串或内部类型就报违规，调用方看不出依赖的是哪个操作。 })
  * $evidence (str * { 原话：给 Measure 带个展位的 tag })
  * $check (str * { 读每个依赖参数：必须写成 `<- $tag (X.Op * { 提示 })`，`X` 是另一篇文档的 public 别名，`Op` 是它导出的操作；类型写成 `str` 或内部类型即违规。 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/DepTagAndApiType/positive }
  * { 反例见 examples/DepTagAndApiType/negative }

DepHintExplainsService =
    tagged[__type__, Object]
  * $statement (str * { 依赖参数的提示要写清这个操作交回什么、拿它做什么，不能只写“依赖 X：”再重复一遍名字。 })
  * $evidence (str * { 原话：这一句话有点像废话 })
  * $check (str * { 提示含返回与用途，无“依赖 X：” })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/DepHintExplainsService/positive }
  * { 反例见 examples/DepHintExplainsService/negative }

HintFolded =
    tagged[__type__, Object]
  * $statement (str * { 函数的提示块一律折行：起始标记、提示内容、结束标记各占一行，再短的提示也不写成一行。 })
  * $evidence (str * { 原话：无论长短都要折行 })
  * $check (str * { 每个函数提示块必须折行：`<- {` 独占一行开始，提示内容另起，`}` 独占一行结束；整块写成一行即违规。 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/HintFolded/positive }
  * { 反例见 examples/HintFolded/negative }

OrphanIsUnreachable =
    tagged[__type__, Object]
  * $statement (str * { 孤立不是“看起来没人用”，而是从根 README 的 public 出发、沿字段类型与参数类型走不到的定义；只在说明文字里被提到，不算走到。 })
  * $evidence (str * { 原话：只要没人使用就是孤立 })
  * $check (str * { 从根文档 public 导出的名字出发，沿字段类型、参数类型与 public 转发逐层走；走不到的定义记为孤立；只在说明文字里出现不算走到。 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/OrphanIsUnreachable/positive }
  * { 反例见 examples/OrphanIsUnreachable/negative }

DeleteAllFileKinds =
    tagged[__type__, Object]
  * $statement (str * { 删除时不看文件类型：文档、生成物、脚本、数据都用同一条判据——从根 README 的 public 出发走不走得到；只按 .viba.md 一种文件判就报违规。 })
  * $evidence (str * { 原话：不限于 python 文件 })
  * $check (str * { 对仓库里每种文件（`.viba.md`、生成物、脚本、数据）都按同一条判据回答“谁依赖它”：从根 public 出发的可达性；只对其中一类文件做判断即违规。 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/DeleteAllFileKinds/positive }
  * { 反例见 examples/DeleteAllFileKinds/negative }

GeneratedFollowsSource =
    tagged[__type__, Object]
  * $statement (str * { 生成物必须跟源头一致：对象定义改了要重新生成 schema，字段集合与生成物对不上就报违规；删改之后还要重查有没有多余的生成物。 })
  * $evidence (str * { 原话：json_schema 重新生成了吗 })
  * $check (str * { 从对象定义生成 schema：属性集合取对象定义的字段、去掉函数定义；与仓库里的 `schema.json` 比对，属性多一个或少一个即违规。 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/GeneratedFollowsSource/positive }
  * { 反例见 examples/GeneratedFollowsSource/negative }

VariantCarriesType =
    tagged[__type__, Object]
  * $statement (str * { 和类型的每个变体后面都要跟一个类型，把这一种情况的数据带上；只写标签、或标签后面跟空括号，都算没有类型。 })
  * $evidence (str * { 原话：这个错大发了 })
  * $check (str * { 遍历每个 `Oneof`：每个变体必须写成 `| $tag (Type * { 提示 })`；变体只有 `()` 或字符串字面量即违规。 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/VariantCarriesType/positive }
  * { 反例见 examples/VariantCarriesType/negative }

NoRecordPlusKind =
    tagged[__type__, Object]
  * $statement (str * { 不要用一个记录加一个 $kind 字段来表示状态；状态要写成和类型，每种情况一个变体，各带自己的数据。 })
  * $evidence (str * { 原话：替代继承/Oneof })
  * $check (str * { 同一个对象里同时出现 `$kind` 字段与纯字符串枚举类型即违规；状态要写成和类型，每个变体带着自己的类型。 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/NoRecordPlusKind/positive }
  * { 反例见 examples/NoRecordPlusKind/negative }

VariantNamesProblem =
    tagged[__type__, Object]
  * $statement (str * { 变体名要写这一种情况或这个问题，不是写话题；把它填进“这条报的是___”要读得通。 })
  * $evidence (str * { 原话：一个叫需求的 Rule })
  * $check (str * { 代入“这条报的是___” })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/VariantNamesProblem/positive }
  * { 反例见 examples/VariantNamesProblem/negative }

TypeNameSaysContent =
    tagged[__type__, Object]
  * $statement (str * { 类型名要说清里面装的是什么：装违规的类型叫 Violation，不叫 Lesson；名字与内容对不上，读的人猜不到它的用途。 })
  * $evidence (str * { 原话：这哪是 Lesson 啊 })
  * $check (str * { 读类型名与变体是否同类 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/TypeNameSaysContent/positive }
  * { 反例见 examples/TypeNameSaysContent/negative }

PolarityConsistent =
    tagged[__type__, Object]
  * $statement (str * { 类型名与变体名的正负要一致：类型名是正面说法，变体名也得是正面说法；否则两者一起改用负面说法，不能一正一负。 })
  * $evidence (str * { 原话：否则要么都是负面的 })
  * $check (str * { 标 positive/negative 比对 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/PolarityConsistent/positive }
  * { 反例见 examples/PolarityConsistent/negative }

TagFormConsistent =
    tagged[__type__, Object]
  * $statement (str * { 同一个和类型里的标签形态要统一：要么全是对问题的描述，要么全是术语名词，要么全是动作动词，不能混着写。 })
  * $evidence (str * { 原话：inline_hint 只是名词 })
  * $check (str * { 逐标签归三类 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/TagFormConsistent/positive }
  * { 反例见 examples/TagFormConsistent/negative }

VariantTypeFormConsistent =
    tagged[__type__, Object]
  * $statement (str * { 变体标签后面的类型名，要和标签同一个形态：标签是术语，类型名也是术语；标签是问题描述，类型名也得是问题描述。 })
  * $evidence (str * { 原话：不只是 tag })
  * $check (str * { 逐标签与它后面的类型名比对 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/VariantTypeFormConsistent/positive }
  * { 反例见 examples/VariantTypeFormConsistent/negative }

NameTripleConsistent =
    tagged[__type__, Object]
  * $statement (str * { 文件名、需求背景、public 三处要说同一件事，信息量一致：文件名的关键词出现在需求背景里，public 的导出行与背景声明的操作对得上。 })
  * $evidence (str * { 原话：信息量一定要一致 })
  * $check (str * { 文件名关键词∈背景；public=背景声明 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/NameTripleConsistent/positive }
  * { 反例见 examples/NameTripleConsistent/negative }

PublicCoversChain =
    tagged[__type__, Object]
  * $statement (str * { public 必须覆盖需求的全链路：需求背景里点到的每个操作，都要能从根 README 的 public 出发走到；留在内部 apis 里没导出，就报违规。 })
  * $evidence (str * { 原话：怎么构建一条样本 })
  * $check (str * { 需求操作逐个查可达 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/PublicCoversChain/positive }
  * { 反例见 examples/PublicCoversChain/negative }

VirtualEdgeBeforeDelete =
    tagged[__type__, Object]
  * $statement (str * { 删一个名字之前，先查说明文字里有没有提到它：真引用（字段类型或参数类型里出现，闭包走得到）与提及（只在说明里出现）要分开列；只有提及的名字也要补成真引用或保留，不能直接删。 })
  * $evidence (str * { 原话：想想概念之间的引用关系 })
  * $check (str * { 对每个待删名字，列出两类边：真引用（出现在字段类型或参数类型里）与提及（只出现在说明文字里）；删除记录里缺这两类边即违规。 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/VirtualEdgeBeforeDelete/positive }
  * { 反例见 examples/VirtualEdgeBeforeDelete/negative }

FixWholeClass =
    tagged[__type__, Object]
  * $statement (str * { 用户点出一处问题时，要按同一条判据把整类问题都找出来：先列出所有同类命中，再逐项改完，不能只改被点到的那一处。 })
  * $evidence (str * { 原话：不能我说一句你只做一句 })
  * $check (str * { 列同类命中并逐项勾销 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/FixWholeClass/positive }
  * { 反例见 examples/FixWholeClass/negative }

RenameIsSemantic =
    tagged[__type__, Object]
  * $statement (str * { 改名不是字符串替换：旧名字对应的类型名、提示文字与所有引用要一起升级，改成新名字该有的说法；只替换名字、其余照旧就报违规。 })
  * $evidence (str * { 原话：就改了个名字 })
  * $check (str * { 改名后问形态/类型/引用 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/RenameIsSemantic/positive }
  * { 反例见 examples/RenameIsSemantic/negative }

BackgroundNamesPublic =
    tagged[__type__, Object]
  * $statement (str * { 每篇文档的需求背景收尾要写清：根 README 从这里取哪些名字；这句话要与本文档 public 的导出行对得上，对不上就报违规。 })
  * $evidence (str * { 九篇都补过这句 })
  * $check (str * { 背景清单=public 导出行 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/BackgroundNamesPublic/positive }
  * { 反例见 examples/BackgroundNamesPublic/negative }

InnerSumForFailures =
    tagged[__type__, Object]
  * $statement (str * { 同一个语义位置的多种失败，要收进内层的和类型里：外层和类型的变体数不变，内层按失败的种类增加，不要把所有失败平铺在外层。 })
  * $evidence (str * { 点赞 Mismatch })
  * $check (str * { 外层变体数不变、内层增加 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/InnerSumForFailures/positive }
  * { 反例见 examples/InnerSumForFailures/negative }

PrincipleIntoKb =
    tagged[__type__, Object]
  * $statement (str * { 用户讲清的一条原则，必须落进知识库，不能只留在对话里：写成一条规则类型，写清原文、依据、检查方法，并附正例与反例。 })
  * $evidence (str * { 原话：显然要写到 design-by-viba })
  * $check (str * { 知识库有篇讲它并带本次例子 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/PrincipleIntoKb/positive }
  * { 反例见 examples/PrincipleIntoKb/negative }

SixChecksPerRound =
    tagged[__type__, Object]
  * $statement (str * { 每一轮固定跑六项检查：解析、加载、闭包、环、旧名，以及文件名、需求背景、public 三者一致；报告里要贴出这六项的数字，不能只说“检查过了”。 })
  * $evidence (str * { goal 要求反复审查 })
  * $check (str * { 贴六项数字 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/SixChecksPerRound/positive }
  * { 反例见 examples/SixChecksPerRound/negative }

VerifiedBeforeDone =
    tagged[__type__, Object]
  * $statement (str * { 验证没跑完，不宣布完成、不推送；宣布完成时要附上跑过的命令与输出，让别人能复核。 })
  * $evidence (str * { 原话：json_schema 重新生成了吗 })
  * $check (str * { 完成附命令与输出 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/VerifiedBeforeDone/positive }
  * { 反例见 examples/VerifiedBeforeDone/negative }

GraphBeforeDelete =
    tagged[__type__, Object]
  * $statement (str * { 删之前先把概念图画出来：闭包只告诉你哪些名字够不到，不告诉你该不该删；还要查说明文字里的提及，确认没有漏掉的引用再删。 })
  * $evidence (str * { SampleConfigBase 被误删 })
  * $check (str * { 删前查虚边再删 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/GraphBeforeDelete/positive }
  * { 反例见 examples/GraphBeforeDelete/negative }

HintAddsInformation =
    tagged[__type__, Object]
  * $statement (str * { 说明要有新信息：把它删掉，读者得到的信息不能减少；删掉也不缺什么，这句话就是废话。 })
  * $evidence (str * { 原话：有点像废话 })
  * $check (str * { 删掉说明问信息量 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/HintAddsInformation/positive }
  * { 反例见 examples/HintAddsInformation/negative }

ViolationAttribution =
    tagged[__type__, Object]
  * $statement (str * { 每条违规都要能归因到三样：违反的是哪条规则、在哪个文件的哪一行、证据原文是什么；缺一样就报违规。 })
  * $evidence (str * { 原话：清晰指出违反原则 })
  * $check (str * { 读每条 `Finding`：必须能读出规则、位置（文件与行号）与证据原文三样；缺一样即违规。 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/ViolationAttribution/positive }
  * { 反例见 examples/ViolationAttribution/negative }

RuleBeforeAction =
    tagged[__type__, Object]
  * $statement (str * { 规则先于动作：动手之前先把可复核的判据写下来，再按判据做事；判据没有写进规则文档，就报违规。 })
  * $evidence (str * { 先有规则才有后续删除 })
  * $check (str * { 动作前有可复核判据 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/RuleBeforeAction/positive }
  * { 反例见 examples/RuleBeforeAction/negative }

FixedStructure =
    tagged[__type__, Object]
  * $statement (str * { 结构固定、入口唯一：根 README 是唯一的入口，每篇设计文档的五节顺序固定，不能多出第二个入口。 })
  * $evidence (str * { 五段+唯一根 })
  * $check (str * { 仓库只有一个入口（根 `README.viba.md`）；每篇设计文档的 `##` 章节按固定顺序排列；多一个入口或章节不合顺序即违规。 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/FixedStructure/positive }
  * { 反例见 examples/FixedStructure/negative }

InterfaceAnswersNeed =
    tagged[__type__, Object]
  * $statement (str * { 接口要对得起输入与需求：参数要对应需求背景写的输入，返回值要交回需求要的结果；交回文件路径这类答非所问的结果，就报违规。 })
  * $evidence (str * { Read 被否定 })
  * $check (str * { 接口对应输入与操作 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/InterfaceAnswersNeed/positive }
  * { 反例见 examples/InterfaceAnswersNeed/negative }

DesignPhaseSpecOnly =
    tagged[__type__, Object]
  * $statement (str * { 设计阶段只留规范：实现代码、生成的 schema、样例数据都按同一条可达性判据删掉；从根 README 的 public 出发走不到的文件留在仓库里，就报违规。 })
  * $evidence (str * { 删代码/生成物/样例 })
  * $check (str * { 对仓库里的每个文件回答：从根 public 出发有没有边到它；代码、生成物、样例数据与文档都一样，没有边即违规。 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/DesignPhaseSpecOnly/positive }
  * { 反例见 examples/DesignPhaseSpecOnly/negative }

PureEnumAllowed =
    tagged[__type__, Object]
  * $statement (str * { 纯字符串枚举只允许用在确实没有数据的取值上；这个取值本来要带失败原因、数量这类数据，却只写成标签，就报违规。 })
  * $evidence (str * { 没有数据的取值没有被纠正过 })
  * $check (str * { 检查变体是否本应有数据 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/PureEnumAllowed/positive }
  * { 反例见 examples/PureEnumAllowed/negative }

DefineNewWords =
    tagged[__type__, Object]
  * $statement (str * { 自造词或生僻词第一次出现时，要在同一段里当场解释它指什么；不解释就直接用，读者读不懂，就报违规。 })
  * $evidence (str * { AGENTS.md 禁词规定 })
  * $check (str * { 生僻词同段有定义 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/DefineNewWords/positive }
  * { 反例见 examples/DefineNewWords/negative }

ScoldingIsRequirement =
    tagged[__type__, Object]
  * $statement (str * { 用户训斥的话也是需求：把原话逐字摘进规则的依据里，从原话反推出规则，单独成一条，不能只记一句转述。 })
  * $evidence (str * { 这句话本身也是经验 })
  * $check (str * { 复盘含原话与规则 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/ScoldingIsRequirement/positive }
  * { 反例见 examples/ScoldingIsRequirement/negative }

PublicOnlyOwnNames =
    tagged[__type__, Object]
  * $statement (str * { public 只导出本文档 types 与 apis 里的名字：每个导出行只能来自本文档的模块，把别的文档的名字转发出来，就报违规。 })
  * $evidence (str * { 这也是规则 })
  * $check (str * { 读每篇文档 `public.viba` 的每个导出行 `X = alias.Y`；`alias` 指向的模块必须属于本文档（模块名前缀与文档名相同）；转发别的文档的名字即违规。 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/PublicOnlyOwnNames/positive }
  * { 反例见 examples/PublicOnlyOwnNames/negative }

TextReviewedBySubagent =
    tagged[__type__, Object]
  * $statement (str * { 交付自然语言之前，要起一个独立的 subagent 审查文字：不得过分口语，尽量用标准术语，读起来不能拗口；审查者、发现与判定要留下记录。 })
  * $evidence (str * { 这条规则也是铁律 })
  * $check (str * { 交付前有审查记录，覆盖口语、术语、拗口 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/TextReviewedBySubagent/positive }
  * { 反例见 examples/TextReviewedBySubagent/negative }


ChangeBoundary =
    tagged[__type__, Object]
  * $statement (str * { 只改任务范围内、并且事先声明过范围的对象：先对照任务范围与改动清单，越界的改动要先确认；没有确认的越界项就算违规。 })
  * $evidence (str * { 三方评审一致：没有边界感与超出任务范围同源 })
  * $check (str * { 对照任务范围与改动清单，越界项未获确认即违规 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/ChangeBoundary/positive }
  * { 反例见 examples/ChangeBoundary/negative }

TargetBeforeEdit =
    tagged[__type__, Object]
  * $statement (str * { 改之前先确认目标文件唯一：有同名文件就列全路径；改完再逐文件核对 diff，看有没有动错。 })
  * $evidence (str * { 改错文件不会被任何现有检查发现 })
  * $check (str * { 改前列出目标路径并确认唯一，改后 diff 逐文件核对 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/TargetBeforeEdit/positive }
  * { 反例见 examples/TargetBeforeEdit/negative }

FunctionScope =
    tagged[__type__, Object]
  * $statement (str * { 函数只用它的参数与返回值表达语义，不替调用方保管知识：不读参数与返回值之外的状态，也不让调用方传入它本可以自己判断的约定，例如“是不是最后一项”。 })
  * $evidence (str * { 依赖规则只约束调用写法，不约束函数掌握的知识 })
  * $check (str * { 检查函数体是否使用了参数与返回值之外的状态或约定 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/FunctionScope/positive }
  * { 反例见 examples/FunctionScope/negative }

ThirdPersonReadable =
    tagged[__type__, Object]
  * $statement (str * { 文档要写给没看过这段对话的人：术语第一次出现就给定义，“上一轮”“刚才”这类指代要换成具体定义，不能假设读者知道上下文。 })
  * $evidence (str * { 自造词规则只管生词，不管对读者的假设 })
  * $check (str * { 把文档交给未参与对话的读者，术语与指代必须能读懂 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/ThirdPersonReadable/positive }
  * { 反例见 examples/ThirdPersonReadable/negative }

NoChangeLog =
    tagged[__type__, Object]
  * $statement (str * { 文档只写现在是什么，变更写进提交信息：正文出现“本次”“改为”“新增”这类变更叙述，就报违规。 })
  * $evidence (str * { 说明信息量规则管不到整篇写成变更史 })
  * $check (str * { 搜索正文里的变更叙述（“本次”“今天”“改为”“新增”等）；命中即违规，变更写进提交信息。 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/NoChangeLog/positive }
  * { 反例见 examples/NoChangeLog/negative }

SectionMatchesHeading =
    tagged[__type__, Object]
  * $statement (str * { 每一节只回答本节标题问的事：基本操作列步骤，types 写字段，限制说明各归其位，不塞进别的节。 })
  * $evidence (str * { 结构规则只查章节名与顺序，不查内容是否对题 })
  * $check (str * { 逐节读首句与末句，是否在回答本节标题 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/SectionMatchesHeading/positive }
  * { 反例见 examples/SectionMatchesHeading/negative }

SectionDetailConsistent =
    tagged[__type__, Object]
  * $statement (str * { 同一篇文档里各章节的详略要一致：不能一节一句话带过，另一节讲到实现细节；差得太远的章节要报出来。 })
  * $evidence (str * { 原话：同一文档各章节详略一致 })
  * $check (str * { 逐节看它展开到多细：一句话、一段话，还是逐条讲到实现；同篇差得远的报出来 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/SectionDetailConsistent/positive }
  * { 反例见 examples/SectionDetailConsistent/negative }

DocsNameOnlyPublic =
    tagged[__type__, Object]
  * $statement (str * { 文档正文只提对方 public 里的名字，不暴露内部 api：正文提到内部 api 就报违规，读者会以为那是可用的接口。 })
  * $evidence (str * { 外部只依赖 public 管 import，管不到正文提到内部 api })
  * $check (str * { 扫描文档正文中出现的名字，是否都能在目标文档的 public 找到 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/DocsNameOnlyPublic/positive }
  * { 反例见 examples/DocsNameOnlyPublic/negative }

ExplainHardParts =
    tagged[__type__, Object]
  * $statement (str * { 难点要先铺垫：首次出现的新概念先给定义或例子，读不懂的推导放进附录，不假设读者自己会。 })
  * $evidence (str * { 现有规则没有铺垫或附录的要求 })
  * $check (str * { 找出首次出现的新概念，检查前文是否给出定义或例子 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/ExplainHardParts/positive }
  * { 反例见 examples/ExplainHardParts/negative }

PublicApiGeneral =
    tagged[__type__, Object]
  * $statement (str * { 对外 api 不耦合内部实现细节：参数与返回值不引用内部类型，也不要求调用方知道内部的存储布局或约定。 })
  * $evidence (str * { 接口对得起需求只管方向，不管是否耦合内部 })
  * $check (str * { 检查 public api 的参数与返回是否引用了内部类型或内部约定 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/PublicApiGeneral/positive }
  * { 反例见 examples/PublicApiGeneral/negative }

NoTimeBoundContent =
    tagged[__type__, Object]
  * $statement (str * { 文档不写“今天”“本次”“当前对话”这类与时刻或对话绑定的内容，只写适用条件；命中时间词或对话指代就报违规。 })
  * $evidence (str * { 现有条款不管与时刻、受众耦合的内容 })
  * $check (str * { 搜索正文里的时间词（今天、本次、当前）与对话指代（上一轮、刚才）；命中即违规，应改写成适用条件。 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/NoTimeBoundContent/positive }
  * { 反例见 examples/NoTimeBoundContent/negative }

SmallFunctions =
    tagged[__type__, Object]
  * $statement (str * { 函数要短，圈复杂度受控，短的 if 也计入分支数；分支多、行数长的函数要报出来。 })
  * $evidence (str * { 规则集没有函数长度与圈复杂度的约束 })
  * $check (str * { 统计分支数与行数，超过阈值即违规 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/SmallFunctions/positive }
  * { 反例见 examples/SmallFunctions/negative }

RuleHasExamples =
    tagged[__type__, Object]
  * $statement (str * { 每条规则都要有正例与反例：规则类型末尾两行提示各给一条路径，路径指向真实存在的示例仓库，缺一条就报违规。 })
  * $evidence (str * { 规则要有明确示例，这也是规则 })
  * $check (str * { 读每个规则叶子类型：必须有两行提示，分别给出正例与反例的路径，且路径指向的仓库存在；缺一行或路径不存在即违规。 })
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

只有一个操作：按规则检查。给出仓库路径，逐条规则检查，交回违规清单；每条违规带上规则叶子类型与位置。检查前先问 `must_judged_by_agent[这条规则的叶子类型]`：true 的交给 agent 判，false 的按 `$check` 用程序判；没判的不得当作通过。

## apis.viba

```viba apis
import rules.types as rules

CheckViolations =
     list[rules.Finding]
  <- $repo (str * { 仓库路径：里面是一组 .viba.md 文档 })
  <- $rules (list[rules.Rule] * { 这次要执行的规则；从规则集里取 })
  <- {
    按规则检查：先问 must_judged_by_agent[这条规则的叶子类型]，true 的交给 agent 判，false 的执行它的 $check；不符合的记成一条 Finding，带上规则、位置与证据；返回违规清单
  }
```
