# main.py

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, PlainTextResponse
import uvicorn
import os # Environment variables ko access karne ke liye

# --- FastAPI Application Initialization ---
app = FastAPI()

# --- Dummy Database/Data ---
# Ek simple Python list orders store karne ke liye.
# Production mein aap yahan ek proper database (e.g., PostgreSQL, SQLite) use karengi.
orders_db = []

# --- Root Endpoint ---
# Yeh ek simple endpoint hai, sirf yeh check karne ke liye ki aapka server chal raha hai ya nahi.
# Jab aap bot ke public URL ko browser mein kholegi, toh yeh message dikhega.
@app.get("/")
async def root():
    return {"message": "Voice Order Bot API is running! Ready to take orders."}

# --- VAPI Webhook Endpoint ---
# Yeh sabse important endpoint hai. VAPI service saare events yahan bhejegi.
# Aapko apne VAPI provider ke dashboard mein is URL ko set karna hoga (e.g., your_domain.com/webhook/vapi).
@app.post("/webhook/vapi")
async def vapi_webhook(request: Request):
    """
    This endpoint acts as the webhook receiver for VAPI.
    It listens for events sent by the VAPI service (e.g., incoming call, speech recognized).
    """
    try:
        # VAPI providers aam taur par data JSON format mein bhejte hain.
        # Agar aapka VAPI provider XML ya form-data bhejta hai, toh is line ko adjust karna hoga.
        payload = await request.json()
        print(f"Received VAPI webhook data: {payload}") # Debugging ke liye payload print karein

        # VAPI event type ko payload se nikalen.
        # Har VAPI provider ke event types thode alag ho sakte hain (e.g., 'call.started', 'speech.recognized').
        # Apne VAPI provider ki documentation zarur check karein.
        event_type = payload.get("event")

        # --- Event Handling Logic ---
        if event_type == "call_started":
            # Jab koi naya phone call aata hai.
            print("Call started event received. Welcoming user.")
            response_text = "Welcome to our voice order bot. Please tell me what you would like to order."
            # VAPI ko bataen ki yeh text bolna hai. 'response_action: say' VAPI specific hai.
            return JSONResponse({"response_action": "say", "text": response_text})

        elif event_type == "speech_recognized":
            # Jab VAPI user ki awaaz ko text mein convert kar leti hai.
            transcript = payload.get("transcript") # User ne jo bola, uska text form
            confidence = payload.get("confidence") # Pehchanne ki accuracy (0.0 to 1.0)
            print(f"Speech Recognized: '{transcript}' (Confidence: {confidence})")

            # User ke command (transcript) ko process karein.
            bot_response = process_voice_command(transcript)

            # Bot ka jawaab VAPI ko wapas bhej dein taaki woh bol sake.
            return JSONResponse({"response_action": "say", "text": bot_response})

        elif event_type == "call_ended":
            # Jab phone call khatam hota hai.
            print("Call ended event received. Performing cleanup if any.")
            # Yahan aap call se related koi cleanup ya logging kar sakti hain.
            return JSONResponse({"status": "success"}) # VAPI ko OK response bhej dein

        else:
            # Agar koi aisa event type aaye jo hum handle nahi kar rahe.
            print(f"Unhandled VAPI event type: {event_type}")
            return JSONResponse({"status": "ignored", "message": "Unknown event type"}, status_code=200)

    except Exception as e:
        # Koi bhi error hone par, usko log karein aur 500 Internal Server Error response dein.
        print(f"Error processing VAPI webhook: {e}")
        return PlainTextResponse(f"Error processing webhook: {e}", status_code=500)

# --- Core Business Logic Function ---
# Yeh function user ke transcribed speech ko process karta hai.
# Yahan aapki bot ki "intelligence" aayegi.
def process_voice_command(transcript: str) -> str:
    """
    Processes the user's transcribed speech to determine intent and generate a response.
    This is where your Natural Language Processing (NLP) or simple keyword matching logic goes.
    For a real-world bot, you'd use a more sophisticated NLP library or a service like Dialogflow/Lex.
    """
    transcript_lower = transcript.lower() # Case-insensitivity ke liye lowercase karein

    if "order" in transcript_lower and ("pizza" in transcript_lower or "pizzas" in transcript_lower):
        # Ek simple order ka example.
        # Advance bots quantity (e.g., "do pizza") aur toppings bhi nikalte hain.
        item = "pizza"
        quantity = 1
        orders_db.append({"item": item, "quantity": quantity, "status": "pending"})
        return f"Okay, I've placed an order for {quantity} {item}. Is there anything else?"

    elif "status" in transcript_lower and "order" in transcript_lower:
        # Order status check karna.
        if orders_db:
            latest_order = orders_db[-1] # Bas last order ka status bata rahe hain
            return f"Your latest order is for {latest_order['quantity']} {latest_order['item']} and its status is {latest_order['status']}."
        else:
            return "You don't have any pending orders with us."

    elif "hello" in transcript_lower or "hi" in transcript_lower:
        # Simple greeting
        return "Hello! How can I help you today?"

    elif "thank you" in transcript_lower or "bye" in transcript_lower:
        # Ending conversation
        return "You're welcome! Goodbye, have a great day!"

    else:
        # Jab bot user ki baat na samajh paye.
        return "I'm sorry, I didn't understand that. Can you please repeat or try something like 'order pizza'?"

# --- Running the FastAPI Application ---
# Yeh block server ko directly chalanay ke liye hai, khas kar development ke dauran.
# Production environment mein aapke sir Gunicorn (ya koi aur WSGI server) ka istemal karenge
# jo Uvicorn workers ko manage karega, jaisa ki Dockerfile aur Systemd setup mein bataya tha.
if __name__ == "__main__":
    # Port ko environment variable se lenge, agar company specify karti hai.
    # Agar environment variable 'PORT' set nahi hai, toh default 8000 use karein.
    port = int(os.environ.get("PORT", 8000))
    # host="0.0.0.0" ensure karta hai ki application container ke andar saari network interfaces par listen kare.
    # reload=False production ke liye achha hai (performance aur stability ke liye).
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)