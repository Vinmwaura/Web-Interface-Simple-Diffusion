from flask import (
    Flask,
    request,
    jsonify,
    current_app)

from apps.interface import bp

from apps.interface.utils import (
    convert_binary_to_numpy,
    convert_numpy_to_base64)
from apps.interface.controllers import (
    generate_base_diffusion,
    generate_sr_diffusion)

@bp.route("/api/generate_doodle_images", methods=["POST"])
def generate_doodle_images():
    # Read image file string data
    canvas_image = request.files["canvas_image"]
    if canvas_image.filename != "":
        img = convert_binary_to_numpy(canvas_image)
    else:
        # Error No image passed.
        data_dict = {
            "image": None,
            "message": "No / Invalid Image passed.",
            "status": 400
        }

        resp = jsonify(data_dict)
        resp.status_code = 400
        return resp 
    
    # Conditional Information for Base Diffusion.
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
        
        img = generate_base_diffusion(
            cond_img=img,
            commands=commands)

        if upsample:
            upsample_commands = ["--model_path", current_app.config["DOODLE_SR_PATH"]]

            upsample_commands.append("--device")
            upsample_commands.append(current_app.config["DEVICE"])

            upsample_commands.append("--cold_step_size")
            upsample_commands.append(sr_skip_step)

            img = generate_sr_diffusion(
                lr_image=img,
                commands=upsample_commands)
    except Exception as e:
        print(f"An error occured generating image: {e}")
        data_dict = {
            "image": None,
            "message": "An error occured generaing image.",
            "status": 500}

        resp = jsonify(data_dict)
        resp.status_code = 500
        return resp 
    
    # Convert numpy image to base64.
    b64_img = convert_numpy_to_base64(img)
    data_dict = {
        "image": b64_img,
        "message": "Successfully generated Image.",
        "status": 200}
    resp = jsonify(data_dict)
    resp.status_code = 200
    return resp

@bp.route("/api/generate_myface_images", methods=["POST"])
def generate_myface_images():
    # Left Eye.
    left_eye = request.form.get("left_eye", False)
    if left_eye == "false":
        left_eye = "0"
    else:
        left_eye = "1"

    # Right Eye.
    right_eye = request.form.get("right_eye", False)
    if right_eye == "false":
        right_eye = "0"
    else:
        right_eye = "1"

    # Mouth.
    mouth = request.form.get("mouth", False)
    if mouth == "false":
        mouth = "0"
    else:
        mouth = "1"

    # Showing Teeth
    showing_teeth = request.form.get("showing_teeth", False)
    if showing_teeth == "false":
        showing_teeth = "0"
    else:
        showing_teeth = "1"

    # Conditional Information for Base Diffusion.
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
        commands = ["--model_path", current_app.config["MYFACE_BASE_PATH"]]

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

        commands.append("--label")
        commands.append(left_eye)
        commands.append(right_eye)
        commands.append(mouth)
        commands.append(showing_teeth)

        img = generate_base_diffusion(commands=commands)

        if upsample:
            upsample_commands = ["--model_path", current_app.config["MYFACE_SR_PATH"]]

            upsample_commands.append("--device")
            upsample_commands.append(current_app.config["DEVICE"])

            upsample_commands.append("--cold_step_size")
            upsample_commands.append(sr_skip_step)

            upsample_commands.append("--label")
            upsample_commands.append(left_eye)
            upsample_commands.append(right_eye)
            upsample_commands.append(mouth)
            upsample_commands.append(showing_teeth)

            img = generate_sr_diffusion(
                lr_image=img,
                commands=upsample_commands)

    except Exception as e:
        print(f"An error occured generating image: {e}")
        data_dict = {
            "image": None,
            "message": "An error occured generaing image.",
            "status": 500}

        resp = jsonify(data_dict)
        resp.status_code = 500
        return resp

    # Convert numpy image to base64.
    b64_img = convert_numpy_to_base64(img)
    data_dict = {
        "image": b64_img,
        "message": "Successfully generated Image.",
        "status": 200}
    resp = jsonify(data_dict)
    resp.status_code = 200
    return resp

