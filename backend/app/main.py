from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import resume, quiz, progress, explain

app = FastAPI(title="Vidyamitra API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resume.router, prefix="/resume", tags=["resume"])
app.include_router(quiz.router, prefix="/quiz", tags=["quiz"])
app.include_router(progress.router, prefix="/progress", tags=["progress"])
app.include_router(explain.router, prefix="/explain", tags=["explain"])

@app.get("/")
def root():
    return {"status": "ok"}