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

@bp.route("/api/myposes", methods=["POST"])
def generate_body_poses():
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

@bp.route("/api/myface", methods=["POST"])
def generate_myface():
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

@bp.route("/api/celeb_faces", methods=["POST"])
def generate_celeb_faces():
    # Bald,
    bald = request.form.get("bald", False)
    bald = "-1" if bald == "false" else "1"
    
    # Black_Hair
    black_hair = request.form.get("black_hair", False)
    black_hair = "-1" if black_hair == "false" else "1"

    # Blond_Hair
    blond_hair = request.form.get("blond_hair", False)
    blond_hair = "-1" if blond_hair == "false" else "1"

    # Brown_Hair
    brown_hair = request.form.get("brown_hair", False)
    brown_hair = "-1" if brown_hair == "false" else "1"

    # Bushy_Eyebrows
    bushy_eyebrows = request.form.get("bushy_eyebrows", False)
    bushy_eyebrows = "-1" if bushy_eyebrows == "false" else "1"

    # Eyeglasses
    eyeglasses = request.form.get("eyeglasses", False)
    eyeglasses = "-1" if eyeglasses == "false" else "1"

    # Goatee
    goatee = request.form.get("goatee", False)
    goatee = "-1" if goatee == "false" else "1"

    # Gray_Hair
    gray_hair = request.form.get("gray_hair", False)
    gray_hair = "-1" if gray_hair == "false" else "1"

    # Male
    male = request.form.get("male", False)
    male = "-1" if male == "false" else "1"

    # Mouth_Slightly_Open
    mouth_open = request.form.get("mouth_open", False)
    mouth_open = "-1" if mouth_open == "false" else "1"

    # Mustache
    mustache = request.form.get("mustache", False)
    mustache = "-1" if mustache == "false" else "1"

    # No_Beard
    no_beard = request.form.get("no_beard", False)
    no_beard = "-1" if no_beard == "false" else "1"

    # Sideburns
    sideburns = request.form.get("sideburns", False)
    sideburns = "-1" if sideburns == "false" else "1"

    # Smiling
    smiling = request.form.get("smiling", False)
    smiling = "-1" if smiling == "false" else "1"

    # Straight_Hair
    straight_hair = request.form.get("straight_hair", False)
    straight_hair = "-1" if straight_hair == "false" else "1"

    # Wavy_Hair
    wavy_hair = request.form.get("wavy_hair", False)
    wavy_hair = "-1" if wavy_hair == "false" else "1"

    # Wearing_Earrings
    wearing_earrings = request.form.get("wearing_earrings", False)
    wearing_earrings = "-1" if wearing_earrings == "false" else "1"

    # Wearing_Hat
    wearing_hat = request.form.get("wearing_hat", False)
    wearing_hat = "-1" if wearing_hat == "false" else "1"

    # Wearing_Lipstick
    wearing_lipstick = request.form.get("wearing_lipstick", False)
    wearing_lipstick = "-1" if wearing_lipstick == "false" else "1"

    # Wearing_Necklace
    wearing_necklace = request.form.get("wearing_necklace", False)
    wearing_necklace = "-1" if wearing_necklace == "false" else "1"

    # Wearing_Necktie
    wearing_necktie = request.form.get("wearing_necktie", False)
    wearing_necktie = "-1" if wearing_necktie == "false" else "1"

    # Conditional Information for Base Diffusion.
    seed = request.form.get("seed", None)
    if not seed:
        seed = None

    sample_alg = request.form.get("sample_alg", "ddpm")

    base_skip_step = request.form.get("base_skip_step", 100)
    if not base_skip_step:
        base_skip_step = None

    try:
        commands = ["--model_path", current_app.config["CELEBFACE_BASE_PATH"]]

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
        commands.append(bald)
        commands.append(black_hair)
        commands.append(blond_hair)
        commands.append(brown_hair)
        commands.append(bushy_eyebrows)
        commands.append(eyeglasses)
        commands.append(goatee)
        commands.append(gray_hair)
        commands.append(male)
        commands.append(mouth_open)
        commands.append(mustache)
        commands.append(no_beard)
        commands.append(sideburns)
        commands.append(smiling)
        commands.append(straight_hair)
        commands.append(wavy_hair)
        commands.append(wearing_earrings)
        commands.append(wearing_hat)
        commands.append(wearing_lipstick)
        commands.append(wearing_necklace)
        commands.append(wearing_necktie)

        img = generate_base_diffusion(commands=commands)
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
    # Centroids Index.
    centroids_index = request.form.get("centroids_index", 0)
    centroids_index = int(centroids_index)

    centroids_labels = [0] * 75
    centroids_labels[centroids_index] = 1
    centroids_labels = [str(x) for x in centroids_labels]

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
        commands = ["--model_path", current_app.config["ANIMEPORTRAITS_BASE_PATH"]]

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
        commands.extend(centroids_labels)

        img = generate_base_diffusion(commands=commands)

        if upsample:
            upsample_commands = ["--model_path", current_app.config["ANIMEPORTRAITS_SR_PATH"]]

            upsample_commands.append("--device")
            upsample_commands.append(current_app.config["DEVICE"])

            upsample_commands.append("--cold_step_size")
            upsample_commands.append(sr_skip_step)

            upsample_commands.append("--label")
            upsample_commands.extend(centroids_labels)

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
