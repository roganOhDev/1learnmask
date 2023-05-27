from sqlalchemy import Column, Text, INTEGER, select, desc
from sqlalchemy.ext.declarative import declarative_base
from const.database_config import engine, get_db

Base = declarative_base()
Base.metadata.create_all(bind=engine)


class AirQuality(Base):
    __tablename__ = "air_quality"

    id = Column(INTEGER, primary_key=True, autoincrement="auto")
    dataTime = Column(Text, nullable=False)
    pm10Value = Column(INTEGER, nullable=False)
    pm25Value = Column(INTEGER, nullable=False)

    def __init__(self, data_time, pm_10_value, pm_25_value):
        self.dataTime = data_time
        self.pm25Value = pm_25_value
        self.pm10Value = pm_10_value

    def save(self):
        db = next(get_db())
        db.add(self)
        db.commit()

    @staticmethod
    def get_latest_data():
        db = next(get_db())
        stmt = select(AirQuality).order_by(desc(AirQuality.dataTime))
        return db.execute(stmt).fetchone()

    @staticmethod
    def get_2_days_data(datetime: str):
        db = next(get_db())
        stmt = select(AirQuality).where(AirQuality.dataTime >= datetime).order_by(desc(AirQuality.dataTime))
        return db.execute(stmt).fetchall()
