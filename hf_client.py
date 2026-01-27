import os
import json
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
HUGGINGFACE_MODEL = os.getenv("HUGGINGFACE_MODEL", "meta-llama/Llama-3.1-8B-Instruct:novita")

# Initialize OpenAI client with HuggingFace endpoint
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HUGGINGFACE_API_KEY,
)

def test_huggingface_connection():
    try:
        if not HUGGINGFACE_API_KEY:
            print("❌ HUGGINGFACE_API_KEY not found in .env file")
            return False

        print(f"API Key found: {HUGGINGFACE_API_KEY[:10]}...")
        print(f"Testing model: {HUGGINGFACE_MODEL}")

        # Simple test request
        response = client.chat.completions.create(
            model=HUGGINGFACE_MODEL,
            messages=[
                {"role": "user", "content": "Hello"}
            ],
            max_tokens=10
        )

        if response.choices[0].message.content:
            print("Connected to HuggingFace API")
            print(f"Model: {HUGGINGFACE_MODEL}")
            return True
        else:
            print("Empty response from API")
            return False

    except Exception as e:
        print(f"Connection error: {e}")
        return False

def send_message(user_message, conversation_history=None, system_prompt=None):
    try:
        # Build messages array
        messages = []

        # Add system prompt
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })

        # Add conversation history (last 5 messages for context)
        if conversation_history:
            for msg in conversation_history[-5:]:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })

        # Add current user message
        messages.append({
            "role": "user",
            "content": user_message
        })

        # Make API request
        response = client.chat.completions.create(
            model=HUGGINGFACE_MODEL,
            messages=messages,
            max_tokens=500,
            temperature=0.7,
            top_p=0.9
        )

        # Extract response
        ai_response = response.choices[0].message.content
        return ai_response.strip() if ai_response else "No response generated"

    except Exception as e:
        return f"Error: {str(e)}"

def save_conversation(conversation, candidate_data=None, filename=None):
    try:
        os.makedirs("data", exist_ok=True)

        timestamp = datetime.now()

        if not filename:
            if candidate_data and "name" in candidate_data:
                name = candidate_data["name"].strip().replace(" ", "_")
                name = "".join(c for c in name if c.isalnum() or c == "_")
                filename = f"data/{name}_{timestamp.strftime('%Y%m%d_%H%M%S')}.json"
            else:
                filename = f"data/candidate_{timestamp.strftime('%Y%m%d_%H%M%S')}.json"

        data = {
            "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "candidate_info": candidate_data or {},
            "conversation": conversation,
            "total_messages": len(conversation),
            "llm_provider": "HuggingFace (OpenAI-compatible)",
            "model": HUGGINGFACE_MODEL
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"Saved to filename: {filename}")
        return filename

    except Exception as e:
        print(f"Error saving conversation: {e}")
        return None