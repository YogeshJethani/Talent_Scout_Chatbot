import streamlit as st
# from ollama_base import test_ollama_connection (Local API)
from hf_client import test_huggingface_connection
from utils import(
initialize_session_state,
    get_initial_greeting,
    get_ai_response,
    check_exit_intent,
    generate_farewell_message,
    save_candidate_conversation
)

st.set_page_config(
    page_title="TalentScout Hiring Assistant",
    page_icon="💼",
    layout="wide"
)

st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
        font-size: 1.1rem;
    }
    .chat-message {
        padding: 1.2rem;
        border-radius: 0.8rem;
        margin-bottom: 1rem;
        line-height: 1.6;
    }
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 20%;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .assistant-message {
        background-color: #f8f9fa;
        border-left: 4px solid #1f77b4;
        margin-right: 20%;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .stProgress > div > div > div > div {
        background-color: #1f77b4;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    ### HEADER
    st.markdown('<h1 class="main-header">💼 TalentScout Hiring Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-Powered Recruitment Screening | Powered by Llama 3 (HuggingFace API)</p>', unsafe_allow_html=True)

    if 'hf_tested' not in st.session_state:
        with st.spinner("🔄 Connecting to Ollama..."):
            if test_huggingface_connection():
                st.session_state.hf_tested = True
            else:
                st.error("❌ Cannot connect to HuggingFace. Please make sure API_KEY is correct.")
                st.stop()

    initialize_session_state()

    ### SIDEBAR
    with st.sidebar:
        st.header("📊 Progress Tracker")

        # Calculate progress based on typical conversation flow
        total_messages = len(st.session_state.messages)
        # Rough estimate: greeting + 7 info fields + 5 tech questions = ~15 messages
        progress = min(total_messages / 15, 1.0)

        st.progress(progress)
        st.write(f"**{total_messages}** messages exchanged")

        st.divider()

        st.header("ℹ️ Information Collected")
        if st.session_state.candidate_data:
            for key, value in st.session_state.candidate_data.items():
                display_key = key.replace('_', ' ').title()
                st.write(f"**{display_key}:**")
                st.info(value)
        else:
            st.info("No information collected yet")

        st.divider()

        st.header("🔒 Privacy & Security")
        st.write("✅ Cloud LLM (Llama 3.1)")
        st.write("✅ Data stored locally")
        st.write("✅ GDPR compliant")
        st.write("✅ HuggingFace API")

        st.divider()

        # Reset button
        if st.button("🔄 Start New Conversation", type="secondary", use_container_width=True):
            st.session_state.messages = []
            st.session_state.candidate_data = {}
            st.session_state.conversation_ended = False
            greeting = get_initial_greeting()
            st.session_state.messages.append({
                "role": "assistant",
                "content": greeting
            })
            st.rerun()

        st.divider()

        # System status
        st.header("🖥️ System Status")
        st.write("**LLM:** Llama 3 (Cloud)")
        st.write("**Status:** 🟢 Connected")

    ### MAIN CHAT
    st.divider()

    # Display chat messages
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]

        if role == "user":
            with st.chat_message("user"):
                st.write(content)
        else:
            with st.chat_message("assistant"):
                st.write(content)

    st.divider()

    ### CHAT INPUT & PROCESSING
    if not st.session_state.conversation_ended:
        user_input = st.chat_input("Type your message here... 💬", key="chat_input")

        if user_input:
            # Add user message to history
            st.session_state.messages.append({
                "role": "user",
                "content": user_input
            })

            # Check for exit intent
            if check_exit_intent(user_input):
                farewell_message = generate_farewell_message()

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": farewell_message
                })
                st.session_state.conversation_ended = True

                # Save candidate data
                filename = save_candidate_conversation(
                    st.session_state.candidate_data,
                    st.session_state.messages
                )

                if filename:
                    st.success(f"✅ Your information has been saved securely!")

                st.rerun()

            else:
                # Get AI response
                with st.spinner("🤔 Thinking..."):
                    try:
                        # Get response from AI
                        bot_response = get_ai_response(
                            user_input,
                            st.session_state.messages[:-1]  # Exclude the message we just added
                        )

                        # Add bot response to history
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": bot_response
                        })

                    except Exception as e:
                        error_message = f"""I apologize, but I'm experiencing technical difficulties.

                        **Error Details:** {str(e)}

                        **Troubleshooting:**
                        1. Check your HUGGINGFACE_API_KEY in .env file
                        2. Verify you have internet connection
                        3. Try again in a few moments

                        Please try again or contact support@talentscout.com"""

                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": error_message
                        })

                st.rerun()

    else:
        st.info("✅ This conversation has ended. Click 'Start New Conversation' in the sidebar to begin again.")

        # Show download option
        if st.session_state.messages:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("📥 Download Conversation Summary", type="primary", use_container_width=True):
                    filename = save_candidate_conversation(
                        st.session_state.candidate_data,
                        st.session_state.messages
                    )
                    if filename:
                        st.success(f"✅ Data saved to: {filename}")

    ### FOOTER
    st.divider()

    st.markdown("""
        <div style='text-align: center; color: #999; font-size: 0.9rem; padding: 1rem;'>
            <strong>TalentScout AI</strong> | Powered by Llama 3 (HuggingFace) | 
            <a href='mailto:support@talentscout.com' style='color: #1f77b4;'>Contact Support</a> | 
            <a href='https://github.com/YogeshJethani/Talent_Scout_Chatbot' style='color: #1f77b4;'>GitHub</a>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()