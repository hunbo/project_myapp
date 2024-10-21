from sqlalchemy import Column, Integer, Boolean, Text, Float, String
from database import Base


#sales-dashboard 테이블
class Sales(Base):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True, index=True)
    sales_amount = Column(Float, nullable=False )
    month = Column(String(2), nullable=False)

#todos 테이블
class Todo(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True)
    task = Column(Text)
    completed = Column(Boolean, default=False)