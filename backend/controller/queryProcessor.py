 # import function
from .utils import *
from .find import *
from .chat_from_bot import *
 
user_sessions = {} 
def process_query(user_id: str, query: str, kb: dict):
    """
    Handles query with clarification logic for Devil Fruits.
    """
    ql = query.lower()

    # --- If we're waiting for clarification ---
    if user_id in user_sessions:
        session = user_sessions[user_id]
        pending = session.get("pending_category")

        if pending == "devil_fruit":
            explain_words = [
                "explain", "definition", "what is", "details",
                "tell me more", "about it", "it"
            ]
            if any(word in ql for word in explain_words):
                user_sessions.pop(user_id, None)
                return {"text": "A Devil Fruit is a mystical fruit that grants the eater special powers, but at the cost of the ability to swim."}["text"]
            char = find_character_by_name_or_alias(query)
            if char:
                user_sessions.pop(user_id, None)
                return format_explanation_answer(char)

            return {"text": "I couldn't find that character in my data. Which character's Devil Fruit do you want to know?"}

    # --- If vague Devil Fruit question ---
    # --- If vague Devil Fruit question ---
    # Extract all possible character names from KB
    if "devil fruit" in ql:
        possible_chars = [c["name"].lower() for c in kb["characters"]]
        for c in kb["characters"]:
            possible_chars.extend([a.lower() for a in c.get("aliases", [])])
    
        # If none of those names/aliases are in the query, ask for clarification
        if not any(name in ql for name in possible_chars):
            user_sessions[user_id] = {"pending_category": "devil_fruit"}
            return "Are you asking what a Devil Fruit is, or a specific character’s Devil Fruit?"
    

    # --- Fallback: normal  lookup ---
    ans = find_by_devil_fruit(query)
    if ans:
        return ans
    # 2) Ship
    ans = find_ship(query)
    if ans:
        return ans
    # 3) Role (“who is the helmsman”, etc.)
    c = find_character_by_role(query)
    if c:
        return format_character_answer(c)
    # 4) Name / alias
    c = find_character_by_name_or_alias(query)
    if c:
        return format_character_answer(c)
    # Fallback
    return {"text": "Sorry, I couldn't find anything for that in the Straw Hats.", "card": None}

   

