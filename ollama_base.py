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

if __name__ == "__main__":
    result = test_ollama_connection()

    if result:
        print("TEST PASSED - Ready to go!")
    else:
        print("TEST FAILED - Check errors above")