from fastapi import param_functions
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import BigInteger, SmallInteger
from .database import engine

Base = declarative_base()
Base.metadata.create_all(bind=engine)

# Stage与Author多对多关联中间表
class StageAuthor(Base):
  __tablename__ = 'stages_authors'

  stage_id = Column(Integer, primary_key=True, index=True)
  author_id = Column(Integer, primary_key=True, index=True)


class Author(Base):

    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    nickname = Column(String(50), nullable=True)
    email = Column(String(200), unique=True, index=True)
    hashed_password = Column(String(300))
    chain_address = Column(String(300))
    is_active = Column(Boolean, default=True)

    stages = relationship("Stage", back_populates="owner")
    stages_authors = relationship(
        "Stage",
        secondary=StageAuthor,
        back_populates="stages_join")



class Stage(Base):
    __tablename__ = "stages"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), index=True)
    content = Column(Text)
    owner_id = Column(Integer, ForeignKey("authors.id"))

    owner = relationship("Author", back_populates="stages")
    stages_authors = relationship(
        "Author",
        secondary=StageAuthor,
        back_populates="partners")



class Test(Base):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), index=True)
    owner_id = Column(Integer, ForeignKey("authors.id"))
