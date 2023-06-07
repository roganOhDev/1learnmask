import datetime

from sqlalchemy import Column, Text, INTEGER, desc
from sqlalchemy.ext.declarative import declarative_base
from const.database_config import engine, get_db

from sqlalchemy import select

Base = declarative_base()
Base.metadata.create_all(bind=engine)


class Covid(Base):
    __tablename__ = "covid"

    id = Column(INTEGER, primary_key=True, autoincrement="auto")
    date = Column(Text, nullable=False)
    value = Column(INTEGER, nullable=False)
    created_at = Column(Text, nullable=False)

    def __init__(self, value, date):
        self.value = value
        self.date = date

    def save(self):
        db = next(get_db())
        self.created_at = datetime.datetime.now().strftime("%Y-%m-%d")
        db.add(self)
        db.commit()

    @staticmethod
    def get_latest_data():
        db = next(get_db())
        stmt = select(Covid).order_by(desc(Covid.date))
        return db.execute(stmt).fetchone()

    @staticmethod
    def get_by_date(date: str):
        db = next(get_db())
        stmt = select(Covid).where(Covid.date == date)
        return db.execute(stmt).fetchone()

    @staticmethod
    def get_week_data():
        db = next(get_db())
        stmt = select(Covid).order_by(desc(Covid.date)).limit(7)
        return db.execute(stmt).fetchall()

    @staticmethod
    def get_two_weeks_ago_data():
        db = next(get_db())

        subquery = db.query(Covid).order_by(desc(Covid.date)).limit(7).subquery()
        stmt = db.query(Covid).join(subquery, Covid.date == subquery.c.date).filter(
            subquery.c.date.is_(None)).order_by(desc(Covid.date)).limit(7)

        # 쿼리 실행 및 결과 가져오기
        return db.execute(stmt).fetchall()

    @staticmethod
    def get_30_days_data():
        db = next(get_db())
        stmt = select(Covid).order_by(desc(Covid.date)).limit(30)
        return db.execute(stmt).fetchall()
