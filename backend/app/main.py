from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .config import settings
from .database import init_db
from .routes import cart_router, category_router, product_router

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Список строк или паттернов
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все HTTP методы (GET, POST, PUT, DELETE и т.д.)
    allow_headers=["*"],  # Разрешаем все заголовки
)

app.mount("/static", StaticFiles(directory=settings.static_dir), name="static")


app.include_router(product_router)

app.include_router(category_router)

app.include_router(cart_router)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def root():
    return {"message": "Welcome to the API!", "docs": "api/docs"}


@app.get("/health")
def health():
    return {"status": "ok"}
