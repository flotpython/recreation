# -*- coding: utf-8 -*-
#!/usr/bin/python3.6
# Program "verif_temps3.py"


###############################################################################
######################## IMPORTS, Prints and VARIABLES ########################
###############################################################################
"""
Change paths below if this program's filename changed or if 'repbase' and
'repcible' are different.
"""

import os
import sys
import re
import shutil
import pathlib
import time

from zipfile import ZipFile
from datetime import datetime
from datetime import timedelta


print(f"\n{' Démarrage du programme *.py '.center(78, '=')}\n")

# These paths need to be checked, if they aren't correct program won't work
this_prog_name = 'verif_temps3_for_pc_yoann_0function.py'

# This is the working repertory that will be changed in block n°10
repbase = "D:/Programmes/PYTHON/verif_temps3"

# This following folder needs to be created if it doesn't exist:
repcible = "D:/Programmes/PYTHON/verif_temps3/Temp"

# This variable contains the path to file 'trigrammes.txt' in block n°6
lien_trigrammes = "P:/Services/SINF/Trigrammes personnels/trigrammes.txt"

# These 2 following variables are used in block n°7
rep_D8 = 'Y:\Data_Bruker_D8\Archives\Test_doublons_D8'
rep_D5005 = 'Y:\D5005\Data_D5005_Bruker\Archives\Test_doublons'

# If '*.py' file isn't in the correct folder
os.chdir (repbase)
print(os.getcwd())

liste_bsml = []

# These sets and variables are used in block n°5
result = set()
n_errors = 0
caracteres_speciaux = {'"', "'", "°", "à", "é", "è", "ù", "â", "ê", "î", 
"ô", "û", "ç", "ä", "ë", "ï", "ö", "ü", "@", "#", "&", "^", "~", "<", ">", 
"$", "€", "£", "¤", ";", "!"}

# These sets and variables are used in block n°6
message_nbre_caracteres = "Erreur: mauvais nombre de caractères dans \
le nom de fichier ! Probablement 1 caractère en trop ou 1 caractère \
en moins... \n"
message_non_conforme = "Erreur: au moins un des caractères saisis lors de \
la programmation de l'échantillon n'est pas conforme au format \
'AAA-A-999-99-' ou 'AAA-9-999-99-' avec l'extension 'XRD-99' ou 'HTD-99'. \n"
message_trigramme_inconnu = "Erreur: le trigramme est inconnu ou \
appartient à une personne externe au laboratoire."


#####################
#####  Bloc n°1  ####
#####################
"""
Displays last modification of *.py file.
An exception is catched if this file doesn't exist (with a try/except).
"""

try:
    path = pathlib.Path(this_prog_name)
    mtime = path.stat().st_mtime
    mtime_datetime = datetime.fromtimestamp(mtime)

except FileNotFoundError as e:
    print(f"Ooops! {e}")

else:    
    print(f"Dernière modification du fichier *.py le "
          f"{mtime_datetime:%d/%m}/20{mtime_datetime:%y} "
          f"({mtime_datetime:%H:%M}) \n")

    
#####################
#####  Bloc n°2  ####
#####################
"""
Asks user to type name of xjob file (without extension).
A 'while True' loop is implemented because we can make a mistake on 'xjob'
filename.
Starts counting duration of this program after input.
This value will be used at the end of the program.
"""
while True:
    file_xjob = input("\nTaper le nom du fichier xjob sans l'extension: ")
    file_xjob += '.xjob'

    # Starts counting duration of this program
    start = time.time()


    #####################
    #####  Bloc n°3  ####
    #####################
    """
    Checks if xjob filename exists in the specified directory.
    If it exists, 'file_xjob' is oppened. Otherwise it displays an error
    message and we ask user to input 'file_xjob' again.
    """

    print(f"\n\n{' vérifie le nom du fichier xjob saisi '.center(78, '=')}\n")

    # Directory to modify if necessary: should contain all xjob files !
    liste_fichiers = (fichier for fichier in os.listdir(repbase)
                      if fichier.endswith('.xjob'))

    if file_xjob in liste_fichiers:
        print(file_xjob)


        #####################
        #####  Bloc n°4  ####
        #####################
        """
        Opens *.xjob file after checking typed filename (if it exists). 
        Firstable, lines in *.xjob file are cleaned. Then, each value typed in
        "SamplePosition", "RawFile", "SampleID", "ExperimentFile",
        "Sample_holder", "User", "Group", "Price" and "Comment"
        are copied/pasted in 'cleaned2' list.
        """

        with open(file_xjob) as f:
            lines = f.readlines()
            clean_lines = (line.strip() for line in lines)

            # We need a better cleaning by removing '<CellValue>' and '</':
            cleaned2 = [elmt.strip('<CellValue>').strip('</')
                        for elmt in clean_lines
                        if elmt.startswith('<CellValue>')]

        # As a result: all sample numbers to test and *.bsml programs used
        # are in 'cleaned2' list.
        

        #####################
        #####  Bloc n°5  ####
        #####################
        """
        Joins all characters from 'cleaned2' list to copy them into a new set 
        called 'set_all_cleaned2'.
        Checks if unwanted characters are present in 'set_all_cleaned2'.
        If it is the case, it displays an error message and starts counting
        errors (with n_error).
        """

        print(f"\n\n{' vérifie les caractères spéciaux '.center(78, '=')}\n")

        set_all_cleaned2 = set([''.join(a.split()) for elmt in cleaned2
                                for a in elmt])

        result = caracteres_speciaux.intersection(set_all_cleaned2)
        
        if result != set():
            n_errors = len(result)
            print(f"{n_errors} erreur(s): {result}\n"
                  "Merci de vérifier les caractères saisis dans la description"
                  " de l'échantillon ou dans le nom de l'utilisateur.")
            print(f"\nCaractères non désirés: {caracteres_speciaux}")
        else:
            pass

                
        #####################
        #####  Bloc n°6  ####
        #####################
        """
        Checks that programmed sample numbers comply with formats
        'AAA-A-999-99-' or 'AAA-9-999-99-' with 'XRD-99' or 'HTD-99' extension,
        otherwise it displays an error message.
        
        Then if trigram (corresponding to the 3 first letters of each sample 
        number) is uppercased, opens 'trigrammes.txt' file and checks that
        all trigrams typed in '*.xjob' file exist.
        Otherwise it displays an error message.
        
        At the end, this code block displays number of programmed analyses.
        """

        print("\n")
        print(f"""{" vérifie les numéros d'échantillon ".center(78, '=')}\n""")

        # 'liste_brml' contains all sample numbers of xjob file,
        # from trigram to '.brml' extension
        liste_brml = [a[14:] for a in cleaned2
                      if a.startswith("D:\\raw_(brml)\\")]

        # Different regular expressions to comply with sample number, trigram
        # and extension:
        regexp = r"([A-Z]{3}-[A-Z0-9]-[0-9]{3}-[0-9]{2}-XRD-[0-9]{2})"
        regexp_trigram = r"([A-Z^a-z0-9_-]{3})"
        regexp_extension = r"((.)*[.]brml)"

        for filename in liste_brml:
            trigramme, ext = filename[:3], filename[19:]

            if len(filename) != 24:
                n_errors += 1
                print(f"{filename} \n{message_nbre_caracteres}")
            
            if re.match(regexp_trigram, filename):
                pass
            else:
                with open(lien_trigrammes) as f:
                    lines = f.readlines()
                    liste_trigrammes = (line.strip('\n').split(', ')[0]
                                        for line in lines)
                    
                if trigramme not in liste_trigrammes:
                    n_errors += 1
                    print(f"{trigramme} \n{message_trigramme_inconnu} \n")
            
            if re.match(regexp, filename):
                pass
            else:
                n_errors += 1
                print(f"{filename} \n{message_non_conforme}")            
            
            if re.match(regexp_extension, filename):
                pass
            else:
                n_errors += 1
                print(f"Erreur: l'extension rentrée '{ext}' est différente "
                      "de '.brml'. \n")

        msg_count_analyses = " compte le nombre d'analyses programmées "
        print(f"""\n{msg_count_analyses.center(78, '=')}"""
              f"""\n\nNombre d'analyses programmées: {len(liste_brml)}""")

        
        #####################
        #####  Bloc n°7  ####
        #####################
        """
        Checks if sample numbers already exist on 'Y:\' server,
        in 'Test doublons' folders related to D5005 and D8 diffractometers.
        Otherwise it displays an error message.
        """
        
        print(f"\n\n{' vérifie les doublons '.center(78, '=')}\n")

        # All files ending with '.raw' from 'rep_D8' are pasted into
        # this new list
        liste_analyses_D8_depuis_2010 = [file for file in os.listdir(rep_D8)
                                         if file.endswith('.raw')]

        # All filenames from 'rep_D5005' are pasted into this new list,
        # but all characters are capitalized
        liste_old_analyses_D5005 = [old_file.upper() for old_file
                                    in os.listdir(rep_D5005)]
        
        # 'liste_brml2' is created with a generating expression (bit-efficient)
        liste_brml2 = (brml[:-5] for brml in liste_brml)

        for brml2 in liste_brml2:
            # If file already exists in rep_D8 directory
            if brml2 + '.raw' in liste_analyses_D8_depuis_2010:
                n_errors += 1
                print("Erreur: le numéro", brml2, "existe déjà dans la base "
                      "de données du D8. Merci d'en attribuer un autre ou "
                      "d'incrémenter l'extension après 'XRD'. \n")
                continue        # continues with the next iteration of the loop

            if brml2 + '.RAW' in liste_old_analyses_D5005:
                # = old diffractograms
                n_errors += 1
                print("Erreur: le numéro", brml2, "existe déjà dans la base "
                      "de données du D5005. Merci d'en attribuer un autre ou "
                      "d'incrémenter l'extension après 'XRD'. \n")


        #####################
        #####  Bloc n°8  ####
        #####################
        """
        Firstable, this code block checks that *.bsml program exists in the 
        specified directory, otherwise it displays an error message.
        
        Then it saves *.bsml filenames in a list called 'liste_bsml',
        but only if filenames are different from each other.
        """

        for a in cleaned2:
            # For each element 'a', we start looking for those which begin by
            # 'D:\Bruker_nov2012\'
            if a.startswith("D:\\Bruker_nov2012\\"):
                
                # String under format
                # 'Prog_4-80-0,02-0,5_STANDARD_couteau-auto.'
                string_bsml = a.strip("D:\\Bruker_nov2012\\DIFFDAT\\bsml")
                
                # String under format
                # 'Prog_4-80-0,02-0,5_STANDARD_couteau-auto.bsml'
                string_bsml2 = string_bsml + "bsml"

                if string_bsml2 not in os.listdir (repbase):
                    # This repertory needs to be modified when repertory
                    # containing bsml files is changed
                    n_errors += 1
                    print(f"Erreur: le fichier {string_bsml2} n'existe pas "
                          f"dans le répertoire {repbase}.\n")
                else:
                    # We add each string_bsml2 to 'liste_bsml' which contains
                    # all programs
                    liste_bsml.append(string_bsml2)


        #####################
        #####  Bloc n°9  ####
        #####################
        """
        Firstable, different variables are created.
        'bsml' filenames with spaces are processed in this code block
        because they're splitted into 2 elements in 'liste_bsml': one starting
        by 'Prog_' and one finishing by 'bsml'. These elements are joined
        together and the new element is added in 'liste_bsml'.
        Splitted elements are deleted.

        'liste_bsml' is converted into a set called 'set_bsml2'.
        By this way all doublons are deleted, which means that 'set_bsml2' only
        contains different 'bsml' files. Indeed, this code block checks
        if these files (with '.zip' extension instead of 'bsml') already exist
        in the folder 'Temp'.
        
        Then this code block copies '*.bsml' files from 'set_bsml2' to folder
        'Temp' if these files don't already exist.
        '*.bsml' files are then converted into '*.zip'.
        """

        # Lists and variables
        liste_zip = []
        liste_zip_i = []
        a = 0
        bsml_tmp1 = ""
        bsml_tmp2 = ""

        bsml_temp = [bsml for bsml in liste_bsml
                     if not (bsml.startswith("Prog")
                     and bsml.endswith("bsml"))]

        while a < len(bsml_temp):
            if bsml_temp[a].startswith("Prog_"):
                bsml_tmp1 = bsml_temp[a]
                a += 1
                
            if bsml_temp[a].endswith("bsml"):
                bsml_tmp2 = bsml_temp[a]
                a += 1
                                    
            bsml_tmp_f = bsml_tmp1 + " " + bsml_tmp2
            liste_bsml.append(bsml_tmp_f)
                
            bsml_tmp1 = ""
            bsml_tmp2 = ""

        for bsml in liste_bsml:
            # Deletes bsml from 'liste_bsml' if it doesn't start with "Prog_"
            if not bsml.startswith("Prog_"):
                liste_bsml.remove(bsml)

            # Deletes bsml if it starts with "Prog_" and if it doesn't end
            # with "bsml"
            if bsml.startswith("Prog_") and not bsml.endswith("bsml"):
                liste_bsml.remove(bsml)

        set_bsml2 = set(liste_bsml)
        

        ##### 1st big condition: if there isn't any file in 'Temp' folder #####
        if os.listdir(repcible) is None:
            # print("Il n'y a pas de fichier dans le dossier Temp.")
            for f in os.listdir(repbase):
                src = pathlib.PurePosixPath(repbase, f)
                cible = pathlib.PurePosixPath(repcible, f)

                if f in set_bsml2:
                    # Copy of each file '*.bsml' from list into 'Temp' folder
                    print("Copie du fichier *.bsml...\n")
                    shutil.copy(src, cible)

            for file in os.listdir(repcible):
                cible = pathlib.PurePosixPath(repcible, file)
                # Add filenames without extensions in 'liste_zip_i' from
                # repertory 'repcible':
                liste_zip_i.append('{}'.format(cible.stem))
                
            # We remove '.bsml' extension of each 'bsml' file to convert it
            # later into '.zip'
            liste_file = [bsml.rstrip("bsml").rstrip(".")
                          for bsml in set_bsml2]

            for file2 in liste_file:
                zip_file = file2 + ".zip"
                # Repertory + filename to rename
                bsml_dir = repcible + '/' + file2 + ".bsml"
                # Repertory + filename renamed
                zip_dir = repcible + '/' + zip_file 

                if (file2 + ".bsml") in os.listdir(repcible):
                    # File *.bsml is renamed in *.zip to open it later
                    os.rename(bsml_dir, zip_dir)


        ### 2nd big condition: if there is at least 1 file in 'Temp' folder ###
        else:
            liste_zip.extend(os.listdir(repcible))

            for file in os.listdir(repcible):
                cible = pathlib.PurePosixPath(repcible, file)
                # Add filenames without extensions in 'liste_zip_i' from
                # repertory 'repcible':
                liste_zip_i.append('{}'.format(cible.stem))
                
            # We remove '.bsml' extension to convert the file into '.zip'
            liste_file = [bsml.rstrip("bsml").rstrip(".")
                          for bsml in set_bsml2]
                
            # If file doesn't exist in 'liste_zip_i', thus 'bsml' program has
            # to copy file in 'file3_bsml'
            file3_bsml = [file2 + ".bsml" for file2 in liste_file
                          if file2 not in liste_zip_i]
                                
            for f in os.listdir(repbase):
                # src = 'repbase' repertory + filename
                src = pathlib.PurePosixPath(repbase, f)
                # cible = 'repcible' repertory + filename
                cible = pathlib.PurePosixPath(repcible, f)
                
                """ This piece of code can be useful to debug:
                # print("src =", src)
                # print('path  : {}'.format(src))    # File's repertory
                # print('name  : {}'.format(src.name))    # Filename
                # with extension
                # print('suffix: {}'.format(src.suffix))    # The extension
                # print('stem  : {}'.format(src.stem), '\n')    # Filename
                # without extension
                """
                
                if f in set_bsml2 and f in file3_bsml:
                    # Copy of each file *.bsml from list into folder 'Temp'
                    print("Copie du fichier *.bsml...\n")
                    shutil.copy(src, cible)

                    for file2 in liste_file:
                        zip_file = file2 + ".zip"
                        # Repertory + filename to rename
                        bsml_dir = repcible + '/' + file2 + ".bsml"
                        # Repertory + filename renamed
                        zip_dir = repcible + '/' + zip_file

                        if (file2 + ".bsml") in os.listdir(repcible):
                            # File *.bsml is renamed in *.zip to open it later
                            os.rename(bsml_dir, zip_dir)

                            
        ######################
        #####  Bloc n°10  ####
        ######################
        """
        Firstable, this code block counts number of errors occurred
        in this program and displays a message.
        
        Then it counts number of 'bsml' programs to use and put data
        in a dictionary.
        Next it opens *.zip files saved in folder 'Temp' to get the duration
        of each program, which is included in an XML file.
        This duration is multiplied by number of program uses and it is added
        to 'estimated_time' list.
        
        Constants are added to the duration of all analyses:
        loading/unloading of each sample-holder, time to set work power on
        the diffractometer, time for arms of the goniometer to move down and
        be in position for the beginning of the analyse...
        
        Current date & time are integrated to determine the estimated end
        date & time of all analyses.
        This is displayed at the end of the program.
        """

        # par exemple test4 doit renvoyer 12 erreurs: 3 caractères illicites,
        # 5 erreurs sur les numéros d'échantillons + 4 doublons
        # 9 analyses sont programmées et doivent durer 8h 9min et 34s.

        #### Lists:
        estimated_time = []

        #### Constants:
        # Loading first sample (22s)
        load_1st_sample = 22
        # Time to set work power + arms of the goniometer moving in position
        setpower_et_gonio = 15
        # arms of the goniometer moving in position (5s)
        descente_bras_gonio = 5
        # Unloading/loading next sample (to repeat by number of samples - 1)
        unload_load = 42
        # Unloading last sample (26s)
        unload_last_sample = 26

        print(f"""\n{" estime la date/l'heure de fin ".center(78, '=')}\n""")
        
        if n_errors == 0:
            print('Aucune erreur détectée, bravo!!! \n')
        elif n_errors > 0:
            print(f"ATTENTION: nombre d'erreurs détectées = {n_errors} \n"
                  "Merci de vérifier et corriger les erreurs avant de lancer "
                  "les jobs...\n\n")

        # Counts duplicates of programs in 'liste_bsml' and puts data
        # in a dict:
        compteur = {f: liste_bsml.count(f) for f in set(liste_bsml)}

        # Changes working repertory to make some operations
        os.chdir (repcible)

        # Looks for duration in each program:
        for file in os.listdir(repcible):
            for bsml in set_bsml2:
                bsml2 = bsml.rstrip("bsml").rstrip(".")
                if bsml2 == file.rstrip(".zip"):
                    with ZipFile(file) as myzip:
                        with myzip.open('Experiment0/MeasurementContainer.xml') \
                             as myfile:
                            lines = myfile.readlines()

                            # List containing all elements beginning
                            # by "<EstimatedTime":
                            clean_lines = (line.strip().decode('utf8') for line
                                           in lines)

                            for elmt in clean_lines:                    
                                if "<EstimatedTime" in elmt:
                                    # duration needs to be a float
                                    duration = float(elmt.strip(
                                        '<EstimatedTime Unit="s" Value=/>'))
                                    # Duration * number of uses of each program
                                    durations = duration * compteur[bsml]
                                    # Adds durations to list 'estimated_time'
                                    estimated_time.append(durations)
                                    
        # Sums all durations and constants in 'tot_duration':
        tot_duration = sum(estimated_time) + load_1st_sample \
                + setpower_et_gonio \
                + (unload_load + descente_bras_gonio) * (len(liste_bsml) - 1) \
                + unload_last_sample

        # Counts sums of days/hours/minutes/seconds that must be floats:
        sum_days = int(tot_duration / (3600 * 24))
        sum_hours = int(tot_duration / 3600 - (sum_days * 24))
        sum_mins = int((tot_duration / 60) - (sum_hours * 60) -
                       (sum_days * 24 * 60))
        sum_secs = int(tot_duration - (sum_mins * 60) - (sum_hours * 3600) -
                       (sum_days * 3600 * 24))
       

        # Displays current date and hour:
        date = datetime.now()

        print(date.strftime('Date actuelle = %d/%m/%Y, %H:%M:%S'), "\n\n")


        # Displays a message:
        msg = "Les analyses doivent se terminer dans: "
        if sum_days:
            msg += f"{sum_days} jour(s) "
        if sum_hours:
            msg += f"{sum_hours} heure(s) "
        msg += f"{sum_mins} minutes {sum_secs} secondes.\n"
        print(msg)


        # Calculates end of analyses by adding all durations to current date
        # and time
        endtime = date + timedelta(days=sum_days, hours=sum_hours,
                                   minutes=sum_mins, seconds=sum_secs)

        print("Fin des analyses prévue le: "
              f"{endtime.strftime('%d/%m/%Y à %H:%M:%S')}")
        break   


    # End of block n°3, if 'file_xjob' doesn't exist we repeat the code between
    # block n°2 and block n°10, otherwise we exit loop 'while' (block n°2)
    else:
        print("Ooops! Le fichier tapé n'existe pas, recommençons.")



# Displays program duration in seconds with 2 digits after the decimal point,
# this will be removed in the final program
end = time.time()
print(f"\n\n\n\n\nDurée du programme = {round((end - start), 2)} secondes")


input("\nAppuyer sur la touche 'Entrée' pour quitter le programme...")

##################################    END    ##################################
