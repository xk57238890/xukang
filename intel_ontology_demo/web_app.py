from __future__ import annotations

import streamlit as st

from intel_ontology_demo.services.ontology_editor import OntologyEditor
from intel_ontology_demo.services.pipeline import IntelOntologyPipeline
from intel_ontology_demo.ui.console_view import render_combined, render_instances, render_ontology


st.set_page_config(page_title="情报动态本体 Demo", layout="wide")


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
    st.title("情报系统动态本体构建 Demo")
    st.caption("支持 KAG/OpenSPG 风格初始化、自动本体演化、人工本体编辑、双视图展示")

    pipeline = build_pipeline()
    editor = OntologyEditor()
    ensure_state()

    with st.sidebar:
        st.header("控制面板")
        extract_mode = st.selectbox("抽取模式", ["kag", "llm"], index=0)
        view_mode = st.radio("展示模式", ["combined", "split"], index=0)
        if st.button("重置图谱", type="secondary"):
            reset_state()
            st.success("已重置为初始本体")

    text = st.text_area(
        "输入情报文本",
        value="Alice joined ACME. ACME in Shanghai.",
        height=130,
        help="kag模式示例: Alice joined ACME. ACME in Shanghai.\nllm模式示例: drone observed near harbor",
    )

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("本体编辑")
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
        st.subheader("抽取与融合")
        if st.button("执行抽取并入图", type="primary"):
            st.session_state.knowledge_state = pipeline.extract_and_merge(
                st.session_state.knowledge_state,
                text,
                mode=extract_mode,
            )
            st.success("已完成抽取与入图（含自动本体演化）")

    st.divider()
    st.subheader("图谱展示")
    state = st.session_state.knowledge_state

    if view_mode == "combined":
        st.code(render_combined(state), language="text")
    else:
        left, right = st.columns(2)
        with left:
            st.markdown("**本体层**")
            st.code(render_ontology(state), language="text")
        with right:
            st.markdown("**实例层**")
            st.code(render_instances(state), language="text")


if __name__ == "__main__":
    main()
