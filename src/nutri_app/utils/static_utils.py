import os
from flask import url_for, current_app

def static_versioned(filename):
    file_path = os.path.join(current_app.root_path, 'static', filename)
    
    if os.path.exists(file_path):
        version = int(os.path.getmtime(file_path))
        return url_for('static', filename=filename, v=version)
    
    return url_for('static', filename=filename)