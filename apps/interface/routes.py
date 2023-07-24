from flask import render_template

from apps.interface import bp

@bp.route('/')
def index():
    return render_template("interface/home.html")
