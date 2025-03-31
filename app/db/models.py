from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    yandex_id = Column(String, unique=True, index=True)
    username = Column(String)
    is_superuser = Column(Boolean, default=False)  # Добавлено
    files = relationship("AudioFile", back_populates="owner")

class AudioFile(Base):
    __tablename__ = "audio_files"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    filepath = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="files")
