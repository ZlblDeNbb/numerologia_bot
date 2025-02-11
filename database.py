from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.exc import SQLAlchemyError
import datetime

# Создание базы с SQLAlchemy ORM
Base = declarative_base()


# Модель пользователя
class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)

    queries = relationship("Query", back_populates="user")


# Модель запроса
class Query(Base):
    __tablename__ = 'queries'

    query_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    query_type = Column(String, nullable=False)
    query_text = Column(Text)
    response_text = Column(Text)
    timestamp = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="queries")


# Менеджер базы данных
class DatabaseManager:
    def __init__(self, db_url = "postgresql+psycopg2://constantine:dox123456@db:5432/numerology_bot"):
        # Создаем движок SQLAlchemy
        self.engine = create_engine(db_url)
        # Создаем таблицы в базе данных (если их еще нет)
        Base.metadata.create_all(self.engine)
        # Создаем сессию
        self.Session = sessionmaker(bind=self.engine)

    # Добавление пользователя
    def add_user(self, user_id, username):
        session = self.Session()
        try:
            user = session.query(User).filter_by(user_id=user_id).first()
            if not user:
                user = User(user_id=user_id, username=username)
                session.add(user)
                session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error adding user: {e}")
        finally:
            session.close()

    # Добавление запроса
    def add_query(self, user_id, query_type, query_text, response_text):
        session = self.Session()
        try:
            query = Query(
                user_id=user_id,
                query_type=query_type,
                query_text=query_text,
                response_text=response_text,
                timestamp=datetime.datetime.now()
            )
            session.add(query)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error adding query: {e}")
        finally:
            session.close()

    # Закрытие подключения
    def close(self):
        self.engine.dispose()

__all__ = ()
