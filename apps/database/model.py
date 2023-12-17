from sqlalchemy import Text, Boolean, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(DeclarativeBase):
    pass


class ModelLogs(BaseModel):
    __tablename__ = "ModelLogs"

    id: Mapped[int] = mapped_column(primary_key=True)
    model_output: Mapped[str] = mapped_column(Text)
    accuracy: Mapped[float] = mapped_column(Float)
    is_right: Mapped[bool] = mapped_column(Boolean, nullable=True)

