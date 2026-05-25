# STLA SmartCockpit Simulation
This project demonstrates a Software-Defined Vehicle (SDV) architecture inspired by the Stellantis STLA Brain and SmartCockpit platforms.

## 🏗️ System Architecture
This diagram shows how data flows from the virtual vehicle to the driver's dashboard via an MQTT broker and an AI-driven backend.

```mermaid
graph TD
    subgraph "Vehicle Layer (Ubuntu VM)"
        A[Python Car Simulator] -- "Generates VSS Data" --> B(Eclipse Kuksa Databroker)
        B -- "Publish via MQTT" --> C{Mosquitto Broker}
    end

    subgraph "Edge/Backend Layer (Ubuntu or Windows)"
        C -- "Subscribe" --> D[FastAPI Backend]
        D -- "Send Telemetry" --> E[AI Engine: Ollama/OpenAI]
        E -- "Return Smart Insights" --> D
    end

    subgraph "User Layer (Windows Host)"
        D -- "WebSockets/REST" --> F[React Dashboard]
        F -- "Visualizes Data" --> G((User))
    end

    subgraph "Future Phase: Cloud"
        D -. "Log Data" .-> H[AWS S3/DynamoDB]
    end
