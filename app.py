import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
from engine import A7DOResearchEngine, Hypothesis

st.set_page_config(layout="wide")
st.title("🧠 A7DO Research Engine v0.1")

# -------------------------------------------------
# Persistent Engine (stored in session state)
# -------------------------------------------------
if "engine" not in st.session_state:
    st.session_state.engine = A7DOResearchEngine()

if "hypothesis" not in st.session_state:
    st.session_state.hypothesis = None

engine = st.session_state.engine


# -------------------------------------------------
# 1️⃣ Hypothesis Input
# -------------------------------------------------
st.header("1️⃣ Hypothesis")

hyp_text = st.text_input("Enter hypothesis")

if hyp_text:
    if st.session_state.hypothesis is None:
        st.session_state.hypothesis = Hypothesis(hyp_text)

hypothesis = st.session_state.hypothesis


# -------------------------------------------------
# 2️⃣ Add Structural Relations
# -------------------------------------------------
if hypothesis:
    st.header("2️⃣ Add Structural Relations")

    col1, col2, col3 = st.columns(3)

    with col1:
        source = st.text_input("Source")

    with col2:
        relation = st.text_input("Relation")

    with col3:
        target = st.text_input("Target")

    if st.button("Add Relation"):
        if source and relation and target:
            engine.add_relation(source, relation, target)
            st.success(f"Added: {source} --{relation}--> {target}")
        else:
            st.warning("Fill all fields before adding relation.")


# -------------------------------------------------
# 📊 Graph View
# -------------------------------------------------
if engine.graph:
    st.header("📊 Graph View")

    G = nx.DiGraph()

    for src in engine.graph:
        for tgt in engine.graph[src]:
            rel = engine.graph[src][tgt]
            G.add_edge(src, tgt, label=rel)

    pos = nx.spring_layout(G)

    fig, ax = plt.subplots()
    nx.draw(G, pos, with_labels=True, ax=ax)
    edge_labels = nx.get_edge_attributes(G, "label")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)

    st.pyplot(fig)


# -------------------------------------------------
# 3️⃣ Run Analysis
# -------------------------------------------------
if hypothesis:
    st.header("3️⃣ Run Analysis")

    if st.button("Analyze"):
        result = engine.analyze(hypothesis)

        st.subheader("Z–Σ Output")
        st.write(result)


# -------------------------------------------------
# 📈 Confidence Evolution Plot
# -------------------------------------------------
if hypothesis and hypothesis.history:
    st.header("📈 Confidence Evolution")

    Z_vals = [h["Z"] for h in hypothesis.history]
    S_vals = [h["Sigma"] for h in hypothesis.history]
    C_vals = [h["confidence"] for h in hypothesis.history]

    fig2, ax2 = plt.subplots()
    ax2.plot(C_vals, label="Confidence")
    ax2.plot(Z_vals, label="Z")
    ax2.plot(S_vals, label="Sigma")
    ax2.legend()

    st.pyplot(fig2)