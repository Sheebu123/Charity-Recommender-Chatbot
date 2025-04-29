import streamlit as st
import google.generativeai as genai

# Config Gemini
genai.configure(api_key="AIzaSyBB15keH-fj3pDgjSJAk_uOid_nSKTdlUw")

# Load the model
model = genai.GenerativeModel(model_name="gemini-1.5-pro")

# Page config
st.set_page_config(page_title="Charity Recommender", page_icon="🎁", layout="centered")

# Sidebar interactivity
st.sidebar.title("Customize Your Experience 🎛️")
selected_cause = st.sidebar.selectbox("Choose a cause you're interested in:", [
    "Children's Education", 
    "Animal Welfare", 
    "Healthcare", 
    "Women Empowerment", 
    "Disaster Relief", 
    "Environmental Protection"
])
urgency = st.sidebar.slider("How urgent is your need for suggestions?", 1, 10, 5)
show_suggestions = st.sidebar.button("Use Selected Cause")

if show_suggestions:
    st.session_state["user_input"] = f"I want to donate to {selected_cause.lower()}"

# Header
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🤖 Charity Recommender Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Helping you find the best charities to support</p>", unsafe_allow_html=True)

# Suggested prompts
suggested_prompts = [
    "I want to donate to children's education",
    "Suggest a charity for animal welfare",
    "I want to donate to health related",
    "Any trusted charity for women empowerment?"
]

st.markdown("### 💡 Try a Suggested Prompt:")
cols = st.columns(4)
for i, prompt in enumerate(suggested_prompts):
    with cols[i]:
        if st.button(prompt):
            st.session_state["user_input"] = prompt

# Input box
user_input = st.text_input("🗣️ Ask your question below", key="user_input")

# Relevancy check
def is_relevant_query(query):
    keywords = ['charity', 'donate', 'help', 'support', 'contribute', 'non-profit']
    return any(word in query.lower() for word in keywords)

# Response
if user_input:
    st.markdown("----")
    with st.spinner("Thinking... 💭"):
        if is_relevant_query(user_input):
            response = model.generate_content(f"You are a charity recommender bot. Based on the following user interest (urgency level {urgency}/10), suggest 3-4 trusted charities with brief descriptions and their websites if available:\n\n{user_input}")
            st.success("✅ Suggestions:")
            st.markdown(response.text)
        else:
            st.warning("❗🔍 I'm here to help with charity and donation-related questions. Try asking about a cause you care about, like education, health, or animals! 🐾📚❤️")
