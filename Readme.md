# Telecommunication Networks Project — Smart Factory IIoT

End-to-end simulation of a 5-layer telecommunication network for an
Industrial IoT (IIoT) Smart Factory sensor monitoring application.

---

## 👨‍🎓 Project Information

| Field | Details |
|---|---|
| **Course** | EC-314 Telecommunication Networks |
| **Branch** | Mathematics and Computing |
| **Project Type** | End-Semester Project |

### 👥 Team Members

| Name | Roll Number |
|---|---|
| **Sudhanshu Gurupanch** | 2212124044 |
| **Nihal Gupta** | 22124030 |

---

## 📡 Project Overview

This project implements a complete end-to-end telecommunication network simulation
for a **Smart Factory Industrial IoT (IIoT)** application, where sensors monitor
temperature and vibration data and transmit it to a control server through a
multi-layer network stack.

---

## 🏗️ Architecture (5 Layers)

1. **Application Layer** — Smart Factory sensor data (temperature, vibration)
2. **Transport Layer** — Segmentation with sequence numbers
3. **Network Layer** — IP addressing + Dijkstra's shortest-path routing
4. **Data Link Layer** — Framing with CRC-32 + Stop-and-Wait ARQ
5. **Physical Layer** — BPSK modulation over AWGN channel

---

## 🎯 QoS / KPI Targets

| Metric | Target |
|---|---|
| Latency | < 100 ms |
| Reliability (PDR) | > 99% |
| Bit Error Rate (BER) | < 10⁻⁵ |
| Jitter | < 20 ms |

---

## 📋 Project Steps Implemented

- [x] **Step 1:** Choose Application + Define QoS/KPI
- [x] **Step 2:** Send data in packets (Transport)
- [x] **Step 3:** Define address of nodes (Network)
- [x] **Step 4:** Selection of path (Dijkstra routing protocol)
- [x] **Step 5:** Convert packet into frame + ARQ
- [x] **Step 6:** Design Physical Layer (BPSK)
- [x] **Step 7:** AWGN Channel implementation
- [x] **Step 8:** Evaluate KPIs

---

## 📊 Queueing Theory Analysis

The project includes M/M/1 queueing system analysis:
- **A(t)** = Pr[time between senders ≤ t] — Arrival distribution
- **B(t)** = Pr[service time ≤ t] — Service distribution
- **Sₙ = Wₙ + Xₙ** — Total time = Waiting time + Service time

---

## 🛠️ Installation

```bash
pip install -r requirements.txt