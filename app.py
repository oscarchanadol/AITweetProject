import streamlit as st
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
import os
from datetime import datetime
# from apikey import apikey
from dotenv import load_dotenv

# Set up OpenAI API key
# os.environ["OPENAI_API_KEY"] = apikey
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize the language model
llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
# llm = OpenAI(temperature=0.7)

# Create a prompt template including mood
prompt_template = PromptTemplate(
    input_variables=["topic", "platform", "mood"],
    template="Create a compelling {platform} post about {topic} in a {mood} tone. The post should be engaging, informative, and appropriate for the platform's style and character limit."
)

# Initialize session state for post history
if 'post_history' not in st.session_state:
    st.session_state.post_history = []

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
        st.session_state.post_history.append({
            "timestamp": timestamp, 
            "platform": platform, 
            "topic": topic, 
            "mood": mood_description(mood),  # Store mood description
            "post": post
        })
        st.success(f"Generated {platform} post (Mood: {mood_description(mood)}):")
        st.write(post)
    else:
        st.warning("Please enter a topic.")

# Display post history
st.header("Post History")
for post in reversed(st.session_state.post_history):
    with st.expander(f"{post['timestamp']} - {post['platform']} post about {post['topic']} (Mood: {post['mood']})"):
        st.write(post['post'])