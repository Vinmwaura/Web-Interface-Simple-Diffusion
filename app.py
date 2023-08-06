import os

from flask import Flask

from config import Config

from diffusion_apps.model_resource import ModelResource

def create_app(config_class=Config):
    template_dir = os.path.abspath("./apps/templates")
    static_dir = os.path.abspath("./apps/static")
    app = Flask(
        __name__,
        template_folder=template_dir,
        static_folder=static_dir)
    app.config.from_object(config_class)

    # Used to limit access to resources such as CPU/CUDA by models.
    model_resource_obj = ModelResource()
    app.config["model_resource"] = model_resource_obj

    # Secure File Uploads.
    app.config["MAX_CONTENT_LENGTH"] = 1_024 * 1_024
    app.config["UPLOAD_EXTENSIONS"] = [".png", ".jpg"]

    # Supported Sampling Algorithms.
    app.config["ALLOWED_SAMPLING_ALG"] = ["ddim", "ddpm"]
    app.config["DEFAULT_SKIP_STEP"] = 100

    # Initialize Flask extensions here.

    # Blueprints.
    from apps.interface import bp as interface_bp
    app.register_blueprint(interface_bp, url_prefix='/')

    return app
