import datetime

from sqlalchemy import Column, Text, INTEGER, desc, select
from sqlalchemy.ext.declarative import declarative_base
from const.database_config import engine, get_db

Base = declarative_base()
Base.metadata.create_all(bind=engine)


class Cold(Base):
    __tablename__ = "cold"

    id = Column(INTEGER, primary_key=True, autoincrement="auto")
    year = Column(INTEGER, nullable=False)
    date = Column(Text, nullable=False)
    value = Column(INTEGER, nullable=False)

    def __init__(self, value, year, date):
        self.value = value
        self.year = year
        self.date = date

    def save(self):
        db = next(get_db())
        db.add(self)
        db.commit()

    @staticmethod
    def get_all_by_date(now: datetime.datetime):
        now = now.isoformat()
        now_date = now[5:7] + "-" + now[8:10]

        db = next(get_db())
        stmt = select(Cold).where(Cold.date == now_date)
        return db.execute(stmt).fetchall()
