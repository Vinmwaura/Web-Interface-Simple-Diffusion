import os
import sys

from dotenv import load_dotenv

# Loads .env variables if any.
env_file = ".env"
env = os.path.join(os.getcwd(), env_file)
if os.path.exists(env):
    load_dotenv(env)

"""
TODO: Decouple module from Web-Interface module and make API endpoints to be
able to run as a separate service.
"""
DIFFUSION_LIB_PATH = os.environ.get("DIFFUSION_LIB_PATH")
sys.path.append(DIFFUSION_LIB_PATH)
