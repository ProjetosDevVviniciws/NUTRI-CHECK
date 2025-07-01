from src.nutri_app import bcrypt

def gerar_hash(senha):
    return bcrypt.generate_password_hash(senha).decode('utf-8')

def verificar_senha(senha_hash, senha_texto):
    return bcrypt.check_password_hash(senha_hash, senha_texto)