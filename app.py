import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx

from engine import A7DOResearchEngine
from models import SymbolicRelation, SymbolicHypothesis

st.set_page_config(layout="wide")
st.title("🧠 A7DO Research Engine v0.3 (Symbolic)")

# -------------------------------------------------
# Session State
# -------------------------------------------------
if "engine" not in st.session_state:
    st.session_state.engine = A7DOResearchEngine()

if "hypothesis_obj" not in st.session_state:
    st.session_state.hypothesis_obj = None

engine = st.session_state.engine
hypothesis = st.session_state.hypothesis_obj

# -------------------------------------------------
# 1️⃣ Symbolic Hypothesis Input
# -------------------------------------------------
st.header("1️⃣ Symbolic Hypothesis")

col1, col2, col3 = st.columns(3)

with col1:
    subject = st.text_input("Hypothesis Subject", key="hyp_subject")

with col2:
    hyp_relation = st.text_input("Hypothesis Relation", key="hyp_relation")

with col3:
    obj = st.text_input("Hypothesis Object", key="hyp_object")

if st.button("Set Hypothesis"):
    if subject and hyp_relation and obj:
        st.session_state.hypothesis_obj = SymbolicHypothesis(subject, hyp_relation, obj)
        st.success("Hypothesis set.")
    else:
        st.warning("Fill all hypothesis fields.")

hypothesis = st.session_state.hypothesis_obj

# -------------------------------------------------
# 2️⃣ Add Structural Relations
# -------------------------------------------------
st.header("2️⃣ Add Structural Relations")

col4, col5, col6 = st.columns(3)

with col4:
    src = st.text_input("Relation Source", key="rel_source")

with col5:
    rel = st.text_input("Relation Type", key="rel_type")

with col6:
    tgt = st.text_input("Relation Target", key="rel_target")

if st.button("Add Relation"):
    if src and rel and tgt:
        relation_obj = SymbolicRelation(src, rel, tgt)
        engine.add_relation(relation_obj)
        st.success(f"Added: {src} --{rel}--> {tgt}")
    else:
        st.warning("Fill all relation fields.")

# -------------------------------------------------
# Graph View
# -------------------------------------------------
if engine.graph:
    st.header("📊 Graph View")

    G = nx.DiGraph()

    for s in engine.graph:
        for t in engine.graph[s]:
            G.add_edge(s, t, label=engine.graph[s][t])

    pos = nx.spring_layout(G)

    fig, ax = plt.subplots()
    nx.draw(G, pos, with_labels=True, ax=ax)
    edge_labels = nx.get_edge_attributes(G, "label")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)

    st.pyplot(fig)

# -------------------------------------------------
# Run Analysis
# -------------------------------------------------
st.header("3️⃣ Run Analysis")

if st.button("Analyze"):
    if hypothesis is None:
        st.warning("Set hypothesis first.")
    else:
        result = engine.analyze(hypothesis)

        st.subheader("Z–Σ Output")
        st.write({
            "Z": result["Z"],
            "Sigma": result["Sigma"],
            "confidence": result["confidence"]
        })

        st.subheader("🔎 Paths")

        if result["paths"]:
            for p in result["paths"]:
                st.write(" → ".join(p))
        else:
            st.write("No path found.")

        st.subheader("🧩 Missing Links")

        if result["missing_links"]:
            for m in result["missing_links"]:
                st.write(f"{m[0]} → {m[2]} (suggested)")
        else:
            st.write("No missing links detected.")

# -------------------------------------------------
# Confidence Evolution
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