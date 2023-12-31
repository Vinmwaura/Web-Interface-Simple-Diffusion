import os
from dotenv import load_dotenv

import torch

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Loads .env variables if any.
env_file = ".env"
env = os.path.join(os.getcwd(), env_file)
if os.path.exists(env):
    load_dotenv(env)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default secret')
    DEVICE = os.environ.get('DEVICE', 'cuda' if torch.cuda.is_available() else 'cpu')

    BODY_POSE_IMG_DIM = os.environ.get('BODY_POSE_IMG_DIM', 128)
    MYFACE_IMG_DIM = os.environ.get('MYFACE_IMG_DIM', 128)
    CELEBFACE_IMG_DIM = os.environ.get('CELEBFACE_IMG_DIM', 128)
    ANIMEPORTRAITS_IMG_DIM = os.environ.get('ANIMEPORTRAITS_IMG_DIM', 128)

    BODY_POSE_BASE_PATH = os.environ.get("BODY_POSE_BASE_PATH")
    BODY_POSE_SR_PATH = os.environ.get("BODY_POSE_SR_PATH")
    MYFACE_BASE_PATH = os.environ.get("MYFACE_BASE_PATH")
    MYFACE_SR_PATH = os.environ.get("MYFACE_SR_PATH")
    CELEBFACE_BASE_PATH = os.environ.get("CELEBFACE_BASE_PATH")
    ANIMEPORTRAITS_BASE_PATH = os.environ.get("ANIMEPORTRAIT_BASE_PATH")
    ANIMEPORTRAITS_SR_PATH = os.environ.get("ANIMEPORTRAIT_SR_PATH")
