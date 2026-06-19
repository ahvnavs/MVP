import time
import json
import random
import paho.mqtt.client as mqtt

# Configuration
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "pg_smartgrid/telemetry/meter_001"

# Initialize variables
cumulative_energy_kwh = 1250.50

def generate_telemetry(inject_anomaly=False):
    global cumulative_energy_kwh

    # Simulate realistic Indian grid parameters (Single Phase)
    voltage = round(random.uniform(220.0, 240.0), 2)
    # Simulate a normal PG room load (e.g., lights, fan, occasional AC/Geyser)
    current = round(random.uniform(0.5, 8.0), 2)
    power_w = round(voltage * current, 2)

    # Anomaly Injection: Simulating the "Trust Deficit"
    if inject_anomaly:
        # Simulate the 40% underreporting corruption
        power_w = round(power_w * 0.60, 2)
        current = round(current * 0.60, 2)

        # Simulate fraudulent administrative billing (round multiples of 10)
        if random.random() > 0.5:
            power_w = float(int(power_w / 10) * 10)

    # Accumulate energy (simulating kWh usage over 5-second intervals)
    energy_added = (power_w * 5) / 3600000
    cumulative_energy_kwh += energy_added

    payload = {
        "meter_id": "meter_001",
        "voltage_v": voltage,
        "current_a": current,
        "power_w": power_w,
        "total_energy_kwh": round(cumulative_energy_kwh, 4),
        "timestamp": int(time.time()),
        "anomaly_flag": inject_anomaly
    }
    return payload

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}")

# Setup MQTT Client
client = mqtt.Client("Virtual_Meter_001")
client.on_connect = on_connect
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

print(f"Starting Virtual Smart Meter... Publishing to {MQTT_TOPIC}")

try:
    while True:
        # Inject an anomaly 15% of the time to test your future monitoring stack
        is_corrupted = random.random() < 0.15

        telemetry = generate_telemetry(inject_anomaly=is_corrupted)
        json_payload = json.dumps(telemetry)

        # Publish to the broker
        client.publish(MQTT_TOPIC, json_payload)

        if is_corrupted:
            print(f" Payload: {json_payload}")
        else:
            print(f" Payload: {json_payload}")

        time.sleep(5) # Send data every 5 seconds

except KeyboardInterrupt:
    print("\nShutting down Virtual Smart Meter...")
    client.loop_stop()
    client.disconnect()
