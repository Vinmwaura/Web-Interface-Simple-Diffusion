import os
import imghdr

from werkzeug.utils import secure_filename

def valid_param_value(param, param_dict):
    try:
        out = param_dict[param]
        return True, out
    except KeyError:
        # Error Invalid base skip value.
        data_dict = {
            "image": None,
            "message": "Invalid Param value.",
            "status": 400
        }
        return False, data_dict

# Validates Image uploaded.
def validate_image_extension(stream):
    header = stream.read(512) # Header check.
    stream.seek(0) # Reset stream pointer.
    format = imghdr.what(None, header)
    if not format:
        return False
    return "." + (format if format != "jpeg" else "jpg")

def validate_canvas_image(canvas_image, valid_img_extensions):
    canvas_filename = secure_filename(canvas_image.filename)
    if canvas_filename != "":
        file_ext = os.path.splitext(canvas_filename)[1]
        if file_ext not in valid_img_extensions or \
            file_ext != validate_image_extension(canvas_image.stream):

            # Error Invalid Image.
            data_dict = {
                "image": None,
                "message": "Invalid Image passed.",
                "status": 400
            }
            return False, data_dict
        else:
            return True, None
    else:
        # Error No image passed.
        data_dict = {
            "image": None,
            "message": "No Image passed.",
            "status": 400
        }
        return False, data_dict

def is_valid_int(int_repr):
    if type(int_repr) == str:
        valid = int_repr.isnumeric()
    else:
        valid = (type(int_repr) == int)
    return valid

def is_valid_seed(seed, default_val=None):
    seed = default_val if seed == "" else seed

    # Check if seed is valid.
    if seed is not None and not is_valid_int(seed):
        # Error Invalid seed value.
        data_dict = {
            "image": None,
            "message": "Invalid seed value.",
            "status": 400
        }

        return False, data_dict

    return True, None

def is_valid_sample_alg(sample_alg, list_sample_alg):
    if sample_alg not in list_sample_alg:
        # Invalid Sampling Algorithm.
        data_dict = {
            "image": None,
            "message": "Invalid Sampling Algorithm parameter passed.",
            "status": 400
        }
        return False, data_dict
    return True, None

def is_valid_skip_step(skip_step):
    if not is_valid_int(skip_step):
        # Error Invalid skip value.
        data_dict = {
            "image": None,
            "message": "Invalid Skip Step value.",
            "status": 400
        }
        return False, data_dict
    return True, None
