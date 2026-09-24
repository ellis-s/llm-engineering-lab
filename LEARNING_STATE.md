# LLM 应用开发工程师学习状态

> 这是跨聊天窗口继续学习的唯一进度存档。每日任务与验收内容以仓库中的《LLM应用开发工程师_14周每日执行计划_V2.1.xlsx》为准；本文件记录学员背景、执行约定、当前进度、阶段交付和待办。更新时保留已完成记录，不把计划任务误记为已完成。

## 学习者与目标

- 目标岗位：LLM Application Engineer / LLM 应用开发工程师。
- 背景：近 10 年前端开发经验，有 Python 基础；前端部分按项目需要回查，不重复系统学习。
- 目标结果：能独立设计、编码、调试、评测和部署 LLM 应用，形成可展示的 GitHub 项目与面试证据。
- 导师协作：按当天进度安排具体路线、讲解关键概念、布置实战任务，检查代码/实验/设计并进行 Code Review 和阶段验收。

## 计划基线

- 版本：V2.1，14 周、98 个连续日历日。
- 计划起始日：2026-09-24；计划第 98 天：2026-12-30。
- 计划时长：约 812 小时（工作日约 8.5 小时，周日约 7 小时；以 Excel 每日计划为准）。
- 主线方法：课程/资料不超过约 20%，其余时间用于独立编码、实验、项目、复盘和验收。
- 每日节奏：看主线资源（≤90 分钟）→ 关闭教程独立实现 → 做实验或故障演练 → 合入项目 → 提交 Review → 根据反馈修改重构 → 周测。
- 学习标准：每项核心能力都要达到“知道、能写、能解释、能排障”；看完课程或照抄代码不算完成。
- 每周日安排周测；未通过时先回补薄弱点，再进入下一阶段。第 9 周开始求职准备与定向投递，不等到全部学完。

## 仓库与计划文件

- 学习仓库：`llm-engineering-lab`
- 本地路径：`/Users/sunhongfei/AI/projects/llm-engineering-lab`
- 每日计划：`LLM应用开发工程师_14周每日执行计划_V2.1.xlsx`
- 每日执行表包含具体任务、产出、资源、验收标准和状态。遇到日期或任务调整时，记录原因，并同步维护计划表与本文件。

## 当前进度

- 状态更新时间：2026-09-24
- 当前阶段：第 1 周「基础重建」—— Python 工程、FastAPI、HTTP/SSE、pytest。
- 当前日：Day 1（2026-09-24，周四）。
- 今日主题：Python 工程复盘（typing / dataclass / Pydantic / 异常），建立 uv 项目骨架。
- 今日计划产出：`pyproject.toml`、`.env`、logging 与配置模块、Git 提交；能从空目录搭建工程并解释目录职责。
- 已完成：学习仓库已创建；V2.1 Excel 已放入仓库。
- 进行中：尚未记录 Day 1 学习结果。
- 阻塞/疑问：暂无已记录事项。
- 进度口径：目前没有任务被确认完成；按实际提交、实验结果与验收情况更新，不依据计划日期自动推进。

## 14 周路线与阶段交付

| 周 | 学习主线 | 阶段交付 / 验收重点 |
|---|---|---|
| 1 | Python 工程、FastAPI、HTTP/SSE、pytest | 项目 1 v0：LLM Chat API；90 分钟从空目录写出核心 API、SSE 和基础异常处理 |
| 2 | LLM API、Prompt、Structured Output、原生 Tool Calling | 项目 1 v1：AI 内容分析服务与工具调用循环；能脱离框架实现 JSON 输出和工具调用 |
| 3 | Embedding、相似度、Chunk、TopK、最小 RAG | RAG Lab 1：纯 Python 检索器；解释 cosine/dot/TopK/Recall@K 并复现召回失败 |
| 4 | LangChain、向量库、文档解析、Metadata、BM25 | RAG Lab 2：上传、metadata 过滤、dense + BM25；能讲清完整 RAG 链路 |
| 5 | Hybrid、Rerank、Query Rewrite、引用、评测 | RAG Eval v1：100 条评测集、至少 3 轮可复现实验及对比结论 |
| 6 | 企业知识库与全栈集成 | 项目 2 v1：上传/解析/检索/引用/Streaming；Docker 启动基础环境 |
| 7 | Tool Calling、ReAct、Workflow 与状态 | Agent Lab：天气/计算器/HTTP API/数据库查询工具；手写工具循环并说明 Agent 与 Workflow 的边界 |
| 8 | LangGraph、State、Checkpoint、HITL、Memory | 项目 3 v1：RAG + DB/API Tool + Workflow；处理中断恢复、异常分支和记忆策略 |
| 9 | MCP Server/Client、工具暴露、作品集与求职启动 | 项目 3 v2：自建 MCP Server；简历 v1、GitHub README/架构图、第一批定向投递 |
| 10 | PostgreSQL、Redis、asyncio、Docker、可靠性与安全 | 项目 3 v3：鉴权/缓存/日志/测试/Docker Compose；完成超时、重试、fallback、health check 故障演练 |
| 11 | 离线评测、回归、Trace、Token/Cost/Latency | Evaluation/Observability 模块：评测数据集、指标、Trace 和版本对比报告 |
| 12 | Ollama、vLLM、OpenAI-compatible API、模型解耦 | Model Gateway：至少两个后端可切换；启动并调用本地模型服务，记录基础性能 |
| 13 | 旗舰企业 AI 工作助手实现与集成 | RC：RAG + Agent + MCP + DB + Redis + Eval + Trace + Docker；完成设计取舍与故障案例说明 |
| 14 | 项目精修、简历、面试与投递 | 简历 v2、项目演示、30 道核心面试题、3 轮模拟面试、定向投递；30 分钟完整答辩 |

## 项目与毕业证据

- 项目 1：LLM Chat API（FastAPI、SSE、LLM API、pytest）。
- 项目 2：企业知识库系统（RAG、PostgreSQL/pgvector、Redis、React）。
- 项目 3 / 旗舰项目：Agent + MCP 企业 AI 助手，最终扩展到评测、Trace、模型解耦和部署。
- 配套实验：最小检索器、RAG 优化评测、FC/MCP 接入对比、Memory、故障转移与健康检测、vLLM 服务实验。
- 提交 Review 的材料：代码或仓库、运行/测试说明、个人设计说明、测试或评测结果、具体卡点、希望重点检查的方面。
- 毕业判断：看独立完成能力及代码、实验数据、项目交付和面试表达证据，不以课程完成比例判断。

## 后续进度记录

每次学习后追加一条，不覆盖历史：

```text
日期 / Day：
计划主题：
完成情况：完成 / 部分完成 / 未开始 / 延期
代码或实验产出：
验收结果：
遇到的问题与下一步：
导师 Review 结论 / 修改项：
```

### 学习日志

| 日期 / Day | 完成情况 | 产出与验收 | 问题 / 下一步 |
|---|---|---|---|
| 2026-09-24 / Day 1 | 未记录 | 等待实际学习后填写 | 按计划完成工程骨架并提交验收材料 |

## 新聊天窗口续接说明

开始新窗口时，提供本文件与 V2.1 Excel（或让导师读取仓库中的文件），并说明最近完成的 Day、实际产出和当前卡点。导师先核对本文件与每日计划表，再从下一个未完成日继续；如果进度落后或发生调整，先制定合理补课/顺延安排，不跳过未通过的验收。
