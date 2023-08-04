import os
import torch

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default secret')
    DEVICE = os.environ.get('DEVICE', 'cuda' if torch.cuda.is_available() else 'cpu')

    BODY_POSE_IMG_DIM = os.environ.get('BODY_POSE_IMG_DIM', 128)
    MYFACE_IMG_DIM = os.environ.get('MYFACE_IMG_DIM', 128)
    CELEBFACE_IMG_DIM = os.environ.get('CELEBFACE_IMG_DIM', 128)
    ANIMEPORTRAITS_IMG_DIM = os.environ.get('ANIMEPORTRAITS_IMG_DIM', 128)

    BODY_POSE_BASE_PATH = os.environ.get(
        "BODY_POSE_BASE_PATH",
        os.path.join(
            BASE_DIR,
            "diffusion_apps/models/bodypose_base.json"))
    BODY_POSE_SR_PATH = os.environ.get(
        "BODY_POSE_SR_PATH",
        os.path.join(
            BASE_DIR,
            "diffusion_apps/models/bodypose_sr.json"))
    
    MYFACE_BASE_PATH = os.environ.get(
        "MYFACE_BASE_PATH",
        os.path.join(
            BASE_DIR,
            "diffusion_apps/models/myface_base.json"))
    MYFACE_SR_PATH = os.environ.get(
        "MYFACE_SR_PATH",
        os.path.join(
            BASE_DIR,
            "diffusion_apps/models/myface_sr.json"))
    
    CELEBFACE_BASE_PATH = os.environ.get(
        "CELEBFACE_BASE_PATH",
        os.path.join(
            BASE_DIR,
            "diffusion_apps/models/celebface_base.json"))
    
    ANIMEPORTRAITS_BASE_PATH = os.environ.get(
        "ANIMEPORTRAIT_BASE_PATH",
        os.path.join(
            BASE_DIR,
            "diffusion_apps/models/animeportraits_base.json"))
    ANIMEPORTRAITS_SR_PATH = os.environ.get(
        "ANIMEPORTRAIT_SR_PATH",
        os.path.join(
            BASE_DIR,
            "diffusion_apps/models/animeportraits_sr.json"))
