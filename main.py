from fastapi import FastAPI, Header, HTTPException , Depends
from fastapi import security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from database import get_connection
from auth import hash_password, verify_password,create_token, decode_token
from datetime import date

app = FastAPI()
security = HTTPBearer()

@app.post("/register")
def register(username: str, email: str, password: str):
    conn = get_connection()
    cursor = conn.cursor()
    
    hashed = hash_password(password)  
    
    cursor.execute(
        "INSERT INTO users (username,email,password,created_date) VALUES (%s,%s,%s,%s)",
        (username,email,hashed,date.today())
    )
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return {"message": "User registered successfully"}

@app.post("/login")
def login(email: str, password: str):
    conn = get_connection()
    cursor = conn.cursor()
    
    # email se user dhundho
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    
    # agar user nahi mila
    if not user:
        return {"error": "User not found"}
    
    # password verify karo
    if not verify_password(password,user[3]):
        return {"error": "Wrong password"}
    
    # token banao
    token = create_token({"user_id": user[0], "email": user[2]})
    
    return {"token": token}


@app.post("/notes")
def create_note(title: str, content: str, credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials  # automatically token milta hai!
    user = decode_token(token)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token!")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    user_id = user["user_id"]
    
    cursor.execute(
        "INSERT INTO notes (user_id, title, content, created_date) VALUES (%s,%s,%s,%s)",
        (user_id, title, content, date.today())
    )
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return {"message": "Notes created successfully"}


@app.get("/notes")
def get_notes(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user = decode_token(token)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token!")
    
    user_id = user["user_id"]
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM notes WHERE user_id = %s",(user_id,))
    notes = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return {"notes": notes}

@app.delete("/notes/{note_id}")
def delete_note(note_id: int, credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user = decode_token(token)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token!")
    
    user_id = user["user_id"]
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "DELETE FROM notes WHERE user_id= %s AND note_id = %s",
        (user_id, note_id)
    )
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return {"message": "Note deleted succesful"}