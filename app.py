import streamlit as st
import json
import pandas as pd
import os
from datetime import datetime
import google.generativeai as genai
import re

# ---------------- CONFIG ----------------
st.set_page_config(page_title="AI Recruit Bot")
st.title("🤖 AI Recruit Bot")

# ---------------- GEMINI CONFIG ----------------
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Gemini API key not found in secrets.")
    st.stop()

model = genai.GenerativeModel("models/gemini-2.5-flash")

# ---------------- SAVE FUNCTION ----------------
def save_data(data):
    json_file = "candidates.json"

    if os.path.exists(json_file):
        with open(json_file, "r") as file:
            existing_data = json.load(file)
    else:
        existing_data = []

    existing_data.append(data)

    with open(json_file, "w") as file:
        json.dump(existing_data, file, indent=4)

    df = pd.DataFrame(existing_data)
    df.to_csv("candidates.csv", index=False)

# ---------------- LLM QUESTION GENERATION ----------------
def generate_questions_llm(skills):
    try:
        prompt = f"""
You are a senior technical interviewer.

Based on these candidate skills: {skills}

Generate exactly 5 short technical interview questions.

STRICT RULES:
- Only questions
- No explanation
- No heading
- One question per line
- Do NOT include numbering
"""

        response = model.generate_content(prompt)
        text = response.text.strip()

        # Clean extraction
        lines = text.split("\n")
        questions = []

        for line in lines:
            line = line.strip()

            # Remove numbering if Gemini still adds
            line = re.sub(r'^\d+[\).\-\s]*', '', line)

            if len(line) > 5:
                questions.append(line)

        # Guarantee 5 questions
        if len(questions) < 5:
            questions = questions + ["Explain a project where you used " + skills] * (5-len(questions))

        return questions[:5]

    except Exception as e:
        st.error(f"Gemini Error: {e}")
        return []

# ---------------- SESSION STATE ----------------
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.data = {}
    st.session_state.questions = []
    st.session_state.current_q = 0
    st.session_state.answers = []

# ---------------- STEP FLOW ----------------

# STEP 0 - Greeting
if st.session_state.step == 0:
    st.write("Hello 👋 Welcome to the AI Hiring Assistant.")
    if st.button("Start Application"):
        st.session_state.step = 1
        st.rerun()

# STEP 1 - Name
elif st.session_state.step == 1:
    name = st.text_input("Enter your Full Name")
    if st.button("Next"):
        if name:
            st.session_state.data["Name"] = name
            st.session_state.step = 2
            st.rerun()

# STEP 2 - Email
elif st.session_state.step == 2:
    email = st.text_input("Enter your Email ID")
    if st.button("Next"):
        if email:
            st.session_state.data["Email"] = email
            st.session_state.step = 3
            st.rerun()

# STEP 3 - Phone
elif st.session_state.step == 3:
    phone = st.text_input("Enter your Phone Number")
    if st.button("Next"):
        if phone:
            st.session_state.data["Phone"] = phone
            st.session_state.step = 4
            st.rerun()

# STEP 4 - Skills
elif st.session_state.step == 4:
    skills = st.text_area("Enter your Technical Skills (comma separated)")
    if st.button("Generate Interview Questions"):
        if skills:
            st.session_state.data["Skills"] = skills
            with st.spinner("Generating AI interview questions..."):
                st.session_state.questions = generate_questions_llm(skills)

            if len(st.session_state.questions) == 0:
                st.error("Failed to generate questions. Try again.")
            else:
                st.session_state.step = 5
                st.rerun()

# STEP 5 - Ask Questions
elif st.session_state.step == 5:
    questions = st.session_state.questions
    q_index = st.session_state.current_q

    if q_index < len(questions):
        st.subheader(f"Question {q_index + 1}")
        st.write(questions[q_index])

        answer = st.text_area("Your Answer")

        if st.button("Submit Answer"):
            if answer:
                st.session_state.answers.append({
                    "question": questions[q_index],
                    "answer": answer
                })
                st.session_state.current_q += 1
                st.rerun()

    else:
        st.session_state.data["Interview_QA"] = st.session_state.answers
        st.session_state.data["Timestamp"] = str(datetime.now())

        save_data(st.session_state.data)

        st.session_state.step = 6
        st.rerun()

# STEP 6 - End Message
elif st.session_state.step == 6:
    st.success("✅ Thank you! Your interview responses have been recorded.")
    st.write("Our HR team will review your answers and contact you soon.")
    st.balloons()

    if st.button("New Application"):
        st.session_state.step = 0
        st.session_state.data = {}
        st.session_state.questions = []
        st.session_state.answers = []
        st.session_state.current_q = 0
        st.rerun()