# 可持续演化的智能情报知识中枢系统（KAG/OpenSPG Demo）

这个 Demo 已从“静态图谱演示”升级为“可落地闭环系统原型”，核心闭环：

> 数据采集 → 本体演化 → 图谱构建（含事件）→ 推理分析 → 决策问答

## 1. 系统四层架构（可直接用于PPT）

### ① 数据采集层
- 多源接入：新闻/RSS、社交媒体、报告文本（可扩展 API / Scrapy）。
- 增量更新：按 `doc_id` 去重，只处理新文档。
- 实现：`DataIngestionService.collect()`。

### ② 语义解析层
- 双抽取路径：`kag` 规则抽取 + `llm` 风格抽取。
- 支持实体、关系以及**事件级抽取**（时间、主体、行为、对象、地点、结果）。

### ③ 动态本体层（核心）
- 本体初始化（情报基础 schema）。
- 自动本体演化（新类/新关系自动进入 schema）。
- 本体版本管理（每次结构变更记录版本 + 时间轴，支持回溯基础）。

### ④ 知识图谱与推理应用层
- 图谱包含：实体节点、关系边、事件子图。
- 推理：关键人物网络、风险路径。
- 应用：组织近期活动问答（KG 约束，减少胡编）。

---

## 2. 目录结构

```text
intel_ontology_demo/
├── adapters/
│   ├── extractors.py         # 实体/关系/事件抽取
│   └── kag_adapter.py        # 本体初始化、自动演化、版本快照、入图
├── services/
│   ├── data_ingestion.py     # 多源采集 + 增量去重
│   ├── ontology_editor.py    # 人工本体编辑
│   ├── pipeline.py           # 数据->本体->图谱->推理 编排
│   └── reasoning.py          # 推理与问答
├── ui/
│   └── console_view.py       # 本体/实例/时间轴视图
├── main.py                   # CLI入口
└── web_app.py                # Streamlit 前端入口
```

---

## 3. 快速开始

### 安装依赖

```bash
pip install -e .
```

### CLI 运行

```bash
python -m intel_ontology_demo.main --mode kag
```

或 LLM 风格抽取：

```bash
python -m intel_ontology_demo.main --mode llm --text "2026-04-21: RedGroup deployed DroneX to Harbor"
```

### 前端运行

```bash
streamlit run intel_ontology_demo/web_app.py
```

---

## 4. Demo 可展示的“甲方价值点”

1. **双视图联看**：Schema（本体）+ Graph（实例/事件）。
2. **本体演化时间轴**：展示 Day1/Day3/Day5 的类与关系增长。
3. **完整情报故事线**：从原始文本自动形成事件链与风险路径。
4. **智能问答**：如“某组织最近活动有哪些？”

---

## 5. 一句话卖点

本系统构建了一个“可持续演化的本体驱动知识图谱平台”，可在多源情报持续输入下自动扩展知识结构、维护语义一致性，并提供可解释推理与高可信问答支持。

---

## 附：SWaT + KDD 统一复现实验模板

仓库新增 `tsad_template/`，用于快速搭建时间序列异常检测的统一实验：

- 统一数据加载接口：`swat.csv` / `kdd.csv`
- 统一模型接口：当前内置 `iforest` 基线
- 统一评测输出：Precision / Recall / F1 / AUPR
- 统一入口：`python tsad_template/run_experiment.py --dataset swat --model iforest`

详见 `tsad_template_README.md`。
