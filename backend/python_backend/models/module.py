from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from database import Base


class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    content = Column(Text, nullable=True)  # Module overview content
    module_type = Column(String, nullable=True)  # e.g., "ROS 2", "Gazebo", "NVIDIA Isaac", "VLA"
    week_number = Column(Integer, nullable=True)  # Week number in curriculum
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())