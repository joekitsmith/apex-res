from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apex_res.routers.two_gradient import two_gradient_router
from apex_res.routers.user import user_router

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(two_gradient_router, prefix="/two_gradient", tags=["Two gradient"])
app.include_router(user_router, prefix="/user", tags=["User"])


@app.get("/health", tags=["health_check"])
def health_check():
    """Health check"""
    return {"message": "Server is healthy"}
