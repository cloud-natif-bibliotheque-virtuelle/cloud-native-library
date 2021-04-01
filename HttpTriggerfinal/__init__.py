import logging
import mysql.connector
import azure.functions as func
import os

# config = {
#   'host':'serveur-mysql-library2.mysql.database.azure.com',
#   'user':'nous@serveur-mysql-library2',
#   'password':'123Codons',
#   'database':'library',
#   'client_flags': [mysql.connector.ClientFlag.SSL],
#   'ssl_ca':'C:\\Users\\utilisateur\\Documents\\python\\deuxieme_partie\\library_azur\\BaltimoreCyberTrustRoot.crt(1).pem'
# }


config = {
  'host': os.environ['hostlibrary'],
  'user': os.environ['userlibrary'],
  'password': os.environ['passwordlibrary'],
  'database':'library',
  'client_flags': [mysql.connector.ClientFlag.SSL],
  'ssl_ca': os.environ['sslibrary']
}


def listelivre():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT titre FROM liste_livres
    """)
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
        f"voici les livres disponibles dans votre base de donnée : {listelivre()},",
        status_code=200
    )

    a=2