# 🚀 FastAPI Social Media Backend

🔗 **A modern, scalable backend for a social media application built using FastAPI.**  
It supports user authentication, posts, likes, and social interactions with clean API design.

---

## 🌐 **Project Overview**

This project provides a **RESTful backend** for a social media platform where users can:

- Register & log in securely  
- Create and view posts  
- Interact with other users  
- Access APIs via Swagger UI  

Built with **FastAPI**, this backend is fast, lightweight, and production-ready.

---

## ✨ **Key Features**

✅ User authentication (login & register)  
✅ Secure API endpoints  
✅ Create, read, and manage posts  
✅ RESTful architecture  
✅ Automatic Swagger & ReDoc documentation  
✅ Easy to deploy and scale  

---

## 🧠 **How It Works**

1️⃣ User registers or logs in  
2️⃣ Authentication token is generated  
3️⃣ User creates / fetches posts  
4️⃣ Backend processes requests via FastAPI  
5️⃣ JSON responses returned to client  

---

## 🛠️ **Tech Stack**

| Technology | Usage |
|----------|------|
| ⚡ **FastAPI** | Backend framework |
| 🐍 **Python** | Core language |
| 🔐 **JWT / OAuth** | Authentication |
| 🗄 **SQLite / PostgreSQL** | Database |
| 📦 **Pydantic** | Data validation |
| 🌐 **Uvicorn** | ASGI server |

---

## 📂 **Project Structure**

```text
fastapi-social-backend/
│
├── app/
│   ├── main.py              # App entry point
│   ├── models.py            # Database models
│   ├── schemas.py           # Request/response schemas
│   ├── auth.py              # Authentication logic
│   ├── routes/
│   │   ├── users.py         # User routes
│   │   └── posts.py         # Post routes
│
├── requirements.txt         # Dependencies
├── README.md                # Documentation
└── database.db              # Database file
⚙️ Installation & Setup
🔹 1. Clone the Repository
git clone https://github.com/Shravanthi-K/fastapi-social-backend.git
cd fastapi-social-backend

🔹 2. Create Virtual Environment
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows

🔹 3. Install Dependencies
pip install -r requirements.txt

▶️ Run the Server
uvicorn app.main:app --reload


📌 Server runs at:

http://127.0.0.1:8000

📘 API Documentation

FastAPI automatically provides interactive docs:

🔹 Swagger UI
👉 http://127.0.0.1:8000/docs

🔹 ReDoc
👉 http://127.0.0.1:8000/redoc

🧪 Sample API Endpoints
Method	Endpoint	Description
POST	/register	Register user
POST	/login	User login
POST	/posts	Create post
GET	/posts	View posts
📈 Use Cases

🔹 Social media platforms
🔹 Backend for React / Flutter apps
🔹 Learning FastAPI & REST APIs
🔹 Scalable microservices

🚧 Future Improvements

🌟 Add likes & comments
🌟 Add follow/unfollow users
🌟 Add role-based access control
🌟 Dockerize the application
🌟 Deploy to cloud (Render / AWS)

🤝 Contributing

Contributions are welcome! 🚀

Fork the repository

Create a new branch

Commit your changes

Open a Pull Request

📜 License

This project is licensed under the MIT License.

🙌 Acknowledgements

FastAPI documentation

Python open-source community

Uvicorn & Pydantic contributors

⭐ If you like this project, don’t forget to star the repository!
