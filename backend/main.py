import subprocess
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.db import init_db
from routes.execution_routes import router as execution_router
from routes.analysis_routes import router as analysis_router
from routes.correction_routes import router as correction_router
from routes.teaching_routes import router as teaching_router
from routes.ast_routes import router as ast_router

app = FastAPI(
    title="Codevanta — Intelligent Java & Python Analyzer",
    description="Deterministic code analysis, compilation, correction, and teaching platform without LLMs.",
    version="1.0.0"
)

# Enable CORS for local Vite frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,

    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup lifecycle
@app.on_event("startup")
def on_startup():
    init_db()

# Register all API routers
app.include_router(execution_router)
app.include_router(analysis_router)
app.include_router(correction_router)
app.include_router(teaching_router)
app.include_router(ast_router)

@app.get("/api/health")
async def health_check():
    """Returns the live environment and compiler status."""
    javac_ver = "Unavailable"
    java_ver = "Unavailable"
    
    try:
        proc = subprocess.run(["javac", "-version"], capture_output=True, text=True, timeout=2)
        javac_ver = proc.stdout.strip() or proc.stderr.strip()
    except Exception as e:
        javac_ver = f"Error: {e}"

    try:
        proc = subprocess.run(["java", "-version"], capture_output=True, text=True, timeout=2)
        java_ver = (proc.stdout.strip() or proc.stderr.strip()).splitlines()[0]
    except Exception as e:
        java_ver = f"Error: {e}"

    return {
        "status": "online",
        "platform": sys.platform,
        "python_version": sys.version.split()[0],
        "javac_version": javac_ver,
        "java_version": java_ver,
        "mode": "deterministic_rule_based"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
