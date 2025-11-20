"""
Launch Script for AI Sales Assistant API
"""
import uvicorn
from app.main import app

if __name__ == "__main__":
    print("")
    print("="*70)
    print("🚀 Starting AI Sales Assistant API Server")
    print("="*70)
    print("")
    print("📡 Server will start on: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔄 Interactive API: http://localhost:8000/redoc")
    print("")
    print("Press CTRL+C to stop the server")
    print("="*70)
    print("")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
