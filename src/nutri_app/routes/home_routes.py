from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    return render_template("home.html")