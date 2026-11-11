# Data-Link-Handover
a repository for handover the data link work that was done in my On-Job-Training with Gamuda Technologies.

# ExpressLRS to ArduPilot SITL Real-Time MAVLink Bridge

An ultra-low-latency hardware-in-the-loop (HIL) telemetry bridge developed during On-Job-Training with Gamuda Technologies. This repository provides the pipeline that captures native MAVLink RC override packets from an ExpressLRS (ELRS) receiver and injects them directly into ArduPilot Software-In-The-Loop (SITL) simulations via Mission Planner.

---

## 📌 Project Overview and Architecture

+---------------------+         2.4GHz ELRS         +------------------------+
|  RadioMaster T8L    |  >    |  ExpressLRS Receiver   |
|     Transmitter     |                             |  (Serial Output)       |
+---------------------+                             +------------------------+
|
| UART / FTDI (COM6)
| 460,800 baud
v
+---------------------+         TCP Socket          +------------------------+
| Mission Planner     |  <    | Python Injection Proxy |
| SITL Simulation     |       Port: 14556           | (sitl_injector.py)   |
| (Target: 1, Comp: 0)|                             | (GCS System ID: 255)   |
+---------------------+                             +------------------------+

---

## 🛠️ Hardware & Software Stack

- **Transmitter:** Radiomaster T8L
- **Protocol:** ExpressLRS (2.4GHz) configured for MAVLink telemetry output
- **Interface:** FTDI USB-to-UART Serial Converter (`COM6`[or designated com port] `460800` baud)
- **Runtime / Libraries:** Python 3.10+, `pymavlink`
- **Ground Control & Simulation:** Mission Planner, ArduPilot SITL (Multirotor model)

---

## ⚡ Quick Start Guide

### 1. Prerequisites & Installation

Clone the repository and install dependencies:

```bash
git clone [https://github.com/masbi98/Data-Link-Handover.git]
cd Data-Link-Handover
pip install -r requirements.txt