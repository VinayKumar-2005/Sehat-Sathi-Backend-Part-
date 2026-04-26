from app import create_app
from extensions import db
from models.workout_plan import WorkoutPlan
from models.user import User
import json

app = create_app()

def check_database():
    with app.app_context():
        print("\n🕵️‍♂️ INSPECTING DATABASE...\n")
        
        # 1. Count Total Plans
        total_plans = WorkoutPlan.query.count()
        print(f"📊 Total Saved Plans in DB: {total_plans}")

        if total_plans == 0:
            print("❌ Database is empty! (Plan save nahi hua)")
            return

        # 2. Fetch the latest plan
        latest_entry = WorkoutPlan.query.order_by(WorkoutPlan.id.desc()).first()
        user = User.query.get(latest_entry.user_id)
        
        print(f"✅ Found Latest Plan for User: {user.email} (ID: {user.id})")
        print(f"💾 Saved At: {latest_entry.created_at}")
        
        # 3. Show a snippet of the JSON content
        plan_data = json.loads(latest_entry.plan_data)
        split_name = plan_data.get('workout', {}).get('split_name', 'Unknown')
        print(f"📝 Plan Name in DB: {split_name}")
        print("-" * 40)
        print("🎉 CONFIRMED: Data is permanently stored on disk!")

if __name__ == "__main__":
    check_database()