import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
from engine import A7DOResearchEngine, Hypothesis

st.set_page_config(layout="wide")
st.title("🧠 A7DO Research Engine v0.1")

# -------------------------------------------------
# Persistent State
# -------------------------------------------------
if "engine" not in st.session_state:
    st.session_state.engine = A7DOResearchEngine()

if "hypothesis_obj" not in st.session_state:
    st.session_state.hypothesis_obj = None

engine = st.session_state.engine


# -------------------------------------------------
# 1️⃣ Hypothesis Section
# -------------------------------------------------
st.header("1️⃣ Hypothesis")

hyp_text = st.text_input(
    "Enter hypothesis",
    value="" if st.session_state.hypothesis_obj is None 
    else st.session_state.hypothesis_obj.text
)

if st.button("Set Hypothesis"):
    if hyp_text.strip() == "":
        st.warning("Enter a hypothesis first.")
    else:
        st.session_state.hypothesis_obj = Hypothesis(hyp_text)
        st.success("Hypothesis set.")

hypothesis = st.session_state.hypothesis_obj


# -------------------------------------------------
# 2️⃣ Relation Builder (Always Visible)
# -------------------------------------------------
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
        st.warning("Fill all three fields.")


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
st.header("3️⃣ Run Analysis")

if st.button("Analyze"):
    if hypothesis is None:
        st.warning("Set a hypothesis first.")
    else:
        result = engine.analyze(hypothesis)
        st.subheader("Z–Σ Output")
        st.write(result)


# -------------------------------------------------
# 📈 Confidence Evolution
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