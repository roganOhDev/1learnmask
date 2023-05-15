from sqlalchemy import Column, Text, INTEGER, select
from sqlalchemy.ext.declarative import declarative_base
from const.database_config import engine, get_db

Base = declarative_base()
Base.metadata.create_all(bind=engine)


class AirQualityPm10(Base):
    __tablename__ = "air_quality10"

    id = Column(INTEGER, primary_key=True, autoincrement= "auto")
    dataTime = Column(Text, nullable=False)
    pm10Value = Column(INTEGER, nullable=False)

    def __init__(self, data_time, pm_10_value):
        self.dataTime = data_time
        self.pm10Value = pm_10_value

    def save(self):
        db = next(get_db())
        db.add(self)
        db.commit()

    @staticmethod
    def select(where_data_time: str):
        db = next(get_db())
        stmt =  select(AirQualityPm10).where(AirQualityPm10.dataTime == where_data_time)
        return db.execute(stmt).first()

