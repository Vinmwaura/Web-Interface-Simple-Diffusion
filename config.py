import os
import torch

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default secret')
    DEVICE = os.environ.get('DEVICE', 'cuda' if torch.cuda.is_available() else 'cpu')
    DOODLE_IMG_DIM = os.environ.get('DOODLE_IMG_DIM', 128)
    DOODLE_BASE_PATH = os.environ.get("DOODLE_BASE_PATH", "./models/doodle_base.json")
    DOODLE_SR_PATH = os.environ.get("DOODLE_SR_PATH", "./models/doodle_sr.json")
