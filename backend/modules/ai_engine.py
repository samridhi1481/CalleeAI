# Simple AI engine for CalleeAI
# Later we can replace this with Gemini / Llama / local LLM

def generate_reply(user_text: str) -> str:
    user_text = user_text.lower()

    # Basic rule-based bot
    if "hello" in user_text or "hi" in user_text:
        return "Hello! How can I assist you today?"
    if "help" in user_text:
        return "Sure, I’m here to help. Please tell me what you need."
    if "problem" in user_text:
        return "I understand. Can you explain the problem in more detail?"

    # Default reply
    return "Thank you for your message. How can I assist you further?"
