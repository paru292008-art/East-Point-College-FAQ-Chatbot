import streamlit as st
import speech_recognition as sr
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS
from io import BytesIO

st.set_page_config(page_title="East Point College FAQ", page_icon="🎓")
st.markdown("""
<style>
.stApp p,
.stApp span,
.stApp label,
.stApp div[data-testid="stMarkdownContainer"] {
    color: #000000 !important;
    font-size: 18px !important;
    font-weight: 800 !important;
    opacity: 1 !important;
}
.stApp p,
.stApp span,
.stApp label,
.stApp div[data-testid="stMarkdownContainer"] {
    color: #1A1A1A !important;
    font-weight: 700 !important;
}
.stApp {
    background-color: #f4f7fb;
}
.stApp, .stApp p, .stApp span, .stApp label {
    color: #000000 !important;
    font-weight: 600 !important;
}
h1 {
    color: #123b66;
    text-align: center;
}
h2, h3 {
    color: #245580;
}
.stTextInput input {
    border-radius: 12px;
}
.stButton button {
    background-color: #70452F;
    color: white;
    border-radius: 10px;
    border: none;
}
</style>
""", unsafe_allow_html=True)

st.title("🎓 East Point College of Engineering and Technology")
st.subheader("AI-Powered College FAQ Chatbot")

st.write("Welcome! Ask me about fees, courses, hostel and transport.")
st.info("Choose a topic, type your question or speak using the microphone.")

def get_answer(question):
    q = question.lower()

    if "fee" in q or "fees" in q or "cet" in q:
        if "management" in q:
            return """Management Quota Fees (2025-26):

CSE: ₹14,26,500
CSE (AI & ML): ₹14,26,500
CSE (Data Science): ₹14,26,500
CSE (IoT & Cyber Security): ₹13,26,500
ISE: ₹12,26,500
ECE: ₹9,76,500
Civil: ₹6,01,500
M.Tech: ₹2,01,500

Hostel, transport and mess fees are separate."""

        return """CET Quota Fees (2024-25):

UG courses: ₹1,21,610
PG courses: ₹80,110

Please confirm the applicable course and academic year with the college."""

    elif "management" in q:
        return get_answer("management fees")

    elif "course" in q or "branch" in q:
        return """Engineering Courses:

1. Computer Science and Engineering (CSE)
2. CSE - Artificial Intelligence and Machine Learning
3. CSE - Data Science
4. CSE - IoT and Cyber Security
5. Information Science and Engineering (ISE)
6. Electronics and Communication Engineering (ECE)
7. Civil Engineering
8. M.Tech - Product Design and Manufacturing
9. M.Tech - Construction Technology"""

    elif "hostel" in q:
        return "Hostel information: Please contact the college office for accommodation, facilities and fees."

    elif "transport" in q or "bus" in q:
        return "Transport information: Please contact the college office for bus routes, timings and transport fees."

    elif "admission" in q:
        return "For admission details, please contact the college admission office."

    elif "timing" in q or "time" in q:
        return "Please contact the college office for the latest college timings."

    else:
        return "Sorry, I don't have that information yet. Please ask about fees, courses, hostel or transport."


# Quick question buttons
for topic in ["Fees", "Courses", "Hostel", "Transport", "Admissions"]:
    if st.button(topic):
        st.session_state.answer = get_answer(topic)


# Voice input
st.subheader("🎙️ Ask using your voice")

audio = mic_recorder(
    start_prompt="Start Recording",
    stop_prompt="Stop Recording",
    just_once=True,
    key="voice_recorder")


if audio and audio.get("bytes"):
    try:
        recognizer = sr.Recognizer()

        recorded_audio = sr.AudioData(
    audio["bytes"],
    audio["sample_rate"],
    audio["sample_width"])


        spoken_question = recognizer.recognize_google(
            recorded_audio,
            language="en-IN")
        

        st.success("You said: " + spoken_question)
        st.session_state.question = spoken_question
        st.session_state.answer = get_answer(spoken_question)

    except sr.UnknownValueError:
        st.warning("Sorry, I could not understand your voice. Please try again.")

    except sr.RequestError:
        st.error("Speech recognition needs an internet connection.")

    except Exception as e:
        st.error("Voice input error: " + str(e))


# Text input
st.subheader("Or type your question")
question = st.text_input(
    "Ask your question here:",
    key="question",
    placeholder="Type your question about East Point College...",
    help="Ask about fees, courses, hostel or transport."
)

if st.button("Submit"):
    if question.strip():
        st.session_state.answer = get_answer(question)
    else:
        st.warning("Please type or speak a question.")


# Display answer and voice output
if "answer" in st.session_state:
    st.subheader("🤖 Chatbot Answer")
    st.write(st.session_state.answer)

    try:
        speech = gTTS(
            text=st.session_state.answer,
            lang="en"
        )

        audio_file = BytesIO()
        speech.write_to_fp(audio_file)

        st.subheader("🔊 Listen to the Answer")
        st.audio(audio_file.getvalue(), format="audio/mp3")

    except Exception:
        st.warning("Voice output needs an internet connection.")
st.subheader("⭐ Rate Our Chatbot")

rating = st.radio(
    "How would you rate our chatbot?",
    ["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"]
)

if st.button("Submit Rating"):
    st.success("Thank you for rating our chatbot!")
