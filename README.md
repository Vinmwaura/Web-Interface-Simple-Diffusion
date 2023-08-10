# Web-Interface-Simple-Diffusion
A Simple web app for interacting with some custom simple diffusion models trained on various datasets.

## Requirements
To be able to run the code you require anaconda on your machine and create an environment and install dependencies from requirements.txt file by running the following commands:
```
conda create --name diffusion_env --file requirements.txt
```
To activate the conda environment run:
```
conda activate diffusion_env
```
You will then need to clone the project: https://github.com/Vinmwaura/Simple-Diffusion-Model into the folder: diffusion_apps/diffusion_lib folder.

In addition to the above you will need to download the models/weights [here](https://huggingface.co/VinML/Simple_Diffusion_Models) and perform the following steps to configure the web app to use them:
+ Extract the compressed files in the folder of your choice.
+ You can either:
  - Move the files(*.pt, .json) into the folder: diffusion_apps/models
  - Open the .env file and edit the respective variable names to the path of the json file.

### Configuring .env file
The web app requires the following .env variables to function, create a .env file in the root of the project directory, copy the variables and edit accordingly:
```
SECRET_KEY=<Secrey key, not to be shared>
FLASK_ENV=production
FLASK_DEBUG=False
BODY_POSE_BASE_PATH="<External path to my_body_pose_128.json>"
BODY_POSE_SR_PATH="/<External path to my_body_pose_SR:128-256.json>"
MYFACE_BASE_PATH="<External path to my_face_128.json>"
MYFACE_SR_PATH="<External path to my_face_SR:128-256.json>"
CELEBFACE_BASE_PATH="<External path to celeb_faces_128.json>"
ANIMEPORTRAIT_BASE_PATH="<External path to anime_portraits:128.json>"
ANIMEPORTRAIT_SR_PATH="<External path to anime_portraits_SR:128-256.json>"
```

One way to generate the secret key is to run the command below and add to SECRET_KEY variable:
```
python -c 'import secrets; print(secrets.token_hex())'
```

### Running web app
If configured properly, to run the webapp on your machine:
+ Ensure the run_interface.sh file is executable (Not to be executed everytime):
```
chmod +x run_interface.sh
```
+ To execute the webapp:
```
./run_interface.sh
```

## Interfaces
### My_Body_Pose Tab
https://github.com/Vinmwaura/Web-Interface-Simple-Diffusion/assets/12788331/3803e445-f453-495b-8e47-9c7c51287cfc

### My_Face Tab
https://github.com/Vinmwaura/Web-Interface-Simple-Diffusion/assets/12788331/576dbe0c-5ca9-4ec7-a05c-3764843d80bd

### Celebrity_Face Tab
https://github.com/Vinmwaura/Web-Interface-Simple-Diffusion/assets/12788331/c58d7332-820b-4b99-afe4-c58773184728

### Anime_Portraits Tab
https://github.com/Vinmwaura/Web-Interface-Simple-Diffusion/assets/12788331/8a1ae69d-d325-411d-b0f9-6d051369abfd
