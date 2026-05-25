from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import paho.mqtt.client as mqtt
import json
import threading

app = FastAPI(title="STLA SmartCockpit Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows the dashboard to connect
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DATABASE (In-Memory for now) ---
# This acts as a "Shadow" of the car's current state
vehicle_state = {
    "speed": 0,
    "battery": 0,
    "tire_pressure": 0,
    "last_update": None
}

# --- MQTT LOGIC (The Listener) ---
MQTT_BROKER = "localhost"
MQTT_TOPIC = "vss/vehicle/telemetry"

def on_message(client, userdata, msg):
    global vehicle_state
    try:
        data = json.loads(msg.payload)
        # Update our "Digital Twin" state
        vehicle_state["speed"] = data["signals"]["Speed"]
        vehicle_state["battery"] = data["signals"]["BatteryLevel"]
        vehicle_state["tire_pressure"] = data["signals"]["TirePressure"]
        vehicle_state["last_update"] = data["timestamp"]
        print(f"📈 Backend Updated: {vehicle_state['speed']} km/h")
    except Exception as e:
        print(f"⚠️ Error parsing data: {e}")

# Start MQTT in a separate thread so it doesn't block the API
def start_mqtt():
    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    client.on_message = on_message
    client.connect(MQTT_BROKER, 1883)
    client.subscribe(MQTT_TOPIC)
    client.loop_forever()

mqtt_thread = threading.Thread(target=start_mqtt, daemon=True)
mqtt_thread.start()

# --- API ENDPOINTS (The Interface) ---

@app.get("/")
def read_root():
    return {"message": "STLA Backend is Online", "status": "Ready"}

@app.get("/vehicle/status")
def get_vehicle_status():
    """This is what the React Dashboard will call every second."""
    return vehicle_state

@app.get("/vehicle/alerts")
def get_alerts():
    """Simple Logic Service: Check for danger zones."""
    alerts = []
    if vehicle_state["battery"] < 20:
        alerts.append("LOW BATTERY: Please find a charging station.")
    if vehicle_state["tire_pressure"] < 30:
        alerts.append("SAFETY ALERT: Check tire pressure immediately.")
    return {"alerts": alerts}