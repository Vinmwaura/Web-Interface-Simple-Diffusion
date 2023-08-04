
import os
import sys

# TODO: Decouple module from Web-App and make api endpoint to be able to run as a service.
# Change to match name of folder if needed.
module_name = "simple_diffusion"

dir_path = os.path.dirname(os.path.abspath(__file__))
diff_lib_path = os.path.join(
    dir_path,
    "diffusion_lib",
    module_name)

if os.path.isdir(diff_lib_path):
    sys.path.append(diff_lib_path)
