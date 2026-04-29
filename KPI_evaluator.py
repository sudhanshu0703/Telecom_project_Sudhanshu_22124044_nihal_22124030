"""
Step 8: KPI Evaluation
"""
import numpy as np

class KPIEvaluator:
    def __init__(self):
        self.metrics = {
            "packets_sent": 0,
            "packets_received": 0,
            "total_latency": 0,
            "latencies": [],
            "ber_values": [],
            "retransmissions": 0,
            "bits_transmitted": 0
        }

    def record_packet(self, success, latency_ms, ber, retx=0, bits=0):
        self.metrics["packets_sent"] += 1
        if success:
            self.metrics["packets_received"] += 1
            self.metrics["latencies"].append(latency_ms)
        self.metrics["ber_values"].append(ber)
        self.metrics["retransmissions"] += retx
        self.metrics["bits_transmitted"] += bits

    def evaluate(self, qos_targets, total_time_sec):
        sent = self.metrics["packets_sent"]
        recv = self.metrics["packets_received"]
        latencies = self.metrics["latencies"]

        reliability = recv / sent if sent > 0 else 0
        avg_latency = np.mean(latencies) if latencies else 0
        jitter = np.std(latencies) if len(latencies) > 1 else 0
        avg_ber = np.mean(self.metrics["ber_values"]) if self.metrics["ber_values"] else 0
        throughput_bps = self.metrics["bits_transmitted"] / total_time_sec if total_time_sec > 0 else 0

        report = {
            "Packets Sent": sent,
            "Packets Received": recv,
            "Reliability (PDR)": f"{reliability*100:.2f}%",
            "Avg Latency (ms)": f"{avg_latency:.2f}",
            "Jitter (ms)": f"{jitter:.2f}",
            "Avg BER": f"{avg_ber:.2e}",
            "Throughput (bps)": f"{throughput_bps:.2f}",
            "Retransmissions": self.metrics["retransmissions"],
            "QoS Met - Latency": avg_latency < qos_targets["max_latency_ms"],
            "QoS Met - Reliability": reliability > qos_targets["min_reliability"],
            "QoS Met - BER": avg_ber < qos_targets["max_ber"],
            "QoS Met - Jitter": jitter < qos_targets["max_jitter_ms"]
        }
        return report