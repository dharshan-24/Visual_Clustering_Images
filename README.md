

 # 🧠 Visual Clustering Dashboard

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green.svg)
![React](https://img.shields.io/badge/React-Frontend-61DAFB.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-DINOv2-red.svg)
![Docker](https://img.shields.io/badge/Docker-Containerization-2496ED.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

> AI-powered image clustering and visualization dashboard using **DINOv2 embeddings** and **unsupervised learning**.

---

## 🚀 Overview
**Visual Clustering Dashboard** is an AI-driven web application that automatically groups visually similar images using state-of-the-art **self-supervised vision embeddings (DINOv2)**.  
Users can upload large image collections and explore clusters through an interactive dashboard.

This project demonstrates **Computer Vision + Machine Learning + Full-Stack Engineering** skills in a production-style architecture.

---


## ✨ Key Features
- 📤 Upload image datasets (bulk upload)
- 🧬 Automatic feature extraction using DINOv2
- 📊 K-Means / Hierarchical clustering
- 🖼️ Interactive cluster visualization dashboard
- 🔍 Filter, search & tag clusters
- 🧾 Export cluster reports (CSV)
- ⚡ Scalable backend with REST APIs
- 🐳 Docker-ready deployment

---



**\# Backend setup**

venv\\Scripts\\activate

cd backend

uvicorn main:app --reload

pip install -r requirements.txt

---

**\# Frontend setup**

venv\\Scripts\\activate

cd frontend

npm install

npm start

---


\# Run (2 terminals)

**\# Terminal 1:**

cd backend

uvicorn main:app --reload

---

**\# Terminal 2:**

cd frontend

npm start

---


✅ Group 1 (Green)  → 5 Computer    | 92.1% similarity ⭐⭐⭐

✅ Group 2 (Blue)   → 5 Birds       | 88.5% similarity ⭐⭐⭐

✅ Group 3 (Purple) → 3 Animals     | 85.2% similarity ⭐⭐⭐

✅ Group 4 (Red)    → 5 Humans      | 76.3% similarity ⭐⭐

---

**\# 🏗️ Tech Stack**



\*\*Backend:\*\* Python • FastAPI • PyTorch • Transformers • scikit-learn

\*\*Frontend:\*\* React • CSS3

\*\*AI/ML:\*\* DINOv2 • DBSCAN • Cosine Similarity


---

**\# 🎯 Use Cases**



\- 📷 Photography organization

\- 🛍️ E-commerce product catalogs

\- 🔬 Research image datasets

\- 🗂️ ML training data management


**Front End UI Pages**

**Group 1**

<img width="1920" height="1080" alt="Screenshot 2026-03-02 111053" src="https://github.com/user-attachments/assets/bb47fa99-4e64-4485-8d4f-32fae8db9921" />

**Group  2**

<img width="1920" height="1080" alt="Screenshot 2026-03-02 111107" src="https://github.com/user-attachments/assets/f87833f7-3ac5-436c-b0b8-ad195f568939" />

**Group 3**

<img width="1920" height="1080" alt="Screenshot 2026-03-02 111122" src="https://github.com/user-attachments/assets/b0de2c51-5fcf-4bbe-8f11-e5a1a9588460" />

**Group 4**

<img width="1920" height="1080" alt="Screenshot 2026-03-02 111143" src="https://github.com/user-attachments/assets/b0299b36-2744-4d2e-8493-0ee0c51b8816" />


**Backend**






---

**\# 📖 API Endpoints**



\- POST /upload - Upload images

\- GET /cluster?eps=0.25 - Cluster images

\- GET /cluster/stats/{id} - Get statistics

\- GET /download/cluster/{id} - Download ZIP

---

**\# 📞 Contact**

Email: dharshanlak2005@gmail.com


Phone: 9043813443

---

**👨‍💻 Author**

Dharshan Lakshmanan
AI / ML Developer | Computer Vision Enthusiast

GitHub: https://github.com/dharshan-24

LinkedIn: https://www.linkedin.com/in/dharshanl/






 



