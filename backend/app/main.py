from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import routes_admin, routes_chat, routes_docs
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Research Assistant Backend",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(routes_admin.router)
app.include_router(routes_chat.router)
app.include_router(routes_docs.router)

@app.get("/")
def root():
    return {"status": "ok", "message": "Welcome to Research Assistant API"}
