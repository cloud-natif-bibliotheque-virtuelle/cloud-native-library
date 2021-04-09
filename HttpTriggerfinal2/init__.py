import logging
import azure.functions as func
import mysql.connector
import os
import json
from jinja2 import Template


config_sql = {
  'host': os.environ['hostlibrary'],
  'user': os.environ['userlibrary'],
  'password': os.environ['passwordlibrary'],
  'database': os.environ['library'],
  'client_flags': [mysql.connector.ClientFlag.SSL],
  'ssl_ca': os.environ['sslibrary']
}


def infoslivre(name):
    """ Cette fonction permet de récupérer les colonnes
        titre, infos, url_blob et nombre_mot 
        dans la base de données.
    """
    logging.debug("Connexion à la base de données")
    conn = mysql.connector.connect(**config_sql)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM liste_livres WHERE titre = %s;
    """, (name,))
    logging.info("Connexion ok") 
    rows = cursor.fetchone()
    rows = list(rows)
    logging.debug(f"Infos livre {rows}")
    return rows


def affichage(name):
    """ Cette fonction permet de faire la liaison avec
        le document index2.html et de générer une page 
        HTML.
    """
    logging.info('affichage du html d"un livre')
    with open('index2.html') as file_:
        template = Template(file_.read())
    logging.info('connexion index2.html')
    result = template.render(rows=infoslivre(name))
    return result


def main(req: func.HttpRequest) -> func.HttpResponse:
    """ Liens de direction vers infos du livre.
    """

    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(affichage(name), status_code=200, mimetype="text/html")
    else:
        return func.HttpResponse(
            "This HTTP triggered function executed successfully.\
            Pass a name in the query\
            string or in the request body for a personalized response.",
            status_code=200
        )