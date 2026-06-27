from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Como tens um arquivo docker-compose.yml, provavelmente usarás PostgreSQL ou MySQL no futuro.
# Para testar rápido agora, vamos usar SQLite (ele cria um arquivo local automático).
DATABASE_URL = "sqlite:///./phydex.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criamos a Base declarativa que os modelos precisam herdar
Base = declarative_base()

# Função utilitária para abrir e fechar a conexão com o banco nas rotas
def obter_bd():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()