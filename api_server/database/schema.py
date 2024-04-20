from sqlalchemy import (JSON, ForeignKey, String, TypeDecorator,
                        func, types)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime
class Base(DeclarativeBase):
    pass


class MetroLine(Base):
    __tablename__ = "metro_line"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    line_number: Mapped[int]
    name: Mapped[str]
    

class MetroStation(Base):
    __tablename__ = "metro_station"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    
    line_id: Mapped[int] = mapped_column(ForeignKey("metro_line.id"))
    
    line: Mapped[MetroLine] = relationship()
    
class History(Base):
    __tablename__ = "history"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    request: Mapped[str]
    response: Mapped[str] = mapped_column(nullable=True)
    
    webhook: Mapped[str]
    
    user_ray_id: Mapped[str]
    neuro_ray_id: Mapped[str]
    
    timestamp: Mapped[datetime] = mapped_column(server_default=func.now())
    

class FlowData(Base):
    __tablename__ = "flow_data"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    timestamp: Mapped[datetime]
    
    count: Mapped[int]
    
    metro_station_id: Mapped[int] = mapped_column(ForeignKey("metro_station.id"))
    
    
    metro_station: Mapped[MetroStation] = relationship()
    
    