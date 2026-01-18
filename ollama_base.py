import requests
import json
from datetime import datetime

OLLAMA_HOST = "http://localhost:11434"
OLLAMA_MODEL = "llama3"
OLLAMA_TIMEOUT = 60

def test_ollama_connection():
    try:
        response = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        response.raise_for_status()

        models = response.json().get("models", [])
        model_names = [model.get("name") for model in models]

        print("Connected to OLLAMA")
        print(f"Available models: {', '.join(model_names)}")

        if OLLAMA_MODEL in model_names or any(OLLAMA_MODEL in name for name in model_names):
            print(f"{OLLAMA_MODEL} is ready")
            return True
        else:
            print(f"{OLLAMA_MODEL} is not ready")
            return False

    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Ollama. Is it running?")
        print("   Run: ollama serve")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def send_message(user_message, conversation_history=None, system_prompt=None):
    messages = []

    if system_prompt:
        messages.append({
            "role": "system",
            "content": system_prompt
        })

    if conversation_history:
        messages.extend(conversation_history)

    messages.append({
        "role": "user",
        "content": user_message
    })

    #Call OLLAMA API
    response = requests.post(
        f"{OLLAMA_HOST}/api/chat",
        json={
            "model": OLLAMA_MODEL,
            "messages": messages,
            "stream": False
        },
        timeout=60
    )

    # Extract AI response
    result = response.json()
    ai_response = result["message"]["content"]

    return ai_response

def save_conversation(conversation, candidate_data=None, filename=None):
    import os
    os.makedirs("data", exist_ok=True)

    # Generate timestamp ONCE
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    datetime_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not filename:
        # Extract candidate name if available
        if candidate_data and "name" in candidate_data:
            # Clean the name (remove spaces, special chars)
            name = candidate_data["name"].strip().replace(" ", "_")
            # Remove any special characters that might break filenames
            name = "".join(c for c in name if c.isalnum() or c == "_")
            filename = f"data/{name}_{timestamp}.json"
        else:
            # Fallback to "candidate" if no name available
            filename = f"data/candidate_{timestamp}.json"

    # Prepare data to save
    data = {
        "timestamp": datetime_str,
        "candidate_info": candidate_data or {},
        "conversation": conversation,
        "total_messages": len(conversation)
    }

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Saved to filename: {filename}")
    return(filename)