import logging
import json
import mysql.connector
import azure.functions as func
from mysql.connector import errorcode
import os.path


configuration = {
  'host': os.environ['hostlibrary'],
  'user': os.environ['userlibrary'],
  'password': os.environ['passwordlibrary'],
  'database':'library',
  'client_flags': [mysql.connector.ClientFlag.SSL],
  'ssl_ca': os.environ['sslibrary']
}

def main(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")
    # 300 = limite pour ne lire que les 300 premiers mots du blob
    read = myblob.read(300).decode('utf-8')
    mots = read.split()
    dico_mots = {}
    # TODO creation d'un dictionnaire de mots (prevoir autre table sql par la suite)
    for mot in set(mots):
        dico_mots[mot]=mots.count(mot)
    dico_mots_json= json.dumps(dico_mots)
    logging.info(f"contenu du dico_mots_json{dico_mots_json}")

    try:
        conn = mysql.connector.connect(**configuration)
        print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cursor = conn.cursor()

    url_stock = 'https://librarystokage2.blob.core.windows.net/'+ myblob.name
    logging.info(f"l'url cherché dans la base {url_stock}")
    cursor.execute("UPDATE liste_livres SET nombre_mot = (%s) WHERE url_blob = (%s)",
                  (dico_mots_json, url_stock,))
    logging.info(f"action du cursor.execute pour update = ok")
    conn.commit()
    cursor.close()
    conn.close()
    logging.info(f"La table liste_livres a bien été mise à jour.")
