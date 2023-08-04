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
