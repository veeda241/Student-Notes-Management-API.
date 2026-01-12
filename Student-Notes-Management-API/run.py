"""
Application runner script.
Run this file to start the development server.
"""

import uvicorn
from app.config import settings

if __name__ == "__main__":
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║           Student Notes Management API                       ║
║                                                              ║
║   Server running at: http://localhost:{settings.PORT}                 ║
║   Frontend: http://localhost:{settings.PORT}/                         ║
║   Swagger Docs: http://localhost:{settings.PORT}/docs                 ║
║   ReDoc: http://localhost:{settings.PORT}/redoc                       ║
║                                                              ║
║   Press CTRL+C to stop the server                            ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
