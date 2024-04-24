# SSI_shared_database
This repository contains the code for the shared database construction relating to my Bachelors



# Virtual environment
created a virtual environment using ANACONDA
create: conda create -n pilotenv
activate: conda activate pilotenv
deactivate: conda deactivate

# installing dependencies/requirements
pip install -r requirements.txt

# running main API (DB to Interface)
uvicorn API_DB_to_Interface:app (remember to check port)