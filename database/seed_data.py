import sys
import os

# --- FIX: Add Parent Directory to Path ---
# Ye line python ko batati hai ki 'app' module ek folder upar (root mein) hai
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# -----------------------------------------

from app import create_app
from database.db import db
from models.diet import Diet
from models.workout import Workout
from models.health_history import HealthHistory
from models.health_profile import HealthProfile

app = create_app()

def seed():
    with app.app_context():
        # 1. Clear Old Data
        print("🗑️  Cleaning old database...")
        # Tables ko sahi order mein clear karein taaki Foreign Key error na aaye
        try:
            db.session.query(HealthHistory).delete()
            db.session.query(HealthProfile).delete()
            db.session.query(Diet).delete()
            db.session.query(Workout).delete()
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("⚠️ Table clear karte waqt koi issue nahi, naye tables create kar rahe hain...")

        # Tables create karein (Just in case woh exist na karte hon)
        db.create_all()
        
        # ==========================================
        # 🍎 SECTION 1: MASTER FOOD LIST (BASE DATA)
        # ==========================================
        print("🍎 Preparing Master Food List...")

        base_foods = [
            # --- INDIAN BREADS (Roti/Paratha) ---
            {"name": "Roti (Whole Wheat)", "cal": 100, "pro": 3, "carbs": 18, "fat": 1, "is_veg": True, "restricted_for": "None", "tag": "bread"},
            {"name": "Butter Naan", "cal": 280, "pro": 5, "carbs": 45, "fat": 10, "is_veg": True, "restricted_for": "Weight, Heart", "tag": "bread"},
            {"name": "Garlic Naan", "cal": 290, "pro": 5, "carbs": 46, "fat": 11, "is_veg": True, "restricted_for": "Weight", "tag": "bread"},
            {"name": "Missi Roti", "cal": 140, "pro": 6, "carbs": 20, "fat": 4, "is_veg": True, "restricted_for": "None", "tag": "bread"},
            {"name": "Bajra Roti", "cal": 120, "pro": 4, "carbs": 22, "fat": 2, "is_veg": True, "restricted_for": "None", "tag": "bread"},
            {"name": "Makki Ki Roti", "cal": 180, "pro": 4, "carbs": 30, "fat": 6, "is_veg": True, "restricted_for": "Weight", "tag": "bread"},
            {"name": "Bhatura (Fried)", "cal": 350, "pro": 6, "carbs": 50, "fat": 18, "is_veg": True, "restricted_for": "Weight, Heart, BP", "tag": "snack"},
            
            # --- RICE items ---
            {"name": "Jeera Rice", "cal": 260, "pro": 4, "carbs": 55, "fat": 4, "is_veg": True, "restricted_for": "Sugar", "tag": "rice"},
            {"name": "Biryani (Veg)", "cal": 300, "pro": 6, "carbs": 50, "fat": 10, "is_veg": True, "restricted_for": "Weight", "tag": "rice"},
            {"name": "Biryani (Chicken)", "cal": 400, "pro": 20, "carbs": 45, "fat": 15, "is_veg": False, "restricted_for": "Weight", "tag": "rice"},
            {"name": "Lemon Rice", "cal": 280, "pro": 5, "carbs": 50, "fat": 8, "is_veg": True, "restricted_for": "None", "tag": "rice"},
            {"name": "Khichdi", "cal": 180, "pro": 7, "carbs": 30, "fat": 4, "is_veg": True, "restricted_for": "None", "tag": "rice"},

            # --- DALS & CURRIES (Gravy) ---
            {"name": "Dal Tadka", "cal": 180, "pro": 12, "carbs": 25, "fat": 6, "is_veg": True, "restricted_for": "None", "tag": "gravy"},
            {"name": "Dal Fry (Butter)", "cal": 250, "pro": 12, "carbs": 25, "fat": 14, "is_veg": True, "restricted_for": "Weight", "tag": "gravy"},
            {"name": "Dal Makhani", "cal": 350, "pro": 14, "carbs": 30, "fat": 18, "is_veg": True, "restricted_for": "Weight, Heart", "tag": "gravy"},
            {"name": "Chana Masala", "cal": 260, "pro": 15, "carbs": 38, "fat": 7, "is_veg": True, "restricted_for": "Gas", "tag": "gravy"},
            {"name": "Rajma", "cal": 280, "pro": 14, "carbs": 40, "fat": 8, "is_veg": True, "restricted_for": "Gas", "tag": "gravy"},
            {"name": "Paneer Butter Masala", "cal": 350, "pro": 16, "carbs": 20, "fat": 25, "is_veg": True, "restricted_for": "Weight, Heart", "tag": "gravy"},
            {"name": "Kadai Paneer", "cal": 280, "pro": 18, "carbs": 15, "fat": 18, "is_veg": True, "restricted_for": "None", "tag": "gravy"},
            {"name": "Matar Paneer", "cal": 260, "pro": 16, "carbs": 18, "fat": 15, "is_veg": True, "restricted_for": "None", "tag": "gravy"},
            {"name": "Aloo Gobi", "cal": 180, "pro": 4, "carbs": 25, "fat": 8, "is_veg": True, "restricted_for": "None", "tag": "gravy"},
            {"name": "Malai Kofta", "cal": 400, "pro": 10, "carbs": 35, "fat": 28, "is_veg": True, "restricted_for": "Weight, Heart", "tag": "gravy"},
            {"name": "Sarson Ka Saag", "cal": 200, "pro": 6, "carbs": 15, "fat": 14, "is_veg": True, "restricted_for": "None", "tag": "gravy"},

            # --- BREAKFAST & SNACKS ---
            {"name": "Poha", "cal": 250, "pro": 5, "carbs": 45, "fat": 8, "is_veg": True, "restricted_for": "None", "tag": "breakfast"},
            {"name": "Upma", "cal": 220, "pro": 6, "carbs": 40, "fat": 6, "is_veg": True, "restricted_for": "None", "tag": "breakfast"},
            {"name": "Idli", "cal": 60, "pro": 2, "carbs": 12, "fat": 0, "is_veg": True, "restricted_for": "None", "tag": "breakfast"},
            {"name": "Dosa (Plain)", "cal": 180, "pro": 4, "carbs": 30, "fat": 5, "is_veg": True, "restricted_for": "None", "tag": "breakfast"},
            {"name": "Masala Dosa", "cal": 350, "pro": 6, "carbs": 50, "fat": 12, "is_veg": True, "restricted_for": "Weight", "tag": "breakfast"},
            {"name": "Vada Sambhar", "cal": 300, "pro": 8, "carbs": 35, "fat": 15, "is_veg": True, "restricted_for": "Weight, Heart", "tag": "breakfast"},
            {"name": "Dhokla", "cal": 150, "pro": 6, "carbs": 20, "fat": 5, "is_veg": True, "restricted_for": "None", "tag": "snack"},
            {"name": "Samosa", "cal": 260, "pro": 4, "carbs": 30, "fat": 16, "is_veg": True, "restricted_for": "Weight, Heart, BP", "tag": "snack"},
            {"name": "Kachori", "cal": 280, "pro": 5, "carbs": 32, "fat": 18, "is_veg": True, "restricted_for": "Weight, Heart, BP", "tag": "snack"},
            {"name": "Pakora (Mix Veg)", "cal": 200, "pro": 4, "carbs": 25, "fat": 12, "is_veg": True, "restricted_for": "Weight, Heart", "tag": "snack"},
            {"name": "Pani Puri (6 pcs)", "cal": 120, "pro": 2, "carbs": 25, "fat": 4, "is_veg": True, "restricted_for": "None", "tag": "snack"},
            {"name": "Bhel Puri", "cal": 180, "pro": 4, "carbs": 35, "fat": 5, "is_veg": True, "restricted_for": "None", "tag": "snack"},
            {"name": "Vada Pav", "cal": 300, "pro": 6, "carbs": 45, "fat": 12, "is_veg": True, "restricted_for": "Weight", "tag": "snack"},

            # --- NON-VEG ---
            {"name": "Butter Chicken", "cal": 450, "pro": 25, "carbs": 15, "fat": 30, "is_veg": False, "restricted_for": "Weight, Heart", "tag": "gravy"},
            {"name": "Chicken Tikka Masala", "cal": 350, "pro": 30, "carbs": 10, "fat": 20, "is_veg": False, "restricted_for": "None", "tag": "gravy"},
            {"name": "Tandoori Chicken", "cal": 280, "pro": 35, "carbs": 5, "fat": 12, "is_veg": False, "restricted_for": "None", "tag": "starter"},
            {"name": "Chicken Curry", "cal": 300, "pro": 28, "carbs": 10, "fat": 15, "is_veg": False, "restricted_for": "None", "tag": "gravy"},
            {"name": "Mutton Rogan Josh", "cal": 500, "pro": 25, "carbs": 12, "fat": 40, "is_veg": False, "restricted_for": "Weight, Heart, BP", "tag": "gravy"},
            {"name": "Fish Curry", "cal": 280, "pro": 25, "carbs": 8, "fat": 15, "is_veg": False, "restricted_for": "None", "tag": "gravy"},
            {"name": "Grilled Fish", "cal": 200, "pro": 30, "carbs": 0, "fat": 8, "is_veg": False, "restricted_for": "None", "tag": "starter"},
            {"name": "Egg Curry", "cal": 250, "pro": 14, "carbs": 8, "fat": 18, "is_veg": False, "restricted_for": "None", "tag": "gravy"},
            {"name": "Omelette (2 Eggs)", "cal": 200, "pro": 14, "carbs": 2, "fat": 15, "is_veg": False, "restricted_for": "None", "tag": "breakfast"},

            # --- WESTERN / FANCY ---
            {"name": "Grilled Sandwich", "cal": 250, "pro": 8, "carbs": 35, "fat": 10, "is_veg": True, "restricted_for": "None", "tag": "breakfast"},
            {"name": "Pizza Slice", "cal": 280, "pro": 10, "carbs": 30, "fat": 12, "is_veg": True, "restricted_for": "Weight, Heart", "tag": "fastfood"},
            {"name": "Pasta (Red Sauce)", "cal": 300, "pro": 8, "carbs": 50, "fat": 8, "is_veg": True, "restricted_for": "Weight", "tag": "fastfood"},
            {"name": "Pasta (White Sauce)", "cal": 450, "pro": 10, "carbs": 45, "fat": 25, "is_veg": True, "restricted_for": "Weight, Heart", "tag": "fastfood"},
            {"name": "Burger (Veg)", "cal": 400, "pro": 10, "carbs": 55, "fat": 18, "is_veg": True, "restricted_for": "Weight", "tag": "fastfood"},
            {"name": "Fries (Small)", "cal": 300, "pro": 3, "carbs": 40, "fat": 15, "is_veg": True, "restricted_for": "Weight, Heart", "tag": "snack"},
            {"name": "Salad (Caesar)", "cal": 200, "pro": 8, "carbs": 10, "fat": 15, "is_veg": True, "restricted_for": "None", "tag": "salad"},
            {"name": "Avocado Toast", "cal": 280, "pro": 8, "carbs": 25, "fat": 18, "is_veg": True, "restricted_for": "None", "tag": "breakfast"},
            {"name": "Quinoa Salad", "cal": 220, "pro": 8, "carbs": 35, "fat": 6, "is_veg": True, "restricted_for": "None", "tag": "salad"},
            {"name": "Tofu Stir Fry", "cal": 180, "pro": 16, "carbs": 10, "fat": 9, "is_veg": True, "restricted_for": "None", "tag": "salad"},
            
            # --- SWEETS & DESSERTS ---
            {"name": "Gulab Jamun (1 pc)", "cal": 150, "pro": 2, "carbs": 25, "fat": 5, "is_veg": True, "restricted_for": "Sugar, Weight", "tag": "sweet"},
            {"name": "Rasgulla (1 pc)", "cal": 120, "pro": 2, "carbs": 28, "fat": 1, "is_veg": True, "restricted_for": "Sugar", "tag": "sweet"},
            {"name": "Jalebi (100g)", "cal": 300, "pro": 2, "carbs": 60, "fat": 10, "is_veg": True, "restricted_for": "Sugar, Weight", "tag": "sweet"},
            {"name": "Kheer", "cal": 250, "pro": 6, "carbs": 35, "fat": 10, "is_veg": True, "restricted_for": "Sugar", "tag": "sweet"},
            {"name": "Ice Cream (Scoop)", "cal": 200, "pro": 4, "carbs": 25, "fat": 10, "is_veg": True, "restricted_for": "Sugar, Weight", "tag": "sweet"},
            {"name": "Chocolate Brownie", "cal": 350, "pro": 4, "carbs": 45, "fat": 18, "is_veg": True, "restricted_for": "Sugar, Weight", "tag": "sweet"},

            # --- FRUITS ---
            {"name": "Apple", "cal": 95, "pro": 0.5, "carbs": 25, "fat": 0.3, "is_veg": True, "restricted_for": "None", "tag": "fruit"},
            {"name": "Banana", "cal": 105, "pro": 1, "carbs": 27, "fat": 0.3, "is_veg": True, "restricted_for": "Sugar", "tag": "fruit"},
            {"name": "Mango", "cal": 150, "pro": 1, "carbs": 35, "fat": 0.5, "is_veg": True, "restricted_for": "Sugar", "tag": "fruit"},
            {"name": "Papaya", "cal": 60, "pro": 1, "carbs": 15, "fat": 0.1, "is_veg": True, "restricted_for": "None", "tag": "fruit"},
            {"name": "Watermelon", "cal": 30, "pro": 0.6, "carbs": 8, "fat": 0.2, "is_veg": True, "restricted_for": "None", "tag": "fruit"},
            
            # --- DRINKS ---
            {"name": "Masala Chai", "cal": 120, "pro": 2, "carbs": 20, "fat": 3, "is_veg": True, "restricted_for": "Sugar", "tag": "drink"},
            {"name": "Coffee (Cappuccino)", "cal": 100, "pro": 4, "carbs": 10, "fat": 4, "is_veg": True, "restricted_for": "None", "tag": "drink"},
            {"name": "Lassi (Sweet)", "cal": 250, "pro": 8, "carbs": 35, "fat": 10, "is_veg": True, "restricted_for": "Sugar, Weight", "tag": "drink"},
            {"name": "Coke/Soda (Can)", "cal": 140, "pro": 0, "carbs": 39, "fat": 0, "is_veg": True, "restricted_for": "Sugar, Weight", "tag": "drink"},
            {"name": "Coconut Water", "cal": 40, "pro": 1, "carbs": 9, "fat": 0, "is_veg": True, "restricted_for": "None", "tag": "drink"}
        ]

        # ==========================================
        # 🤖 SECTION 2: THE MULTIPLIER (SMARTER LOGIC)
        # ==========================================
        
        final_food_list = []
        
        food_variations = [
            {"suffix": "(Small Portion)", "cal_mult": 0.5, "desc": "Half portion"},
            {"suffix": "(Large Portion)", "cal_mult": 1.5, "desc": "1.5x portion"},
            {"suffix": "(Spicy/Masala)", "cal_mult": 1.1, "desc": "Added spices"},
            {"suffix": "(Low Oil/Diet)", "cal_mult": 0.8, "desc": "Less fat"},
            {"suffix": "(Fried)", "cal_mult": 1.4, "desc": "Deep fried"},
            {"suffix": "(Butter/Ghee)", "cal_mult": 1.3, "desc": "Added fat"},
            {"suffix": "(Homemade)", "cal_mult": 0.9, "desc": "Less oil than restaurant"},
            {"suffix": "(Restaurant Style)", "cal_mult": 1.2, "desc": "More oil/cream"},
            {"suffix": "(With Cheese)", "cal_mult": 1.4, "desc": "Added cheese"},
            {"suffix": "(No Sugar)", "cal_mult": 0.7, "desc": "Sugar free version"},
            {"suffix": "(Multigrain)", "cal_mult": 0.95, "desc": "Fiber rich"}
        ]

        print("🤖 Generating 2000+ Food Variations (With Logic)...")
        
        for food in base_foods:
            # 1. Add the Original Item
            final_food_list.append(food)

            # 2. Create Variations (SMART FILTERS)
            tag = food.get("tag", "generic") # Retrieve our hidden tag
            
            for var in food_variations:
                suffix = var['suffix']
                
                # --- 🚫 REJECTION LOGIC (Don't create stupid foods) ---
                
                # Rule 1: "Multigrain" only for Breads/Breakfast items
                if "Multigrain" in suffix and tag not in ["bread", "breakfast", "fastfood"]:
                    continue # Multigrain Mango/Coke/Chicken is impossible
                
                # Rule 2: "Fried" not for Drinks, Fruits, Rotis, Rice
                if "Fried" in suffix and tag in ["drink", "fruit", "bread", "rice", "salad"]:
                    continue 

                # Rule 3: "Spicy/Masala" not for Sweets, Fruits, Drinks, Cakes
                if "Spicy" in suffix and tag in ["sweet", "fruit", "drink"]:
                    continue
                
                # Rule 4: "Cheese" not for Sweets, Drinks, Fruits, simple Rotis
                if "Cheese" in suffix and tag in ["sweet", "drink", "fruit", "rice"]:
                    continue

                # Rule 5: "No Sugar" only makes sense for Sweets or Drinks
                if "No Sugar" in suffix and tag not in ["sweet", "drink"]:
                    continue

                # Rule 6: "Butter/Ghee" usually not for Drinks/Fruits/Salads
                if "Butter" in suffix and tag in ["drink", "fruit", "salad"]:
                    continue

                # --- ✅ CREATION LOGIC ---
                new_name = f"{food['name']} {suffix}"
                
                # Update Macros based on multiplier
                new_cal = int(food['cal'] * var['cal_mult'])
                new_carbs = int(food['carbs'] * var['cal_mult'])
                new_fat = int(food['fat'] * var['cal_mult'])
                new_pro = int(food['pro'] * var['cal_mult'])

                # Update Restrictions
                new_restrictions = food['restricted_for']
                
                # If adding fat/fry, add restrictions
                if "Fried" in suffix or "Butter" in suffix or "Cheese" in suffix:
                    if new_restrictions == "None": new_restrictions = "Weight, Heart"
                    elif "Weight" not in new_restrictions: new_restrictions += ", Weight"
                
                # If removing sugar, remove restrictions
                if "No Sugar" in suffix:
                    new_restrictions = new_restrictions.replace("Sugar", "").replace(", ,", ",").strip(",")
                    if new_restrictions == "" or new_restrictions == " ": new_restrictions = "None"

                final_food_list.append({
                    "name": new_name,
                    "cal": new_cal,
                    "pro": new_pro,
                    "carbs": new_carbs,
                    "fat": new_fat,
                    "is_veg": food['is_veg'],
                    "restricted_for": new_restrictions
                })

        print(f"🥦 Total Food Items Ready: {len(final_food_list)}")

        # Bulk Insert Food
        # Note: We are NOT saving the 'tag' to DB yet because your Model doesn't have it.
        # But at least the generated NAMES are now clean.
        for food in final_food_list:
            db.session.add(Diet(
                name=food['name'],
                calories=food['cal'],
                protein=food['pro'],
                carbs=food['carbs'],
                fats=food['fat'],
                is_veg=food['is_veg'],
                restricted_for=food['restricted_for']
            ))

        # ==========================================
        # 🏋️ SECTION 3: WORKOUTS (GYM + HOME MIX)
        # ==========================================
        print("🏋️ Seeding Workouts (Gym & Home Plans)...")
        
        # 1. GYM WORKOUTS (Machines & Weights)
        gym_workouts = [
            # --- CHEST (Push) ---
            {"name": "Push-ups", "type": "Strength (Chest)", "burn": 300, "unsafe": "Wrist Pain"},
            {"name": "Bench Press (Barbell)", "type": "Strength (Chest)", "burn": 400, "unsafe": "Shoulder Injury"},
            {"name": "Incline Dumbbell Press", "type": "Strength (Chest)", "burn": 380, "unsafe": "Shoulder Injury"},
            {"name": "Chest Flys (Machine)", "type": "Strength (Chest)", "burn": 250, "unsafe": "Shoulder Injury"},
            
            # --- BACK (Pull) ---
            {"name": "Pull-ups", "type": "Strength (Back)", "burn": 400, "unsafe": "Shoulder Injury"},
            {"name": "Deadlift", "type": "Strength (Back)", "burn": 500, "unsafe": "Back Pain, Disc Slip"},
            {"name": "Lat Pulldown", "type": "Strength (Back)", "burn": 300, "unsafe": "Shoulder Injury"},
            {"name": "Bent Over Rows", "type": "Strength (Back)", "burn": 350, "unsafe": "Back Pain"},

            # --- LEGS (Squat/Lunge) ---
            {"name": "Squats (Barbell)", "type": "Strength (Legs)", "burn": 450, "unsafe": "Knee Pain, Back Pain"},
            {"name": "Lunges (Walking)", "type": "Strength (Legs)", "burn": 400, "unsafe": "Knee Pain"},
            {"name": "Leg Press", "type": "Strength (Legs)", "burn": 350, "unsafe": "Knee Pain"},
            {"name": "Calf Raises", "type": "Strength (Legs)", "burn": 200, "unsafe": "None"},
            
            # --- SHOULDERS & ARMS ---
            {"name": "Overhead Press (Military)", "type": "Strength (Shoulders)", "burn": 350, "unsafe": "Shoulder Injury, Back Pain"},
            {"name": "Lateral Raises", "type": "Strength (Shoulders)", "burn": 250, "unsafe": "Shoulder Injury"},
            {"name": "Bicep Curls (Dumbbell)", "type": "Strength (Arms)", "burn": 200, "unsafe": "None"},
            {"name": "Tricep Dips", "type": "Strength (Arms)", "burn": 250, "unsafe": "Wrist Pain, Shoulder Injury"},

            # --- CARDIO & HIIT ---
            {"name": "Treadmill Run", "type": "Cardio", "burn": 600, "unsafe": "Knee Pain, Heart"},
            {"name": "Cycling (Spin Class)", "type": "Cardio", "burn": 500, "unsafe": "Knee Pain"},
            {"name": "Jump Rope", "type": "Cardio", "burn": 700, "unsafe": "Knee Pain, Heart"},
        ]

        # 2. HOME WORKOUTS (No Equipment / Desi Style)
        home_workouts = [
            # Upper Body
            {"name": "Push-ups (Standard)", "type": "Chest (Home)", "burn": 300, "unsafe": "Wrist Pain"},
            {"name": "Hindu Push-ups (Desi Sapate)", "type": "Full Body (Home)", "burn": 450, "unsafe": "Back Pain"},
            {"name": "Chair Dips", "type": "Arms (Home)", "burn": 200, "unsafe": "Shoulder Injury"},
            {"name": "Pike Push-ups", "type": "Shoulders (Home)", "burn": 320, "unsafe": "BP (Head Rush)"},
            {"name": "Water Bottle Bicep Curls", "type": "Arms (Home)", "burn": 150, "unsafe": "None"},
            
            # Lower Body
            {"name": "Bodyweight Squats", "type": "Legs (Home)", "burn": 300, "unsafe": "Knee Pain"},
            {"name": "Lunges (Walking in Room)", "type": "Legs (Home)", "burn": 350, "unsafe": "Knee Pain"},
            {"name": "Dand Baithak (Desi Squats)", "type": "Legs (Home)", "burn": 500, "unsafe": "Knee Pain"},
            {"name": "Stair Climbing (Seedhi)", "type": "Cardio (Home)", "burn": 550, "unsafe": "Knee Pain"},
            {"name": "Wall Sit Hold", "type": "Legs (Home)", "burn": 200, "unsafe": "Knee Pain"},
            
            # Core & Cardio
            {"name": "Spot Jogging", "type": "Cardio (Home)", "burn": 400, "unsafe": "None"},
            {"name": "Burpees", "type": "HIIT (Home)", "burn": 700, "unsafe": "Heart, BP, Knee Pain"},
            {"name": "Mountain Climbers", "type": "Core (Home)", "burn": 500, "unsafe": "Back Pain"},
            {"name": "Plank Hold", "type": "Core (Home)", "burn": 200, "unsafe": "Back Pain"},
            {"name": "Jumping Jacks", "type": "Cardio (Home)", "burn": 450, "unsafe": "Knee Pain"},
            
            # Yoga & Flexibility
            {"name": "Surya Namaskar", "type": "Yoga", "burn": 250, "unsafe": "None"},
            {"name": "Cobra Stretch (Bhujangasana)", "type": "Yoga", "burn": 100, "unsafe": "Back Pain"},
            {"name": "Kapalbhati", "type": "Yoga (Breathing)", "burn": 150, "unsafe": "BP, Surgery"},
        ]

        # 🧠 VARIATIONS LOGIC (Sets & Reps)
        # Separate logic for Gym and Home to keep it realistic

        gym_variations = [
            {"suffix": "(Hypertrophy - 3 Sets x 12 Reps)", "burn_mult": 1.0, "risk_add": "None"},
            {"suffix": "(Strength - 5 Sets x 5 Reps)", "burn_mult": 1.1, "risk_add": "Joint Pain"},
            {"suffix": "(Endurance - 4 Sets x 20 Reps)", "burn_mult": 1.2, "risk_add": "None"},
            {"suffix": "(Drop Sets - Advanced)", "burn_mult": 1.3, "risk_add": "Muscle Strain"},
        ]

        home_variations = [
            {"suffix": "(Beginner - Do Your Best)", "burn_mult": 0.6, "risk_add": "None"},
            {"suffix": "(Intermediate - 3 Sets x 15 Reps)", "burn_mult": 1.0, "risk_add": "None"},
            {"suffix": "(Advanced - High Intensity/Till Failure)", "burn_mult": 1.4, "risk_add": "Muscle Strain"},
            {"suffix": "(Tabata - 20s Work/10s Rest)", "burn_mult": 1.5, "risk_add": "Heart, BP"},
        ]

        all_workouts_to_add = []

        # Process GYM Workouts
        for work in gym_workouts:
            all_workouts_to_add.append(work) # Add Base
            for var in gym_variations:
                # Logic: Cardio doesn't have "5 sets of 5 reps"
                if work['type'] == "Cardio" and "Sets" in var['suffix']:
                    continue
                
                unsafe = work['unsafe']
                if var['risk_add'] != "None": 
                    if unsafe == "None": unsafe = var['risk_add']
                    else: unsafe += f", {var['risk_add']}"
                
                all_workouts_to_add.append({
                    "name": f"{work['name']} {var['suffix']}",
                    "type": work['type'],
                    "burn": int(work['burn'] * var['burn_mult']),
                    "unsafe": unsafe
                })

        # Process HOME Workouts
        for work in home_workouts:
            all_workouts_to_add.append(work) # Add Base
            for var in home_variations:
                # Skip Tabata for Yoga (Doesn't make sense)
                if "Yoga" in work['type'] and "Tabata" in var['suffix']:
                    continue
                
                unsafe = work['unsafe']
                if var['risk_add'] != "None":
                    if unsafe == "None": unsafe = var['risk_add']
                    else: unsafe += f", {var['risk_add']}"

                all_workouts_to_add.append({
                    "name": f"{work['name']} {var['suffix']}",
                    "type": work['type'],
                    "burn": int(work['burn'] * var['burn_mult']),
                    "unsafe": unsafe
                })

        print(f"💪 Adding {len(all_workouts_to_add)} Workout Plans (Gym + Home)...")
        for w in all_workouts_to_add:
            db.session.add(Workout(
                name=w['name'],
                workout_type=w['type'],  # Fixed: Maps to correct column
                calories_burn_per_hr=w['burn'],
                unsafe_for=w['unsafe']
            ))

        db.session.commit()
        print("✅ Database Seeded! Master Food List + Gym & Home Workouts Loaded. 🚀")

if __name__ == "__main__":
    seed()