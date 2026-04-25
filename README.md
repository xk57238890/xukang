# 情报系统动态本体构建 Demo（Python）

这是一个可运行的 Python Demo，用于演示：

- 使用 **KAG/OpenSPG 思路** 初始化本体（可替换为真实 KAG SDK）。
- 在信息抽取后对本体进行 **自动演化**（新类/新关系自动补全）。
- 提供本体 **人工编辑能力**（手工增加类和关系）。
- 抽取层支持两种模式：
  - `kag`：规则化、结构化抽取（模拟 KAG 风格）
  - `llm`：纯大模型抽取风格（示例用占位实现）
- 支持 **本体层 + 实例层一起显示** 或 **分开显示**。
- 提供 **前端界面（Streamlit）**，可视化操作本体编辑、抽取入图、图谱查看。

---

## 目录结构

```text
intel_ontology_demo/
├── adapters/
│   ├── extractors.py         # KAG风格抽取 + 纯LLM风格抽取
│   └── kag_adapter.py        # 初始化本体、自动演化、实例入图
├── services/
│   ├── ontology_editor.py    # 本体手工编辑
│   └── pipeline.py           # 流程编排
├── ui/
│   └── console_view.py       # 合并/分离视图
├── main.py                   # CLI入口
└── web_app.py                # Streamlit 前端入口
```

---

## 快速开始

### 安装依赖

```bash
pip install -e .
```

### 1) 运行默认 CLI 示例（KAG风格抽取 + 合并视图）

```bash
python -m intel_ontology_demo.main
```

### 2) 纯大模型风格抽取（触发本体自动演化）

```bash
python -m intel_ontology_demo.main \
  --mode llm \
  --text "drone observed near harbor"
```

该示例会自动演化出：
- 新类：`Asset`, `StrategicArea`
- 新关系：`observed_near`

### 3) 分开显示本体层和实例层

```bash
python -m intel_ontology_demo.main --view split
```

### 4) 演示人工编辑本体（CLI）

```bash
python -m intel_ontology_demo.main --edit-demo
```

会在抽取前手工加入：
- 类：`Operation`
- 关系：`targets(Organization -> Operation)`

---

## 前端界面（Streamlit）

### 启动方式

```bash
streamlit run intel_ontology_demo/web_app.py
```

或使用脚本入口：

```bash
intel-demo-web
```

### 前端可做的操作

1. **选择抽取模式**：`kag` / `llm`。
2. **输入情报文本**，点击“执行抽取并入图”。
3. **编辑本体**：添加类、添加关系。
4. **切换展示模式**：
   - `combined`：本体层与实例层合并展示
   - `split`：本体层与实例层分栏展示
5. **重置图谱**：恢复初始化本体。

---

## 和真实 KAG/OpenSPG 对接建议

当前 Demo 为轻量可运行版本，真实项目可按以下替换：

1. 将 `adapters/kag_adapter.py` 中的初始化逻辑改为调用 OpenSPG/KAG 的本体管理 API。
2. 将 `adapters/extractors.py` 的 `PureLLMExtractor` 改为真实模型调用（OpenAI API/私有部署模型）并解析 JSON 三元组。
3. 将 `KnowledgeState` 持久化到图数据库（如 NebulaGraph/Neo4j），并增加版本化管理，支持审计与回滚。

---

## 定位

这个仓库目标是快速验证“动态本体构建 + 双抽取路径 + 双视图展示 + 前端交互”的产品原型。
如果你要扩展到生产版本，建议优先补齐：

- 抽取质量评估（P/R/F1）
- 本体冲突检测与合并策略
- 人机协同审核流（变更审批）
