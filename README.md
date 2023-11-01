# Web-Interface-Simple-Diffusion
A Simple web app for interacting with some custom simple diffusion models trained on various datasets.

## Requirements
+ Python 3

## Setup
1. Install [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)
2. Create a virtual environment:
```
mkvirtualenv web_interface_diffusion
```
3. To activate the virtualenv:
```
workon web_interface_diffusion
```
4. Install the python libraries for the webapp:
```
pip install -r requirements.txt
```
5. Clone the project: https://github.com/Vinmwaura/Simple-Diffusion-Model on your machine.
6. Install the libraries from the cloned project above by running the script **install_cpu_requirements.sh**, make sure web_interface_diffusion is active.
7. Download the models weights [here](https://huggingface.co/VinML/Custom-Simple-Diffusion-Model) and perform the following steps to configure the web app to use them:
+ Extract the compressed folders into a folder of your choice.
+ Open the **.env** file and edit the respective variable names to the path of the json file as shown in the section below.

### Configuring .env file
The web app requires the following .env variables to function, create a .env file in the root of the project directory, copy the variables and edit accordingly:
```
SECRET_KEY=<Secrey key, not to be shared>
FLASK_ENV=production
FLASK_DEBUG=False
DIFFUSION_LIB_PATH="<Directory path to Simple-Diffusion-Model project, where generate_* scripts are located>"
BODY_POSE_BASE_PATH="<External path to MyBodyPose config json>"
BODY_POSE_SR_PATH="/<External path to MyBodyPose_SR config json>"
MYFACE_BASE_PATH="<External path to MyFace config json>"
MYFACE_SR_PATH="<External path to MyFace_SR config json>"
CELEBFACE_BASE_PATH="<External path to CelebFaces config json>"
ANIMEPORTRAIT_BASE_PATH="<External path to AnimePortraits config json>"
ANIMEPORTRAIT_SR_PATH="<External path to AnimePortraits_SR config json>"
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
+ To run the webapp:
```
sh run_interface.sh
```

## Interfaces Examples
### My_Body_Pose Tab
![Body_Pose](./assets/BodyPoses.mp4)

### My_Face Tab
![Face](./assets/Face.mp4)

### Celebrity_Face Tab
![Celebrity_Faces](./assets/Celeb_Face.mp4)

### Anime_Portraits Tab
![Anime_Portraits](./assets/Anime_Portraits.mp4)
