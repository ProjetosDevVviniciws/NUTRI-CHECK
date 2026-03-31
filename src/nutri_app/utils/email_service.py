from flask_mail import Message
from src.nutri_app import mail
from flask import render_template, current_app
import os

def enviar_email_reset(email, link, nome):
    msg = Message(
        subject="Recuperação de senha - NutriCheck",
        recipients=[email]
    )
    
    logo_path = os.path.join(current_app.root_path, "static", "images", "logo_email.png")
    
    with open(logo_path, "rb") as fp:
        msg.attach(
            filename="logo.png",
            content_type="image/png",
            data=fp.read(),
            disposition="inline",
            headers={"Content-ID": "<logo>"}
        )

    logo_src = "cid:logo"
    
    msg.html = render_template(
        "emails/body_email.html",
        link=link,
        nome=nome,
        logo_src=logo_src
    )

    mail.send(msg)