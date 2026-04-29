"""
Application Layer - Smart Factory Sensor Application
Generates sensor data (temperature, vibration) for IIoT monitoring
"""
import random
import time
import json

class SmartFactoryApp:
    def __init__(self, sensor_id):
        self.sensor_id = sensor_id
        self.qos = {
            "max_latency_ms": 100,
            "min_reliability": 0.99,
            "max_ber": 1e-5,
            "max_jitter_ms": 20
        }

    def generate_data(self):
        """Generate sensor reading"""
        data = {
            "sensor_id": self.sensor_id,
            "timestamp": time.time(),
            "temperature": round(random.uniform(20.0, 85.0), 2),
            "vibration": round(random.uniform(0.0, 5.0), 3),
            "status": "OK"
        }
        return json.dumps(data).encode('utf-8')

    def get_qos(self):
        return self.qos