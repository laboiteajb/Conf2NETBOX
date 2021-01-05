# Conf2NETBOX
Script d'importation de backup de switch dans NETBOX

Executer Conf2Netbox.py pour lancer le script

#### config.cfg
[NETBOX]  
server = https://netbox.societe.com  
token = votre_token  
cert = votre_certificat.pem (à la racine du projet)  

### Automatisation  
[GENERAL]  
...  
noquest = True  

[IMPORT]  
region = nom_de_la_region  
site = nom_du_site  
device = nom_du_device  
device_type = alcatel(en cours de dev)  
path = path_du_fichier_de_config(boot.cfg pour alcatel)  