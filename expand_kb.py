"""
Fitness & Nutrition Synthetic Data Expansion Script
Generates 10,000+ realistic question-pattern variations across all 14 domain intents.
Supports English, Roman Urdu, and colloquial fitness variations.
"""

import json
import itertools
import os

KB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "knowledge_base.json")

with open(KB_PATH, "r", encoding="utf-8") as f:
    kb = json.load(f)

# Base intent semantic cores
INTENT_CORES = {
    "greeting": {
        "prefixes": [
            "", "aoa ", "salam ", "assalam o alaikum ", "hello ", "hi ", "hey ",
            "good morning ", "good evening ", "adab ", "pyare coach ", "kese ho ",
            "kya haal hai ", "salam sir ", "hello brother "
        ],
        "keywords": [
            "fitcraft", "coach", "fitness buddy", "trainer", "bhai", "sir", "dost",
            "kese hain aap", "sab khairiat", "are you ready", "let's start", "workout shuru karein"
        ],
        "suffixes": ["", " please", " coach", " bhai", " sir", " suniye", " bataiye", " aaj kya program hai"]
    },
    "goodbye": {
        "prefixes": [
            "", "ok ", "acha ", "chalo ", "thank you ", "shukriya ", "bohot shukriya ",
            "thanks a lot ", "thanks coach ", "bundle of thanks ", "jazakallah ", "shukran "
        ],
        "keywords": [
            "bye", "goodbye", "allah hafiz", "khuda hafiz", "see you later", "see you tomorrow",
            "phir milenge", "kal baat hogi", "take care", "shukriya guidance ke liye",
            "zabardast advice", "bohot maza aya", "baad me baat karte hain", "alvida"
        ],
        "suffixes": ["", " coach", " bhai", " sir", " for your help", " thank you", " take care", " see you soon"]
    },
    "identity_and_capabilities": {
        "prefixes": [
            "", "who are you ", "what is your name ", "tum kaun ho ", "apna intro do ",
            "what can you do ", "tum kya kar sakte ho ", "help me ", "features batao ",
            "kya madad karoge ", "how do you work ", "menu dikhao ", "capabilities kya hain "
        ],
        "keywords": [
            "fitcraft ai", "fitness coach", "personal trainer", "features list",
            "bot capabilities", "options kya hain", "tumhara kaam kya hai",
            "kya kya services hain", "how can you guide me", "tell me about yourself",
            "apni khusosiyat batao", "system overview", "help options"
        ],
        "suffixes": ["", " please", " guide me", " details do", " in short", " batao", " explain karein"]
    },
    "fat_loss_belly_fat": {
        "prefixes": [
            "", "how to ", "tips for ", "best way to ", "kaise karein ", "tarika batao ",
            "mujhe karna hai ", "fastest way to ", "sabse asan tarika ", "kya karun ",
            "guide on ", "scientific way to ", "pakistan me ", "ghar par "
        ],
        "keywords": [
            "lose belly fat", "belly fat loss", "pait ki charbi kam", "pait kam karne ka tarika",
            "wazan kam karna", "weight loss journey", "reduce tummy fat", "burn stubborn visceral fat",
            "caloric deficit diet", "cardio for fat loss", "burn fat fast", "how to get 6 pack abs",
            "love handles khatam", "weight kam karne ka diet plan", "motapa kam kaise karein",
            "fat burning workouts", "fat loss for beginners", "loose stomach weight",
            "charbi pighlane ka tarika", "belly fat khatam karna"
        ],
        "suffixes": [
            "", " fast", " at home", " without gym", " in 30 days", " for beginners",
            " ghar baithe", " jaldi", " in urdu", " without supplements", " desi diet se",
            " naturally", " without side effects", " asani se"
        ]
    },
    "muscle_gain_hypertrophy": {
        "prefixes": [
            "", "how to ", "best tips for ", "kaise karein ", "mujhe karna hai ",
            "tarika batao ", "rules for ", "guide on ", "best workout for ", "pakistan me "
        ],
        "keywords": [
            "build muscle", "muscle building", "muscle hypertrophy", "biceps size barhana",
            "body banana", "chest size increase", "wazan barhana", "mass gain", "lean bulk",
            "gain muscle mass", "progressive overload meaning", "doley ka size",
            "how to get bigger muscles", "muscle gain diet", "hardgainer muscle gain",
            "muscles kaise banayein", "bodybuilding tips", "fast muscle hypertrophy",
            "shoulders wide karna", "stronger banna"
        ],
        "suffixes": [
            "", " at home", " with dumbbells", " fast", " for skinny guys", " desi diet se",
            " natural tarike se", " in gym", " without steroids", " jaldi", " ghar par"
        ]
    },
    "high_protein_pakistani_diet": {
        "prefixes": [
            "", "what are ", "list of ", "sasta ", "best ", "kaunsa hai ", "batao ",
            "budget friendly ", "student ke liye ", "how much protein in ", "top sources of "
        ],
        "keywords": [
            "high protein pakistani food", "desi protein sources", "sasta protein in pakistan",
            "protein in boiled eggs", "chicken breast protein", "daal chawal protein complete",
            "chana protein count", "homemade paneer protein", "cheap protein for students",
            "pakistani diet plan for gym", "rohu fish protein", "dahi yogurt protein",
            "peanut butter calories and protein", "daily protein requirement", "protein foods list",
            "bina whey protein ke diet", "sasti body banane ki khorak", "high protein desi nashta",
            "eggs protein vs chicken", "chana chat for gym"
        ],
        "suffixes": [
            "", " in pakistan", " under 400 rs", " for students", " in karachi lahore",
            " saste daamon", " rozana", " per 100g", " guide", " list", " with prices"
        ]
    },
    "creatine_and_supplements": {
        "prefixes": [
            "", "is it safe ", "how to use ", "kya safe hai ", "kese use karein ",
            "side effects of ", "best time to take ", "facts about ", "guide on "
        ],
        "keywords": [
            "creatine monohydrate", "creatine safe for beginners", "creatine dosage per day",
            "creatine loading phase", "whey protein safe", "creatine hair loss myth",
            "creatine kidney damage reality", "fish oil omega 3", "multivitamin for gym",
            "pre workout drink side effects", "creatine with water", "creatine timing",
            "supplements zaroori hain ya nahi", "creatine ke nuqsanat", "original creatine in pakistan",
            "creatine benefits for brain and muscle"
        ],
        "suffixes": [
            "", " for beginners", " in pakistan", " safely", " daily", " with water",
            " without loading", " kya sach hai", " side effects", " guide"
        ]
    },
    "desk_worker_back_pain": {
        "prefixes": [
            "", "how to fix ", "best stretches for ", "exercises for ", "dard ka ilaj ",
            "kamar dard khatam karne ka tarika ", "relief from ", "solutions for "
        ],
        "keywords": [
            "desk worker back pain", "lower back pain from sitting", "neck pain from computer",
            "tech neck fix", "programmer posture correction", "rounded shoulders exercise",
            "cat cow stretch", "chin tucks for neck", "hip flexor tightness sitting",
            "doorway chest stretch", "chair ergonomic stretches", "office chair back pain",
            "kamar dard student desk", "gardan me khinchaaw", "scoliosis posture stretches",
            "spine mobility at home", "back pain relief without medicine"
        ],
        "suffixes": [
            "", " at office desk", " for coders", " for students", " at home",
            " in 5 minutes", " without equipment", " instantly", " daily routine"
        ]
    },
    "home_workout_tips": {
        "prefixes": [
            "", "best ", "how to do ", "routine for ", "ghar par ", "bina gym ke ",
            "tarika for ", "exercises for ", "guide on "
        ],
        "keywords": [
            "home workout routine", "bodyweight calisthenics", "pushups correct form",
            "bodyweight squats depth", "pullups at home without bar", "chair dips for triceps",
            "mountain climbers reps", "plank hold time", "no equipment chest workout",
            "ghar par body banana", "full body home workout", "calisthenics progression",
            "knee pushups for beginners", "ghar par biceps exercise", "home abs workout"
        ],
        "suffixes": [
            "", " at home", " for beginners", " with no equipment", " in 20 minutes",
            " without weights", " ghar baithe", " step by step", " effectively"
        ]
    },
    "water_and_hydration": {
        "prefixes": [
            "", "how much ", "kitna ", "benefits of ", "signs of ", "rules for ",
            "rozana ", "daily "
        ],
        "keywords": [
            "water intake per day", "kitna paani peena chahiye", "dehydration symptoms in gym",
            "water during workout sets", "paani ke fayde for skin and fat loss",
            "urine color hydration chart", "water retention vs fat", "cold water vs warm water",
            "electrolytes in summer workout", "how many liters of water daily"
        ],
        "suffixes": [
            "", " in pakistan summer", " for fat loss", " daily", " during gym",
            " in liters", " for active people", " rozana"
        ]
    },
    "skinny_fat_solution": {
        "prefixes": [
            "", "what is ", "how to fix ", "kya hota hai ", "kaise theek karein ",
            "diet for ", "routine for ", "best approach for "
        ],
        "keywords": [
            "skinny fat body recomposition", "thin arms big belly solution", "patlay baazu nikla hua pait",
            "skinny fat calorie deficit or surplus", "maintenance calories recomposition",
            "skinny fat lifting weights", "cardio or lifting for skinny fat", "body recomp timeline",
            "skinny fat protein target", "skinny fat se aesthetic body kaise banayein"
        ],
        "suffixes": [
            "", " for beginners", " at home", " step by step", " in urdu",
            " without losing more weight", " realistically", " permanently"
        ]
    },
    "intermittent_fasting": {
        "prefixes": [
            "", "what is ", "rules for ", "how to do ", "kya hai ", "kese karein ",
            "benefits of ", "guide on "
        ],
        "keywords": [
            "intermittent fasting 16 8 protocol", "fasting for fat loss", "fasting eating window",
            "fasting hours zero calorie drinks", "black coffee during fasting", "roza aur intermittent fasting",
            "fasting mistakes to avoid", "break fast best meal", "autophagy and fasting",
            "intermittent fasting se wazan kam karna"
        ],
        "suffixes": [
            "", " for fat loss", " properly", " daily", " for beginners",
            " in pakistan", " eating schedule", " rules"
        ]
    },
    "injury_prevention_form": {
        "prefixes": [
            "", "how to avoid ", "how to fix ", "kaise bachein ", "correct form for ",
            "reason for ", "safe way to do "
        ],
        "keywords": [
            "knee pain during squats", "elbow pain in bench press", "lower back rounding deadlift",
            "shoulder impingement lateral raises", "gym injuries se kaise bachein",
            "warmup before lifting weights", "joint pain vs muscle soreness", "wrist pain pushups",
            "muscle cramp prevention gym", "ego lifting dangers"
        ],
        "suffixes": [
            "", " in gym", " permanently", " safety tips", " proper form",
            " without doctor", " safely"
        ]
    },
    "sleep_and_recovery": {
        "prefixes": [
            "", "why is ", "how much ", "importance of ", "tips for ", "kitni zaroori hai ",
            "rules for "
        ],
        "keywords": [
            "sleep for muscle growth", "human growth hormone in deep sleep", "kitne ghantay neend chahiye",
            "muscle recovery 48 hours rule", "overtraining symptoms in gym", "rest days between workouts",
            "sore muscles DOMS recovery", "sleep quality for fitness", "post workout recovery hacks",
            "fatigue and muscle repair"
        ],
        "suffixes": [
            "", " for muscle building", " daily", " for students", " naturally",
            " properly", " scientific guide"
        ]
    }
}

total_count = 0
for intent in kb.get("intents", []):
    tag = intent.get("tag")
    if tag == "fallback" or tag not in INTENT_CORES:
        continue
    
    cfg = INTENT_CORES[tag]
    existing = set(intent.get("patterns", []))
    
    # Generate combinatorial variations
    for p in cfg["prefixes"]:
        for k in cfg["keywords"]:
            for s in cfg["suffixes"]:
                combo = f"{p}{k}{s}".strip().lower()
                # Clean punctuation and multiple spaces
                combo = " ".join(combo.split())
                if len(combo) >= 4:
                    existing.add(combo)
    
    intent["patterns"] = sorted(list(existing))
    total_count += len(intent["patterns"])
    print(f"Intent '{tag}': {len(intent['patterns'])} patterns")

print(f"\nTotal synthetic patterns across all intents: {total_count}")

# Save updated knowledge base
with open(KB_PATH, "w", encoding="utf-8") as f:
    json.dump(kb, f, indent=2, ensure_ascii=False)

print("Saved to knowledge_base.json successfully!")
