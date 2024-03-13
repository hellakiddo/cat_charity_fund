from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from app.models.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    pass
