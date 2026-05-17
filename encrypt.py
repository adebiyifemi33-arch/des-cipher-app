from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad
import base64

app = FastAPI()

class DESRequest(BaseModel):
    text: str
    key: str

@app.post("/api/encrypt")
def encrypt_text(request: DESRequest):
    if len(request.key) != 8:
        raise HTTPException(status_code=400, detail="Key must be exactly 8 characters long.")
    cipher = DES.new(request.key.encode('utf-8'), DES.MODE_ECB)
    padded_text = pad(request.text.encode('utf-8'), DES.block_size)
    encrypted_bytes = cipher.encrypt(padded_text)
    return {"result": base64.b64encode(encrypted_bytes).decode('utf-8')}
