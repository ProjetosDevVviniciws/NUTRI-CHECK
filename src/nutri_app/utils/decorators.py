from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user
from src.nutri_app.database import engine
from sqlalchemy import text

def perfil_completo_required(f):
    @wraps(f)
    def decoreted_function(*args, **kwargs):
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT calorias_meta, proteinas_meta, carboidratos_meta, gorduras_meta
                FROM usuarios
                WHERE id = id:
            """), {"id": current_user.id}).fetchone()
            
            if result is None or any(valor is None for valor in result):
                flash("Complete seu perfil antes de acessar essa funcionalidade.", category="warning")
                return redirect(url_for('perfil.perfil_usuario'))
            
        return f(*args, **kwargs)
    return decoreted_function