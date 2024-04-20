from sqlalchemy import (JSON, ForeignKey, String, TypeDecorator,
                        func, types)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class RayTracker(Base):
    __tablename__ = "ray_tracker"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int]
    ray_id: Mapped[str]
    

# class UserMetrics(Base):
#     __tablename__ = "user_metrics"
    # TODO: Create user metrics
    
    