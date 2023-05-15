from sqlalchemy import Column, Text, INTEGER
from sqlalchemy.ext.declarative import declarative_base
from const.database_config import engine, get_db

Base = declarative_base()
Base.metadata.create_all(bind=engine)


class Capture(Base):
    __tablename__ = "covid"

    id = Column(INTEGER, primary_key=True, autoincrement= "auto")
    date = Column(Text, nullable=False)
    value = Column(INTEGER, nullable=False)

    def __init__(self, value, date):
        self.value = value
        self.date = date

    def save(self):
        db = next(get_db())
        db.add(self)
        db.commit()
