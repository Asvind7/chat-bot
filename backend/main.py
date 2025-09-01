
from controller.chat_from_bot import *
from controller.queryProcessor import process_query
# ---------- Routes ----------
@app.get("/ask")
def ask(q: str = Query(..., description="Your question")):
    res_text = process_query("local_user", q, KB)  # New clarification logic
    return JSONResponse({"text": res_text})\
        
        

@app.get("/health")
def health():
    return {"ok": True}
