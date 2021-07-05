
import os
import json
from pydantic import BaseModel
from fastapi import HTTPException


# Pour les besoins de la formation nous sauvegarderons les données
# de cette application dans un fichier json.
# En temps normal il faudrait se servir d'une véritable base de données (SQL) :
# https://fastapi.tiangolo.com/tutorial/sql-databases/


# A chaque fois qu'on voudra faire une opération sur les données, il faudra :
# - Télécharger le contenu du fichier json dans une variable python : `db_dict = get_db()`
# - Faire les opérations sur cette variable : `db_dict`
# - Sauvegarder le contenu de la varaible `db_dict` dans le fichier json : `save_db(db_dict)`


DB_FILENAME = 'db.json'


class Database:

    """
    Le schéma du dictionnaire de la base de donnée est le suivant :
    {
        "clients": {
            <client_id>: {
                "name": <name>,
                "first_name": <first_name>,
                "accounts": {
                    <account_id>: {
                        "balance": <balance>,
                        "transactions": [
                            {
                                "label": <label>,
                                "value": <value>,
                                "type": <withdrawal|deposit>,
                                "date": <date>
                            }
                        ]
                    }
                }
            }
        }
    }
    """

    def __init__(self):
        self._db = self.download()

    def download(self):
        """
        Télécharge la base de donnée du fichier json.
        retourne le contenu du json dans un dict.
        Créer le fichier s'il n'éxiste pas.
        """
        if not os.path.isfile(DB_FILENAME):
            json_file = open(DB_FILENAME, 'w')
            json.dump({"clients": {}}, json_file)

        with open(DB_FILENAME, 'r') as json_file:
            return json.load(json_file)

    def save(self):
        """
        Sauvegarde db_dict dans le ficher json.
        """
        json_dict = json.dumps(self._db, indent=2)
        with open(DB_FILENAME, 'w') as json_file:
            json_file.write(json_dict)

    def get_clients(self):
        return self._db['clients']

    def get_client(self, client_id):
        """
        Récupère un client.
        """
        try:
            return self.get_clients()[client_id]
        except KeyError:
            raise HTTPException(status_code=404, detail="Client not found")

    def get_account(self, client_id, account_id):
        """
        Récupère un compte client.
        """
        client = self.get_client(client_id)
        accounts = client.setdefault('accounts', {})

        try:
            return accounts[account_id]
        except KeyError:
            raise HTTPException(status_code=404, detail="Account not found")
