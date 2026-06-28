from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Mudamos a porta para 6543 (Modo Pooler do Supabase) e forçamos o uso seguro de SSL
DATABASE_URL = "postgresql://postgres:20PhokeTON9470029@db.ispudphtjljcmrvnyzex.supabase.co:6543/postgres?sslmode=require"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def obter_bd():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()