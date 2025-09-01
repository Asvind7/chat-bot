from .find import *

def format_character_answer(c):
    bounty = f" Bounty: {c['bounty']:,}." if c.get("bounty") else ""
    df = ""
    if c.get("devil_fruit"):
        df = f" Devil Fruit: {c['devil_fruit']['name']} ({c['devil_fruit']['type']})."
    text = f"{c['name']} — {c['role']}. {c['summary']}{df}{bounty}"
    return {
        "text": text,
        "card": {
            "title": c["name"],
            "subtitle": c["role"],
        }
    }
    
def format_explanation_answer(c):
    bounty = f" Bounty: {c['bounty']:,}." if c.get("bounty") else ""
    df = ""
    text=""
    if c.get("devil_fruit"):
        df = f" Devil Fruit: {c['devil_fruit']['name']} ({c['devil_fruit']['type']}) it ({c['devil_fruit']['description']})."
        text = f"{c['name']} has eaten  {df}"
    else:
        text = f"{c['name']} doesn't have any devil fruit"
    return {
        "text": text,
        "card": {
            "title": c["name"],
            "subtitle": c["role"],
        }
    }
    