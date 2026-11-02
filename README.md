# 🏋️‍♂️ FitCraft AI — Home Workout, BMR & Macro Nutrition Planner

**Project:** AI Fitness, Home Workout & Macro Nutrition Coach  
**Domain:** Health, Sports Science & Personalized Nutrition  
**Student Name:** Zubair  
**Interface:** Streamlit (`app.py`)  
**Database:** SQLite3 (`fitcraft.db`)  
**NLU Engine:** Python Standard Library (`difflib.SequenceMatcher` + Jaccard token overlap)  

---

## 📌 Project Overview
**FitCraft AI** is an intelligent, domain-specific fitness and nutrition planning chatbot designed specifically for students and busy working professionals. It bridges the gap between expensive gym memberships/trainers and accessible, science-backed fitness guidance. 

FitCraft AI incorporates fuzzy natural language understanding (`difflib`) to answer queries in Roman Urdu and English (e.g., *"belly fat kaise kam karein"*, *"high protein desi diet"*), computes scientific BMR/TDEE targets via the Mifflin-St Jeor formula, generates customized home workout routines, and maintains persistent workout and weight records in a local SQLite database.

---

## 🌟 Key Features

### 1. 💬 AI Fitness Coach (`st.chat_message`, `st.chat_input`)
- **Bilingual Conversational Interface:** Understands English and conversational Roman Urdu.
- **Typo & Spelling Tolerance (`difflib`):** Accurately detects intents even with typos (e.g. `'wight loss'`, `'protien'`, `'creatine safe'`, `'belly fat kam kerna'`).
- **Confidence & Intent Badges:** Assistant bubble displays category, matched intent tag, and confidence score.
- **Transcript Export:** Download full chat logs as `.txt`.

### 2. 📊 BMR, TDEE & Macro Nutrition Calculator
- Uses the **Mifflin-St Jeor equation** to calculate:
  - **BMR (Basal Metabolic Rate):** Baseline daily calorie expenditure.
  - **TDEE (Total Daily Energy Expenditure):** Adjusted for activity level.
  - **BMI Score & Category:** Underweight, Normal, Overweight, Obese.
  - **Macro-Nutrient Split:** Exact daily targets in grams and calories for **Protein, Carbohydrates, and Fats**.
  - **Hydration Target:** Minimum daily water intake in Liters.

### 3. 🏋️ Custom Workout Routine Generator
- Generates step-by-step workout routines based on:
  - Fitness Level (Beginner / Intermediate / Advanced)
  - Equipment (Bodyweight / Calisthenics, Dumbbells Only, Full Gym)
  - Target Focus (Full Body Burn, Upper Body, Lower Body & Core, Desk Worker Stretches)
- Displays table with sets, reps, rest periods, target muscles, and form coaching cues.
- Export routine as printable `.txt`.

### 4. 📈 Workout & Weight Tracker (SQLite Database)
- Users log their daily workout sessions (Duration, Calories burned, Body weight, Notes).
- Stored permanently in SQLite `fitcraft.db` with interactive tabular history.

### 5. 🥗 Desi High-Protein Diet & Meal Guide
- Pakistani food nutritional comparison table (Boiled Eggs, Chicken Breast, Chana, Daal, Paneer, Dahi).
- Sample student meal plan under PKR 400/day yielding 72g+ protein.

### 6. 🤖 Optional Google Gemini API Connectivity
- Paste a free Gemini API key in the sidebar for open-ended custom workout recipes and advice.

---

## 🛠️ Technologies Used
- **Language:** Python 3.10+ (Tested on Python 3.13)
- **Frontend / UI:** Streamlit
- **Database:** SQLite3 (`fitcraft.db`)
- **NLU / NLP Engine:** Python Standard Library (`difflib`, `re`, `json`, `datetime`, `urllib.request`)

---

## 📁 File Structure
```text
D:/Zubair Project/
│
├── app.py                         # Main Streamlit Application
├── knowledge_base.json            # External Self-Written Fitness Knowledge Base (15 Intents)
├── requirements.txt               # Dependencies file (streamlit)
├── VIVA_QUESTIONS_AND_ANSWERS.md  # Complete 9 Compulsory Viva Defense Q&As
└── README.md                      # Project Documentation
```

---

## 🚀 How to Run the Project

### 1. Open Terminal and Navigate to Directory
```bash
cd "D:\Zubair Project"
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit Application
```bash
python -m streamlit run app.py
```
*(Or `streamlit run app.py`)*

The web app will launch automatically in your browser at `http://localhost:8501`.
