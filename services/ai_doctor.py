import google.generativeai as genai
import os
from models.chat_log import ChatLog
from extensions import db

# Configure API Key (Ensure this is set in your env or config)
# Using the key from previous context
API_KEY = "AIzaSyB0MV2Xa2saNPH38Pg06dVPkZgmx5uwyRA"
genai.configure(api_key=API_KEY)

def get_ai_response(user_id, user_message, profile):
    """
    Generates a medical-safe response using Gemini, 
    contextualized with User Profile data.
    """
    
    # 1. Build Context String
    context_str = "User Profile:\n"
    if profile:
        context_str += (
            f"- Age: {profile.age}\n"
            f"- Gender: {profile.gender}\n"
            f"- Weight: {profile.weight}kg\n"
            f"- Existing Conditions/Injuries: {profile.injury}\n"
            f"- Goal: {profile.goal}\n"
            f"- Diet: {profile.diet_preference}\n"
        )
    else:
        context_str += "No profile data available.\n"

    # 2. Strict System Prompt (Safety First)
    system_instruction = f"""
    You are 'Sehat Sathi', an empathetic AI Health Assistant (Nurse/Guide).
    
    {context_str}

    ### YOUR RULES:
    1. **Role:** You are a caring friend with medical knowledge, NOT a doctor.
    2. **Safety:** NEVER prescribe medication dosages. NEVER diagnose serious diseases (Cancer, Heart Attack, etc.).
    3. **Tone:** Warm, Hinglish (Hindi+English mix allowed if user asks), Simple, and Encouraging.
    4. **Action:** - If the symptom is minor (headache, acidity), suggest home remedies or lifestyle changes compatible with their profile.
       - If the symptom is severe (chest pain, fainting, bleeding), IMMEDIATELY tell them to visit a doctor/hospital.
    5. **Context:** Use the User Profile data. (e.g., If user has knee injury, do not suggest running).

    User Query: "{user_message}"
    
    Reply in a short, helpful paragraph (max 100 words).
    """

    # 3. Call AI Model
    try:
        model = genai.GenerativeModel('gemini-2.5-flash') # Using fast model
        response = model.generate_content(system_instruction)
        ai_text = response.text.strip()
        return ai_text
    except Exception as e:
        return "I am having trouble connecting to the server. Please check your internet or try again later."

def save_chat(user_id, sender, message):
    """Saves chat to DB"""
    try:
        log = ChatLog(user_id=user_id, sender=sender, message=message)
        db.session.add(log)
        db.session.commit()
        return True
    except Exception as e:
        print(f"Chat Save Error: {e}")
        return False