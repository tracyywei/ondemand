from flask import Flask, render_template, request, jsonify
import os
from fastapi import FastAPI, Request
import time
import hmac
from hashlib import sha256

app = Flask(__name__)
fast_app = FastAPI()

@app.route("/")
def start():
    return render_template('index.html')

@fast_app.post("/webhook")
async def receive_message(request: Request):
    payload = await request.body()
    headers = request.headers.get("elevenlabs-signature")
    if headers is None:
        return
    timestamp = headers.split(",")[0][2:]
    hmac_signature = headers.split(",")[1]

    tolerance = int(time.time()) - 30 * 60
    if int(timestamp) < tolerance:
        return

    full_payload_to_sign = f"{timestamp}.{payload.decode('utf-8')}"
    mac = hmac.new(
        key=secret.encode("utf-8"),
        msg=full_payload_to_sign.encode("utf-8"),
        digestmod=sha256,
    )
    digest = 'v0=' + mac.hexdigest()
    if hmac_signature != digest:
        return

    return {"status": "received"}
       
if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)