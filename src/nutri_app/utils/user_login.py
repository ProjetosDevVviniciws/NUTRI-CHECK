from flask_login import UserMixin
from src.nutri_app import login_manager
from src.nutri_app.database import engine
from sqlalchemy import text

class UserLogin(UserMixin):
    def __init__(self, usuario_row):
        self.id = usuario_row.id
        self.nome = usuario_row.nome
        self.email = usuario_row.email
        self.senha = usuario_row.senha
        
    def get_id(self):
        return str(self.id)
    
@login_manager.user_loader
def load_user(user_id):
    with engine.connect() as conn:
        query = text("SELECT * FROM usuarios WHERE id = :id")
        result = conn.execute(query, {"id": int(user_id)})
        row = result.fetchone()
        
        if row:
            return UserLogin(row)
        return None
