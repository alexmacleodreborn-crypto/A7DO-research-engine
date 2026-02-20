import streamlit as st
import matplotlib.pyplot as plt
from engine import A7DOResearchEngine, Hypothesis

st.set_page_config(layout="wide")
st.title("🧠 A7DO Research Engine v0.1")

# Persistent engine in session
if "engine" not in st.session_state:
    st.session_state.engine = A7DOResearchEngine()

engine = st.session_state.engine

# -----------------------------
# Hypothesis Input
# -----------------------------
st.header("1️⃣ Hypothesis")

hyp_text = st.text_input("Enter hypothesis")

if hyp_text:
    hypothesis = Hypothesis(hyp_text)

    st.header("2️⃣ Add Structural Relations")

    col1, col2, col3 = st.columns(3)

    with col1:
        source = st.text_input("Source")
    with col2:
        relation = st.text_input("Relation")
    with col3:
        target = st.text_input("Target")

    if st.button("Add Relation"):
        engine.add_relation(source, relation, target)
        st.success("Relation added")

    st.header("3️⃣ Run Analysis")

    if st.button("Analyze"):
        result = engine.analyze(hypothesis)

        st.subheader("Z–Σ Output")
        st.write(result)

        if hypothesis.history:
            Z_vals = [h["Z"] for h in hypothesis.history]
            S_vals = [h["Sigma"] for h in hypothesis.history]
            C_vals = [h["confidence"] for h in hypothesis.history]

            fig, ax = plt.subplots()
            ax.plot(C_vals, label="Confidence")
            ax.plot(Z_vals, label="Z")
            ax.plot(S_vals, label="Sigma")
            ax.legend()
            st.pyplot(fig)