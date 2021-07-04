# Bank API (with python FastAPI)
Project used for python formation. This project provite a simple banking application with the following features :
* Manage clients (crud)
* Manage accounts (crud + operations : withdrawal & deposit)



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