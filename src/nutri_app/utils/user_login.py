from flask_login import UserMixin

class UserLogin(UserMixin):
    def __init__(self, usuario_row):
        self.id = usuario_row.id
        self.usuario = usuario_row.usuario
        self.email = usuario_row.email
        self.senha = usuario_row.senha
        
    def get_id(self):
        return str(self.id)
