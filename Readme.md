# Telecommunication Networks Project — Smart Factory IIoT

End-to-end simulation of a 5-layer telecommunication network for an
Industrial IoT Smart Factory sensor monitoring application.

## Architecture (5 Layers)
1. **Application** — Smart Factory sensor data (temperature, vibration)
2. **Transport** — Segmentation with sequence numbers
3. **Network**   — IP addressing + Dijkstra's shortest-path routing
4. **Data Link** — Framing with CRC-32 + Stop-and-Wait ARQ
5. **Physical**  — BPSK modulation over AWGN channel

## QoS / KPI Targets
|
 Metric      
|
 Target     
|
|
-------------
|
------------
|
|
 Latency     
|
 < 100 ms   
|
|
 Reliability 
|
 > 99%      
|
|
 BER         
|
 < 10⁻⁵     
|
|
 Jitter      
|
 < 20 ms    
|

## Installation
```bash
pip install -r requirements.txt