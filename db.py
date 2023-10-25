# psqldb.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# DATABASE_URI = "postgresql://radhakrishnan:1D1sWtcoTVBB7U26tX2EOJ9a1Q4zu82x@dpg-ckp2oi8ujous738qgcdg-a:5432/guviproject" # manual
# DATABASE_URI = "postgresql://radhakrishnan:1D1sWtcoTVBB7U26tX2EOJ9a1Q4zu82x@dpg-ckp2oi8ujous738qgcdg-a/guviproject" #internal
DATABASE_URI = "postgresql://radhakrishnan:1D1sWtcoTVBB7U26tX2EOJ9a1Q4zu82x@dpg-ckp2oi8ujous738qgcdg-a.oregon-postgres.render.com/guviproject" #external
# DATABASE_URI = 'postgresql://postgres:ags009@localhost:5432/curd' #local


engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def CreateTables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()