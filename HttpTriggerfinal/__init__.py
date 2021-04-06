import logging
import azure.functions as func
import mysql.connector
import os
import json


config_sql = {
  'host': os.environ['hostlibrary'],
  'user': os.environ['userlibrary'],
  'password': os.environ['passwordlibrary'],
  'database':os.environ['library'],
  'client_flags': [mysql.connector.ClientFlag.SSL],
  'ssl_ca': os.environ['sslibrary']
}


def listelivre():
    logging.debug("connection à la base de données")
    conn = mysql.connector.connect(**config_sql)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT titre FROM liste_livres
    """)
    logging.info("la connection s'est bien passée!")
    rows = cursor.fetchall()
    liste_rows = []
    for row in rows :
        liste_rows += row
    logging.debug(f"liste livre {liste_rows}")
    return liste_rows


def liste_html():
    logging.info('Regarde si livre existe ou pas pour créer liste.')
    livres = listelivre()
    html_liste_livres = """<span class="Liste livre">"""
    for livre in livres :
        if livre != livres[-1]:
            html_liste_livres += livre
            html_liste_livres += """</span><br> <span class="Liste livres">"""
        else:
            html_liste_livres += livre
            html_liste_livres += "</span>"
    return html_liste_livres


def result_html():
    logging.info('Sort info en HTML.')
    result="""<!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <center>
        <title>library</title>
        </head>
        <h3>Voici la liste des livres présents dans la base de données</h3>
        <body>
        <style>
        ul
        {
            line-height:70px;
        }
        </style>
        <div>
            <ul>"""+liste_html()+"""</ul>
        </div>
        <div>Made by Djan, Emilie, Sarah, Stephanie</div>
        </body>
        </center>
        </html>"""
    return result


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    return func.HttpResponse(
        result_html(), status_code=200, mimetype='text/html'
    )
