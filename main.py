from fastapi import FastAPI, Request
import json, re

app = FastAPI()

@app.post("/order")
async def receive_order(request: Request):
    data = await request.json()
    transcript = data.get("transcript", "")
    phone = data.get("phone_number", "Unknown")

    # Parse order from text (basic example)
    order_match = re.findall(r"(\d+)\s(\w+)", transcript)
    address_match = re.search(r"address is (.+)", transcript)

    order_items = [{"item": i[1], "quantity": int(i[0])} for i in order_match]
    address = address_match.group(1) if address_match else "Not provided"

    order_data = {
        "phone": phone,
        "items": order_items,
        "address": address,
        "original_message": transcript
    }

    # Save to file
    with open("orders.json", "a") as f:
        f.write(json.dumps(order_data) + "\n")

    return {"message": "Order received"}
