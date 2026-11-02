"""
FitCraft AI - Smart Home Workout & Nutrition Coach
Author: Zubair
Course: Python AI Chatbot Project
Technologies: Python, Streamlit, SQLite3, difflib, json, re, datetime, Google Gemini REST API
Theme: Ultra-Clean Professional Light Theme
Tabs:
  1. 💬 AI Fitness Coach (with difflib NLU + Google Gemini 1.5 Flash)
  2. 🏋️ Custom Workout Generator
  3. 🥗 Desi Protein Guide
"""

import streamlit as st
import json
import sqlite3
import re
import os
import random
from difflib import SequenceMatcher
from datetime import datetime
import urllib.request
import urllib.error

# ---------------------------------------------------------
# 1. Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="FitCraft AI — Home Workout & Nutrition Coach",
    page_icon="🏋️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# 2. Ultra-Clean Professional Light Theme CSS
# ---------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

:root {
    --primary: #0284c7;
    --primary-dark: #0369a1;
    --primary-light: #e0f2fe;
    --accent: #0d9488;
    --text-main: #0f172a;
    --text-muted: #64748b;
    --card-bg: #ffffff;
    --page-bg: #f8fafc;
    --border-color: #e2e8f0;
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif !important;
    color: #0f172a !important;
}

/* ── App Light Background ── */
.stApp {
    background-color: #f8fafc !important;
}

/* ── Hero Banner (Clean Minimalist Professional) ── */
.hero-card {
    background: linear-gradient(135deg, #ffffff 0%, #f0f9ff 100%);
    border: 1px solid #bae6fd;
    border-radius: 20px;
    padding: 28px 32px;
    margin-bottom: 24px;
    box-shadow: 0 4px 20px -2px rgba(2, 132, 199, 0.08);
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #e0f2fe;
    border: 1px solid #7dd3fc;
    color: #0369a1;
    padding: 4px 14px;
    border-radius: 999px;
    font-size: 0.74rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 12px;
}
.hero-title {
    font-size: 2.1rem;
    font-weight: 800;
    color: #0f172a;
    margin: 0 0 8px 0;
    letter-spacing: -0.5px;
}
.hero-title span {
    color: #0284c7;
}
.hero-subtitle {
    font-size: 0.98rem;
    color: #475569;
    margin: 0 0 16px 0;
    line-height: 1.5;
}
.hero-tags {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
}
.hero-tag {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    color: #334155;
    padding: 6px 14px;
    border-radius: 10px;
    font-size: 0.78rem;
    font-weight: 600;
    box-shadow: 0 1px 3px rgba(0,0,0,0.03);
}

/* ── Tab Navigation (Modern Crisp Pill Style) ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: #e2e8f0;
    padding: 6px;
    border-radius: 14px;
    border: 1px solid #cbd5e1;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 10px;
    color: #475569 !important;
    padding: 10px 22px;
    font-weight: 600;
    font-size: 0.92rem;
    border: none !important;
    transition: all 0.2s ease;
}
.stTabs [data-baseweb="tab"]:hover {
    color: #0f172a !important;
    background: rgba(255, 255, 255, 0.6);
}
.stTabs [aria-selected="true"] {
    background: #ffffff !important;
    color: #0284c7 !important;
    font-weight: 700 !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08) !important;
}

/* ── Sidebar (Clean Crisp White) ── */
[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid #e2e8f0 !important;
}
[data-testid="stSidebar"] * {
    color: #1e293b !important;
}
.sidebar-panel {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 16px;
    margin-bottom: 14px;
}
.sidebar-panel h4 {
    color: #0369a1 !important;
    font-size: 0.78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin: 0 0 10px 0;
}

/* ── Sidebar Buttons ── */
[data-testid="stSidebar"] .stButton > button {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    color: #334155 !important;
    border-radius: 10px !important;
    font-size: 0.8rem !important;
    padding: 8px 12px !important;
    text-align: left !important;
    justify-content: flex-start !important;
    transition: all 0.2s ease !important;
    margin-bottom: 4px !important;
    width: 100% !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.02) !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: #f0f9ff !important;
    border-color: #38bdf8 !important;
    color: #0284c7 !important;
    transform: translateX(4px) !important;
}

/* ── Chat Messages ── */
.chat-wrap {
    display: flex;
    flex-direction: column;
    gap: 14px;
    margin-bottom: 24px;
}
.chat-msg-user {
    align-self: flex-end;
    background: #0284c7;
    color: #ffffff !important;
    padding: 14px 20px;
    border-radius: 18px 18px 4px 18px;
    max-width: 78%;
    font-size: 0.95rem;
    line-height: 1.6;
    box-shadow: 0 4px 14px rgba(2, 132, 199, 0.25);
    margin-left: auto;
    margin-top: 6px;
    margin-bottom: 6px;
}
.chat-msg-bot {
    align-self: flex-start;
    background: #ffffff;
    color: #1e293b !important;
    padding: 16px 22px;
    border-radius: 18px 18px 18px 4px;
    max-width: 82%;
    border: 1px solid #e2e8f0;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
    font-size: 0.95rem;
    line-height: 1.7;
    margin-top: 6px;
    margin-bottom: 6px;
}
.chat-msg-bot strong {
    color: #0284c7;
}

/* Chips in Bot message */
.meta-chips {
    display: flex;
    gap: 6px;
    margin-top: 10px;
    flex-wrap: wrap;
    align-items: center;
}
.chip {
    font-size: 0.72rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 8px;
    display: inline-flex;
    align-items: center;
    gap: 4px;
}
.chip-intent { background: #fef3c7; color: #92400e; border: 1px solid #fde68a; }
.chip-conf   { background: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; }
.chip-cat    { background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; }
.chip-source { background: #f3e8ff; color: #7e22ce; border: 1px solid #e9d5ff; }

/* ── Workout Cards ── */
.routine-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 12px;
    box-shadow: 0 2px 8px -2px rgba(0, 0, 0, 0.04);
    transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
}
.routine-card:hover {
    transform: translateY(-2px);
    border-color: #38bdf8;
    box-shadow: 0 6px 16px -2px rgba(2, 132, 199, 0.12);
}
.routine-title {
    font-size: 1.08rem;
    font-weight: 700;
    color: #0f172a;
    margin: 0;
}
.badge-pill {
    font-size: 0.74rem;
    padding: 4px 10px;
    border-radius: 8px;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
}
.badge-volume { background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; }
.badge-muscle { background: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; }
.badge-rest   { background: #fffbeb; color: #b45309; border: 1px solid #fde68a; }

/* ── Food Guide Cards ── */
.food-item {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 12px;
    box-shadow: 0 2px 8px -2px rgba(0, 0, 0, 0.04);
    transition: transform 0.2s ease, border-color 0.2s ease;
}
.food-item:hover {
    transform: translateY(-2px);
    border-color: #34d399;
}
.food-protein-num {
    font-size: 1.25rem;
    font-weight: 800;
    color: #059669;
}

/* ── Action Buttons ── */
.stButton > button[kind="primary"] {
    background: #0284c7 !important;
    border: 1px solid #0284c7 !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 12px 24px !important;
    box-shadow: 0 4px 14px rgba(2, 132, 199, 0.25) !important;
    color: #ffffff !important;
}
.stButton > button[kind="primary"]:hover {
    background: #0369a1 !important;
    border-color: #0369a1 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 18px rgba(2, 132, 199, 0.35) !important;
}
.stDownloadButton > button {
    background: #0d9488 !important;
    color: #ffffff !important;
    border: 1px solid #0d9488 !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    padding: 10px 20px !important;
}
.stDownloadButton > button:hover {
    background: #0f766e !important;
    color: #ffffff !important;
    transform: translateY(-1px) !important;
}

/* Inputs */
.stTextInput > div > div > input, .stSelectbox > div > div {
    background: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 10px !important;
    color: #0f172a !important;
}

/* Mode banner */
.status-pill-banner {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 10px 18px;
    margin-bottom: 18px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.85rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.03);
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. SQLite Database Initialization
# ---------------------------------------------------------
DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fitcraft.db")

def init_database():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS chat_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT,
            bot_response TEXT,
            intent TEXT,
            confidence REAL,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

init_database()

def log_chat_to_db(user_msg, bot_msg, intent, conf):
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.cursor().execute(
            "INSERT INTO chat_logs (user_message, bot_response, intent, confidence, timestamp) VALUES (?, ?, ?, ?, ?)",
            (user_msg, bot_msg, intent, float(conf), datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"DB log error: {e}")

# ---------------------------------------------------------
# 4. Knowledge Base & Hybrid NLU Engine
# ---------------------------------------------------------
KB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "knowledge_base.json")

@st.cache_data
def load_kb():
    if os.path.exists(KB_PATH):
        with open(KB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"intents": []}

kb = load_kb()

class FitCraftEngine:
    STOP_WORDS = {
        "is", "a", "an", "the", "in", "on", "at", "to", "for", "of", "and", "or",
        "me", "mera", "meri", "kya", "hai", "hain", "ke", "ki", "ko", "ka", "par",
        "se", "karein", "karna", "please", "can", "you", "tell", "mujhe", "batao",
        "coach", "sir", "bhai", "zara", "kuch"
    }

    def __init__(self, knowledge):
        self.kb = knowledge
        self.indexed_patterns = []
        for item in self.kb.get("intents", []):
            tag = item.get("tag")
            cat = item.get("category", "General")
            if tag == "fallback":
                continue
            for p in item.get("patterns", []):
                cp = self.preprocess(p)
                tp = self.get_tokens(cp)
                self.indexed_patterns.append((cp, tp, tag, cat))

    def preprocess(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r"[^\w\s]", " ", text)
        return " ".join(text.split())

    def get_tokens(self, text: str) -> set:
        clean_text = self.preprocess(text)
        words = clean_text.split()
        filtered = [w for w in words if w not in self.STOP_WORDS]
        return set(filtered) if filtered else set(words)

    def similarity(self, u_clean: str, p_clean: str, u_tokens: set, p_tokens: set) -> float:
        if u_clean == p_clean or p_clean in u_clean:
            return 1.0

        seq_ratio = SequenceMatcher(None, u_clean, p_clean).ratio()

        if not u_tokens or not p_tokens:
            return seq_ratio

        intersection = u_tokens.intersection(p_tokens)
        union = u_tokens.union(p_tokens)
        jaccard = len(intersection) / len(union) if union else 0.0

        composite = (jaccard * 0.60) + (seq_ratio * 0.40)
        return max(seq_ratio, composite)

    def find_best_intent(self, query: str):
        u_clean = self.preprocess(query)
        u_tokens = self.get_tokens(u_clean)

        best_intent = None
        best_score = 0.0
        best_category = "General"

        # 1. Exact or substring match fast path (sub-millisecond)
        for cp, tp, tag, cat in self.indexed_patterns:
            if u_clean == cp or cp in u_clean:
                return tag, 1.0, cat

        # 2. Token overlap pre-filter (evaluates top relevant candidates first)
        scored_candidates = []
        for cp, tp, tag, cat in self.indexed_patterns:
            overlap = len(u_tokens & tp)
            if overlap > 0:
                scored_candidates.append((overlap, cp, tp, tag, cat))

        # Sort by highest token overlap
        scored_candidates.sort(key=lambda x: x[0], reverse=True)
        top_candidates = scored_candidates[:350] if scored_candidates else self.indexed_patterns[:250]

        for _, cp, tp, tag, cat in top_candidates:
            score = self.similarity(u_clean, cp, u_tokens, tp)
            if score > best_score:
                best_score = score
                best_intent = tag
                best_category = cat
                if best_score >= 0.95:
                    break

        return best_intent, best_score, best_category

    def call_gemini(self, query: str, api_key: str) -> str:
        # Latest verified active models on Google Gemini Developer API
        configs = [
            ("v1beta", "gemini-3.8-flash"),
            ("v1", "gemini-3.8-flash"),
            ("v1beta", "gemini-2.5-flash"),
            ("v1beta", "gemini-1.5-flash"),
        ]
        system_instruction = (
            "You are FitCraft AI, an expert certified fitness trainer & sports nutritionist. "
            "Provide direct, science-backed, friendly fitness advice tailored for Pakistani users "
            "(desirable budget meals like daal, eggs, chana, chicken, and home calisthenics). "
            "Answer clearly in Roman Urdu or English depending on how the user asks. "
            "Format with clean bullet points and bold text."
        )

        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": f"SYSTEM INSTRUCTION: {system_instruction}\n\nUSER QUESTION: {query}"}]
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "topP": 0.95,
                "maxOutputTokens": 800,
            }
        }

        last_error = ""
        for ver, model in configs:
            url = f"https://generativelanguage.googleapis.com/{ver}/models/{model}:generateContent?key={api_key.strip()}"
            try:
                data = json.dumps(payload).encode("utf-8")
                req = urllib.request.Request(url, data=data, headers=headers, method="POST")
                with urllib.request.urlopen(req, timeout=14) as resp:
                    resp_data = json.loads(resp.read().decode("utf-8"))
                    candidates = resp_data.get("candidates", [])
                    if candidates:
                        text_parts = candidates[0].get("content", {}).get("parts", [])
                        if text_parts and "text" in text_parts[0]:
                            return text_parts[0]["text"]
            except urllib.error.HTTPError as he:
                err_body = he.read().decode("utf-8", errors="ignore")
                last_error = f"HTTP {he.code}: {err_body}"
                if he.code == 400 and "API key not valid" in err_body:
                    return "⚠️ **Invalid Gemini API Key:** Aapki paste ki hui API key valid nahi hai. Baraye mehrbani Google AI Studio (aistudio.google.com) se nayi free key generate karke paste karein."
            except Exception as e:
                last_error = str(e)

        return (
            f"⚠️ **Gemini API Error:** {last_error[:180]}\n\n"
            "Kindly check:\n"
            "1. Is your API key active and valid from Google AI Studio?\n"
            "2. Ensure you have active internet connectivity."
        )

    def respond(self, query: str, gemini_key: str = "", force_gemini: bool = False):
        has_key = bool(gemini_key and len(gemini_key.strip()) > 20)

        # Force Gemini Mode
        if force_gemini and has_key:
            reply = self.call_gemini(query, gemini_key)
            log_chat_to_db(query, reply, "gemini_direct", 0.98)
            return {
                "response": reply,
                "intent": "gemini_generative",
                "confidence": 0.98,
                "category": "Gemini AI",
                "source": "Gemini 1.5 Flash"
            }

        # Local NLU Match
        intent, conf, cat = self.find_best_intent(query)
        if intent and conf >= 0.50:
            for item in self.kb.get("intents", []):
                if item.get("tag") == intent:
                    reply = random.choice(item.get("responses", ["I am here to help!"]))
                    log_chat_to_db(query, reply, intent, conf)
                    return {
                        "response": reply,
                        "intent": intent,
                        "confidence": conf,
                        "category": cat,
                        "source": "Local NLU (difflib)"
                    }

        # Hybrid Fallback to Gemini if low confidence
        if has_key:
            reply = self.call_gemini(query, gemini_key)
            log_chat_to_db(query, reply, "gemini_fallback", 0.92)
            return {
                "response": reply,
                "intent": "generative_fallback",
                "confidence": 0.92,
                "category": "AI Fitness Advisor",
                "source": "Gemini 1.5 Flash"
            }

        # Rule-based Fallback
        fallback_item = next((i for i in self.kb.get("intents", []) if i.get("tag") == "fallback"), None)
        reply = random.choice(fallback_item["responses"]) if fallback_item else "Mujhe samajh nahi aya. Baraye mehrbani apna sawal rephrase karein."
        log_chat_to_db(query, reply, "fallback", conf)
        return {
            "response": reply,
            "intent": "fallback",
            "confidence": conf,
            "category": "General",
            "source": "Local Fallback"
        }

engine = FitCraftEngine(kb)

# ---------------------------------------------------------
# 5. Session State Management
# ---------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": (
            "Assalam o Alaikum! Main **FitCraft AI** hoon — aapka personal Fitness, Home Workout & Nutrition Coach! 🏋️‍♂️\n\n"
            "Mujhse aap in topics par kisi bhi waqt guidance le sakte hain:\n"
            "• **Fat Loss & Belly Fat:** Calorie deficit, local Pakistani diet modifications\n"
            "• **Muscle Building:** Progressive overload, hypertrophy, protein intake\n"
            "• **Sasta Desi Protein:** Ande (eggs), chicken, daal, chana, paneer ke macro stats\n"
            "• **Desk Worker Relief:** Computer/phone se hone wale gardan aur kamar dard ke stretches\n"
            "• **Creatine & Supplements:** Real facts, correct doses, safe usage"
        ),
        "intent": "greeting",
        "confidence": 1.0,
        "category": "General",
        "source": "FitCraft System"
    }]

if "user_trigger" not in st.session_state:
    st.session_state.user_trigger = None

# ---------------------------------------------------------
# 6. Sidebar (Clean Crisp Light Style)
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 10px 0 16px 0;'>
        <div style='font-size: 3rem;'>🏋️‍♂️</div>
        <div style='font-size: 1.35rem; font-weight: 800; color: #0f172a; margin-top: 4px;'>FitCraft AI</div>
        <div style='font-size: 0.76rem; color: #64748b; font-weight: 600; letter-spacing: 0.5px;'>SMART WORKOUT &amp; NUTRITION COACH</div>
    </div>
    """, unsafe_allow_html=True)

    # Gemini API Key Section
    st.markdown('<div class="sidebar-panel"><h4>🤖 Google Gemini 1.5 API</h4>', unsafe_allow_html=True)
    gemini_key = st.text_input(
        "API Key",
        value=os.getenv("GEMINI_API_KEY", ""),
        type="password",
        placeholder="AIzaSy... paste key",
        help="Paste free API key from Google AI Studio (aistudio.google.com)"
    )
    col_k1, col_k2 = st.columns([1, 1])
    with col_k1:
        if gemini_key:
            st.markdown("<span style='color:#059669;font-size:0.75rem;font-weight:700;'>● Key Active</span>", unsafe_allow_html=True)
        else:
            st.markdown("<span style='color:#64748b;font-size:0.75rem;'>○ Local Mode</span>", unsafe_allow_html=True)
    with col_k2:
        prefer_gemini = st.checkbox("Force Gemini", value=False, help="Route all queries directly to Gemini 1.5 Flash.")
    st.markdown("</div>", unsafe_allow_html=True)

    # Quick Prompts
    st.markdown('<div class="sidebar-panel"><h4>⚡ Instant Questions</h4>', unsafe_allow_html=True)
    quick_queries = [
        "Belly fat kaise kam karein?",
        "High protein Pakistani diet under PKR 400",
        "How to build muscle at home without gym?",
        "Is creatine safe for beginners in Pakistan?",
        "Desk worker stretches for neck and back pain",
        "Skinny fat body recomposition guide",
        "Kitna paani peena chahiye rozana?",
        "Intermittent fasting 16/8 routine rules"
    ]
    for q in quick_queries:
        if st.button(f"❯ {q}", key=f"q_{abs(hash(q)) % 100000}", use_container_width=True):
            st.session_state.user_trigger = q
    st.markdown("</div>", unsafe_allow_html=True)

    # Student Profile
    st.markdown('<div class="sidebar-panel"><h4>🎓 Project Info</h4>', unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size: 0.82rem; line-height: 1.8; color: #475569;'>
        👤 <b>Student:</b> Zubair<br>
        🎯 <b>Domain:</b> Fitness &amp; Macro Nutrition<br>
        🧠 <b>NLU:</b> difflib SequenceMatcher + Jaccard<br>
        🤖 <b>LLM:</b> Google Gemini 1.5 Flash<br>
        💾 <b>DB:</b> SQLite3
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Chat Actions
    c_btn1, c_btn2 = st.columns(2)
    with c_btn1:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    with c_btn2:
        if st.session_state.messages:
            transcript = "\n".join([
                f"[{m['role'].upper()}]: {m['content']}\n"
                for m in st.session_state.messages
            ])
            st.download_button(
                "📥 Export",
                data=transcript,
                file_name=f"FitCraft_Chat_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True
            )

# ---------------------------------------------------------
# 7. Hero Banner (Light Clean Theme)
# ---------------------------------------------------------
st.markdown("""
<div class="hero-card">
    <div class="hero-badge">⚡ Powered by Python · SQLite · difflib · Google Gemini</div>
    <div class="hero-title">FitCraft AI — <span>Personal Fitness &amp; Nutrition Coach</span></div>
    <div class="hero-subtitle">
        Your complete science-backed fitness companion. Chat with your intelligent coach in Roman Urdu or English, generate customized home workout routines, and explore budget-friendly Pakistani nutrition!
    </div>
    <div class="hero-tags">
        <span class="hero-tag">💬 AI Fitness Chatbot</span>
        <span class="hero-tag">🔥 Fat Loss &amp; Deficit</span>
        <span class="hero-tag">💪 Muscle Hypertrophy</span>
        <span class="hero-tag">🥗 Pakistani High-Protein Diet</span>
        <span class="hero-tag">🧘 Desk Worker Posture Fix</span>
        <span class="hero-tag">🏠 Calisthenics &amp; Dumbbells</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 8. Main Application Tabs
# Restored: 💬 AI Fitness Coach
# Kept: 🏋️ Custom Workout Generator, 🥗 Desi Protein Guide
# Removed: BMR Calculator & Tracker
# ---------------------------------------------------------
tab_chat, tab_workout, tab_food = st.tabs([
    "💬  AI Fitness Coach",
    "🏋️  Custom Workout Generator",
    "🥗  Desi Protein Guide"
])

# =========================================================
# TAB 1 — AI Fitness Coach (Restored with Light Theme)
# =========================================================
with tab_chat:
    # Mode Status Indicator Banner
    if gemini_key:
        if prefer_gemini:
            mode_desc = "🚀 <b>Gemini Primary Mode:</b> All queries are directly processed by Google Gemini 1.5 Flash."
            tag_color = "#0284c7"
            tag_bg = "#e0f2fe"
        else:
            mode_desc = "✨ <b>Hybrid Mode Active:</b> Instant verified NLU with difflib + Gemini 1.5 Flash generative fallback."
            tag_color = "#059669"
            tag_bg = "#ecfdf5"
    else:
        mode_desc = "🛡️ <b>Local NLU Mode:</b> Running 100% offline using `knowledge_base.json` & `difflib`. Add Gemini API Key in sidebar for open questions."
        tag_color = "#0369a1"
        tag_bg = "#f0f9ff"

    st.markdown(f"""
    <div class="status-pill-banner">
        <span>{mode_desc}</span>
        <span style="background:{tag_bg}; color:{tag_color}; padding:4px 12px; border-radius:8px; font-weight:700; font-size:0.75rem;">
            ● Ready
        </span>
    </div>
    """, unsafe_allow_html=True)

    # Chat Bubbles Rendering
    chat_container = st.container()
    with chat_container:
        st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f'<div class="chat-msg-user">🧑‍💻 {msg["content"]}</div>', unsafe_allow_html=True)
            else:
                body = msg["content"].replace("\n", "<br>")
                conf_pct = msg.get("confidence", 0.0) * 100
                chips = f"""
                <div class="meta-chips">
                    <span class="chip chip-intent">🏷️ {msg.get("intent", "N/A")}</span>
                    <span class="chip chip-conf">🎯 {conf_pct:.0f}% Match</span>
                    <span class="chip chip-cat">📁 {msg.get("category", "General")}</span>
                    <span class="chip chip-source">⚡ {msg.get("source", "Engine")}</span>
                </div>
                """ if "intent" in msg else ""
                st.markdown(f'<div class="chat-msg-bot">🤖 {body}{chips}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Chat Input
    query_input = None
    if st.session_state.user_trigger:
        query_input = st.session_state.user_trigger
        st.session_state.user_trigger = None
    else:
        query_input = st.chat_input("Apna fitness, workout ya diet ka sawal likhein... (e.g. 'belly fat kaise kam karein?')")

    if query_input:
        st.session_state.messages.append({"role": "user", "content": query_input})
        with st.spinner("FitCraft AI is analyzing..."):
            ans = engine.respond(query_input, gemini_key, force_gemini=prefer_gemini)
        st.session_state.messages.append({
            "role": "assistant",
            "content": ans["response"],
            "intent": ans["intent"],
            "confidence": ans["confidence"],
            "category": ans["category"],
            "source": ans["source"]
        })
        st.rerun()

# =========================================================
# TAB 2 — Custom Workout Generator
# =========================================================
with tab_workout:
    st.markdown("### 🏋️ Custom Workout Routine Generator")
    st.markdown(
        '<p style="color: #64748b; margin-top: -8px; margin-bottom: 24px;">'
        'Generate structured, science-backed workout plans tailored to your available equipment and training experience.'
        '</p>',
        unsafe_allow_html=True
    )

    wc1, wc2, wc3 = st.columns(3)
    with wc1:
        w_level = st.selectbox("🎯 Fitness Experience Level", ["Beginner", "Intermediate", "Advanced"])
    with wc2:
        w_equip = st.selectbox(
            "🏠 Available Equipment",
            [
                "No Equipment (Bodyweight / Calisthenics)",
                "Dumbbells Only",
                "Full Gym (Barbells, Cables & Machines)"
            ]
        )
    with wc3:
        w_focus = st.selectbox(
            "💡 Target Training Focus",
            [
                "Full Body Metabolic Burn",
                "Upper Body (Chest, Shoulders, Arms)",
                "Lower Body & Core (Legs & Abs)",
                "Desk Worker Posture & Stretches"
            ]
        )

    ROUTINES = {
        "Full Body Metabolic Burn": {
            "No Equipment (Bodyweight / Calisthenics)": [
                ("Jumping Jacks", "2 sets × 45 sec", "Cardio Warmup", "30 sec", "Light on your toes, rhythmic breathing"),
                ("Bodyweight Air Squats", "3 sets × 20 reps", "Quads & Glutes", "45 sec", "Chest up, hips below knees, drive through midfoot"),
                ("Standard Push-ups", "3 sets × 12-15 reps", "Chest & Triceps", "60 sec", "Hands slightly wider than shoulders, core braced tight"),
                ("Walking Bodyweight Lunges", "3 sets × 12 reps/leg", "Quads & Hamstrings", "45 sec", "90-degree angle on both knees, controlled descent"),
                ("Plank Isometric Hold", "3 sets × 45 sec", "Core & Transverse Abdominis", "45 sec", "Hips level with shoulders, don't let lower back sag"),
                ("Mountain Climbers", "3 sets × 30 sec", "Cardio & Core", "30 sec", "Drive knees straight toward chest explosively"),
            ],
            "Dumbbells Only": [
                ("DB Goblet Squats", "3 sets × 12 reps", "Quads & Glutes", "60 sec", "Hold dumbbell vertically at chest, elbows inside knees"),
                ("DB Floor Press", "3 sets × 12 reps", "Chest & Triceps", "60 sec", "Touch triceps lightly to floor, press upward explosively"),
                ("DB Romanian Deadlifts (RDL)", "3 sets × 12 reps", "Hamstrings & Glutes", "60 sec", "Hinge deeply at hips, keep flat spine throughout"),
                ("DB Dual Bent-Over Rows", "3 sets × 12 reps", "Lats & Upper Back", "60 sec", "Pull elbows back toward hips, squeeze shoulder blades"),
                ("DB Standing Overhead Press", "3 sets × 10 reps", "Shoulders & Core", "60 sec", "Brace glutes and abs, press dumbbell overhead"),
            ],
            "Full Gym (Barbells, Cables & Machines)": [
                ("Barbell Back Squats", "4 sets × 8 reps", "Quads & Glutes", "90 sec", "Break parallel cleanly, drive upward through whole foot"),
                ("Barbell Bench Press", "4 sets × 8 reps", "Chest, Anterior Delts", "90 sec", "Retract shoulder blades, pause momentarily on chest"),
                ("Barbell Conventional Deadlift", "3 sets × 6 reps", "Full Posterior Chain", "120 sec", "Keep bar close to shins, hinge with neutral spine"),
                ("Wide-Grip Pull-ups / Lat Pulldown", "3 sets × 10 reps", "Lats & Biceps", "90 sec", "Full stretch at top, pull chin cleanly above bar"),
                ("Cable Lateral Raises", "3 sets × 15 reps", "Side Deltoids", "60 sec", "Control negative tempo, slight forward lean"),
            ]
        },
        "Upper Body (Chest, Shoulders, Arms)": {
            "No Equipment (Bodyweight / Calisthenics)": [
                ("Standard Push-ups", "4 sets × 15 reps", "Chest & Triceps", "60 sec", "Elbows tucked at 45 degrees, full lockout"),
                ("Feet-Elevated Decline Push-ups", "3 sets × 12 reps", "Upper Clavicular Chest", "60 sec", "Feet on chair or bed, lowers emphasis on upper pecs"),
                ("Diamond Close-Grip Push-ups", "3 sets × 10 reps", "Triceps & Inner Chest", "60 sec", "Thumb and index fingers touch, elbows track backward"),
                ("Pike Push-ups", "3 sets × 10 reps", "Shoulders & Upper Chest", "60 sec", "Hips high in inverted V, touch top of forehead to floor"),
                ("Chair Bench Dips", "3 sets × 15 reps", "Triceps & Front Delts", "45 sec", "Keep back close to edge, 90 degree elbow bend"),
            ],
            "Dumbbells Only": [
                ("DB Neutral Grip Floor Press", "4 sets × 12 reps", "Chest & Triceps", "75 sec", "Squeeze pecs at lockout, 2-sec slow lowering"),
                ("DB Standing Lateral Raises", "4 sets × 15 reps", "Lateral Deltoids", "45 sec", "Lead with elbows, pause 1 sec at shoulder height"),
                ("DB Supinated Bicep Curls", "3 sets × 12 reps", "Biceps", "45 sec", "Rotate palms outward at top for maximum peak contraction"),
                ("DB Overhead Tricep Extension", "3 sets × 12 reps", "Triceps Long Head", "45 sec", "Keep elbows pointing straight forward"),
                ("DB Hammer Curls", "3 sets × 12 reps", "Brachialis & Forearms", "45 sec", "Neutral palm grip, strict no-swing form"),
            ],
            "Full Gym (Barbells, Cables & Machines)": [
                ("Incline Barbell Bench Press", "4 sets × 8 reps", "Upper Chest", "90 sec", "Bench at 30 degrees, bar touches upper chest"),
                ("Cable Standing Chest Flyes", "3 sets × 12 reps", "Sternal Pecs", "60 sec", "Wide hug motion, squeeze chest hard in center"),
                ("Seated DB Shoulder Press", "4 sets × 10 reps", "Front & Side Delts", "75 sec", "Full range of motion, avoid arching lower back"),
                ("EZ-Bar Preacher Curls", "3 sets × 12 reps", "Biceps Short Head", "60 sec", "Strict isolation, slow controlled eccentric descent"),
                ("Tricep Rope Pushdowns", "3 sets × 12 reps", "Triceps Lateral Head", "60 sec", "Flare the rope outward at the bottom for peak lock"),
            ]
        },
        "Lower Body & Core (Legs & Abs)": {
            "No Equipment (Bodyweight / Calisthenics)": [
                ("Bulgarian Split Squats", "3 sets × 10 reps/leg", "Quads & Glutes", "75 sec", "Rear foot elevated on bed/couch, sink knee deep"),
                ("Single-Leg Glute Bridges", "3 sets × 15 reps/leg", "Glutes & Hamstrings", "45 sec", "Drive through working heel, squeeze glute at top"),
                ("Step Calf Raises", "4 sets × 20 reps", "Gastrocnemius", "30 sec", "Deep heel drop for stretch, explosive calf contraction"),
                ("Lying Leg Raises", "3 sets × 15 reps", "Lower Rectus Abdominis", "45 sec", "Keep lower back pressed against floor"),
                ("Seated Russian Twists", "3 sets × 20 reps", "Obliques & Core", "45 sec", "Legs elevated slightly, rotate torso side-to-side"),
            ],
            "Dumbbells Only": [
                ("DB Sumo Squats", "4 sets × 15 reps", "Adductors & Glutes", "60 sec", "Wide stance with toes flared out 45 degrees"),
                ("DB Dumbbell Walking Lunges", "3 sets × 12 reps/leg", "Quads & Glutes", "60 sec", "Long strides for glute focus, short for quads"),
                ("DB Romanian Deadlifts", "3 sets × 12 reps", "Hamstring Stretch", "75 sec", "Push hips straight back, feel deep stretch in legs"),
                ("DB Side Goblet Lunges", "3 sets × 10 reps/side", "Abductors & Hips", "45 sec", "Keep non-working leg straight, sit hips back"),
                ("Plank DB Pull-Throughs", "3 sets × 10 reps/side", "Anti-Rotation Core", "45 sec", "Keep hips square to floor without twisting"),
            ],
            "Full Gym (Barbells, Cables & Machines)": [
                ("Barbell Back Squats", "5 sets × 5 reps", "Quads & Posterior", "120 sec", "Heavy compound lifting, brace intra-abdominal pressure"),
                ("Angled Leg Press Machine", "3 sets × 15 reps", "Quad Hypertrophy", "90 sec", "Feet shoulder-width, never lock knees at the top"),
                ("Lying Hamstring Leg Curls", "3 sets × 12 reps", "Hamstrings", "60 sec", "Dorsiflex toes, squeeze hamstrings at apex"),
                ("Standing Machine Calf Raises", "4 sets × 20 reps", "Calves", "30 sec", "Full 2-second stretch at bottom of pedal"),
                ("Cable Kneeling Rope Crunch", "3 sets × 15 reps", "Abs Hypertrophy", "45 sec", "Curl spine like a shrimp, avoid pulling with arms"),
            ]
        },
        "Desk Worker Posture & Stretches": {
            "No Equipment (Bodyweight / Calisthenics)": [
                ("Cat-Cow Spinal Waves", "2 sets × 10 cycles", "Thoracic Mobility", "20 sec", "Deep inhale on cow arch, full exhale on cat curve"),
                ("Doorway Pectoral Stretch", "3 sets × 40 sec", "Chest & Ant Delts", "20 sec", "Forearm on door jamb, gently lean chest forward"),
                ("Chin Tucks (Tech Neck Remedy)", "3 sets × 15 reps", "Deep Neck Flexors", "15 sec", "Draw head straight back like making a double chin"),
                ("Half-Kneeling Hip Flexor Stretch", "2 sets × 40 sec/leg", "Psoas / Hip Flexors", "20 sec", "Squeeze glute of back leg, push hips gently forward"),
                ("Bodyweight Glute Bridges", "3 sets × 20 reps", "Glute Activation", "30 sec", "Reactivates dormant glutes caused by all-day sitting"),
                ("Wall Angels", "3 sets × 10 reps", "Rhomboids & Traps", "30 sec", "Keep elbows and wrists glued to wall while sliding up"),
            ],
            "Dumbbells Only": [
                ("Cat-Cow Spinal Waves", "2 sets × 10 cycles", "Thoracic Spine", "20 sec", "Inhale arch, exhale round"),
                ("Light DB Facepulls / Reverse Fly", "3 sets × 15 reps", "Rear Delts & Rotators", "45 sec", "Focus on upper back retraction, pull to nose level"),
                ("DB Chest-Supported Incline Row", "3 sets × 12 reps", "Mid Back / Rhomboids", "60 sec", "Eliminates lower back strain, strengthens posture"),
                ("DB Cuban Press", "3 sets × 10 reps", "External Shoulder Rotators", "45 sec", "Very light dumbbells, strict smooth rotational tempo"),
                ("DB Romanian Deadlifts", "3 sets × 12 reps", "Hamstrings & Lower Back", "60 sec", "Fixes anterior pelvic tilt caused by prolonged sitting"),
            ],
            "Full Gym (Barbells, Cables & Machines)": [
                ("Cable Facepulls with Rope", "4 sets × 15 reps", "Rear Delts & Upper Back", "45 sec", "Pull hands past ears, rotate forearms upward"),
                ("Wide-Grip Lat Pulldowns", "3 sets × 12 reps", "Lats & Scapulae", "60 sec", "Pull down to clavicle, avoid swinging back"),
                ("Seated Cable Row (Neutral V-Bar)", "3 sets × 12 reps", "Rhomboids & Mid-Traps", "60 sec", "Squeeze shoulder blades together for 1 full second"),
                ("Reverse Pec Deck Fly", "3 sets × 15 reps", "Rear Deltoid Isolation", "45 sec", "Elbows soft, push handles outward and back"),
                ("Foam Roller Thoracic Extension", "2 sets × 60 sec", "Spinal Decompression", "30 sec", "Roll upper back slowly, open up ribcage with arms behind head"),
            ]
        }
    }

    if st.button("⚡ Generate My Custom Routine", type="primary", use_container_width=True):
        routine_exercises = ROUTINES.get(w_focus, {}).get(w_equip, [])
        st.markdown(f"""
        <div style="background: #f0f9ff; border: 1px solid #bae6fd; border-radius: 16px; padding: 20px 24px; margin: 20px 0 16px 0;">
            <div style="font-size:0.75rem; text-transform:uppercase; letter-spacing:0.8px; color:#0284c7; font-weight:700;">Custom Routine Plan</div>
            <h3 style="margin:4px 0 0 0; color:#0f172a;">{w_focus}</h3>
            <p style="margin:6px 0 0 0; color:#64748b; font-size:0.88rem;">
                Level: <b style="color:#0f172a;">{w_level}</b> &nbsp;·&nbsp; 
                Equipment: <b style="color:#0f172a;">{w_equip}</b> &nbsp;·&nbsp; 
                Exercises: <b style="color:#0284c7;">{len(routine_exercises)} Movements</b>
            </p>
        </div>""", unsafe_allow_html=True)

        for idx, (ex_name, volume, muscle, rest, cue) in enumerate(routine_exercises, 1):
            st.markdown(f"""
            <div class="routine-card">
                <div style="display:flex; align-items:center; gap:12px;">
                    <div style="width:30px; height:30px; background:#0284c7; border-radius:8px; display:flex; align-items:center; justify-content:center; font-size:0.82rem; font-weight:800; color:white; flex-shrink:0;">
                        {idx}
                    </div>
                    <p class="routine-title">{ex_name}</p>
                </div>
                <div style="display:flex; gap:8px; flex-wrap:wrap; margin-top:10px;">
                    <span class="badge-pill badge-volume">📊 {volume}</span>
                    <span class="badge-pill badge-muscle">💪 {muscle}</span>
                    <span class="badge-pill badge-rest">⏱ Rest: {rest}</span>
                </div>
                <p style="font-size:0.82rem; color:#64748b; margin:10px 0 0 0; line-height:1.5;">💡 <b>Form Cue:</b> {cue}</p>
            </div>""", unsafe_allow_html=True)

        plan_txt = f"FITCRAFT AI — CUSTOM WORKOUT ROUTINE\n"
        plan_txt += f"Generated: {datetime.now().strftime('%d-%B-%Y %H:%M')}\n"
        plan_txt += f"Focus: {w_focus}\nLevel: {w_level}\nEquipment: {w_equip}\n"
        plan_txt += "="*50 + "\n\n"
        for i, ex in enumerate(routine_exercises, 1):
            plan_txt += f"{i}. {ex[0]}\n   Volume: {ex[1]}\n   Target Muscle: {ex[2]}\n   Rest: {ex[3]}\n   Coaching Form: {ex[4]}\n\n"

        st.download_button(
            "📄 Download Workout Routine (.txt)",
            data=plan_txt,
            file_name=f"FitCraft_Routine_{w_focus[:15].replace(' ','_')}.txt",
            mime="text/plain",
            use_container_width=True
        )

# =========================================================
# TAB 3 — Desi Protein Guide
# =========================================================
with tab_food:
    st.markdown("### 🥗 Affordable Desi High-Protein Food Directory")
    st.markdown(
        '<p style="color: #64748b; margin-top: -8px; margin-bottom: 24px;">'
        'The best, most accessible, and budget-friendly Pakistani whole foods to hit your daily protein targets without expensive imported supplements.'
        '</p>',
        unsafe_allow_html=True
    )

    pakistani_foods = [
        ("🥚", "Whole Eggs (Ublay / Talay Ande)", "2 Large Eggs", "13g", "145 kcal", "PKR 55–65",
         "The gold-standard reference protein (Biological Value: 100). Eat yolk and whites for choline, healthy fats, and full amino acids."),
        ("🍗", "Cooked Chicken Breast", "100g Cooked", "31g", "165 kcal", "PKR 120–140",
         "The leanest high-protein food available locally. Broiler chicken breast is cheap, zero carb, and virtually fat-free."),
        ("🫘", "Safaid Chana (Boiled Chickpeas)", "1 Cup (160g)", "14.5g", "260 kcal", "PKR 45–55",
         "Rich in complex dietary fiber and protein. Great post-workout food that keeps insulin stable for hours."),
        ("🧀", "Fresh Homemade Paneer", "100g", "18g", "210 kcal", "PKR 85–105",
         "Made at home with milk and lemon juice. Loaded with slow-digesting casein protein, ideal right before sleeping."),
        ("🍲", "Masoor / Moong / Daal Chawal", "1 Large Bowl (220g)", "15g", "225 kcal", "PKR 40–55",
         "A Pakistani household staple. Combining lentils with rice or roti creates a complete amino acid profile."),
        ("🥛", "Fresh Dahi (Plain Curd / Yogurt)", "1 Cup (200g)", "9g", "130 kcal", "PKR 40–50",
         "Natural probiotics for gut health and bloating relief, along with bone-strengthening calcium and protein."),
        ("🥜", "Raw Peanuts / Peanut Butter", "2 tbsp (32g)", "8g", "190 kcal", "PKR 40–60",
         "Dense healthy monounsaturated fats. Outstanding cost-to-calorie ratio for hardgainers struggling to gain weight."),
        ("🐟", "Rohu / Rahu Machli (Fish)", "100g", "22g", "135 kcal", "PKR 110–145",
         "Packed with heart-healthy Omega-3 fatty acids and clean lean protein. Excellent for brain health and fat loss."),
    ]

    col_f1, col_f2 = st.columns(2)
    for i, (icon, fname, serving, protein, calories, est_cost, coach_note) in enumerate(pakistani_foods):
        target_col = col_f1 if i % 2 == 0 else col_f2
        with target_col:
            st.markdown(f"""
            <div class="food-item">
                <div style="display:flex; align-items:center; gap:12px; margin-bottom:12px;">
                    <div style="font-size:2rem;">{icon}</div>
                    <div>
                        <div style="font-size:1.05rem; font-weight:700; color:#0f172a; margin:0;">{fname}</div>
                        <div style="font-size:0.78rem; color:#64748b;">Standard Serving: {serving}</div>
                    </div>
                </div>
                <div style="display:flex; gap:16px; background:#f8fafc; padding:10px 14px; border-radius:12px; border:1px solid #e2e8f0; margin-bottom:10px;">
                    <div>
                        <div class="food-protein-num">{protein}</div>
                        <div style="font-size:0.72rem; color:#64748b; text-transform:uppercase; font-weight:600;">Protein</div>
                    </div>
                    <div style="border-left:1px solid #cbd5e1; padding-left:14px;">
                        <div style="font-size:1.1rem; font-weight:700; color:#0284c7;">{calories}</div>
                        <div style="font-size:0.72rem; color:#64748b; text-transform:uppercase; font-weight:600;">Calories</div>
                    </div>
                    <div style="border-left:1px solid #cbd5e1; padding-left:14px;">
                        <div style="font-size:1.1rem; font-weight:700; color:#b45309;">{est_cost}</div>
                        <div style="font-size:0.72rem; color:#64748b; text-transform:uppercase; font-weight:600;">Est. Cost</div>
                    </div>
                </div>
                <p style="font-size:0.8rem; color:#64748b; margin:0; line-height:1.5;">💡 <i>{coach_note}</i></p>
            </div>""", unsafe_allow_html=True)

    # Sample PKR 400 Meal Plan
    st.markdown("""
    <div style="background: #ffffff; border: 1px solid #86efac; border-radius: 18px; padding: 26px; margin-top: 12px; box-shadow: 0 4px 16px -2px rgba(16, 185, 129, 0.08);">
        <h4 style="color:#059669; margin:0 0 10px 0; font-size:1.15rem;">📅 Daily Student Budget Meal Plan — Under PKR 400 (~75g Protein)</h4>
        <p style="color:#475569; font-size:0.86rem; margin-bottom:16px;">
            Designed specifically for Pakistani students and budget-conscious individuals who want science-based gains without imported supplements.
        </p>
        <table style="width:100%; border-collapse:collapse; font-size:0.88rem; color:#334155;">
            <tr style="border-bottom:1px solid #f1f5f9;">
                <td style="padding:10px 8px; font-weight:700; color:#0f172a; width:22%;">🌅 Breakfast</td>
                <td style="padding:10px 8px;">3 Boiled Eggs + 1 Whole-wheat Roti + Chai / Water</td>
                <td style="padding:10px 8px; color:#059669; font-weight:700; text-align:right;">~19.5g Protein</td>
            </tr>
            <tr style="border-bottom:1px solid #f1f5f9;">
                <td style="padding:10px 8px; font-weight:700; color:#0f172a;">☀️ Lunch</td>
                <td style="padding:10px 8px;">1 Large Bowl Daal + 1 Plate Steamed Chawal + Kachumber Salad</td>
                <td style="padding:10px 8px; color:#059669; font-weight:700; text-align:right;">~15g Protein</td>
            </tr>
            <tr style="border-bottom:1px solid #f1f5f9;">
                <td style="padding:10px 8px; font-weight:700; color:#0f172a;">🏋️ Pre-Workout</td>
                <td style="padding:10px 8px;">1 Banana + 1 Spoon Peanut Butter + 1 Glass Doodh (Milk)</td>
                <td style="padding:10px 8px; color:#059669; font-weight:700; text-align:right;">~12g Protein</td>
            </tr>
            <tr>
                <td style="padding:10px 8px; font-weight:700; color:#0f172a;">🌙 Dinner</td>
                <td style="padding:10px 8px;">100g Chicken Salan / Breast + 1 Roti + 1 Small Cup Dahi</td>
                <td style="padding:10px 8px; color:#059669; font-weight:700; text-align:right;">~33g Protein</td>
            </tr>
        </table>
        <div style="margin-top:16px; padding:12px 16px; background:#f0fdf4; border:1px solid #bbf7d0; border-radius:12px; font-size:0.86rem; color:#15803d;">
            ✅ <b>Total Daily Yield: ~79.5g Complete Protein</b> — Ideal for anyone weighing 60-75kg to recover and build lean muscle tissue.
        </div>
    </div>""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 9. Clean Light Footer
# ---------------------------------------------------------
st.markdown("<br><hr style='border:none; border-top:1px solid #e2e8f0; margin:40px 0 20px 0;'>", unsafe_allow_html=True)
st.markdown("""
<div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; color:#94a3b8; font-size:0.8rem; padding-bottom:20px;">
    <div>
        🏋️‍♂️ <b>FitCraft AI</b> — Academic AI Project by <span style="color:#0f172a; font-weight:600;">Zubair</span>
    </div>
    <div>
        Standard Library NLU (<code style="color:#0284c7; background:#e0f2fe; padding:2px 6px; border-radius:4px;">difflib</code>) · SQLite3 · Google Gemini 1.5 Flash
    </div>
</div>
""", unsafe_allow_html=True)
