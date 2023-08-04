import cv2

from threading import Semaphore

import torch

# Diffusion Function.
from generate_images_diffusion import generate_images_diffusion as diffusion_sampling
from generate_sr_images_diffusion import generate_sr_images_diffusion as diffusion_upsampling_sampling

from diffusion_apps.utils import convert_tensor_to_numpy


class ModelResource:
    def __init__(self):
        # Ensures only one thread from API request can use the
        # resource(CPU / CUDA) to generate an image.
        self.semaphore = Semaphore()

    def generate_diffusion(
            self,
            cond_img,
            br_commands,
            sr_commands,
            cond_img_dim=128,
            log=print):
        # TODO: Implement a Queue to handle waiting requests that can return updates.
        if self.semaphore.acquire(blocking=False):
            try:
                # Generates Low Resolution Image using Diffusion Model.
                if cond_img is not None:
                    cond_img_dim_shape = (
                        cond_img_dim,
                        cond_img_dim)
                    cond_img = cv2.resize(
                        cond_img,
                        cond_img_dim_shape,
                        interpolation=cv2.INTER_AREA)
                else:
                    cond_img = None

                img_tensor = diffusion_sampling(
                    raw_args=br_commands,
                    log=log,
                    cond_img=cond_img,
                    save_locally=False)
                
                # Converts tensor output to numpy.
                img_numpy = convert_tensor_to_numpy(img_tensor)

                # Generates Super Resolution Image using Diffusion Model if toggled.
                if sr_commands:
                    img_tensor = diffusion_upsampling_sampling(
                        raw_args=sr_commands,
                        lr_img=img_numpy,
                        log=log,
                        save_locally=False)
                    
                    # Converts tensor output to numpy.
                    img_numpy = convert_tensor_to_numpy(img_tensor)
            except Exception as e:
                log(f"An error occured while generating Super Res Image: {e}")
                img_numpy = None
            finally:
                torch.cuda.empty_cache()
                self.semaphore.release()
                ret_status = img_numpy is not None
                return img_numpy, ret_status
        else:
            return None, False
