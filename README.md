 

 🎨 DINOv2 Smart Grouping - AI Visual Clustering Dashboard





\## ✨ Features



\- 🤖 \*\*DINOv2 AI\*\* - State-of-the-art 768-dim feature extraction

\- 📊 \*\*Smart Clustering\*\* - DBSCAN + Hierarchical fallback

\- 🎨 \*\*Color-Coded Groups\*\* - Beautiful visual organization

\- 📈 \*\*Similarity Stats\*\* - Real-time cohesion metrics

\- 🎚️ \*\*Adjustable Sensitivity\*\* - Interactive slider (0.10-0.40)

\- 📥 \*\*Export Groups\*\* - Download clusters as ZIP

\- 🌙 \*\*Dark Theme\*\* - Professional interface



\## 🚀 Quick Start

``````bash

\# Clone repository

git clone https://github.com/yourusername/dinov2-smart-grouping.git

cd dinov2-smart-grouping



**\# Backend setup**

venv\\Scripts\\activate

cd backend

uvicorn main:app --reload

pip install -r requirements.txt



**\# Frontend setup**

venv\\Scripts\\activate
cd frontend
npm install
npm start



\# Run (2 terminals)

\# Terminal 1:

cd backend

uvicorn main:app --reload



\# Terminal 2:

cd frontend

npm start

``````



Open http://localhost:3000 🎉



\## 📸 Demo



Upload images → AI groups them → Download results!



Example output:

``````

✅ Group 1 (Green)  → 5 Computer    | 92.1% similarity ⭐⭐⭐

✅ Group 2 (Blue)   → 5 Birds       | 88.5% similarity ⭐⭐⭐

✅ Group 3 (Purple) → 3 Animals     | 85.2% similarity ⭐⭐⭐

✅ Group 4 (Red)    → 5 Humans      | 76.3% similarity ⭐⭐

``````



\## 🏗️ Tech Stack



\*\*Backend:\*\* Python • FastAPI • PyTorch • Transformers • scikit-learn

\*\*Frontend:\*\* React • CSS3

\*\*AI/ML:\*\* DINOv2 • DBSCAN • Cosine Similarity



\## 🎯 Use Cases



\- 📷 Photography organization

\- 🛍️ E-commerce product catalogs

\- 🔬 Research image datasets

\- 🗂️ ML training data management



\## 📖 API Endpoints



\- POST /upload - Upload images

\- GET /cluster?eps=0.25 - Cluster images

\- GET /cluster/stats/{id} - Get statistics

\- GET /download/cluster/{id} - Download ZIP



Full docs: http://localhost:8000/docs



\## 🤝 Contributing



Contributions welcome! Please read CONTRIBUTING.md



\## 📄 License



MIT License - see LICENSE file



\## 📞 Contact

Email: dharshanlak2005@gmail.com


Phone: 9043813443






 



