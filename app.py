
import os
from database import Database

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, PositiveFloat

app = FastAPI()


# ************************** GET Client **************************

@app.get("/clients/")
async def list_clients():
    """
    Liste les clients de la banque.
    """
    # Récupère les clients de la base
    db = Database()
    db_clients = db.clients

    # Retourne une liste formatée
    api_response = []
    for client_id, client_dict in db_clients.items():
        api_response.append({
            'id': client_id,
            **client_dict
        })
    return api_response


@app.get("/clients/{client_id}")
async def get_client(client_id: str):
    """
    Récupère un client de la banque
    en fonction de son identifiant.
    """
    # Récupère le client de la base
    db = Database()
    db_client = db.get_client(client_id)

    # Retourne la réponse formatée
    return {
        'id': client_id,
        'name': db_client['name'],
        'first_name': db_client['first_name']
    }


# ************************** CREATE/UPDATE/DELETE Client **************************

class Client(BaseModel):
    name: str
    first_name: str


@app.post("/clients/")
async def create_client(client: Client):
    """
    Créer un nouveau client.
    """
    # Récupère les clients de la base
    db = Database()
    db_clients = db.clients

    # Trouve un nouvel identifiant
    client_id = str(int(max(db_clients.keys(), default=0)) + 1)
    # Ajoute le client à la base
    db_clients[client_id] = {
        'name': client.name,
        'first_name': client.first_name,
        'accounts': {}
    }

    # Sauvegarde la base
    db.save()

    return client


@app.put("/clients/{client_id}")
async def update_client(client_id: str, client: Client):
    """
    Met à jour un client.
    """
    # Récupère le client de la base
    db = Database()
    db_client = db.get_client(client_id)

    # Met à jour le client
    db_client.update(client)

    # Sauvegarde la base
    db.save()

    return client


@app.delete("/clients/{client_id}")
async def delete_client(client_id: str):
    """
    Met à jour un client.
    """
    # Vérifie que le client éxiste
    db = Database()
    db.get_client(client_id)

    # Supprime le client
    del db.clients[client_id]

    # Sauvegarde la base
    db.save()


# ************************** GET Client accounts **************************


@app.get("/clients/{client_id}/accounts")
async def get_client_accounts(client_id: str):
    """
    Met à jour un client.
    """
    # Récupère le client de la base
    db = Database()
    db_client = db.get_client(client_id)

    # Retourne une liste formatée
    api_response = []
    for account_id, account_dict in db_client['accounts'].items():
        api_response.append({
            'id': account_id,
            **account_dict
        })
    return api_response


@app.get("/clients/{client_id}/accounts/{account_id}")
async def get_client_account(client_id: str, account_id: str):
    """
    Met à jour un client.
    """
    # Récupère le compte client de la base
    db = Database()
    db_account = db.get_account(client_id, account_id)

    # Retourne la réponse formatée
    return {
        'id': account_id,
        'balance': db_account['balance']
    }


# ************************** CREATE/DELETE Client accounts **************************


@app.post("/clients/{client_id}/accounts")
async def create_client_account(client_id: str):
    """
    Met à jour un client.
    """
    # Récupère le client de la base
    db = Database()
    db_client = db.get_client(client_id)
    db_client_accounts = db_client['accounts']

    # Trouve un nouvel identifiant
    account_id = str(int(max(db_client_accounts.keys(), default=0)) + 1)
    # Ajoute le client à la base
    db_client_accounts[account_id] = {'balance': 0}

    # Sauvegarde la base
    db.save()

    # Retourne la réponse formatée
    return {
        'id': account_id,
        **db_client_accounts[account_id]
    }


@app.delete("/clients/{client_id}/account/{account_id}")
async def delete_account(client_id: str, account_id: str):
    """
    Met à jour un client.
    """
    # Vérifie que le compte client existe
    db = Database()
    db.get_account(client_id, account_id)

    # Supprime le compte
    db_client = db.get_client(client_id)
    del db_client['accounts'][account_id]

    # Sauvegarde la base
    db.save()


# ************************** Client accounts OPERATIONS **************************

class Transaction(BaseModel):
    amount: PositiveFloat


@app.post("/clients/{client_id}/accounts/{account_id}/withdrawal")
async def account_withdrawal(client_id: str, account_id: str, transaction: Transaction):
    """
    Fait un retrait sur le compte d'un client.
    """
    # Récupère le compte client de la base
    db = Database()
    db_account = db.get_account(client_id, account_id)

    # Vérifie si le client peut retirer cette somme
    if db_account['balance'] - transaction.amount < 0:
        raise HTTPException(
            status_code=403,
            detail="Operation forbidden : negative balance."
        )

    # Met à jour le compte
    db_account['balance'] -= transaction.amount

    # Sauvegarde la base
    db.save()

    # Retourne la réponse formatée
    return {
        'id': account_id,
        **db_account
    }


@app.post("/clients/{client_id}/accounts/{account_id}/deposit")
async def account_deposit(client_id: str, account_id: str, transaction: Transaction):
    """
    Fait un retrait sur le compte d'un client.
    """
    # Récupère le compte client de la base
    db = Database()
    db_account = db.get_account(client_id, account_id)

    # Met à jour le compte
    db_account['balance'] += transaction.amount

    # Sauvegarde la base
    db.save()

    # Retourne la réponse formatée
    return {
        'id': account_id,
        **db_account
    }
