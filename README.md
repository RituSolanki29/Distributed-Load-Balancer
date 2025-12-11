# 📦 Distributed Load Balancer & Server Simulation

A multi-server load balancing system with real-time monitoring, algorithm comparison, and automated testing.

---

## 📌 Introduction

This project is a **distributed load-balancing simulation system** built using **Flask**, **Socket.IO**, and Python automation scripts.

It allows you to:

- Spin up multiple backend servers (general, video, API, image, etc.)
- Route requests through a customizable load balancer
- Switch between different load-balancing algorithms in real time
- Monitor server performance via a Dashboard UI
- Run automated tests for distributed load balancing
- Compare algorithms using automated request simulations

This project is ideal for learning, experimenting, or demonstrating **networking, distributed systems, and load-balancing concepts**.

---

## 🚀 Key Functionalities

### 🔹 1. Load Balancer

- Receives all client requests  
- Supports multiple algorithms:
  - **Round Robin**
  - **Least Connections**
  - **Weighted Distribution**
  - **Dynamic Load-based**
- Tracks statistics:
  - Requests per server
  - Response times
  - Processing delays
- Emits real-time updates to dashboard using **Socket.IO**

---

### 🔹 2. Backend Servers

Each backend server runs independently with configurable parameters:

- Accepts requests forwarded by the load balancer  
- Tracks internal statistics:
  - Total requests
  - API / Video / Image request counters
- Simulates processing delay  
- Provides health checks  

Servers can be started individually using batch files:
start_l1.bat
start_l2.bat
start_l3.bat


---

### 🔹 3. Dashboard

Located in `templates/dashboard.html`, it offers:

- Real-time load balancer insights  
- Algorithm switching UI  
- Server health visualization  
- Traffic distribution graph  
- Request count & performance metrics  

---

### 🔹 4. Algorithm Comparison Tool

`compare_algorithms.py` allows:

- Switching algorithms automatically  
- Sending test traffic  
- Collecting performance metrics  
- Logging response times and distribution  
- Generating comparison JSON output  

---

### 🔹 5. Automated Testing

#### ✔ `test_client.py`
Simulates real-world clients sending requests concurrently.

#### ✔ `test_distributed.py`
Stresses multiple servers, measures system performance, and ensures algorithm correctness.

---

### 🔹 6. Logging System

Logs saved automatically inside:


Includes:

- Incoming request logs  
- Algorithm changes  
- Server selection decisions  
- Errors & warnings  

---

### 🔹 7. Utility Scripts

- `setup_firewall.bat` – Windows firewall rule automation  
- `start_all.bat` – Launch LB + all servers  
- `config.json` – Centralized project configuration  

---

## 🧰 Libraries & Tools Used

### **Backend (Python)**

| Library          | Purpose                                      |
|------------------|----------------------------------------------|
| Flask            | Load balancer + backend server API           |
| Flask-SocketIO   | Real-time dashboard updates                   |
| Requests         | Server-to-server communication                |
| Threading / Time | Concurrency & simulation delays               |
| Logging          | Activity and debugging logs                   |
| JSON             | Configuration & output formatting             |

---

## 🖥 Frontend

| Tool                  | Purpose              |
|----------------------|----------------------|
| HTML Templates (Jinja) | Dashboard UI       |
| JavaScript + Socket.IO | Live updates       |

---

## ⚙️ How It Works (Architecture Overview)

### **Step 1 — Users send a request**
All requests go to the **Load Balancer** (port `8080`).

### **Step 2 — Load Balancer selects a server**
Based on the active algorithm:

- Round Robin → Next server in list  
- Least Connections → Server with minimum load  
- Weighted → Higher weight → more traffic  
- Dynamic → Based on server health/response time  

### **Step 3 — Request forwarded**
Load Balancer forwards the request to backend servers:

5001, 5002, 5003, ...


### **Step 4 — Server processes**
Each server:

- Updates counters  
- Simulates workload using `time.sleep()`  
- Returns the response to the load balancer  

### **Step 5 — Load Balancer returns final response**
It also sends real-time updates to the dashboard via **Socket.IO**.

---




