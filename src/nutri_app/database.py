from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()
string_conexao = os.getenv("DATABASE_URL")

engine = create_engine(string_conexao)

def get_usuarios():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM usuarios"))
        return [dict(row) for row in result]