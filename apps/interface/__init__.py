from flask import Blueprint

bp = Blueprint('interface', __name__)

from apps.interface import routes
from apps.interface import api
