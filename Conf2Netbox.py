import inquirer
import os
import sys
from Fonctions.general import netbox, bcolors, config, search_sites, search_devices, build_NB_TabVlanPorttag, build_NB_TabVlanIDtag, get_vlan_group, vlan_to_site, interface_device
from Fonctions.menu import *
from device.switch import fonc_alacatel
from Fonctions.Import import create_vlan, import_untag, import_tag


clear = lambda: os.system('cls')
liste_sites = []
liste_devices = []
liste_device_type = ['alcatel', 'HP']
path = ''


Imp_TabVlanID = [] #ID des VLAN du fichier backup du switch
Imp_TabVlanName = [] #Nom des VLAN du fichier backup du switch
Imp_SystemName = [] #Nom du switch du fichier backup du switch
Imp_TabVlanIDUntag = [] #ID des VLAN Untag du fichier backup du switch
Imp_TabVlanPortUntag = [] #Ports des VLAN Untag du fichier backup du switch
Imp_TabVlanIDtag = [] #ID des VLAN Tag du fichier backup du switch
Imp_TabVlanPorttag = [] #Ports des VLAN Tag du fichier backup du switch

#############################################################################
logo= """
 ██████╗ ██████╗ ███╗   ██╗███████╗██████╗ ███╗   ██╗███████╗████████╗██████╗  ██████╗ ██╗  ██╗
██╔════╝██╔═══██╗████╗  ██║██╔════╝╚════██╗████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██╔═══██╗╚██╗██╔╝
██║     ██║   ██║██╔██╗ ██║█████╗   █████╔╝██╔██╗ ██║█████╗     ██║   ██████╔╝██║   ██║ ╚███╔╝ 
██║     ██║   ██║██║╚██╗██║██╔══╝  ██╔═══╝ ██║╚██╗██║██╔══╝     ██║   ██╔══██╗██║   ██║ ██╔██╗ 
╚██████╗╚██████╔╝██║ ╚████║██║     ███████╗██║ ╚████║███████╗   ██║   ██████╔╝╚██████╔╝██╔╝ ██╗
 ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝     ╚══════╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═════╝  ╚═════╝ ╚═╝  ╚═╝
"""
#############################################################################


#############################################################################
clear()
print(logo)
                                                                                                                                     
                                                                                                                                     
# Recuperation des information du fichier de config
server, token, cert, debug , region, site, device, device_type, path, noquest= config()

# Initialisation de cnx à netbox
netbox = netbox(server, token, cert)

# Recuperation de la liste des region dans netbox
liste_regions = netbox.nb.dcim.regions.all()

# Recuperation de la liste des clients dans netbox
liste_sites_tmp = netbox.nb.dcim.sites.all()

# Recuperation de la liste des vlan
NB_list_vlans = netbox.nb.ipam.vlans.all()

# Recuperation de la liste des group de vlan
NB_vlan_group= netbox.nb.ipam.vlan_groups.all()

# Recuperation de la liste des interfaces
NB_list_interfaces = netbox.nb.dcim.interfaces.all()



# ------------------------- Recuperation de regions -------------------------- #
clear()
print(logo)

print(server, token, cert, debug , region, site, device, device_type, path)
if region == '':
    region = fonc_regions(liste_regions, liste_sites)
else:
    for element in range(0, len(liste_regions)):
        if liste_regions[element].name == region:
            region = liste_regions[element]
        del element
# ---------------------------------------------------------------------------- #

# -------------------------- Recuperation des sites -------------------------- #
liste_sites = search_sites(liste_sites_tmp, region, liste_sites)
clear()
print(logo)

print('Region :', region)
if site == '':
    site = fonc_sites(liste_sites)
else:
    for element in range(0, len(liste_sites)):
        if liste_sites[element].name == site:
            site = liste_sites[element]
        del element
# ---------------------------------------------------------------------------- #

# ------------------- Recuperation de la liste des devices ------------------- #
liste_devices = search_devices(liste_devices, site, netbox)
clear() 
print(logo)

print('Region :', region)
print('Client :', site)
if device == '':
    device = fonc_devices(liste_devices)
else:
    for element in range(0, len(liste_devices)):
        if liste_devices[element].name == device:
            device = liste_devices[element]
        del element
# ---------------------------------------------------------------------------- #

# -------------------------- Recuperation des models ------------------------- #
clear()
print(logo) 

print('Region :', region)
print('Client :', site)
print('Device :', device)
if device_type == '':
    device_type = fonc_device_type(liste_device_type)
# ---------------------------------------------------------------------------- #

# ---------------- Recuperation du fichier de config du device --------------- #
clear() 
print(logo)

print('Region :', region)
print('Client :', site)
print('Device :', device)
print('Model :', device_type)
if path == '':
    path = fonc_path(path)
# ---------------------------------------------------------------------------- #

# ---------------------------- AFFICHAGE DES CHOIX --------------------------- #
clear() 
print(logo)
 
print('Region :', region)
print('Client :', site)
print('Device :', device)
print('Model :', device_type)
print('Fichier conf :', path)
# ---------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------- #
#                RECUPERATION VALEURS DU FICHIER CONFIG ALCATEL                #
# ---------------------------------------------------------------------------- #
if device_type == 'alcatel':
    Imp_SystemName, Imp_TabVlanID, Imp_TabVlanName, Imp_TabVlanIDUntag, Imp_TabVlanPortUntag, Imp_TabVlanIDtag, Imp_TabVlanPorttag = fonc_alacatel(path, Imp_SystemName, Imp_TabVlanID, Imp_TabVlanName, Imp_TabVlanIDUntag, Imp_TabVlanPortUntag, Imp_TabVlanIDtag, Imp_TabVlanPorttag)
# ---------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------- #
#                    AFFICHAGE DE LA CONFIGURATION DU SWITCH                   #
# ---------------------------------------------------------------------------- #
print("# ---------------------------------------------------------------------------- #")
print('')
if noquest == "False":
    reponse = fonc_resume('Appuyer sur "y" pour vérifier la configuration du switch')
    if reponse == True:
        print("# ---------------------------------------------------------------------------- #")
        print("# ------------------------------- Nom du Switch ------------------------------ #")
        print("# ---------------------------------------------------------------------------- #")
        print("Nom du switch : ", Imp_SystemName)
        print("# ---------------------------------------------------------------------------- #")
        print('')
        print("# ---------------------------------------------------------------------------- #")
        print("# ------------------------------ Liste des VLAN ------------------------------ #")
        print("# ---------------------------------------------------------------------------- #")
        for element in range(0, len(Imp_TabVlanID)):
            print("Vlan ID :", Imp_TabVlanID[element], " Nom : ", Imp_TabVlanName[element])
        print("# ---------------------------------------------------------------------------- #")
        print('')
        print("# ---------------------------------------------------------------------------- #")
        print("# ------------------------ Liste des VLAN/Ports Untag ------------------------ #")
        print("# ---------------------------------------------------------------------------- #")
        for element in range(0, len(Imp_TabVlanIDUntag)):
            print("Vlan ID :", Imp_TabVlanIDUntag[element], " port : ", Imp_TabVlanPortUntag[element])
        print("# ---------------------------------------------------------------------------- #")
        print('')
        print("# ---------------------------------------------------------------------------- #")
        print("# ------------------------- Liste des VLAN/Ports tag ------------------------- #")
        print("# ---------------------------------------------------------------------------- #")
        for element in range(0, len(Imp_TabVlanIDtag)):
            print("Vlan ID :", Imp_TabVlanIDtag[element], " port : ", Imp_TabVlanPorttag[element])
        print("# ---------------------------------------------------------------------------- #")
        print('')
        reponse = fonc_resume("Les informations ci-dessus sont'elle correctes ?")
        if reponse == False:
            print('## FIN DU SCIPT ! ##')
            exit()
# ---------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------- #
#                         RECUPERATION DU GROUP DE VLAN                        #
# ---------------------------------------------------------------------------- #
NB_vlan_group = get_vlan_group(site, NB_vlan_group)
# ---------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------- #
#                         RECUPERATION DU GROUP DE VLAN                        #
# ---------------------------------------------------------------------------- #
NB_list_vlans_site, NB_list_vlans_site_name, NB_list_ID_vlans_site = vlan_to_site(NB_list_vlans, site)
# ---------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------- #
#             RECUPERATION DES VLAN NON PRESENT DU SITE DANS NETBOX            #
#                       ET CREATION DES VLAN NON PRENSENT                      #
# ---------------------------------------------------------------------------- #
create_vlan(Imp_TabVlanName, NB_list_vlans_site_name, Imp_TabVlanID, site, NB_vlan_group, netbox)
# ---------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------- #
#                     RECUPERATION DES INTERFACES DU DEVICE                    #
# ---------------------------------------------------------------------------- #
NB_list_interfaces = interface_device(NB_list_interfaces, device, site, liste_devices)
# ---------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------- #
#                      CREATION TABLEAU NB_TabVlanPorttag                      #
# ---------------------------------------------------------------------------- #
NB_TabVlanPorttag = build_NB_TabVlanPorttag(Imp_TabVlanPorttag, NB_list_interfaces)
# ---------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------- #
#                       CREATION TABLEAU NB_TabVlanIDtag                       #
# ---------------------------------------------------------------------------- #
NB_TabVlanIDtag = build_NB_TabVlanIDtag(Imp_TabVlanIDtag, NB_list_vlans_site)
# ---------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------- #
#                    ENREGISTREMENT DES PORT TAG DANS NETBOX                   #
# ---------------------------------------------------------------------------- #
import_tag(Imp_TabVlanPorttag, Imp_TabVlanIDtag, NB_list_interfaces, NB_TabVlanPorttag, NB_TabVlanIDtag)
# ---------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------- #
#                   ENREGISTREMENT DES PORT UNTAG DANS NETBOX                  #
# ---------------------------------------------------------------------------- #
import_untag(Imp_TabVlanIDUntag, NB_list_interfaces, Imp_TabVlanPortUntag, NB_list_vlans_site)
# ---------------------------------------------------------------------------- #
print("Fin du script")
sys.exit()
