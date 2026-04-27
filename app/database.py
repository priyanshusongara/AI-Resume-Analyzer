from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


import os
if not os.path.exists("./data.db"):
    open("./data.db", "w").close()

os.makedirs("/tmp", exist_ok=True)
#DATABASE_URL = "sqlite:///./tmp/data.db"
DATABASE_URL = "sqlite:///./data.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()