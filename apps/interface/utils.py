import base64

import cv2
import numpy as np

# Converts numpy images to base64.
def convert_numpy_to_base64(img_numpy):
    _, im_arr = cv2.imencode('.png', img_numpy)  # im_arr: image in Numpy one-dim array format.
    im_bytes = im_arr.tobytes()
    im_b64 = base64.b64encode(im_bytes)
    encoded_string_decoded = im_b64.decode("UTF-8")
    return encoded_string_decoded

# Converts binary images to numpy images.
def convert_binary_to_numpy(bin_image):
    # Convert string data to numpy array
    file_bytes = np.fromstring(
        bin_image.read(),
        np.uint8)

    # Convert to numpy image.
    cond_img = cv2.imdecode(
        file_bytes,
        cv2.IMREAD_UNCHANGED)

    # Hack to remove alpha channel.
    cond_img = cond_img[:, :, :3]

    return cond_img
