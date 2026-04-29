"""
Main simulation: End-to-end Smart Factory IIoT communication
Implements all 8 steps from project requirements
"""
import time
import random
import numpy as np
import matplotlib.pyplot as plt

from layers.application import SmartFactoryApp
from layers.transport import TransportLayer
from layers.network import NetworkLayer
from layers.datalink import DataLinkLayer
from layers.physical import PhysicalLayer
from utils.queueing import MM1Queue
from utils.kpi_evaluator import KPIEvaluator


def simulate_network(num_packets=200, snr_db=12):
    print("=" * 70)
    print("  SMART FACTORY IIoT - TELECOMMUNICATION NETWORK SIMULATION")
    print("=" * 70)

    # Initialize layers
    app = SmartFactoryApp(sensor_id="TEMP_VIB_01")
    transport = TransportLayer()
    network = NetworkLayer()
    datalink = DataLinkLayer(max_retries=3)
    phy = PhysicalLayer(snr_db=snr_db)
    kpi = KPIEvaluator()

    # Step 1: Application & QoS
    qos = app.get_qos()
    print(f"\n[STEP 1] Application: Smart Factory Sensor Monitoring")
    print(f"         QoS Targets: {qos}")

    # Step 4: Routing
    path, total_cost = network.dijkstra("sensor1", "server")
    print(f"\n[STEP 4] Routing path: {' -> '.join(path)}")
    print(f"         Path cost (propagation latency): {total_cost} ms")

    print(f"\n[STEP 7] Channel: AWGN, SNR = {snr_db} dB")
    print(f"\nSimulating {num_packets} packets...\n")

    sim_start = time.time()

    for i in range(num_packets):
        t_start = time.time()

        # Step 2: App generates data, Transport segments
        data = app.generate_data()
        segments = transport.segment(data)

        packet_success = True
        total_retx = 0
        total_bits = 0
        ber_accum = []

        for seg in segments:
            # Step 3: Network adds IP header
            packet = network.add_ip_header(seg, "sensor1", "server")

            # Step 5: Data link framing
            frame = datalink.framing(packet)
            total_bits += len(frame) * 8

            # Steps 6 & 7: Physical layer over AWGN
            def channel_send(f):
                received, ber = phy.transmit(f)
                ber_accum.append(ber)
                # Verify CRC at receiver
                _, valid = datalink.deframe(received)
                return valid

            success, retx = datalink.stop_and_wait_arq(frame, channel_send)
            total_retx += retx
            if not success:
                packet_success = False
                break

        # Latency = propagation + transmission + retransmission delay
        propagation_delay = total_cost  # ms
        transmission_delay = (time.time() - t_start) * 1000
        retx_penalty = total_retx * 5  # 5 ms per retx
        latency = propagation_delay + transmission_delay + retx_penalty

        avg_ber = np.mean(ber_accum) if ber_accum else 0
        kpi.record_packet(packet_success, latency, avg_ber, total_retx, total_bits)

        if (i + 1) % 50 == 0:
            print(f"  Processed {i+1}/{num_packets} packets...")

    sim_duration = time.time() - sim_start

    # Step 8: KPI Evaluation
    print("\n" + "=" * 70)
    print("  [STEP 8] KPI EVALUATION REPORT")
    print("=" * 70)
    report = kpi.evaluate(qos, sim_duration)
    for k, v in report.items():
        marker = ""
        if "QoS Met" in k:
            marker = " ✅" if v else " ❌"
        print(f"  {k:<28}: {v}{marker}")

    # Queueing analysis
    print("\n" + "=" * 70)
    print("  QUEUEING ANALYSIS (M/M/1)")
    print("=" * 70)
    arrival_rate = num_packets / sim_duration
    service_rate = arrival_rate * 1.5  # μ > λ for stability
    queue = MM1Queue(arrival_rate, service_rate)
    print(f"  Arrival rate (λ)     : {arrival_rate:.2f} pkt/s")
    print(f"  Service rate (μ)     : {service_rate:.2f} pkt/s")
    print(f"  Utilization (ρ)      : {queue.rho:.3f}")
    print(f"  Avg Waiting Time Wn  : {queue.avg_waiting_time()*1000:.2f} ms")
    print(f"  Avg Service Time Xn  : {queue.avg_service_time()*1000:.2f} ms")
    print(f"  Avg Total Time Sn    : {queue.avg_total_time()*1000:.2f} ms")
    print(f"  Avg Population (L)   : {queue.avg_population():.2f} packets")

    return kpi, report


def ber_vs_snr_analysis():
    """Plot BER vs SNR (classic PHY layer evaluation)"""
    snr_range = np.arange(0, 15, 1)
    ber_results = []

    test_data = b"SmartFactoryTestPayload" * 10
    for snr in snr_range:
        phy = PhysicalLayer(snr_db=snr)
        bers = []
        for _ in range(50):
            _, ber = phy.transmit(test_data)
            bers.append(ber)
        ber_results.append(np.mean(bers))

    plt.figure(figsize=(10, 6))
    plt.semilogy(snr_range, ber_results, 'o-', linewidth=2, markersize=8)
    plt.xlabel("SNR (dB)", fontsize=12)
    plt.ylabel("Bit Error Rate (BER)", fontsize=12)
    plt.title("BER vs SNR — BPSK over AWGN Channel", fontsize=13)
    plt.grid(True, which='both', alpha=0.5)
    plt.tight_layout()
    plt.savefig("results/ber_vs_snr.png", dpi=120)
    print("\n📊 Saved plot: results/ber_vs_snr.png")


def latency_analysis(kpi):
    """Plot latency distribution"""
    latencies = kpi.metrics["latencies"]
    if not latencies:
        return
    plt.figure(figsize=(10, 6))
    plt.hist(latencies, bins=30, color='steelblue', edgecolor='black', alpha=0.8)
    plt.axvline(np.mean(latencies), color='red', linestyle='--',
                linewidth=2, label=f'Mean = {np.mean(latencies):.2f} ms')
    plt.xlabel("Latency (ms)", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.title("End-to-End Latency Distribution", fontsize=13)
    plt.legend()
    plt.grid(True, alpha=0.4)
    plt.tight_layout()
    plt.savefig("results/latency_distribution.png", dpi=120)
    print("📊 Saved plot: results/latency_distribution.png")


if __name__ == "__main__":
    import os
    os.makedirs("results", exist_ok=True)

    random.seed(42)
    np.random.seed(42)

    kpi, report = simulate_network(num_packets=200, snr_db=12)
    latency_analysis(kpi)
    ber_vs_snr_analysis()

    print("\n✅ Simulation complete! Check the 'results/' folder for plots.\n")