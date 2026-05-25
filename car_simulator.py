import paho.mqtt.client as mqtt
import json
import time
import random

# --- CONFIGURATION ---
BROKER = "localhost"  # Since Mosquitto is running on your VM
PORT = 1883
TOPIC = "vss/vehicle/telemetry"

client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)

def connect_to_broker():
    try:
        client.connect(BROKER, PORT, 60)
        print(f"✅ Connected to MQTT Broker at {BROKER}")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        exit(1)

def simulate_vehicle():
    # Initial state
    speed = 0
    battery = 80
    tire_pressure = 32.0

    print("🚀 Starting STLA Vehicle Simulation...")
    
    while True:
        # Simulate dynamic changes
        speed = random.randint(0, 120)
        battery -= 0.1 if speed > 0 else 0.01
        
        # Occasionally simulate an issue (Low tire pressure)
        if random.random() > 0.95:
            tire_pressure = round(random.uniform(25.0, 28.0), 1)
        else:
            tire_pressure = 32.0

        # Create a VSS-style JSON payload
        payload = {
            "vehicle_id": "STLA-JEEP-001",
            "timestamp": time.time(),
            "signals": {
                "Speed": speed,
                "BatteryLevel": round(battery, 2),
                "TirePressure": tire_pressure,
                "Status": "Driving" if speed > 0 else "Parked"
            }
        }

        # Publish the data
        client.publish(TOPIC, json.dumps(payload))
        print(f"📡 Sent Telemetry: Speed={speed}km/h, Battery={round(battery,1)}%")
        
        time.sleep(2) # Send data every 2 seconds

if __name__ == "__main__":
    connect_to_broker()
    simulate_vehicle()