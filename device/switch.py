import re

# Alcatel
def fonc_alacatel(path, Imp_SystemName, Imp_TabVlanID, Imp_TabVlanName, Imp_TabVlanIDUntag, Imp_TabVlanPortUntag, Imp_TabVlanIDtag, Imp_TabVlanPorttag):

    # Ouvrir le fichier en lecture seule
    ContFichierConfig = open(path, "r")
    line = ContFichierConfig.readline()
    while line:
        # recuperation des vlan
        if "vlan" in line and "enable name" in line:
            line = re.sub('^(vlan\s)', '', line)
            Imp_TabVlanID.append(re.sub('\senable\sname\s.*\n', '', line))
            line = re.sub('.*enable\sname\s"', '', line)
            Imp_TabVlanName.append(re.sub('"\n', '', line))
        # Recuperation du non du switch
        elif "system name" in line:
            line = (re.sub('^system name ', '', line))
            Imp_SystemName.append(re.sub('\n', '', line))


        # Recuperation des vlan untag
        elif "vlan" in line and "port default" in line:
            line = re.sub('^vlan ', '', line)
            Imp_TabVlanIDUntag.append(re.sub(' port default (.*)\n', '', line))
            line = re.sub('(.*) port default ', '', line)
            Imp_TabVlanPortUntag.append(re.sub('\n', '', line))

        # Recuperation des vlan tag
        elif "vlan" in line and "802.1q" in line and "TAG PORT" in line:
            line = re.sub('^vlan ', '', line)
            Imp_TabVlanIDtag.append(re.sub(' 802.1q (.*)\n', '', line))
            line = re.sub('(.*) 802.1q ', '', line)
            Imp_TabVlanPorttag.append(re.sub(' "TAG PORT (.*)\n', '', line))
        line = ContFichierConfig.readline()
    ContFichierConfig.close()
    return Imp_SystemName, Imp_TabVlanID, Imp_TabVlanName, Imp_TabVlanIDUntag, Imp_TabVlanPortUntag, Imp_TabVlanIDtag, Imp_TabVlanPorttag