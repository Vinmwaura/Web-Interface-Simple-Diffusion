import base64

import cv2
import numpy as np


# Converts image format from tensor: [C,H,W] to numpy: [H,W,C]
def convert_tensor_to_numpy(img_tensor):
    # Converts image format from [C,H,W] to [H,W,C]
    img_tensor = img_tensor.permute(0, 2, 3, 1)
    
    # Converts image range from [-1, 1] to [0, 255]
    img_tensor = ((img_tensor + 1) / 2) * 255

    # Assumes only one image was generated.
    # Removes first dimension at the begining: [C,H,W]
    img_tensor = img_tensor.squeeze(0)

    img_numpy = img_tensor.cpu().numpy()

    return img_numpy

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
