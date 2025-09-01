from .utils import *

def find_character_by_name_or_alias(q: str):
    ql = (q or "").strip().lower()
    if not ql:
        return None

    # 1) Direct contains/equality checks (both directions) on names & aliases
    for c in KB["characters"]:
        name = c.get("name", "").strip().lower()
        if name and (ql == name or ql in name or name in ql):
            return c
        for alias in c.get("aliases", []):
            al = (alias or "").strip().lower()
            if al and (ql == al or ql in al or al in ql):
                return c

    # 2) Token overlap (e.g., "zoro" vs "roronoa zoro")
    q_tokens = set(ql.split())
    if q_tokens:
        for c in KB["characters"]:
            name_tokens = set(c.get("name", "").lower().split())
            if q_tokens & name_tokens:
                return c
            alias_tokens = set()
            for alias in c.get("aliases", []):
                alias_tokens |= set((alias or "").lower().split())
            if q_tokens & alias_tokens:
                return c

    # 3) Fuzzy fallback (names + aliases)
    try:
        from difflib import get_close_matches
        corpus = []
        owner = []
        for c in KB["characters"]:
            nm = c.get("name", "")
            if nm:
                corpus.append(nm.lower())
                owner.append(nm)
            for alias in c.get("aliases", []):
                if alias:
                    corpus.append(alias.lower())
                    owner.append(nm)

        matches = get_close_matches(ql, corpus, n=1, cutoff=0.6)
        if matches:
            target = matches[0]
            # map back to the character by owner list
            for key, who in zip(corpus, owner):
                if key == target:
                    for c in KB["characters"]:
                        if c.get("name", "").lower() == who.lower():
                            return c
                    break
    except Exception:
        pass

    return None


def find_character_by_role(q: str):
    ql = q.lower()
    for kw, role in ROLE_KEYWORDS.items():
        if kw in ql:
            for c in KB["characters"]:
                if role.lower() in c["role"].lower():
                    return c
    return None

def find_by_devil_fruit(q: str):
    ql = q.lower()
    # fruit name in query?
    for fruit_name, user in DF_TO_CHAR.items():
        if fruit_name in ql:
            char = next(c for c in KB["characters"] if c["name"] == user)
            return {
                "text": f"{fruit_name} is used by {user}. {char['devil_fruit']['description']}",
                "card": {
                    "title": fruit_name,
                    "subtitle": f"User: {user}",
                }
            }
    # who ate ... ?
    if any(w in ql for w in ["who ate", "who has", "whose devil fruit", "user of"]):
        c = find_character_by_name_or_alias(q)
        if c and c.get("devil_fruit"):
            df = c["devil_fruit"]["name"]
            return {
                "text": f"{c['name']} ate the {df} ({c['devil_fruit']['type']}). {c['devil_fruit']['description']}",
                "card": {
                    "title": c["name"],
                    "subtitle": df,
                }
            }
    # what is x's fruit
    m = re.search(r"(?:what(?:'s| is) )?(.*?)(?:'s|s) (?:devil )?fruit", ql)
    if m:
        name_guess = m.group(1).strip()
        c = find_character_by_name_or_alias(name_guess)
        if c and c.get("devil_fruit"):
            df = c["devil_fruit"]
            return {
                "text": f"{c['name']}'s Devil Fruit is {df['name']} ({df['type']}). {df['description']}",
                "card": {
                    "title": c["name"],
                    "subtitle": df["name"],

                }
            }
    return None

def find_ship(q: str):
    ql = q.lower()
    for s in KB["ships"]:
        if s["name"].lower() in ql:
            return {
                "text": f"{s['name']}: {s['summary']}",
                "card": {
                    "title": s["name"],
                    "subtitle": s.get("type", ""),
                }
            }
    m = get_close_matches(q, SHIP_NAMES, n=1, cutoff=0.6)
    if m:
        s = next(x for x in KB["ships"] if x["name"] == m[0])
        return {
            "text": f"{s['name']}: {s['summary']}",
            "card": {
                "title": s["name"],
                "subtitle": s.get("type", ""),
            }
        }
    return None