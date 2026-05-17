from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from Crypto.Cipher import DES
from Crypto.Util.Padding import unpad
import base64

app = FastAPI()

class DESRequest(BaseModel):
    text: str
    key: str

@app.post("/api/decrypt")
def decrypt_text(request: DESRequest):
    if len(request.key) != 8:
        raise HTTPException(status_code=400, detail="Key must be exactly 8 characters long.")
    try:
        cipher = DES.new(request.key.encode('utf-8'), DES.MODE_ECB)
        encrypted_bytes = base64.b64decode(request.text)
        decrypted_bytes = unpad(cipher.decrypt(encrypted_bytes), DES.block_size)
        return {"result": decrypted_bytes.decode('utf-8')}
    except Exception:
        raise HTTPException(status_code=400, detail="Decryption failed. Invalid key or corrupted data.")
