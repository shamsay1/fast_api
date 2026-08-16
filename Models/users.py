from sqlalchemy import Column,Integer, String
from .database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True,index=True)
    firstname = Column(String(100))
    lastname = Column(String(100))
    email = Column(String(100))
    password = Column(String(255))
    status = Column(String(100),default="Active")
    licenses = relationship("License", back_populates="user")


