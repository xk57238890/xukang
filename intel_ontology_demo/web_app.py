from __future__ import annotations

import streamlit as st

from intel_ontology_demo.services.ontology_editor import OntologyEditor
from intel_ontology_demo.services.pipeline import IntelOntologyPipeline
from intel_ontology_demo.ui.console_view import (
    render_combined,
    render_instances,
    render_ontology,
    render_ontology_timeline,
)


st.set_page_config(page_title="情报知识中枢 Demo", layout="wide")


@st.cache_resource
def build_pipeline() -> IntelOntologyPipeline:
    return IntelOntologyPipeline()


def ensure_state() -> None:
    if "knowledge_state" not in st.session_state:
        pipeline = build_pipeline()
        st.session_state.knowledge_state = pipeline.bootstrap("intel")


def reset_state() -> None:
    pipeline = build_pipeline()
    st.session_state.knowledge_state = pipeline.bootstrap("intel")


def main() -> None:
    st.title("可持续演化的智能情报知识中枢系统（KAG Demo）")
    st.caption("数据 → 本体 → 图谱 → 推理 → 决策 闭环演示")

    pipeline = build_pipeline()
    editor = OntologyEditor()
    ensure_state()

    with st.sidebar:
        st.header("控制面板")
        extract_mode = st.selectbox("抽取模式", ["kag", "llm"], index=0)
        view_mode = st.radio("图谱展示模式", ["combined", "split"], index=0)
        if st.button("重置图谱", type="secondary"):
            reset_state()
            st.success("已重置为初始本体")

    with st.expander("① 数据采集层（增量更新 + 去重）", expanded=False):
        news = st.text_area("新闻/RSS", value="2026-04-21: RedGroup deployed DroneX to Harbor")
        social = st.text_area("社交媒体", value="drone observed near harbor")
        report = st.text_area("报告/PDF抽取文本", value="On 2026-04-20 Alice attacked Depot at Harbor resulting disruption")
        if st.button("执行多源接入并融合", type="primary"):
            st.session_state.knowledge_state = pipeline.ingest_multisource(
                st.session_state.knowledge_state,
                {
                    "news": [news],
                    "social": [social],
                    "report": [report],
                },
            )
            st.success("多源数据已入图（自动去重 + 增量处理）")

    st.subheader("②/③ 语义解析与动态本体层")
    text = st.text_area(
        "输入情报文本",
        value="Alice joined ACME. ACME in Shanghai. On 2026-04-20 Alice attacked Depot at Harbor resulting disruption",
        height=120,
    )

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**本体人工编辑（人机协同）**")
        with st.form("add_class_form", clear_on_submit=True):
            class_name = st.text_input("类名", placeholder="Operation")
            class_desc = st.text_input("类说明", placeholder="行动对象")
            add_class_btn = st.form_submit_button("添加类")
            if add_class_btn and class_name.strip():
                editor.add_class(st.session_state.knowledge_state, class_name.strip(), class_desc.strip() or "手工添加")
                st.success(f"已添加类: {class_name.strip()}")

        with st.form("add_relation_form", clear_on_submit=True):
            relation_name = st.text_input("关系名", placeholder="targets")
            source_class = st.text_input("源类", placeholder="Organization")
            target_class = st.text_input("目标类", placeholder="Operation")
            relation_desc = st.text_input("关系说明", placeholder="组织指向行动")
            add_relation_btn = st.form_submit_button("添加关系")
            if add_relation_btn and relation_name.strip() and source_class.strip() and target_class.strip():
                editor.add_relation(
                    st.session_state.knowledge_state,
                    relation_name.strip(),
                    source_class.strip(),
                    target_class.strip(),
                    relation_desc.strip() or "手工添加关系",
                )
                st.success(f"已添加关系: {relation_name.strip()}")

    with c2:
        st.markdown("**抽取与入图（含事件级建模）**")
        if st.button("执行抽取并入图"):
            st.session_state.knowledge_state = pipeline.extract_and_merge(
                st.session_state.knowledge_state,
                text,
                mode=extract_mode,
            )
            st.success("抽取完成：实体/关系/事件已更新")

    st.divider()
    state = st.session_state.knowledge_state
    st.subheader("④ 知识图谱层：本体层 + 实例层")
    if view_mode == "combined":
        st.code(render_combined(state), language="text")
    else:
        left, right = st.columns(2)
        with left:
            st.markdown("**本体层（Schema）**")
            st.code(render_ontology(state), language="text")
        with right:
            st.markdown("**实例层（Graph）**")
            st.code(render_instances(state), language="text")

    st.subheader("本体演化时间轴")
    st.code(render_ontology_timeline(state), language="text")

    st.subheader("⑤ 推理与应用层")
    r1, r2 = st.columns(2)
    with r1:
        st.markdown("**关键人物网络（路径推理）**")
        st.json(pipeline.reasoner.find_key_person_network(state))
    with r2:
        st.markdown("**风险路径（可解释）**")
        st.write(pipeline.reasoner.infer_risk_paths(state) or ["暂无高风险路径"])

    org_name = st.text_input("智能问答：某组织最近的活动", value="RedGroup")
    if st.button("查询活动"):
        answer = pipeline.reasoner.answer_recent_activities(state, org_name)
        st.success(answer)


if __name__ == "__main__":
    main()
