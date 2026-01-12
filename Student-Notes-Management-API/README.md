# 📚 Student Notes Management API

A clean, modular FastAPI application for managing student notes. Built with scalability in mind, ready for MySQL integration.

## ✨ Features

- **Full CRUD Operations**: Create, Read, Update, Delete notes
- **Pagination**: Built-in pagination for large datasets
- **Filtering**: Filter notes by subject, student name, or search terms
- **Tags**: Organize notes with tags
- **Swagger Documentation**: Interactive API documentation
- **Modular Architecture**: Clean separation of concerns
- **MySQL Ready**: Designed for easy database migration

## 🏗️ Project Structure

```
Student-Notes-Management-API/
├── app/
│   ├── __init__.py          # Package initialization
│   ├── main.py               # FastAPI application
│   ├── config.py             # Configuration settings
│   │
│   ├── models/               # SQLAlchemy models (for MySQL)
│   │   ├── __init__.py
│   │   └── note.py
│   │
│   ├── schemas/              # Pydantic schemas
│   │   ├── __init__.py
│   │   └── note.py
│   │
│   ├── routes/               # API route handlers
│   │   ├── __init__.py
│   │   └── notes.py
│   │
│   ├── services/             # Business logic
│   │   ├── __init__.py
│   │   └── note_service.py
│   │
│   └── database/             # Database configuration
│       ├── __init__.py
│       └── in_memory.py
│
├── requirements.txt          # Python dependencies
├── run.py                    # Application runner
├── .env.example              # Environment variables template
└── README.md                 # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Student-Notes-Management-API
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/macOS
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment (optional)**
   ```bash
   copy .env.example .env
   # Edit .env with your settings
   ```

5. **Run the application**
   ```bash
   python run.py
   ```

6. **Open your browser**
   - API Documentation: http://localhost:8000/docs
   - Alternative Docs: http://localhost:8000/redoc

## 📖 API Endpoints

### Notes

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/notes/` | Get all notes (paginated) |
| GET | `/api/v1/notes/{id}` | Get a specific note |
| POST | `/api/v1/notes/` | Create a new note |
| PUT | `/api/v1/notes/{id}` | Update a note |
| DELETE | `/api/v1/notes/{id}` | Delete a note |
| GET | `/api/v1/notes/subjects` | Get all unique subjects |
| GET | `/api/v1/notes/students` | Get all unique student names |
| GET | `/api/v1/notes/tag/{tag}` | Get notes by tag |

### Health

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/info` | API information |

## 📝 Example Usage

### Create a Note

```bash
curl -X POST "http://localhost:8000/api/v1/notes/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Introduction to FastAPI",
    "content": "FastAPI is a modern, fast web framework for building APIs with Python.",
    "subject": "Web Development",
    "student_name": "John Doe",
    "tags": ["python", "fastapi", "web"]
  }'
```

### Get All Notes with Filtering

```bash
curl "http://localhost:8000/api/v1/notes/?subject=Computer%20Science&page=1&page_size=10"
```

### Update a Note

```bash
curl -X PUT "http://localhost:8000/api/v1/notes/1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Title",
    "tags": ["updated", "python"]
  }'
```

## 🔧 MySQL Integration

To switch from in-memory storage to MySQL:

1. **Install MySQL driver**
   ```bash
   pip install pymysql
   ```

2. **Update `.env`**
   ```env
   DATABASE_URL=mysql+pymysql://user:password@localhost:3306/notes_db
   ```

3. **Create database tables** (coming in next version)
   ```python
   from app.models.note import Base
   from sqlalchemy import create_engine
   
   engine = create_engine(DATABASE_URL)
   Base.metadata.create_all(bind=engine)
   ```

## 🧪 Testing

```bash
# Run with pytest (install pytest first)
pip install pytest pytest-asyncio httpx
pytest
```

## 📄 License

MIT License - feel free to use this project for learning and development.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

Built with ❤️ using [FastAPI](https://fastapi.tiangolo.com/)
