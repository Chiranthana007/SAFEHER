# verify_bot.py
# Automated tests to verify SafeHer crisis detection and bot prompt structures.

import sys
from bot import detect_crisis, SYSTEM_PROMPTS, check_ollama_status

def test_crisis_detection():
    print("Running Crisis Detection Tests...")
    
    # Crisis triggers
    crisis_cases = [
        "I want to kill myself",
        "please help me domestic violence",
        "my partner is beating me",
        "he has a gun and is threatening my life",
        "I am feeling suicidal",
        "help I am in immediate danger"
    ]
    
    # Non-crisis triggers
    normal_cases = [
        "How do I file a Zero FIR?",
        "Can you suggest a daily affirmation?",
        "Help me report online cyber fraud",
        "I want to know about my right to privacy",
        "How to do box breathing?"
    ]
    
    failed = 0
    for case in crisis_cases:
        if not detect_crisis(case):
            print(f"❌ FAILED: Crisis not detected for: '{case}'")
            failed += 1
        else:
            print(f"✅ PASSED: Crisis detected for: '{case}'")
            
    for case in normal_cases:
        if detect_crisis(case):
            print(f"❌ FAILED: False positive crisis detected for: '{case}'")
            failed += 1
        else:
            print(f"✅ PASSED: No crisis detected for: '{case}'")
            
    return failed == 0

def test_prompts():
    print("\nRunning Prompt Configuration Tests...")
    if "safety" not in SYSTEM_PROMPTS or "support" not in SYSTEM_PROMPTS:
        print("❌ FAILED: System prompts missing safety or support configurations.")
        return False
    
    if len(SYSTEM_PROMPTS["safety"]) < 100 or len(SYSTEM_PROMPTS["support"]) < 100:
        print("❌ FAILED: System prompts are too short or empty.")
        return False
        
    print("✅ PASSED: System prompts loaded correctly.")
    return True

def test_ollama_connection():
    print("\nChecking local Ollama connection...")
    is_running = check_ollama_status()
    if is_running:
        print("🟢 Ollama is running and accessible at http://localhost:11434")
    else:
        print("🟡 Ollama is offline. SafeHer will run in Heuristic Simulator mode (fallback enabled).")
    return True

if __name__ == "__main__":
    success = True
    if not test_crisis_detection():
        success = False
    if not test_prompts():
        success = False
    test_ollama_connection()
    
    if success:
        print("\n🎉 All automated unit checks passed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Some unit tests failed. Please review errors.")
        sys.exit(1)
