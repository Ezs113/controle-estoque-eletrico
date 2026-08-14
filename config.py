import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


class Config:
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "controle-de-estoque",
    )
    DATABASE = BASE_DIR / "banco" / "estoque.db"
