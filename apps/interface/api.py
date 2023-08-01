import os
import glob
import base64
import tempfile

import cv2
import numpy as np

from flask import (
    Flask,
    request,
    jsonify,
    current_app)

from apps.interface import bp

from generate_images_diffusion import generate_images_diffusion as diffusion_sampling
from generate_sr_images_diffusion import generate_sr_images_diffusion as diffusion_upsampling_sampling

@bp.route("/api/generate_doodle_images", methods=["POST"])
def generate_doodle_images():
    # Read image file string data
    canvas_image = request.files["canvas_image"]
    if canvas_image.filename != '':
        # Convert string data to numpy array
        file_bytes = np.fromstring(canvas_image.read(), np.uint8)
        # Convert numpy array to image
        img = cv2.imdecode(file_bytes, cv2.IMREAD_UNCHANGED)

        # Hack to remove alpha channel.
        img = img[:,:,:3]
    else:
        # Error No image passed.
        data_dict = {
            "images": None,
            "message": "No / Invalid Image passed.",
            "status": 400
        }

        resp = jsonify(data_dict)
        resp.status_code = 400
        return resp 

    cond_img = cv2.resize(img, (int(current_app.config["DOODLE_IMG_DIM"]), int(current_app.config["DOODLE_IMG_DIM"])), interpolation=cv2.INTER_AREA)
    seed = request.form.get("seed", None)
    if not seed:
        seed = None

    sample_alg = request.form.get("sample_alg", "ddpm")
    base_skip_step = request.form.get("base_skip_step", 100)
    if not base_skip_step:
        base_skip_step = None
    upsample = request.form.get("upsample", False)
    if upsample == "false":
        upsample = False
    else:
        upsample = True
    sr_skip_step = request.form.get("sr_skip_step", 100)
    if not sr_skip_step:
        sr_skip_step = None

    try:
        commands = ["--model_path", current_app.config["DOODLE_BASE_PATH"]]
    
        commands.append("--device")
        commands.append(current_app.config["DEVICE"])
        if seed:
            commands.append("-s")
            commands.append(seed)
        if sample_alg:
            commands.append("--diff_alg")
            commands.append(sample_alg)
        
        if sample_alg == "ddim":
            commands.append("--ddim_step_size")
            commands.append(base_skip_step)
        
        img_tensor = diffusion_sampling(
            raw_args=commands,
            log=print,
            cond_img=cond_img,
            save_locally=False)
        if upsample:
            upsample_commands = ["--model_path", current_app.config["DOODLE_SR_PATH"]]

            upsample_commands.append("--device")
            upsample_commands.append(current_app.config["DEVICE"])

            upsample_commands.append("--cold_step_size")
            upsample_commands.append(sr_skip_step)

            img_tensor = diffusion_upsampling_sampling(
                raw_args=upsample_commands,
                lr_img=img_tensor,
                log=print,
                save_locally=False)

    except Exception as e:
        print(f"An error occured generating image: {e}")
        data_dict = {
            "images": None,
            "message": "An error occured generaing image.",
            "status": 500}

        resp = jsonify(data_dict)
        resp.status_code = 500
        return resp 
    
    # Permute image to be of format: [H, W, C]
    img_tensor = img_tensor.permute(0, 2, 3, 1)
    img_tensor = ((img_tensor + 1) / 2) * 255
    img_tensor = img_tensor.squeeze(0)
    img_numpy = img_tensor.cpu().numpy()

    _, im_arr = cv2.imencode('.png', img_numpy)  # im_arr: image in Numpy one-dim array format.
    im_bytes = im_arr.tobytes()
    im_b64 = base64.b64encode(im_bytes)
    encoded_string_decoded = im_b64.decode("UTF-8")

    data_dict = {
        "image": encoded_string_decoded,
        "message": "Successfully generated Image",
        "status": 200
    }
    resp = jsonify(data_dict)
    resp.status_code = 200
    return resp
