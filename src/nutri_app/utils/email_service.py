from flask import render_template, current_app
import os
import resend

resend.api_key = os.getenv("RESEND_API_KEY")

def enviar_email_reset(email, link, nome):
    
    logo_src = "https://nutri-check-nw20.onrender.com/static/images/logo_email.png"
    
    html_content = render_template(
        "emails/body_email.html",
        link=link,
        nome=nome,
        logo_src=logo_src
    )
    
    resend.Emails.send({
        "from": "NutriCheck <onboarding@resend.dev>",
        "to": [email],
        "subject": "Recuperação de senha - NutriCheck",
        "html": html_content
    })