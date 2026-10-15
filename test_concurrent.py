
import requests
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
import uuid

URL = "http://127.0.0.1:5000/payment"

# Tạo khóa mới cho lượt kiểm thử này
IDEMPOTENCY_KEY = f"race-test-{uuid.uuid4()}"
AMOUNT = "100"

start_together = Barrier(2)

payload = {
    "idempotency_key": IDEMPOTENCY_KEY,
    "amount": AMOUNT,
    "pan": "TEST-CARD",
    "expiry": "12/30",
    "cvv": "123",
}

def send_request():
    start_together.wait()
    response = requests.post(URL, data=payload, timeout=10)
    return response.status_code, response.text[:200]

with ThreadPoolExecutor(max_workers=2) as executor:
    futures = [
        executor.submit(send_request),
        executor.submit(send_request),
    ]
    results = [future.result() for future in futures]

print("Test key:", IDEMPOTENCY_KEY)

for index, result in enumerate(results, start=1):
    print(f"Request {index}: HTTP {result[0]}")
    print(result[1])
    print("-" * 40)
