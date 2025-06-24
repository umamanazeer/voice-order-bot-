#  Voice Order Bot API (FastAPI + VAPI Webhook)

This is a simple FastAPI-based voice order bot that integrates with VAPI (Voice API) platforms. It receives voice-based commands, processes them, and responds accordingly (e.g., placing orders, checking order status).

---

##  Features

- Accepts voice call events via a webhook.
- Supports basic commands like ordering pizza, checking order status, greetings, etc.
- Maintains a simple in-memory orders list.
- Uses FastAPI for creating endpoints.
- Configurable for deployment via Docker or any server.

---

##  Requirements

- Python 3.8+
- `fastapi`
- `uvicorn`

You can install dependencies via:

```bash
pip install fastapi uvicorn
```

---

##  Project Structure

```
.
├── main.py          # Main FastAPI app with VAPI webhook logic
├── README.md        # Project overview and instructions
```

---

## How to Run

###  Run Locally

```bash
python main.py
```
uvicorn main:app --reload --host 0.0.0.0 --port 8000
Server will start at: `http://localhost:8000/`

---

##  Webhook Endpoint(Using Postman)

 Method  Endpoint            Description                        
----------------------------------------------------------------
 `GET`   `http://localhost:8000/`                 Root health-check route            
 `POST`  `http://localhost:8000/webhook/vapi`     Main webhook for receiving VAPI events 

---

##  Supported VAPI Events

 Event Type          Action Performed                                                  
---------------------------------------------------------------------------------------
`call_started`    : Welcomes the caller                                               
`speech_recognized` : Processes spoken commands (like "order pizza", "order status") 
`call_ended`      : Ends session gracefully                                           


##  Example Commands You Can Speak

- "I want to order a pizza"
- "Check my order status"
- "Hello"
- "Thank you"

