from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine

Base = declarative_base()


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    status = Column(String)
    owner = Column(String)


engine = create_engine("sqlite:///database.db", pool_size=100)
Base.metadata.create_all(engine)


SessionLocal = sessionmaker(bind=engine)