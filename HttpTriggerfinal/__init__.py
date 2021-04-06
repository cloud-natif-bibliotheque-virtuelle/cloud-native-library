import logging
import mysql.connector
import azure.functions as func
import os
import json



config = {
  'host': os.environ['hostlibrary'],
  'user': os.environ['userlibrary'],
  'password': os.environ['passwordlibrary'],
  'database':'library',
  'client_flags': [mysql.connector.ClientFlag.SSL],
  'ssl_ca': os.environ['sslibrary']
}



def listelivre():
    logging.info('connection à la base de donné')
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT titre FROM liste_livres
    """)
    logging.info("la connection c'est bien passer!")
    # res1 =[]
    # result = cursor.fetchall()
    # res =[]
    # for row in result:
    #     res.append(row["titre"])
    # for row in cursor.fetchall():
    #     res1.append(row)
    # cursor.execute("SELECT titre FROM liste_livres;")
    rows = cursor.fetchall()
    liste_rows = []
    for row in rows :
        liste_rows += row
    # res2=[]
    # for titre in res1 :
    #     titre= " ".join(titre)
    #     res2.append(titre)
    # return " ".join(res1).replace(" ",", ")
    
    return liste_rows
# print(listelivre())

def liste_html():
    logging.info('Regarde si livre existe ou pas pour créer liste.')
    livres = listelivre()
    html_liste_livres = """<span class="Liste livre">"""
    for livre in livres :
        if livre != livres[-1]:
            html_liste_livres += livre
            html_liste_livres += """</span><br><span class="Liste livres">"""
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
        <h3>Voici la liste des livres présents dans la base de donnée</h3>
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
    


# def main(req: func.HttpRequest) -> func.HttpResponse:
#     logging.info('Python HTTP trigger function processed a request.')

#     name = req.params.get('name')
#     if not name:
#         try:
#             req_body = req.get_json()
#         except ValueError:
#             pass
#         else:
#             name = req_body.get('name')

#     if name:
#         return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
#     else:
#         return func.HttpResponse(
#              "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
#              status_code=200
#         )
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    return func.HttpResponse(
        result_html(), status_code=200, mimetype='text/html'
    )

