import google.generativeai as genai
import json
import os
import time

# --- CONFIGURATION ---
API_KEY = "AIzaSyB0MV2Xa2saNPH38Pg06dVPkZgmx5uwyRA"
genai.configure(api_key=API_KEY)

def generate_ai_plan(profile):
    """
    Generates a Context-Aware User Plan:
    1. Workout: Adapts to Environment & Goal.
    2. Schedule: Full 7-Day Plan (Detailed).
    3. Nutrition: Smart Macros + Micros + Timing.
    """
    
    # 1. SAFER DATA EXTRACTION
    env = getattr(profile, 'workout_environment', 'Gym') 
    level = getattr(profile, 'experience_level', 'Beginner')
    
    # 2. CONTEXT BUILDING
    user_context = (
        f"USER PROFILE:\n"
        f"- Goal: {profile.goal} (CRITICAL: Adjust Volume & Intensity for this)\n"
        f"- Environment: {env} (CRITICAL: Use ONLY equipment found here)\n"
        f"- Experience: {level}\n"
        f"- Injury: {profile.injury} (SAFETY: Swap dangerous moves)\n"
        f"- Diet: {profile.diet_preference}\n"
        f"- Stats: {profile.weight}kg, {profile.height}cm, {profile.gender}\n"
    )

    # 3. MASTER PROMPT (Now enforces 5-6 exercises per day & Intensity)
    system_instruction = f"""
    You are 'Sehat Sathi', an expert AI Trainer. Generate a detailed weekly plan.

    ### A. WORKOUT RULES:
    1. **Structure:** Provide a FULL 7-Day Plan (Mon-Sun).
    2. **Volume:** Each workout day MUST have **5 to 6 exercises**.
    3. **Intensity Guide:** For every exercise, specify the 'intensity' (e.g., "Heavy / RPE 9", "Moderate", "Bodyweight", "To Failure").
    
    ### B. ENVIRONMENT LOGIC:
    - **Gym:** Use machines, barbells, dumbbells. (Split: Double Body Part Split).
    - **Home:** Bodyweight, Bands, Furniture. (Split: Upper/Lower or Full Body).
    - **Yoga:** Vinyasa, Hatha, Restorative flows.

    ### C. GOAL LOGIC:
    - **Powerlifting:** Low Reps (3-5), High Weight (RPE 8-9), Long Rest.
    - **Hypertrophy:** Moderate Reps (8-12), Moderate Weight, Focus on Squeeze.
    - **Weight Loss:** High Reps (15+), Low Rest, High Intensity (HIIT).

    ### OUTPUT FORMAT (Strict JSON):
    {{
        "analysis": {{
            "macro_goals": {{ "calories": 2000, "protein": "150g", "carbs": "200g", "fats": "60g" }},
            "safety_alerts": ["..."]
        }},
        "nutrition": {{
            "breakfast": "...",
            "lunch": "...",
            "pre_workout": "...",
            "post_workout": "...",
            "dinner": "...",
            "micro_focus": [ {{ "nutrient": "...", "reason": "...", "source": "..." }} ],
            "timing_rules": ["...", "..."]
        }},
        "workout": {{
            "environment_used": "{env}",
            "split_name": "...",
            "schedule": {{
                "Monday": {{ 
                    "focus": "...", 
                    "exercises": [ 
                        {{ "name": "Exercise Name", "sets": "3", "reps": "8-12", "intensity": "Moderate (RPE 7)" }},
                        {{ "name": "Next Exercise", "sets": "3", "reps": "...", "intensity": "..." }}
                    ] 
                }},
                "Tuesday": {{ "focus": "...", "exercises": [] }},
                "Wednesday": {{ "focus": "...", "exercises": [] }},
                "Thursday": {{ "focus": "...", "exercises": [] }},
                "Friday": {{ "focus": "...", "exercises": [] }},
                "Saturday": {{ "focus": "...", "exercises": [] }},
                "Sunday": {{ "focus": "Rest", "exercises": [] }}
            }}
        }}
    }}
    """
    
    # 4. GENERATION
    models_to_try = [
        'gemini-2.5-flash',
    ]

    print(f"\n🤖 Sehat Sathi: Generating Detailed {env} Plan for {profile.goal}...")

    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            full_prompt = user_context + "\n" + system_instruction
            
            response = model.generate_content(full_prompt)
            clean_text = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_text)
        except Exception as e:
            print(f"⚠️ {model_name} error/busy. Trying next...")
            time.sleep(1)

    return {"error": "AI Service Unavailable"}