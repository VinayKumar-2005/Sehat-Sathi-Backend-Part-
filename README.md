# SehatSaathi 🏥❤️🤖

**AI Personal Health Caretaker**  
A smart preventive healthcare ecosystem that helps users track health, receive personalized diet/workout plans, monitor risks, and interact with an AI health assistant.

---

# 📌 Overview

SehatSaathi is a full-stack AI-powered healthcare application designed to become a user’s **daily health companion**.

It combines:

- Personalized health profiling
- AI health guidance
- Diet planning
- Workout recommendations
- Health risk alerts
- Progress analytics
- Family health support
- Medical assistance chat

This app does **not replace doctors**. It acts as a smart support layer for preventive healthcare.

---

# 🚀 Why SehatSaathi?

Modern healthcare systems face common issues:

- People visit doctors too late
- Preventive care is ignored
- Generic diet/workout plans fail
- Small clinics get overloaded
- No all-in-one personal health platform exists

### SehatSaathi solves this by offering:

✅ Personalized recommendations  
✅ Daily health monitoring  
✅ AI-based assistance  
✅ Family health management  
✅ Emergency risk alerts  
✅ Better health awareness  

---

# 🧠 Core Features

---

## 1️⃣ Authentication System

- User Signup
- Secure Login
- JWT Authentication
- Session Handling
- Logout Support

---

## 2️⃣ Health Profile System

Store and manage:

- Name
- Age
- Gender
- Height
- Weight
- Lifestyle
- Sleep habits
- Medical history
- Allergies
- Injuries
- BP / Sugar / Oxygen logs

---

## 3️⃣ AI Health Logic Engine

Smart health analysis based on:

- BMI
- Blood Pressure
- Sugar Levels
- Goals
- Lifestyle
- Existing disease history

Outputs:

- Risk levels
- Safe food suggestions
- Unsafe food warnings
- Workout limits

---

## 4️⃣ Personalized Diet System

Includes:

- Breakfast
- Lunch
- Dinner
- Snacks
- Pre-workout meal
- Post-workout meal

Tracks:

- Calories
- Protein
- Restrictions
- Diet preference (Veg / Egg / Non-Veg / Vegan)

---

## 5️⃣ Workout Recommendation Engine

Provides:

- Home workouts
- Gym plans
- Beginner routines
- Weight loss plans
- Muscle gain plans
- Injury-safe exercises

---

## 6️⃣ AI Nurse / Medical Assistant

Chat-based health support:

- Ask symptoms
- Get basic suggestions
- Home remedies
- Risk seriousness detection
- Doctor referral suggestions

---

## 7️⃣ Red Alert System 🚨

Detects dangerous situations:

- High BP
- Sugar spike
- Oxygen drop
- Chest pain patterns
- Severe symptoms

Actions:

- Emergency warning
- Hospital recommendation
- Fast medical response guidance

---

## 8️⃣ Progress Tracking

Visual analytics for:

- Weight changes
- Workout consistency
- Diet adherence
- BP trends
- Sugar trends
- Recovery score

---

## 9️⃣ Family Health Module

Manage separate profiles for:

- Parents
- Children
- Spouse

Track and monitor family health easily.

---

# 🏗️ Tech Stack

---

## Frontend

### Flutter

Used for:

- Android App
- Future iOS Support
- Smooth UI
- Cross-platform experience

---

## Backend

### FastAPI (Python)

Used for:

- REST APIs
- Authentication
- Business logic
- AI integrations
- Secure services

---

## Database

### PostgreSQL / Supabase

Stores:

- Users
- Health profiles
- Logs
- Chat history
- Alerts
- Reports
- Analytics

---

## AI Layer

### Gemini API / LLM

Used for:

- AI Nurse Chat
- Symptom guidance
- Context memory
- Smart responses

---

## Security

- JWT Authentication
- Secure password hashing
- Protected routes
- Session management

---

# 🎨 UI Design Language

### Brand Identity

**SehatSaathi = Care + Trust + Intelligence**

### Color Palette

| Purpose | Color |
|--------|-------|
| Primary | #1FB6A6 |
| Medical Blue | #0A2540 |
| White | #FFFFFF |
| Background Grey | #F4F6F8 |
| Emergency Red | #E63946 |
| Accent Purple | #7B4CC9 |

---

# 📱 Frontend Screens

- Splash Screen
- Login / Signup
- Onboarding
- Home Dashboard
- Diet Screen
- Workout Screen
- AI Chat
- Progress Screen
- Hospital Screen
- Profile / Settings

---

# 📂 Suggested Project Structure

```bash
sehat_saathi/
│
├── backend/
│   ├── app/
│   ├── routes/
│   ├── models/
│   ├── services/
│   └── main.py
│
├── frontend/
│   ├── lib/
│   ├── assets/
│   └── pubspec.yaml
│
└── README.md