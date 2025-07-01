from flask import Blueprint, render_template, request

agua_bp = Blueprint('agua', __name__)

@agua_bp.route('/agua', methods=['GET', 'POST'])
def registrar_agua():
    return render_template('agua.html')