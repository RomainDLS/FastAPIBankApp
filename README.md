# Bank API (with python FastAPI)
Project used for python formation. This project provite a simple banking application with the following features :
* Manage clients (crud)
* Manage accounts (crud)
* Do operations on accounts : withdrawal & deposit
* Record and show transactions



# Developer Documentation

## Install
This project can run on linux. Python 3 must be installed :

#### Run in shell :
```bash
# Clone project
mkdir fast_api_bank
git clone git@github.com:RomainDLS/FastAPIBankApp.git fast_api_bank

# Install requirements
cd fast_api_bank
pip install -r requirements.txt
```

## Run server
```bash
uvicorn app:app --reload
```
API url : http://127.0.0.1:8000/  
Swagger doc : http://127.0.0.1:8000/docs

# Update this project

Update main branch and then merge main in `part_1`, `part_2`, `part_3`. Command to update all branchs from main :
```
git checkout main
git pull
git checkout part_1 && git merge main && git push
git checkout part_2 && git merge main && git push
git checkout part_3 && git merge main && git push
```