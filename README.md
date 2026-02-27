 

 🎨 DINOv2 Smart Grouping - AI Visual Clustering Dashboard



\[!\[Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)

\[!\[React](https://img.shields.io/badge/React-18.0+-61DAFB.svg)](https://reactjs.org/)

\[!\[FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com/)

\[!\[License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)



> Automatically group images by visual similarity using Meta's DINOv2 vision transformer and DBSCAN clustering.



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



\# Backend setup

cd backend

python -m venv venv

venv\\Scripts\\activate

pip install -r requirements.txt



\# Frontend setup

cd ..\\frontend

npm install



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

✅ Group 1 (Green)  → 5 cats    | 92.1% similarity ⭐⭐⭐

✅ Group 2 (Blue)   → 5 dogs    | 88.5% similarity ⭐⭐⭐

✅ Group 3 (Purple) → 3 cars    | 85.2% similarity ⭐⭐⭐

✅ Group 4 (Red)    → 5 humans  | 76.3% similarity ⭐⭐

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



\*\*Created by:\*\* \[Lancy Mariyal J]

\- GitHub: \[@1927lanc](https://github.com/ 1927lanc)

 
 \- Email: 1927lanc@gmail.com
## 👥 Team Workflow
 

This update is submitted via pull request to demonstrate collaborative development workflow.


---



⭐ Star this repo if it helped you!

 

