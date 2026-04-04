from flask_mail import Message
from src.nutri_app import mail
from flask import render_template, current_app
import os
import threading

def enviar_email_async(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            print("ERRO AO ENVIAR EMAIL:", str(e))

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

    thread = threading.Thread(
        target=enviar_email_async,
        args=(current_app._get_current_object(), msg)
    )
    
    thread.start()