import streamlit as st
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
import os
from datetime import datetime
from dotenv import load_dotenv
import json

# import streamlit_authenticator as stauth

# Load environment variables from .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize the language model
llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)

# Create a prompt template including mood
prompt_template = PromptTemplate(
    input_variables=["topic", "platform", "mood"],
    template="Create a compelling {platform} post about {topic} in a {mood} tone. The post should be engaging, informative, and appropriate for the platform's style and character limit."
)

# File to store post history
HISTORY_FILE = "post_history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f)

# Load post history
if 'post_history' not in st.session_state:
    st.session_state.post_history = load_history()

# Mood description function
def mood_description(mood):
    if mood <= 3:
        return "sad and serious"
    elif 4 <= mood <= 6:
        return "neutral and balanced"
    elif 7 <= mood <= 8:
        return "happy and positive"
    else:
        return "excited and energetic"

def generate_post(topic, platform, mood):
    mood_desc = mood_description(mood)  # Get mood description based on slider value
    prompt = prompt_template.format(topic=topic, platform=platform, mood=mood_desc)
    response = llm.invoke(prompt)
    return response

# Authentication
def check_password():
    """Returns True if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password incorrect, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True

if check_password():
    # Streamlit app UI
    st.title("Social Media Post Generator")

    # User input
    topic = st.text_input("Enter a topic or interest:")
    platform = st.selectbox("Choose a social media platform:", ["Twitter", "Instagram", "LinkedIn", "Facebook"])
    mood = st.slider("Select your mood (1 = Sad, 10 = Excited)", 1, 10)  # Mood slider

    # Generate post button
    if st.button("Generate Post"):
        if topic:
            post = generate_post(topic, platform, mood)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_post = {
                "timestamp": timestamp, 
                "platform": platform, 
                "topic": topic, 
                "mood": mood_description(mood),  # Store mood description
                "post": post
            }
            st.session_state.post_history.append(new_post)
            save_history(st.session_state.post_history)  # Save to file
            st.success(f"Generated {platform} post (Mood: {mood_description(mood)}):")
            st.write(post)
        else:
            st.warning("Please enter a topic.")

    # Display post history
    st.header("Post History")
    for post in reversed(st.session_state.post_history):
        with st.expander(f"{post['timestamp']} - {post['platform']} post about {post['topic']} (Mood: {post['mood']})"):
            st.write(post['post'])

    # Add a clear history button
    if st.button("Clear History"):
        st.session_state.post_history = []
        save_history([])
        st.success("History cleared!")
