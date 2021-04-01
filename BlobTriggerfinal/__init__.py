import logging
import json
import azure.functions as func



def main(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")
    read = myblob.read().decode('utf-8')
    mots = read.split()
    dico_mots = {}
    for mot in set(mots):
        dico_mots[mot]=mots.count(mot)
    # mettre le dico dans la base
    logging.info(f"contenu du read: {dico_mots['hello']} + contenu du blob: {json.dumps(read)}")


a = 2 



