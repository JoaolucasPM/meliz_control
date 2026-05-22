from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from src.models.base import db



class Product(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    produto: Mapped[str] = mapped_column()
    cliente: Mapped[str] = mapped_column()
    valor_venda: Mapped[float] = mapped_column()
    