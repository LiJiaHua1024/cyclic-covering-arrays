# 项目主控与推进路线图 (Project Control & Execution Roadmap)

> **基准真相源**：[`theorem_ledger.md`](file:///C:/Users/李家华/OneDrive/桌面/三合一菲尔兹奖/theorem_ledger.md)  
> **工程规范**：Prompt 生成严格遵循 [`prompt engineering guide.md`](file:///D:/LLM%20Engineering/prompt%20engineering%20guide.md)  
> **定位**：主控（Main Control / 仓库管理 / 外部强模型提示词设计 / 杂活协同）

---

## 一、 当前仓库真实状态审计 (Reality Check)

根据最新独立评估建议，对现有资产进行严格对账：

| 模块 / 命题 | 账本与代码声称 | 独立审计结论与待办事项 | 状态 |
|---|---|---|---|
| **$C_{21}$ 修补排斥** | 代码与账本仅覆盖 **1 行与 2 行排斥** | 外部讨论中提到的“三行排斥”尚无代码与证书支持。**禁止在账本中超前声明三行排斥**，如需确立需单独编写三行剪枝排斥验证脚本。 | ⚠️ 保持诚实对齐 |
| **Zenodo DOI** | `10.5281/zenodo.22918432` | 页面指向软件记录 *Exact 13-Row Fault-Tolerant Combinatorial Testing under C14 Exclusion Constraints*。不可将其表述为“同行评议学术认可”，仅作为代码快照归档凭证。 | ⚠️ 定位校准 |
| **$N(n)=\Theta(\log n)$ (第5章)** | 随机行选取的概率上界 | 缺少**行互异（Distinct Rows）**的明确概率论证（尽管 $\binom{M}{2}/L_n \to 0$ 极其显然，但数学严格证明中不可留白）。 | 📝 待补充细节 |
| **$\lim LP(n)=12$ (第4章)** | 有限环传递矩阵指数收敛 | 需补充有限环长 $n$ 下迹归一化 $\operatorname{tr}(T^n)$ 后的单调性与下界保证，严密证明每一个有限环上的分数解均合法且目标值单调收敛。 | 📝 待严格化 |
| **$C_{20}$ 极值** | 已严格证明 $N(20)=13$ (定理 T11) | 求解器在 2.9 秒求得显式 13 行解，并通过 CP-SAT 紧致排斥结合 T1 排除 12 行。 | ✅ 已完成闭环 |
| **$C_{21}$ 极值** | 已严格证明 $N(21)=13$ (定理 T10) | 求解器在 4.2 秒求得显式 13 行解，并通过 CP-SAT 紧致排斥排除 12 行。连续 13 行平台扩展至 9 个连续整数 $[13, 21]$，全局跃迁阈值推高至 $n^*_{\text{global}} \ge 22$。 | ✅ 已完成闭环 |

---

## 二、 阶段推进计划 (Phased Execution Plan)

### 阶段 1：数学证明审计与手稿漏洞修补（低垂果实，提升可信度）
- **目标**：将手稿中的推测性/简略性论证升级为无可挑剔的数学定理。
- **任务清单**：
  1. `manuscript/05_integer_complexity.md`：补全概率构造中行互异（distinct rows）的 union bound 与严格界。
  2. `manuscript/04_asymptotic_lp_limit.md`：补全有限环 $C_n$ 上的周期加权与 $\operatorname{tr}(T^n)$ 极值控制，给出精确的分数解构造。
  3. 文献脉络补全：在引言与综述中正式引入 **CAFE (Covering Arrays Avoiding Forbidden Edges)** 与 **Constrained Covering Arrays** 的既有文献（如 Danziger et al., Colbourn et al., 2009 起的一般约束图文献），确立学术定位。

### 阶段 2：$C_{20}$ 精确判定（核心突破点）——【✅ 已达成】
- **成果**：已精确判定 $LP(20) = 12, N(20) = 13$。
- **产出**：[`solve_c20.py`](file:///C:/Users/李家华/OneDrive/桌面/三合一菲尔兹奖/solve_c20.py)，[`data/solution_c20.txt`](file:///C:/Users/李家华/OneDrive/桌面/三合一菲尔兹奖/data/solution_c20.txt)，入库定理 **[T11]**。

### 阶段 3：$C_{21}$ 精确求解与终极平坦带扩展——【✅ 已达成】
- **成果**：已精确判定 $LP(21) = 12, N(21) = 13$。
- **产出**：
  1. [`solve_c21.py`](file:///C:/Users/李家华/OneDrive/桌面/三合一菲尔兹奖/solve_c21.py)：CP-SAT 精确求解器（4.2 秒出解，4 秒排除 12 行）。
  2. [`data/solution_c21.txt`](file:///C:/Users/李家华/OneDrive/桌面/三合一菲尔兹奖/data/solution_c21.txt)：13 行二元矩阵见证（819 项覆盖全量通过）。
  3. 账本更新定理 **[T10]**，将连续 13 行平台推高至 9 个连续整数 $[13, 21]$，全局跃迁阈值刷新至 $n^*_{\text{global}} \ge 22$。

### 阶段 4：从单环向一般约束图推广与前沿探索
- **目标**：将单个环图 $C_n$ 的方法推广到一般连通图、弦图、树状约束等（结合 CAFE 文献）；探索 $C_{22}$ 状态。

---

## 三、 外部超强 AI 提示词分发标准规范 (Prompt Dispatch Protocol)

严格遵循 `D:\LLM Engineering\prompt engineering guide.md`，执行**规格说明学 + 环境设计**：

1. **零废话原则**：严禁角色扮演（"你是菲尔兹级数学家"）、严禁情绪施压（"这对我很重要"）、严禁通用咒语（"请一步步思考"）。
2. **信息论测试**：每一句话必须是模型从其他材料中推断不出来的私有规则、硬性约束或输出契约。
3. **结构规范**：
   - `[TASK & INTENT]`：要做什么 + 为什么做（意图是最高效的压缩规格）。
   - `[REQUIRED CONTEXT FILES]`：明确指引用户首次调用时需上传的文件列表。
   - `[HARD CONSTRAINTS & BOUNDARIES]`：数学规范、库依赖（尽量纯标准库或明确指定 or-tools）、行互异要求、验证口径。
   - `[OUTPUT CONTRACT]`：要求交付代码/证明的具体格式、签名、可运行测试。
   - `[FAILURE & EXCEPTION HANDLING]`：遇 UNSAT/超时时的降级策略。
4. **外化与对账**：强 AI 输出的任何结论，必须经过主控在本地运行测试、验证通过后，方可写入 `theorem_ledger.md`。
