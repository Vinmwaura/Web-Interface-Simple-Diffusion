from flask import (
    request,
    jsonify,
    current_app)

from apps.interface.utils import (
    convert_binary_to_numpy,
    convert_numpy_to_base64)
from apps.interface import bp

from apps.interface.validators import *

@bp.route("/api/myposes", methods=["POST"])
def generate_body_poses():
    # Read image file string data
    canvas_image = request.files["canvas_image"]
    
    # Check if canvas image is valid.
    valid_img, error = validate_canvas_image(
        canvas_image=canvas_image,
        valid_img_extensions=current_app.config["UPLOAD_EXTENSIONS"])

    if not valid_img:
        resp = jsonify(error)
        resp.status_code = error["status"]
        return resp
    
    img = convert_binary_to_numpy(canvas_image)

    # Seed Params.
    seed = request.form.get("seed")
    valid_seed, error = is_valid_seed(seed)
    if not valid_seed:
        resp = jsonify(error)
        resp.status_code = error["status"]
        return resp

    # Diffusion Sample Algorithms Params.
    sample_alg = request.form.get("sample_alg", "ddpm")
    valid_sample_alg, error = is_valid_sample_alg(
        sample_alg,
        current_app.config["ALLOWED_SAMPLING_ALG"]) 
    if not valid_sample_alg:
        resp = jsonify(error)
        resp.status_code = error["status"]
        return resp
    
    # Base Model Skip Steps Params.
    default_skip_step = current_app.config["DEFAULT_SKIP_STEP"]
    base_skip_step = request.form.get(
        "base_skip_step",
        default_skip_step)
    valid_base_skip_step, error = is_valid_skip_step(base_skip_step)
    if not valid_base_skip_step:
        resp = jsonify(error)
        resp.status_code = error["status"]
        return resp

    # Upsample Params.
    valid_upsample_params = {
        "false": False,
        "true": True,
        None: False
    }
    upsample = request.form.get("upsample")
    valid_upsample, out = valid_param_value(upsample, valid_upsample_params)
    if not valid_upsample:
        resp = jsonify(out)
        resp.status_code = error["status"]
        return resp
    upsample = out
    
    # Super Resolution Model Skip Steps Params.
    sr_skip_step = request.form.get(
        "sr_skip_step",
        default_skip_step)
    valid_sr_skip_step, error = is_valid_skip_step(sr_skip_step)
    if not valid_sr_skip_step:
        resp = jsonify(error)
        resp.status_code = error["status"]
        return resp

    try:
        # Base Resolution Parameters.
        br_commands = [
            "--model_path",
            current_app.config["BODY_POSE_BASE_PATH"]]
    
        br_commands.append("--device")
        br_commands.append(current_app.config["DEVICE"])
        if seed:
            br_commands.append("-s")
            br_commands.append(str(seed))

        br_commands.append("--diff_alg")
        br_commands.append(sample_alg)
        
        if sample_alg == "ddim":
            br_commands.append("--ddim_step_size")
            br_commands.append(str(base_skip_step))
        
        if upsample:
            # Super Resolution Parameters.
            sr_commands = [
                "--model_path",
                current_app.config["BODY_POSE_SR_PATH"]]

            sr_commands.append("--device")
            sr_commands.append(current_app.config["DEVICE"])

            sr_commands.append("--cold_step_size")
            sr_commands.append(str(sr_skip_step))
        else:
            sr_commands = None

        # Get Hardware Resource if available to generate image.
        model_resource_ = current_app.config["model_resource"]
        img, ret_status = model_resource_.generate_diffusion(
            cond_img=img,
            br_commands=br_commands,
            sr_commands=sr_commands,
            cond_img_dim=current_app.config["BODY_POSE_IMG_DIM"],
            log=print)

        if ret_status == False:
            # Error No image returned.
            data_dict = {
                "image": None,
                "message": "Server busy, please try again after a few minutes.",
                "status": 503
            }

            resp = jsonify(data_dict)
            resp.status_code = 503
            return resp 
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

@bp.route("/api/myface", methods=["POST"])
def generate_myface():
    valid_face_param = {
        "false": 0,
        "true": 1,
        "0": 0,
        "1": 1,
        None: 0}
    
    # Left Eye.
    left_eye = request.form.get("left_eye")
    valid_status, out = valid_param_value(
        left_eye,
        valid_face_param)
    if not valid_status:
        resp = jsonify(out)
        resp.status_code = out["message"]
        return resp
    left_eye = out

    # Right Eye.
    right_eye = request.form.get("right_eye")
    valid_status, out = valid_param_value(
        right_eye,
        valid_face_param)
    if not valid_status:
        resp = jsonify(out)
        resp.status_code = out["message"]
        return resp
    right_eye = out

    # Mouth.
    mouth = request.form.get("mouth")
    valid_status, out = valid_param_value(
        mouth,
        valid_face_param)
    if not valid_status:
        resp = jsonify(out)
        resp.status_code = out["message"]
        return resp
    mouth = out

    # Showing Teeth
    showing_teeth = request.form.get("showing_teeth")
    valid_status, out = valid_param_value(
        showing_teeth,
        valid_face_param)
    if not valid_status:
        resp = jsonify(out)
        resp.status_code = out["message"]
        return resp
    showing_teeth = out

    # Seed Params.
    seed = request.form.get("seed")
    valid_seed, error = is_valid_seed(seed)
    if not valid_seed:
        resp = jsonify(error)
        resp.status_code = error["status"]
        return resp

    # Diffusion Sample Algorithms Params.
    sample_alg = request.form.get("sample_alg", "ddpm")
    valid_sample_alg, error = is_valid_sample_alg(
        sample_alg,
        current_app.config["ALLOWED_SAMPLING_ALG"]) 
    if not valid_sample_alg:
        resp = jsonify(error)
        resp.status_code = error["status"]
        return resp
    
    # Base Model Skip Steps Params.
    default_skip_step = current_app.config["DEFAULT_SKIP_STEP"]
    base_skip_step = request.form.get(
        "base_skip_step",
        default_skip_step)
    valid_base_skip_step, error = is_valid_skip_step(base_skip_step)
    if not valid_base_skip_step:
        resp = jsonify(error)
        resp.status_code = error["status"]
        return resp

    # Upsample Params.
    valid_upsample_params = {
        "false": False,
        "true": True,
        None: False
    }
    upsample = request.form.get("upsample")
    valid_upsample, out = valid_param_value(upsample, valid_upsample_params)
    if not valid_upsample:
        resp = jsonify(out)
        resp.status_code = error["status"]
        return resp
    upsample = out
    
    # Super Resolution Model Skip Steps Params.
    sr_skip_step = request.form.get(
        "sr_skip_step",
        default_skip_step)
    valid_sr_skip_step, error = is_valid_skip_step(sr_skip_step)
    if not valid_sr_skip_step:
        resp = jsonify(error)
        resp.status_code = error["status"]
        return resp

    try:
        br_commands = [
            "--model_path",
            current_app.config["MYFACE_BASE_PATH"]]

        br_commands.append("--device")
        br_commands.append(current_app.config["DEVICE"])
        if seed:
            br_commands.append("-s")
            br_commands.append(str(seed))
        if sample_alg:
            br_commands.append("--diff_alg")
            br_commands.append(str(sample_alg))

        if sample_alg == "ddim":
            br_commands.append("--ddim_step_size")
            br_commands.append(str(base_skip_step))

        br_commands.append("--label")
        br_commands.append(str(left_eye))
        br_commands.append(str(right_eye))
        br_commands.append(str(mouth))
        br_commands.append(str(showing_teeth))

        if upsample:
            sr_commands = [
                "--model_path",
                current_app.config["MYFACE_SR_PATH"]]

            sr_commands.append("--device")
            sr_commands.append(current_app.config["DEVICE"])

            sr_commands.append("--cold_step_size")
            sr_commands.append(str(sr_skip_step))

            sr_commands.append("--label")
            sr_commands.append(str(left_eye))
            sr_commands.append(str(right_eye))
            sr_commands.append(str(mouth))
            sr_commands.append(str(showing_teeth))
        else:
            sr_commands = None

        # Get Hardware Resource if available to generate image.
        model_resource_ = current_app.config["model_resource"]
        img, ret_status = model_resource_.generate_diffusion(
            cond_img=None,
            br_commands=br_commands,
            sr_commands=sr_commands,
            cond_img_dim=current_app.config["MYFACE_IMG_DIM"],
            log=print)
        
        if ret_status == False:
            # Error No image returned.
            data_dict = {
                "image": None,
                "message": "Server busy, please try again after a few minutes.",
                "status": 503
            }

            resp = jsonify(data_dict)
            resp.status_code = 503
            return resp 
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

@bp.route("/api/celeb_faces", methods=["POST"])
def generate_celeb_faces():
    valid_celeb_param = {
        "false": 0,
        "true": 1,
        "0": 0,
        "1": 1,
        None: 0}
    
    # Bald
    bald = request.form.get("bald")
    status, out = valid_param_value(bald, valid_celeb_param)
    if not status:
        resp = jsonify(out)
        resp.status_code = out["status"]
        return resp
    bald = out

    # Black_Hair
    black_hair = request.form.get("black_hair")
    status, out = valid_param_value(black_hair, valid_celeb_param)
    if not status:
        resp = jsonify(out)
        resp.status_code = out["status"]
        return resp
    black_hair = out

    # Blond_Hair
    blond_hair = request.form.get("blond_hair")
    status, out = valid_param_value(blond_hair, valid_celeb_param)
    if not status:
        resp = jsonify(out)
        resp.status_code = out["status"]
        return resp
    blond_hair = out

    # Brown_Hair
    brown_hair = request.form.get("brown_hair")
    status, out = valid_param_value(brown_hair, valid_celeb_param)
    if not status:
        resp = jsonify(out)
        resp.status_code = out["status"]
        return resp
    brown_hair = out

    # Bushy_Eyebrows
    bushy_eyebrows = request.form.get("bushy_eyebrows")
    status, out = valid_param_value(bushy_eyebrows, valid_celeb_param)
    if not status:
        resp = jsonify(out)
        resp.status_code = out["status"]
        return resp
    bushy_eyebrows = out

    # Eyeglasses
    eyeglasses = request.form.get("eyeglasses")
    status, out = valid_param_value(eyeglasses, valid_celeb_param)
    if not status:
        resp = jsonify(out)
        resp.status_code = out["status"]
        return resp
    eyeglasses = out

    # Goatee
    goatee = request.form.get("goatee")
    status, out = valid_param_value(goatee, valid_celeb_param)
    if not status:
        resp = jsonify(out)
        resp.status_code = out["status"]
        return resp
    goatee = out

    # Gray_Hair
    gray_hair = request.form.get("gray_hair")
    status, out = valid_param_value(gray_hair, valid_celeb_param)
    if not status:
        resp = jsonify(out)
        resp.status_code = out["status"]
        return resp
    gray_hair = out

    # Male
    male = request.form.get("male")
    status, out = valid_param_value(male, valid_celeb_param)
    if not status:
        resp = jsonify(out)
        resp.status_code = out["status"]
        return resp
    male = out

    # Mouth_Slightly_Open
    mouth_open = request.form.get("mouth_open")
    status, out = valid_param_value(mouth_open, valid_celeb_param)
    if not status:
        resp = jsonify(out)
        resp.status_code = out["status"]
        return resp
    mouth_open = out

    # Mustache
    mustache = request.form.get("mustache")
    status, out = valid_param_value(mustache, valid_celeb_param)
    if not status:
        resp = jsonify(out)
        resp.status_code = out["status"]
        return resp
    mustache = out

    # No_Beard
    no_beard = request.form.get("no_beard")
    status, out = valid_param_value(no_beard, valid_celeb_param)
    if not status:
        resp = jsonify(out)
        resp.status_code = out["status"]
        return resp
    no_beard = out

    # Sideburns
    sideburns = request.form.get("sideburns")
    status, out = valid_param_value(sideburns, valid_celeb_param)
    if not status:
        resp = jsonify(out)
        resp.status_code = out["status"]
        return resp
    sideburns = out

    # Smiling
    smiling = request.form.get("smiling")
    status, out = valid_param_value(smiling, valid_celeb_param)
    if not status:
        resp = jsonify(out)
        resp.status_code = out["status"]
        return resp
    smiling = out

    # Straight_Hair
    straight_hair = request.form.get("straight_hair")
    status, out = valid_param_value(straight_hair, valid_celeb_param)
    if not status:
        resp = jsonify(out)
        resp.status_code = out["status"]
        return resp
    straight_hair = out

    # Wavy_Hair
    wavy_hair = request.form.get("wavy_hair")
    status, out = valid_param_value(wavy_hair, valid_celeb_param)
    if not status:
        resp = jsonify(out)
        resp.status_code = out["status"]
        return resp
    wavy_hair = out

    # Wearing_Earrings
    wearing_earrings = request.form.get("wearing_earrings")
    status, out = valid_param_value(wearing_earrings, valid_celeb_param)
    if not status:
        resp = jsonify(out)
        resp.status_code = out["status"]
        return resp
    wearing_earrings = out

    # Wearing_Hat
    wearing_hat = request.form.get("wearing_hat")
    status, out = valid_param_value(wearing_hat, valid_celeb_param)
    if not status:
        resp = jsonify(out)
        resp.status_code = out["status"]
        return resp
    wearing_hat = out

    # Wearing_Lipstick
    wearing_lipstick = request.form.get("wearing_lipstick")
    status, out = valid_param_value(wearing_lipstick, valid_celeb_param)
    if not status:
        resp = jsonify(out)
        resp.status_code = out["status"]
        return resp
    wearing_lipstick = out

    # Wearing_Necklace
    wearing_necklace = request.form.get("wearing_necklace")
    status, out = valid_param_value(wearing_necklace, valid_celeb_param)
    if not status:
        resp = jsonify(out)
        resp.status_code = out["status"]
        return resp
    wearing_necklace = out

    # Wearing_Necktie
    wearing_necktie = request.form.get("wearing_necktie")
    status, out = valid_param_value(wearing_necktie, valid_celeb_param)
    if not status:
        resp = jsonify(out)
        resp.status_code = out["status"]
        return resp
    wearing_necktie = out

    # Seed Params.
    seed = request.form.get("seed")
    valid_seed, error = is_valid_seed(seed)
    if not valid_seed:
        resp = jsonify(error)
        resp.status_code = error["status"]
        return resp

    # Diffusion Sample Algorithms Params.
    sample_alg = request.form.get("sample_alg", "ddpm")
    valid_sample_alg, error = is_valid_sample_alg(
        sample_alg,
        current_app.config["ALLOWED_SAMPLING_ALG"]) 
    if not valid_sample_alg:
        resp = jsonify(error)
        resp.status_code = error["status"]
        return resp
    
    # Base Model Skip Steps Params.
    default_skip_step = current_app.config["DEFAULT_SKIP_STEP"]
    base_skip_step = request.form.get(
        "base_skip_step",
        default_skip_step)
    valid_base_skip_step, error = is_valid_skip_step(base_skip_step)
    if not valid_base_skip_step:
        resp = jsonify(error)
        resp.status_code = error["status"]
        return resp
    
    try:
        br_commands = [
            "--model_path",
            current_app.config["CELEBFACE_BASE_PATH"]]

        br_commands.append("--device")
        br_commands.append(current_app.config["DEVICE"])
        if seed:
            br_commands.append("-s")
            br_commands.append(str(seed))
        if sample_alg:
            br_commands.append("--diff_alg")
            br_commands.append(sample_alg)

        if sample_alg == "ddim":
            br_commands.append("--ddim_step_size")
            br_commands.append(str(base_skip_step))

        br_commands.append("--label")
        br_commands.append(str(bald))
        br_commands.append(str(black_hair))
        br_commands.append(str(blond_hair))
        br_commands.append(str(brown_hair))
        br_commands.append(str(bushy_eyebrows))
        br_commands.append(str(eyeglasses))
        br_commands.append(str(goatee))
        br_commands.append(str(gray_hair))
        br_commands.append(str(male))
        br_commands.append(str(mouth_open))
        br_commands.append(str(mustache))
        br_commands.append(str(no_beard))
        br_commands.append(str(sideburns))
        br_commands.append(str(smiling))
        br_commands.append(str(straight_hair))
        br_commands.append(str(wavy_hair))
        br_commands.append(str(wearing_earrings))
        br_commands.append(str(wearing_hat))
        br_commands.append(str(wearing_lipstick))
        br_commands.append(str(wearing_necklace))
        br_commands.append(str(wearing_necktie))

        # No Super-Resolution.
        sr_commands = None

        model_resource_ = current_app.config["model_resource"]
        img, ret_status = model_resource_.generate_diffusion(
            cond_img=None,
            br_commands=br_commands,
            sr_commands=sr_commands,
            cond_img_dim=current_app.config["CELEBFACE_IMG_DIM"],
            log=print)
        
        if ret_status == False:
            # Error No image passed.
            data_dict = {
                "image": None,
                "message": "Server busy, please try again after a few minutes.",
                "status": 503
            }

            resp = jsonify(data_dict)
            resp.status_code = 503
            return resp 
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

@bp.route("/api/anime_portraits", methods=["POST"])
def generate_anime_portraits():
    valid_params = {}
    for centroid in range(75):
        valid_params[str(centroid)] = centroid
    
    centroids_index = request.form.get("centroids_index", "0")
    status, out = valid_param_value(centroids_index, valid_params)
    if not status :
        resp = jsonify(out)
        resp.status_code = out["status"]
        return resp

    centroids_index = out
    centroids_labels = [0] * 75
    centroids_labels[centroids_index] = 1
    centroids_labels = [str(x) for x in centroids_labels]

    # Seed Params.
    seed = request.form.get("seed")
    valid_seed, error = is_valid_seed(seed)
    if not valid_seed:
        resp = jsonify(error)
        resp.status_code = error["status"]
        return resp

    # Diffusion Sample Algorithms Params.
    sample_alg = request.form.get("sample_alg", "ddpm")
    valid_sample_alg, error = is_valid_sample_alg(
        sample_alg,
        current_app.config["ALLOWED_SAMPLING_ALG"]) 
    if not valid_sample_alg:
        resp = jsonify(error)
        resp.status_code = error["status"]
        return resp
    
    # Base Model Skip Steps Params.
    default_skip_step = current_app.config["DEFAULT_SKIP_STEP"]
    base_skip_step = request.form.get(
        "base_skip_step",
        default_skip_step)
    valid_base_skip_step, error = is_valid_skip_step(base_skip_step)
    if not valid_base_skip_step:
        resp = jsonify(error)
        resp.status_code = error["status"]
        return resp

    # Upsample Params.
    valid_upsample_params = {
        "false": False,
        "true": True,
        None: False
    }
    upsample = request.form.get("upsample")
    valid_upsample, out = valid_param_value(upsample, valid_upsample_params)
    if not valid_upsample:
        resp = jsonify(out)
        resp.status_code = error["status"]
        return resp
    upsample = out
    
    # Super Resolution Model Skip Steps Params.
    sr_skip_step = request.form.get(
        "sr_skip_step",
        default_skip_step)
    valid_sr_skip_step, error = is_valid_skip_step(sr_skip_step)
    if not valid_sr_skip_step:
        resp = jsonify(error)
        resp.status_code = error["status"]
        return resp

    try:
        # Base Resolution Parameters.
        br_commands = [
            "--model_path",
            current_app.config["ANIMEPORTRAITS_BASE_PATH"]]
    
        br_commands.append("--device")
        br_commands.append(current_app.config["DEVICE"])
        if seed:
            br_commands.append("-s")
            br_commands.append(str(seed))

        br_commands.append("--diff_alg")
        br_commands.append(sample_alg)
        
        if sample_alg == "ddim":
            br_commands.append("--ddim_step_size")
            br_commands.append(str(base_skip_step))
        
        br_commands.append("--label")
        br_commands.extend(centroids_labels)
        
        if upsample:
            # Super Resolution Parameters.
            sr_commands = [
                "--model_path",
                current_app.config["ANIMEPORTRAITS_SR_PATH"]]

            sr_commands.append("--device")
            sr_commands.append(current_app.config["DEVICE"])

            sr_commands.append("--cold_step_size")
            sr_commands.append(str(sr_skip_step))

            sr_commands.append("--label")
            sr_commands.extend(centroids_labels)
        else:
            sr_commands = None

        # Get Hardware Resource if available to generate image.
        model_resource_ = current_app.config["model_resource"]
        img, ret_status = model_resource_.generate_diffusion(
            cond_img=None,
            br_commands=br_commands,
            sr_commands=sr_commands,
            cond_img_dim=current_app.config["ANIMEPORTRAITS_IMG_DIM"],
            log=print)
        
        if ret_status == False:
            # Error No image returned.
            data_dict = {
                "image": None,
                "message": "Server busy, please try again after a few minutes.",
                "status": 503
            }

            resp = jsonify(data_dict)
            resp.status_code = 503
            return resp
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
