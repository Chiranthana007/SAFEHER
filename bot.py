# bot.py
# Crisis detection logic, system prompts, and Ollama LLM integration for SafeHer.

import re
import requests
import json

# Crisis keywords for instant intercept
CRISIS_KEYWORDS = [
    r"\bkill myself\b",
    r"\bsuicid(e|al)\b",
    r"\bend my life\b",
    r"\bharm myself\b",
    r"\bself[- ]harm\b",
    r"\bbeat(en|ing) me\b",
    r"\bdomestic violence\b",
    r"\bphysically abuse\b",
    r"\brape(d)?\b",
    r"\bassault(ed)?\b",
    r"\bsexual harassment\b",
    r"\bimmediate danger\b",
    r"\bin danger\b",
    r"\bcall the police\b",
    r"\bplease help me\b",
    r"\bthreaten(ed)? my life\b",
    r"\bkidnap(ped)?\b",
    r"\bhostage\b",
    r"\bweapon\b",
    r"\bgun\b",
    r"\bknife\b"
]

def detect_crisis(text: str) -> bool:
    """
    Checks if the user's input contains high-risk keywords indicating a crisis.
    """
    if not text:
        return False
    text = text.lower().strip()
    for pattern in CRISIS_KEYWORDS:
        if re.search(pattern, text):
            return True
    return False

# System prompts for modes
SYSTEM_PROMPTS = {
    "safety": (
        "You are SafeHer, a supportive, compassionate, and highly informative women's safety counselor. "
        "Your goal is to guide women on personal safety, emergency contacts, legal rights, filing complaints, "
        "and cybercrime reporting.\n\n"
        "Guidelines:\n"
        "1. Be reassuring, clear, and highly structured.\n"
        "2. Provide actionable advice: cite laws (like Zero FIR, No Arrest After Sunset) and suggest helplines (like 1091, 112, 1930) where appropriate.\n"
        "3. Use short bullet points and bold text for readability. A user reading this might be in a hurry or anxious.\n"
        "4. If you suspect any immediate danger, immediately remind the user of the red SOS button or to call 112 / 100."
    ),
    "support": (
        "You are SafeHer, a warm, gentle, and deeply empathetic emotional support companion.\n\n"
        "Guidelines:\n"
        "1. Focus on active listening, validation of emotions, and compassionate support.\n"
        "2. Use a soft, encouraging tone. Express warmth, friendship, and understanding (like a comforting hug in text form).\n"
        "3. Help the user reframe negative self-talk, build confidence, or practice stress relief.\n"
        "4. Offer simple coping tips (e.g., 'Let's take a deep breath together' or 'Would you like to try a grounding exercise?').\n"
        "5. Keep responses conversational and comforting. Never give clinical diagnoses, but offer a safe space to vent."
    )
}

# Heuristics-based fallback simulator if Ollama is offline or unavailable
def get_simulation_response(user_input: str, mode: str) -> str:
    user_input = user_input.lower()
    
    if mode == "safety":
        if "fir" in user_input or "police" in user_input or "complain" in user_input:
            return (
                "**Here is information about filing a complaint/FIR:**\n\n"
                "- **Zero FIR**: You can file an FIR at *any* police station, regardless of where the incident happened. They must register it under number '0' and transfer it to the correct station.\n"
                "- **Free Legal Aid**: As a woman, you are entitled to free legal counsel and advice under Section 12 of the Legal Services Act.\n"
                "- **Women Police Officer**: You have the right to record your statement in the presence of a woman police officer at your residence or a place of your choice.\n\n"
                "**Urgent Help:** If you feel unsafe going to the station, dial **112** (Police) or **1091** (Women Helpline) immediately."
            )
        elif "cyber" in user_input or "online" in user_input or "stalk" in user_input or "photo" in user_input or "blackmail" in user_input:
            return (
                "**Here are steps to handle online harassment or cybercrime:**\n\n"
                "1. **Do not delete evidence**: Save screenshots, URLs, chat history, and sender details.\n"
                "2. **Report Online**: Visit the official portal **https://cybercrime.gov.in** and submit a complaint under the 'Report Women/Child Related Crime' section.\n"
                "3. **Call 1930**: For cyber frauds or immediate digital financial scams, call the helpline 1930 immediately.\n"
                "4. **Report on Platform**: Use the platform's 'Report' button to get the content removed.\n\n"
                "You can also contact your local cyber crime cell. Let me know if you need specific advice."
            )
        elif "rights" in user_input or "law" in user_input:
            return (
                "**Important legal rights for women in India:**\n\n"
                "- **Right to No Arrest after Sunset**: Women cannot be arrested between 6 PM and 6 AM except in extraordinary situations with written magistrate permission and a female officer present.\n"
                "- **Right to Privacy**: Your identity in cases of sexual harassment or abuse must be kept strictly confidential under IPC Section 228A.\n"
                "- **Right to Free Assistance**: Government clinics and hospitals must provide free medical aid and first aid immediately to victims of violence.\n\n"
                "Which specific right or law would you like to know more about?"
            )
        else:
            return (
                "I am here to guide you on women's safety, legal rights, and helpline details.\n\n"
                "You can ask me about:\n"
                "- How to report a **cybercrime** or online harassment.\n"
                "- What is a **Zero FIR** and your rights at a police station.\n"
                "- Emergency **helpline numbers** for women or domestic abuse.\n\n"
                "Feel free to ask a specific safety-related question!"
            )
    else:
        # Emotional support mode fallback responses
        if "sad" in user_input or "cry" in user_input or "hurt" in user_input or "lonely" in user_input:
            return (
                "I'm so sorry you're feeling this way, but please know you are not alone. It is completely okay to feel sad or overwhelmed sometimes. "
                "Your feelings are valid, and it takes strength to acknowledge them.\n\n"
                "Please take a gentle breath. If you'd like, you can tell me more about what is making you feel this way, or we can try a simple "
                "breathing exercise to help ease the pressure. I'm right here with you."
            )
        elif "anxious" in user_input or "stress" in user_input or "panic" in user_input or "worry" in user_input:
            return (
                "I hear you, and I can feel how heavy this is for you. Anxiety can feel like a storm, but storms do pass. "
                "Let's try to ground ourselves together.\n\n"
                "- Let's take a deep breath. Inhale for 4 seconds, hold, and release gently.\n"
                "- You can open the **Well-being Space** tab above and try our **Guided Breathing Bubble** or the **5-4-3-2-1 Grounding exercise**.\n\n"
                "I'm here to listen if you want to write down what's on your mind. You are safe here."
            )
        elif "thank" in user_input or "help" in user_input and "friend" in user_input:
            return (
                "You are so welcome! I am always here for you whenever you need a listening ear, a comforting word, or just a quiet space to collect your thoughts. "
                "You are doing great, and I am proud of you."
            )
        else:
            return (
                "Thank you for sharing with me. I'm sending you a big virtual hug! 🌸\n\n"
                "It takes courage to open up. Remember to be gentle with yourself today. You are strong, capable, and worthy of peace.\n\n"
                "If you want to talk about how your day went, something that's stressing you out, or if you just want to read some positive affirmations, I'm here."
            )

def check_ollama_status(url: str = "http://localhost:11434") -> bool:
    """
    Checks if the local Ollama server is running and accessible.
    """
    try:
        response = requests.get(url, timeout=2)
        return response.status_code == 200
    except requests.RequestException:
        return False

def generate_response(prompt: str, history: list, mode: str, model: str, url: str = "http://localhost:11434") -> str:
    """
    Generates a response from the selected Ollama model or falls back to a simulated response if offline.
    """
    if not check_ollama_status(url):
        # Fallback to local heuristic simulator
        return get_simulation_response(prompt, mode)
    
    # Structure system prompt and history for Ollama chat endpoint
    messages = [{"role": "system", "content": SYSTEM_PROMPTS[mode]}]
    
    # Append recent chat history (limit to last 6 messages to stay concise)
    for msg in history[-6:]:
        messages.append({"role": msg["role"], "content": msg["content"]})
        
    # Append current prompt
    messages.append({"role": "user", "content": prompt})
    
    try:
        endpoint = f"{url.rstrip('/')}/api/chat"
        payload = {
            "model": model,
            "messages": messages,
            "stream": False
        }
        
        response = requests.post(endpoint, json=payload, timeout=30)
        if response.status_code == 200:
            result = response.json()
            return result["message"]["content"]
        else:
            return f"Error from Ollama server (Status {response.status_code}).\n\nFallback response:\n{get_simulation_response(prompt, mode)}"
            
    except Exception as e:
        return f"Could not connect to Ollama model. Running fallback:\n\n{get_simulation_response(prompt, mode)}"
