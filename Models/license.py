from .database import Base
from datetime import datetime
from sqlalchemy import Column,String,ForeignKey,Integer,Date,DateTime,Enum
from sqlalchemy.orm import relationship

class License(Base):
    __tablename__ = "licenses"
    id = Column(Integer,primary_key=True,index=True)
    license_number = Column(String(255),unique=True)
    control_number = Column(String(255),unique=True)
    license_type = Column(String(20))
    issue_date = Column(Date)
    expired_date = Column(Date)
    status = Column(Enum('expired','active',name="license_status"), default='active')
    user_id = Column(Integer,ForeignKey('users.id'),nullable=False)
    created_at = Column(DateTime,default=datetime.utcnow)
    user = relationship('User', back_populates='licenses')
