import sys
import argparse
import configparser
import logging
import os.path
from azure.storage.blob import BlobServiceClient, ContainerClient, BlobClient


logging.basicConfig(
    filename="logging_main.log",
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s - %(message)s',
    datefmt='%d/%m/%Y %H:%M:%S',)


def upload(cible, blobclient):
    """ Charge le fichier texte local dans l’objet Blob en appelant 
        la méthode upload_blob.
    """
    with open(cible, "rb") as f:
        logging.info("Upload the blob from a local file")
        blobclient.upload_blob(f)


def main(args,config):
    """
    Fait le liens avec le config.ini
    Fait appel aux fonctions (upload/download/ list).
    """
    blobclient=BlobServiceClient(
        f"https://{config['storage']['account']}.blob.core.windows.net",
        config["storage"]["key"],
        logging_enable=False)
    containerclient=blobclient.get_container_client(config["storage"]["container"])
    # liaison avec le container
    if args.action=="list":

        logging.warning("Connexion et liaison avec le container")
        return listb(args, containerclient)
        #listeb = liste blob
    else:
        if args.action=="upload": 
            #Lié avec le parser = upload
            blobclient=containerclient.get_blob_client(os.path.basename(args.cible))
            #Lié avec le parser = se connecter au blob client et lui envoyer au fichier
            return upload(args.cible, blobclient)
            #Lié avec le parser = downolad 
        elif args.action=="download":
            blobclient=containerclient.get_blob_client(os.path.basename(args.remote))
            #Lié avec le parser = Télécharger fichier
            logging.warning("Télécharge le fichier")
            return download(args.remote, config["general"]["restoredir"], blobclient)
        

if __name__=="__main__":
    #Parser pour utiliser dans son terminal, mode d'emplois dans requirement.txt
    parser=argparse.ArgumentParser("Logiciel d'archivage de documents")
    parser.add_argument("-cfg",default="config.ini",help="chemin du fichier de configuration")
    parser.add_argument("-lvl",default="info",help="niveau de log")
    subparsers=parser.add_subparsers(dest="action",help="type d'operation")
    subparsers.required=True
    
    parser_s=subparsers.add_parser("upload")
    parser_s.add_argument("cible",help="fichier à envoyer")

    parser_r=subparsers.add_parser("download")
    parser_r.add_argument("remote",help="nom du fichier à télécharger")
    parser_r=subparsers.add_parser("list")

    args=parser.parse_args()

    loglevels={"debug":logging.DEBUG, "info":logging.INFO, "warning":logging.WARNING, "error":logging.ERROR, "critical":logging.CRITICAL}
    print(loglevels[args.lvl.lower()])
    logging.basicConfig(level=loglevels[args.lvl.lower()])

    config=configparser.ConfigParser()
    config.read(args.cfg)

    sys.exit(main(args,config))