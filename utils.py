import streamlit as st
import re
#from ollama_base import send_message, save_conversation (LOCAL API)
from hf_client import send_message, save_conversation
from config import (
    SYSTEM_PROMPT,
    EXIT_KEYWORDS,
    EMAIL_PATTERN,
    PHONE_PATTERN
)

def initialize_session_state():
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        greeting = get_initial_greeting()
        st.session_state.messages.append({
            "role": "assistant",
            "content": greeting
        })

    if 'candidate_data' not in st.session_state:
        st.session_state.candidate_data = {}

    if 'conversation_ended' not in st.session_state:
        st.session_state.conversation_ended = False

def get_initial_greeting():
    return """Hello! Welcome to TalentScout's Hiring Assistant.

I'm here to help you through the initial screening process for our technology positions. This conversation will take about 10-15 minutes.

Here's what we'll do:
1. I'll collect some basic information about you
2. Understand your technical expertise and preferred tech stack
3. Ask a few relevant technical questions to assess your skills

Everything is confidential and compliant with data privacy standards.

Let's begin! What is your full name?"""

### OLLAMA Wrapper Function
def get_ai_response(user_message, conversation_history):
    try:
        response = send_message(
            user_message=user_message,
            conversation_history=conversation_history,
            system_prompt=SYSTEM_PROMPT
        )
        return response
    except Exception as e:
        return f"Error connecting to AI: {str(e)}\n\nPlease check your HUGGINGFACE_API_KEY in .env file"


### INPUT Validation
def validate_email(email):
    if not email or not email.strip():
        return False, "Email address cannot be empty"

    if re.match(EMAIL_PATTERN, email.strip()):
        return True, ""
    else:
        return False, "Please provide a valid email address (e.g., john@example.com)"

def validate_phone(phone):
    if not phone or not phone.strip():
        return False, "Phone cannot be empty"

    cleaned_phone = ""
    for char in phone:
        if char.isdigit() or char == "+":
            cleaned_phone += char

    if re.match(PHONE_PATTERN, cleaned_phone):
        return True, ""
    else:
        return False, "Please provide a valid phone number (e.g., +1-234-567-8900 or +91-1234567890)"

def validate_experience(experience):
    try:
        years = float(experience)
        if years < 0:
            return False, "Years of experience cannot be negative"
        if years > 70:
            return False, "Please enter a realistic number of years"
        return True, ""
    except ValueError:
        return False, "Please enter a valid number (e.g., 5 or 5.5)"

### CONVERSATION management
def check_exit_intent(user_input):
    user_input_lower = user_input.lower().strip()

    # Check for exact matches
    if user_input_lower in EXIT_KEYWORDS:
        return True

    # Check for partial matches
    for keyword in EXIT_KEYWORDS:
        if keyword in user_input_lower and len(user_input_lower) < 50:
            return True

    return False

def generate_farewell_message():
    return """Thank you for your time! 🙏

    **Next Steps:**
    1. ✅ Our team will review your information and responses
    2. 📧 We'll contact you within 3-5 business days
    3. 📞 If selected, you'll be invited for a detailed technical interview

    **Good luck with your application!** 🌟

    Feel free to reach out at careers@talentscout.com if you have any questions."""

### DATA Wrapper
def save_candidate_conversation(candidate_data, conversation_history):
    try:
        filename = save_conversation(
            conversation=conversation_history,
            candidate_data=candidate_data
        )
        return filename
    except Exception as e:
        print(f"Error saving conversation: {e}")
        return None

def extract_candidate_name(conversation_history):
    for msg in conversation_history:
        if msg["role"] == "user":
            content = msg["content"].strip()
            if len(content.split()) <= 5:
                return content
    return None

def format_conversation_for_display(messages):
    formatted = []
    for msg in messages:
        role = "You" if msg["role"] == "user" else "Assistant"
        formatted.append(f"{role}: {msg['content']}")
    return "\n\n".join(formatted)