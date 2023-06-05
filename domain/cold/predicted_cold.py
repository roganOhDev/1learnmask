import datetime

from sqlalchemy import Column, Text, INTEGER, desc, select
from sqlalchemy.ext.declarative import declarative_base
from const.database_config import engine, get_db

Base = declarative_base()
Base.metadata.create_all(bind=engine)


class PredictedCold(Base):
    __tablename__ = "predicted_cold"

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
        stmt = select(PredictedCold).where(PredictedCold.date == now_date)
        return db.execute(stmt).fetchall()


    @staticmethod
    def get_latest():
        db = next(get_db())
        stmt = select(PredictedCold).order_by(desc(PredictedCold.date)).limit(1)
        return db.execute(stmt).fetchone()
