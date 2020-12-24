from progress.spinner import Spinner
import sys

# ---------------------------------------------------------------------------- #
#             RECUPERATION DES VLAN NON PRESENT DU SITE DANS NETBOX            #
#                       ET CREATION DES VLAN NON PRENSENT                      #
# ---------------------------------------------------------------------------- #
def create_vlan(Imp_TabVlanName, NB_list_vlans_site_name, Imp_TabVlanID, site, NB_vlan_group, netbox):
    print('')
    spinner = Spinner('Recuperation des VLAN non present du site dans NETBOX et creation des VLAN non present ')
    # Dans la liste des vlan du fichier de config
    for element2 in range(0, len(Imp_TabVlanName)):
        spinner.next()
        # Si le VLAN n'est pas present, creation
        if not Imp_TabVlanName[element2] in NB_list_vlans_site_name:
            print('  Creation du VLAN', Imp_TabVlanName[element2], "avec l'ID", Imp_TabVlanID[element2])
            response = netbox.nb.ipam.vlans.create(
                name = Imp_TabVlanName[element2],
                vid = Imp_TabVlanID[element2],
                tenant = 1,
                site = site.id,
                group = NB_vlan_group.id
            )
    del element2
    print(' OK!')

# ---------------------------------------------------------------------------- #
#                   ENREGISTREMENT DES PORT UNTAG DANS NETBOX                  #
# ---------------------------------------------------------------------------- #
def import_untag(Imp_TabVlanIDUntag, NB_list_interfaces, Imp_TabVlanPortUntag, NB_list_vlans_site):
    vlan1 = ''
    NB_TabVlanUntag = [] # Liste des VLAN Untag NETBOX
    NB_TabVlanPortUntag = [] # Liste des port Untag NETBOX
    print('')
    spinner = Spinner('Recuperation du VLAN par defaut ')
    # Parmi la liste des VLAN du site
    for element3 in range(0, len(NB_list_vlans_site)):
        spinner.next()
        # Si le VLAN 1 est trouvé alors
        if str(NB_list_vlans_site[element3]) == "VLAN 1":
            vlan1 = NB_list_vlans_site[element3]

    # Creation de la liste NB_TabVlanUntag
    print('')
    spinner = Spinner('Creation de la liste NB_TabVlanUntag ')
    # Parmi la liste des VLAN du site
    for element in range(0, len(NB_list_vlans_site)):
        spinner.next()
        # Parmi la liste des VLAN Untag
        for element1 in range(0, len(Imp_TabVlanIDUntag)):
            # Si un element commun est trouvé alors ajout dans NB_TabVlanUntag
            if int(NB_list_vlans_site[element].vid) == int(Imp_TabVlanIDUntag[element1]):
                NB_TabVlanUntag.append(NB_list_vlans_site[element])
    

    # Creation de la liste NB_TabVlanPortUntag
    print('')
    spinner = Spinner('Creation de la liste NB_TabVlanPortUntag ')
    # Parmi la liste des ports Untag
    for element2 in range(0, len(Imp_TabVlanPortUntag)):
        spinner.next()
        # Parmi la liste des interfaces
        for element4 in range(0, len(NB_list_interfaces)):
            # Si un element commun est trouvé alors ajout dans NB_TabVlanPortUntag
            if str(NB_list_interfaces[element4]) == str(Imp_TabVlanPortUntag[element2]):
                NB_TabVlanPortUntag.append(NB_list_interfaces[element4])

    # Application vlan par defaut sur toutes les interfaces
    print('')
    spinner = Spinner('Application vlan par defaut sur toutes les interfaces ')
    # Parmi la liste des interfaces
    for element7 in range(0, len(NB_list_interfaces)):
        spinner.next()
        interface_tmp = NB_list_interfaces[element7]
        interface_tmp.update({"untagged_vlan": vlan1})
        print('  Enregistrement du port', NB_list_interfaces[element7], 'avec le VLAN Untag :', vlan1)

    # Application des VLAN untag
    print('')
    spinner = Spinner('Application des VLAN untag ')
    # Parmi la liste des ports Untag
    for element6 in range(0, len(NB_TabVlanPortUntag)):
        spinner.next()
        # Parmi la liste des interfaces
        for element5 in range(0, len(NB_list_interfaces)):
            # Si un element commun est trouvé alors modification du VLAN Untag sur l'interface
            if str(NB_list_interfaces[element5]) == str(NB_TabVlanPortUntag[element6]):
                interface_tmp = NB_TabVlanPortUntag[element6]
                VLAN_tmp = NB_TabVlanUntag[element6]
                interface_tmp.update({"untagged_vlan": VLAN_tmp})
                print('  Enregistrement du port', NB_list_interfaces[element5], 'avec le VLAN Untag :', VLAN_tmp)
        
    del element
    del element1
    del element2
    del element3
    del element6
    del element7
    #del interface_tmp
    #del VLAN_tmp
    print('OK!')
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
#                    ENREGISTREMENT DES PORT TAG DANS NETBOX                   #
# ---------------------------------------------------------------------------- #
def import_tag(Imp_TabVlanPorttag, Imp_TabVlanIDtag, NB_list_interfaces, NB_TabVlanPorttag, NB_TabVlanIDtag):
    element_precedent = '' # Variable de comparaison dans la boucle
    code = '' # Code à executer pour appliquer les changements dans NETBOX
    element = ''
    print('')
    spinner = Spinner('Application des VLAN Tag ')
    interface_tmp = [] # Variable tmp
    code_tmp=[] # Variable tmp

    # Parmi la liste des interfaces
    for element1 in range(0, len(NB_list_interfaces)):
        spinner.next()
        # Parmis la liste des port Tag
        for element in range(0, len(Imp_TabVlanPorttag)):
            spinner.next()
            # Si une interface et presentes dans la listes des ports Tag alors
            if str(NB_list_interfaces[element1]) == Imp_TabVlanPorttag[element]:
                print('  Enregistrement du port', NB_list_interfaces[element1], 'avec le VLAN Tag :', Imp_TabVlanIDtag[element])
                interface = NB_TabVlanPorttag[element]
                
                # Si element_precedent == '' alors premier element de la liste
                if element_precedent == '':
                    id = "NB_TabVlanIDtag[" + str(Imp_TabVlanIDtag[element]) + "]"
                    code = "interface.update({'tagged_vlans': [" + id
                    element_precedent = Imp_TabVlanPorttag[element]
                    interface_tmp.append(interface)
                    
                # Si element_precedent == Imp_TabVlanPorttag[element] un autre VLAN et detecter sur la meme interface, ajout du VLAN    
                elif element_precedent == Imp_TabVlanPorttag[element]:
                    id = ", NB_TabVlanIDtag[" + str(Imp_TabVlanIDtag[element]) + "]"
                    code = code + id
                    element_precedent = Imp_TabVlanPorttag[element]

                # Pour le reste, on ferme la syntaxe de code et on recommence
                else:
                    code = code + "]})"
                    interface_tmp.append(interface)
                    code_tmp.append(code)


                    id = "NB_TabVlanIDtag[" + str(Imp_TabVlanIDtag[element]) + "]"
                    code = "interface.update({'tagged_vlans': [" + id
                    element_precedent = Imp_TabVlanPorttag[element]
                    

            """else:
                interface = NB_TabVlanPorttag[element]
                interface.update({'tagged_vlans': []})"""
                
    # Boucle terminé,  on ferme la syntaxe de code           
    code = code + "]})"
    code_tmp.append(code)
    
    # On applique les changements à NETBOX
    print( 'OK!')
    for element2 in range(0, len(interface_tmp)):
        interface = interface_tmp[element2]
        exec(code_tmp[element2])
# ---------------------------------------------------------------------------- #

# exemple
# vlan = nb.ipam.vlans.all()
# interface = nb.dcim.interfaces.all()
# interface = interface[0]
# interface.update({"tagged_vlans": [vlan[0],vlan[1]]})


