import json
import re
from difflib import get_close_matches
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# main.py



# ---------- Load data ----------
with open("info/strawhats.json", "r", encoding="utf-8") as f:
    KB = json.load(f)

# Build quick lookups
ROLE_KEYWORDS = {
    "captain": "Captain",
    "swordsman": "Swordsman",
    "first mate": "Swordsman",
    "navigator": "Navigator",
    "sniper": "Sniper",
    "cook": "Cook",
    "chef": "Cook",
    "doctor": "Doctor",
    "archaeologist": "Archaeologist",
    "shipwright": "Shipwright",
    "musician": "Musician",
    "helmsman": "Helmsman"
}



CHAR_NAMES = []
ALIAS_TO_CHAR = {}
DF_TO_CHAR = {}
for c in KB["characters"]:
    CHAR_NAMES.append(c["name"])
    for a in c.get("aliases", []):
        ALIAS_TO_CHAR[a.lower()] = c["name"]
    if c.get("devil_fruit"):
        DF_TO_CHAR[c["devil_fruit"]["name"].lower()] = c["name"]

SHIP_NAMES = [s["name"] for s in KB["ships"]]



# ---------- App ----------
app = FastAPI(title="Straw Hat Chatbot API")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # during dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Helpers ----------
def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())





    