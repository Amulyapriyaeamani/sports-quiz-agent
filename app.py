import json
import streamlit as st

from src.generator import generate_quiz

# ==================================================
# Page Configuration
# ==================================================
st.set_page_config(
    page_title="AI Sports Quiz Generator",
    page_icon="🏆",
    layout="wide"
)

# ==================================================
# Session State
# ==================================================
if "quiz" not in st.session_state:
    st.session_state.quiz = None

# ==================================================
# Header
# ==================================================
st.title("🏆 AI Sports Quiz Generator")

st.markdown("""
Generate AI-powered sports quizzes using:

- 📚 Historical Sports Knowledge (ChromaDB)
- 🌐 Live Sports News (DuckDuckGo Search)
- 🤖 Google Gemini
""")

# ==================================================
# Sidebar
# ==================================================
st.sidebar.title("⚙️ Quiz Settings")

sport = st.sidebar.selectbox(
    "Select Sport",
    ["Cricket", "Football", "Tennis", "Basketball"]
)

difficulty = st.sidebar.selectbox(
    "Select Difficulty",
    ["Easy", "Medium", "Hard"]
)

generate = st.sidebar.button("🚀 Generate Quiz")

st.sidebar.markdown("---")

st.sidebar.info("""
### About

This project combines:

- ChromaDB
- Google Gemini
- DuckDuckGo Search
- Streamlit

to generate AI-powered sports quizzes using Retrieval-Augmented Generation (RAG).
""")

# ==================================================
# Generate Quiz
# ==================================================
if generate:

    with st.spinner("Generating quiz..."):

        try:
            st.session_state.quiz = generate_quiz(
                sport,
                difficulty
            )

            st.success("Quiz generated successfully!")

        except Exception as e:
            st.error(f"Error generating quiz:\n\n{e}")

# ==================================================
# Display Quiz
# ==================================================
if st.session_state.quiz is not None:

    quiz = st.session_state.quiz

    st.markdown("---")

    st.subheader(
        f"🏏 {quiz['sport']} | 🎯 {quiz['difficulty']}"
    )

    total_questions = len(quiz["questions"])

    for i, question in enumerate(quiz["questions"], start=1):

        st.markdown("---")

        progress = i / total_questions
        st.progress(progress)

        st.caption(f"Question {i} of {total_questions}")

        st.markdown(f"### Question {i}")

        st.write(question["question"])

        st.radio(
            "Choose your answer",
            options=list(question["options"].keys()),
            format_func=lambda x, q=question: f"{x}. {q['options'][x]}",
            key=f"question_{i}"
        )

    st.markdown("---")

    # ==================================================
    # Submit Quiz
    # ==================================================
    if st.button("✅ Submit Quiz"):

        score = 0

        st.header("🏆 Results")

        for i, question in enumerate(quiz["questions"], start=1):

            selected = st.session_state[f"question_{i}"]

            if selected == question["correct_answer"]:

                score += 1

                st.success(f"Question {i}: Correct ✅")

            else:

                st.error(f"Question {i}: Incorrect ❌")

                st.write(
                    f"**Correct Answer:** {question['correct_answer']}"
                )

            st.info(question["explanation"])

        st.markdown("---")

        percentage = (score / total_questions) * 100

        st.header(
            f"🎯 Final Score: {score}/{total_questions}"
        )

        st.progress(score / total_questions)

        st.write(f"### Percentage: **{percentage:.0f}%**")

        st.download_button(
            label="📥 Download Quiz (JSON)",
            data=json.dumps(quiz, indent=4),
            file_name="sports_quiz.json",
            mime="application/json"
        )

    st.markdown("---")

    if st.button("🔄 Generate New Quiz"):

        st.session_state.quiz = None

        for key in list(st.session_state.keys()):
            if key.startswith("question_"):
                del st.session_state[key]

        st.rerun()