import inquirer

# ---------------------------------------------------------------------------- #
#                                 MENU REGIONS                                 #
# ---------------------------------------------------------------------------- #
def fonc_regions(liste_regions, liste_sites):

    questions = [
      inquirer.List('region',
                    message="Selectionner la ville",
                    choices=liste_regions,
                ),
    ]
    answers = inquirer.prompt(questions)
    region = answers["region"]
    return region
# ---------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------- #
#                                  MENU SITES                                  #
# ---------------------------------------------------------------------------- #
def fonc_sites(liste_sites):
    questions = [
      inquirer.List('site',
                    message="Selectionner un client",
                    choices=liste_sites,
                ),
    ]
    answers = inquirer.prompt(questions)
    site = answers["site"]
    return site
# ---------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------- #
#                                 MENU DEVICES                                 #
# ---------------------------------------------------------------------------- #
def fonc_devices(liste_devices):
    questions = [
      inquirer.List('device',
                    message="Selectionner un peripherique",
                    choices=liste_devices,
                ),
    ]
    answers = inquirer.prompt(questions)
    device = answers["device"]
    return device
# ---------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------- #
#                               MENU DEVICE TYPE                               #
# ---------------------------------------------------------------------------- #
def fonc_device_type(liste_device_type):
    questions = [
      inquirer.List('device_type',
                    message="Selectionner le type de device",
                    choices=liste_device_type,
                ),
    ]
    answers = inquirer.prompt(questions)
    device_type = answers["device_type"]
    return device_type
# ---------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------- #
#                                   MENU PATH                                  #
# ---------------------------------------------------------------------------- #
def fonc_path(path):
    questions = [
       inquirer.Path('cfg_file',
                     message="Entrer le chemin du fichier de config",
                     exists=True,
                     path_type=inquirer.Path.FILE,
                ),
    ]
    answers = inquirer.prompt(questions)
    path = answers["cfg_file"]
    return path
# ---------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------- #
#                                  MENU RESUME                                 #
# ---------------------------------------------------------------------------- #
def fonc_resume(Text):
    questions = [
    inquirer.Confirm('continue',
                  message=Text),
    ]
    answers = inquirer.prompt(questions)
    reponse = answers['continue']
    return reponse
# ---------------------------------------------------------------------------- #