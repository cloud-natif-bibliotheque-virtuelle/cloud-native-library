import logging
import mysql.connector
import azure.functions as func
import os
from jinja2 import Template


config = {
  'host': os.environ['hostlibrary'],
  'user': os.environ['userlibrary'],
  'password': os.environ['passwordlibrary'],
  'database': 'library',
  'client_flags': [mysql.connector.ClientFlag.SSL],
  'ssl_ca': os.environ['sslibrary']
}


def listelivre():
    """ Cette fonction permet de se connecter à la base de
        données et de récupérer la colonne livre.
    """
    logging.debug("connexion à la base de donnée")
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT titre FROM liste_livres
    """)
    logging.info("la connexion OK")
    rows = cursor.fetchall()
    liste_rows = []
    for row in rows :
        liste_rows += row
    logging.debug(f"liste livre {liste_rows}")
    return liste_rows


def main(req: func.HttpRequest) -> func.HttpResponse:
    """ Cette fonction permet de faire la liaison avec
        le document index.html et de générer une page
        HTML.
    """
    logging.info('Python HTTP trigger function processed a request.')
    with open('index.html') as file_:
        template = Template(file_.read())
    logging.info('connexion index.html')
    result = template.render(dico_livre = listelivre())
    return func.HttpResponse(result, status_code=200, mimetype="text/html")
