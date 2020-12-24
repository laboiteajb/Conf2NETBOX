import pynetbox
import os
import urllib.request
import configparser
from progress.bar import IncrementalBar
from progress.spinner import Spinner

# ----------------------------- CONNECTEUR NETBOX ---------------------------- #
class netbox():
    def __init__(self, server, token, cert):
        os.environ['REQUESTS_CA_BUNDLE'] = cert
        self.nb = pynetbox.api(
        server,
        token=token,
        )
# ---------------------------------------------------------------------------- #

# ----------------------- DEFINITION DE LA CLASS COLOR ----------------------- #
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[32m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
# ---------------------------------------------------------------------------- #

# ----------------------- LECTURE DU FICHIER CONFIG.CFG ---------------------- #
def config():
    bar = IncrementalBar('Lecture du fichier config.cfg', max = 2, suffix='%(percent)d%%')
    config_script = configparser.RawConfigParser()  # On créé un nouvel objet "config"
    config_script.read('config.cfg')  # On lit le fichier de paramètres
    # Récupération basique dans des variables
    debug = config_script.get('GENERAL', 'debug')
    noquest = config_script.get('GENERAL', 'noquest')
    bar.next()
    server = config_script.get('NETBOX', 'server')
    token = config_script.get('NETBOX', 'token')
    cert = config_script.get('NETBOX', 'cert')
    bar.next()
    region = config_script.get('IMPORT', 'region')
    site = config_script.get('IMPORT', 'site')
    device = config_script.get('IMPORT', 'device')    
    device_type = config_script.get('IMPORT', 'device_type')
    path = config_script.get('IMPORT', 'path')
    bar.finish()
    return server, token, cert, debug , region, site, device, device_type, path, noquest
# ---------------------------------------------------------------------------- #

# --------------------- Recherche des sites via la region -------------------- #
def search_sites(liste_sites_tmp, region, liste_sites):
    bar = IncrementalBar('Recherche des sites via la region', max = len(liste_sites_tmp), suffix='%(percent)d%%')
    for element in range(0, len(liste_sites_tmp)):
        print(region)
        bar.next()
        if liste_sites_tmp[element].region.id == region.id:
            liste_sites.append(liste_sites_tmp[element])

    del element
    del liste_sites_tmp
    return liste_sites
    bar.finish()
# ---------------------------------------------------------------------------- #

# --------------------- Recherche des devices via le site -------------------- #
def search_devices(liste_devices, site, netbox):
    liste_devices_tmp = netbox.nb.dcim.devices.all()
    bar = IncrementalBar('Recherche des devices via le site', max = len(liste_devices_tmp), suffix='%(percent)d%%')
    for element in range(0, len(liste_devices_tmp)):
        bar.next()
        if liste_devices_tmp[element].site.id == site.id:
            liste_devices.append(liste_devices_tmp[element])

    del element
    del liste_devices_tmp
    return liste_devices
    bar.finish()
# ---------------------------------------------------------------------------- #

# -------------------- creation tableau NB_TabVlanPorttag -------------------- #
def build_NB_TabVlanPorttag(Imp_TabVlanPorttag, NB_list_interfaces):
    bar = IncrementalBar('Creation tableau NB_TabVlanPorttag', max = len(Imp_TabVlanPorttag), suffix='%(percent)d%%')
    NB_TabVlanPorttag_tmp = []
    for element in range(0, len(Imp_TabVlanPorttag)):
        bar.next()
        for element1 in range(0, len(NB_list_interfaces)):
            if Imp_TabVlanPorttag[element] == str(NB_list_interfaces[element1]):
                NB_TabVlanPorttag_tmp.append(NB_list_interfaces[element1])
    return NB_TabVlanPorttag_tmp
    bar.finish()
# ---------------------------------------------------------------------------- #

# ------------------- creation tableau NB_TabVlanIDtag_tmp ------------------- #
def build_NB_TabVlanIDtag(Imp_TabVlanIDtag, NB_list_vlans_site):
    bar = IncrementalBar('Creation tableau NB_TabVlanIDtag_tmp', max = len(Imp_TabVlanIDtag), suffix='%(percent)d%%')
    NB_TabVlanIDtag_tmp = []
    for element in range(0, len(Imp_TabVlanIDtag)):
        bar.next()
        for element1 in range(0, len(NB_list_vlans_site)):
            #print(Imp_TabVlanIDtag[element], int(NB_list_vlans_site[element1].vid))
            if int(Imp_TabVlanIDtag[element]) == int(NB_list_vlans_site[element1].vid):
                NB_TabVlanIDtag_tmp.append(NB_list_vlans_site[element1])
    return NB_TabVlanIDtag_tmp
    bar.finish()
# ---------------------------------------------------------------------------- #

# ----------------------- Recuperation du group de vlan ---------------------- #
def get_vlan_group(site, NB_vlan_group):
    print('')
    spinner = Spinner('Recuperation du group de VLAN ')
    # Parmi les group de VLAN
    for element in range(0, len(NB_vlan_group)):
        NB_vlan_group_tmp= NB_vlan_group[element]
        spinner.next()
        # Si le group fait parti du site alors
        if NB_vlan_group_tmp.site.id == site.id:
            
            NB_vlan_group= NB_vlan_group_tmp
            print(' OK!')
    del element
    del NB_vlan_group_tmp
    return NB_vlan_group
    
    print('vlan group: ', NB_vlan_group)
# ---------------------------------------------------------------------------- #

# ------------------ Recuperation des VLAN du group de VLAN ------------------ #
def vlan_to_site(NB_list_vlans, site):
    print('')
    spinner = Spinner('Recuperation des VLAN du groupe de VLAN ')
    NB_list_vlans_site = []
    NB_list_vlans_site_name = []
    NB_list_ID_vlans_site = []
    # Parmi la liste de VLAN
    for element1 in range(0, len(NB_list_vlans)):
        spinner.next()
        NB_list_vlans_uni= NB_list_vlans[element1]
        # Si le VLAN fait parti du site alors
        if NB_list_vlans_uni.site.id == site.id:
            NB_list_vlans_site.append(NB_list_vlans_uni)
            NB_list_vlans_site_name.append(NB_list_vlans_uni.name)
            NB_list_ID_vlans_site.append(NB_list_vlans_uni.vid)
            
    del element1
    print(' OK!')
    return NB_list_vlans_site, NB_list_vlans_site_name, NB_list_ID_vlans_site
# ---------------------------------------------------------------------------- #

# ------------------- Recuperation des interfaces du device ------------------ #
def interface_device(NB_list_interfaces, device, site, liste_devices):
    
    NB_list_interfaces_tmp = []
    print('')
    
    # Si le device ne fait pas partie d'un stack alors
    if device.virtual_chassis == None:
        spinner = Spinner('Recuperation des interfaces du device ')
        # Parmi la liste des interfaces
        for element in range(0, len(NB_list_interfaces)):
            spinner.next()
            # Si l'interface appartient au device et au site alors
            if int(NB_list_interfaces[element].device.id) == device.id and str(NB_list_interfaces[element].device.site) == str(site):
                NB_list_interfaces_tmp.append(NB_list_interfaces[element])
                spinner.next()
            else:
                spinner.next()

        NB_list_interfaces = NB_list_interfaces_tmp
        del NB_list_interfaces_tmp
        del element
        return NB_list_interfaces

    # Si le device fait parti d'un stack alors
    else:
        spinner = Spinner('Recuperation des interfaces du stack de device ')
        liste_device_site_tmp = []
        # parmi la liste des devices
        for element1 in range(0, len(liste_devices)):
            spinner.next()
            # Si le stack et le device selectionné alors 
            if str(liste_devices[element1].virtual_chassis) == str(device):
                liste_device_site_tmp.append(liste_devices[element1])
        
        # Parmi la liste des interfaces
        for element in range(0, len(NB_list_interfaces)):
            spinner.next()
            # Si l'interface apartient à la liste des devices du site et fait parti du site alors
            if str(NB_list_interfaces[element].device) in str(liste_device_site_tmp) and str(NB_list_interfaces[element].device.site) == str(site):
                NB_list_interfaces_tmp.append(NB_list_interfaces[element])
                        
                    #else:
                        #spinner.next()
        return NB_list_interfaces_tmp
        del NB_list_interfaces_tmp
        del element
        del element1
        print('OK!')
# ---------------------------------------------------------------------------- #