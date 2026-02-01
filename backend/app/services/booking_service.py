import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Fetch keys from environment variables
BLAND_API_KEY = os.getenv("BLAND_API_KEY")
BLAND_VOICE_ID = os.getenv("BLAND_VOICE_ID") 
MY_NUMBER = os.getenv("MY_NUMBER")

def trigger_call(to_number: str, restaurant_name: str) -> dict:
    if not BLAND_API_KEY:
        raise ValueError("Missing configuration: Ensure BLAND_API_KEY is set in .env")

    # Bland AI API Endpoint
    url = "https://api.bland.ai/v1/calls"
    
    headers = {
        "authorization": BLAND_API_KEY,
        "Content-Type": "application/json"
    }
    
    # French prompt - James parle français
    strict_prompt = (
        "Tu es James, un assistant personnel charmant et confiant. "
        "Ton SEUL OBJECTIF est de réserver une table chez Nando's pour 2 personnes à 20h ce soir. "
        "NE FAIS PAS l'AI générique. NE DIS PAS 'Comment puis-je vous aider?'. "
        "Tu parles avec le personnel du restaurant maintenant. "
        "1. Demande la table poliment mais fermement. "
        "2. Si on te demande un nom, dis 'Tyrone'. "
        "3. Si c'est confirmé, dis 'Parfait, à ce soir!' et TERMINE L'APPEL. "
        "4. S'ils disent non, demande pour 21h. "
        "Garde tes réponses courtes (moins de 20 mots). Parle comme un vrai parisien."
    )

    # Payload for Bland AI
    payload = {
        "phone_number": MY_NUMBER, # Override destination for demo
        "task": strict_prompt,
        
        "first_sentence": f"Allô? C'est bien {restaurant_name}? Je voudrais réserver une table s'il vous plaît.",
        
        "max_duration": 4, # minutes
        "record": True,
        
        "language": "fr", 
        "wait_for_greeting": False 
    }
    
    # Add voice ID if provided (Make sure this ID supports French for best results!)
    if BLAND_VOICE_ID:
        payload["voice"] = BLAND_VOICE_ID

    print(f">> Triggering French Bland AI call to {MY_NUMBER} (Demo override for {restaurant_name})...")
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error triggering call: {e}")
        if 'response' in locals() and response is not None:
             print(f"Response content: {response.content}")
        raise RuntimeError(f"Failed to trigger call: {e}")

# --- EXECUTION ---
if __name__ == "__main__":
    # You can change "Nando's" to something French like "Le Bistro" if you want
    trigger_call(MY_NUMBER, "Nando's")