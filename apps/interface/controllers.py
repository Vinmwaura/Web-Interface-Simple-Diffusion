import cv2
from flask import current_app


# Diffusion Lib.
from generate_images_diffusion import generate_images_diffusion as diffusion_sampling
from generate_sr_images_diffusion import generate_sr_images_diffusion as diffusion_upsampling_sampling

from apps.interface.utils import convert_tensor_to_numpy


# Generates Low Resolution Image using Diffusion Model.
def generate_base_diffusion(commands, cond_img=None, log=print):
    if cond_img is not None:
        img_dim = (
            int(current_app.config["BODY_POSE_IMG_DIM"]),
            int(current_app.config["BODY_POSE_IMG_DIM"]))
        cond_img = cv2.resize(
            cond_img,
            img_dim,
            interpolation=cv2.INTER_AREA)
    else:
        cond_img = None

    img_tensor = diffusion_sampling(
        raw_args=commands,
        log=log,
        cond_img=cond_img,
        save_locally=False)

    # Converts tensor output to numpy.
    img_numpy = convert_tensor_to_numpy(img_tensor)

    return img_numpy

# Generates Super Resolution Image using Diffusion Model.
def generate_sr_diffusion(lr_image, commands, log=print):
    img_tensor = diffusion_upsampling_sampling(
        raw_args=commands,
        lr_img=lr_image,
        log=log,
        save_locally=False)

    # Converts tensor output to numpy.
    img_numpy = convert_tensor_to_numpy(img_tensor)
    return img_numpy
    

