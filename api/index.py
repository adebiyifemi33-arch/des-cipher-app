from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import base64

app = FastAPI()

class DESRequest(BaseModel):
    text: str
    key: str

def validate_key(key: str) -> bytes:
    if len(key) != 8:
        raise HTTPException(status_code=400, detail="Key must be exactly 8 characters long.")
    return key.encode('utf-8')

@app.post("/api/encrypt")
def encrypt_text(request: DESRequest):
    try:
        key_bytes = validate_key(request.key)
        cipher = DES.new(key_bytes, DES.MODE_ECB)
        padded_text = pad(request.text.encode('utf-8'), DES.block_size)
        encrypted_bytes = cipher.encrypt(padded_text)
        return {"result": base64.b64encode(encrypted_bytes).decode('utf-8')}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/decrypt")
def decrypt_text(request: DESRequest):
    try:
        key_bytes = validate_key(request.key)
        cipher = DES.new(key_bytes, DES.MODE_ECB)
        encrypted_bytes = base64.b64decode(request.text)
        decrypted_bytes = unpad(cipher.decrypt(encrypted_bytes), DES.block_size)
        return {"result": decrypted_bytes.decode('utf-8')}
    except Exception:
        raise HTTPException(status_code=400, detail="Decryption failed. Invalid key or corrupted data.")
