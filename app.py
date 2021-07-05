
import os
from datetime import datetime

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, PositiveFloat

from database import Database

app = FastAPI()


# ************************** GET Client **************************

@app.get("/clients/")
async def list_clients():
    """
    Liste les clients de la banque.
    """
    # Récupère les clients de la base
    db = Database()
    db_clients = db.get_clients()

    # Retourne une liste formatée
    api_response = []
    for client_id, client_dict in db_clients.items():
        api_response.append({
            'id': client_id,
            'name': client_dict['name'],
            'first_name': client_dict['first_name'],
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
    db_clients = db.get_clients()

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
    # TODO:
    # Récupère le client de la base
    # Met à jour le client
    # Sauvegarde la base


@app.delete("/clients/{client_id}")
async def delete_client(client_id: str):
    """
    Supprime un client.
    """
    # TODO:
    # Vérifie que le client éxiste
    # Supprime le client
    # Sauvegarde la base
