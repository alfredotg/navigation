from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
import os

engine = create_engine(os.environ.get('DATABASE_URL') + "?charset=utf8mb4", pool_recycle=60)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = automap_base()

Base.prepare(engine, reflect=True)
