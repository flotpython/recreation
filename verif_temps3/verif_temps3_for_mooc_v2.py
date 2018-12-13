# -*- coding: utf-8 -*-
#!/usr/bin/python3.6
# Program "verif_temps3_for_mooc_v2.py"

# Preamble (updated):
"""
This is an update of my program "verif_temps3_for_mooc.py".

I changed different things you told me in the issue related to 'verif_temp3':
- I put paths in variables just after the different imports,
- I tried to remove all global variables, there's still one in function n°2
'input_file_xjob' used to start counting duration of this program,
but I'll probably delete it in my final version.
- I removed the method 'exit()' in function 'input_file_xjob'
- I changed the code to display things with the method center()
- I used the method 'intersection()' in function n°5 'verif_characters'
to find unwanted characters in both sets
- I removed function 'verif_trigrammes' to avoid using a global variable and
I put the code in function n°6 'verif_numerotation'.
- I also removed last big function because I found the method 'timedelta'
(I use it on 2 lines in function n°10) and I could reduce function
'total_duration_time' by removing all conditions on months.
- I tried to put some 'return' in my functions, but as they contain functions
if I put a 'return' somewhere, the function ends... and I want it to launch
next function (with parameters).

Thank you for your comments and I would appreciate if you could criticize /
review my code again ! :-)
"""

# To explain you the context:
"""
I'm working in a chemical laboratory of the CNRS as engineer assistant,
my colleague and I manage 2 diffractometers in our scientific service.
Many samples are analyzed on one of them.
Each day: people prepare samples in holders, then we check them and put them
inside the diffractometer. We program them on the driving software and analyses
are done during the night (thanks to the autochanger, a robot that puts samples
in position under the X-ray beam).

We use different small "house" programs to check the existence of files,
send results files by email, print results (with a network printer),
translate files, copy files on a server... All these programs were coded
in Fortran by a retired researcher and I need to adapt them in Python (I really
don't want to learn how to use Fortran).

I already did a first program to automatically send results files to people,
by typing their trigram (3 letters), because everybody in my lab has a trigram
and an email address (with the same string after the '@').
It works but it can be improved too, I will modify it later.
"""

# About this program:
"""
Now I'm doing a house program to check that sample numbers have not been
analyzed before, because if it appends we'll lose lot of time to manage
our database (we keep all diffractograms from 1999).
So the aim of this program is to check sample numbers, trigrams, unwanted
characters, each sample number must respect a format, the existence of 'bsml'
files which are created by our driving software, and at the end we want to know
when all analyses are finished. We also want to know when there is an error.

This program contains 10 functions and only the 2 first are launched at the end
because other functions are launched from the second one. By this way, I avoid
using global variables.

Each function is documented (I hope enough) but I need to add that 'xjob' file
is an XML file containing all information typed in the driving software among:
sample position, number and description, 'bsml' experiment filename,
sample-holder, username and user group. One 'xjob' file can contain between 1
and N programmed samples (often less than 30).
Brut data files are saved with 'brml' extensions, but they are converted into
'raw' files with another program.
The only way to open 'bsml' experiment files when we don't have the driving
software on our computer is to replace 'bsml' extension by 'zip'. We can find
XML files inside the 'zip' where we get the duration of each 'bsml' file.
"""

# 10 functions (updated):
"""
- First function only displays last modification of this file (if it exists)
otherwise a try/except catches the exception 'FileNotFoundError'
- In second one we ask user to type 'xjob' filename without its extension and
we start counting duration of the program
- Then third function checks the existence of this 'xjob' filename
- 4th function opens this file and cleans lines
- Functions 5 and 6 check unwanted characters, sample numbers formats and
trigrams
- Functions 7 and 8 check the existence of these numbers in our database and
'bsml' experiment files
- Function 9 fix an error when 'bsml' filename has a space, copy 'bsml' files
in a folder and convert them into 'zip' files. There are 2 conditions because
if the folder is empty (at the beginning) it doesn't work.
- Function 10 calculates durations of each 'bsml', adds them with constants
to current date and time to determine the estimated end date & time
of all analyses. Then it displays results under format:
"Fin des analyses prévue le: dd/mm/yyyy à HH:MM:SS"

- At the end: programs counts and displays its duration (few seconds),
depending on the number of programmed analyses.

I won't add the display of my program when it's well-executed (with errors),
because the display has not changed significantly.
"""


###############################################################################
######################## IMPORTS, Prints and VARIABLES ########################
###############################################################################
"""
Change paths below if this program's filename changed or if 'repbase' and
'repcible' are different.
"""

import os
import sys
import shutil
import pathlib
import time

from zipfile import ZipFile
from datetime import datetime
from datetime import timedelta


print(f"\n{' Démarrage du programme *.py '.center(78, '=')}\n")

# These variables need to be checked, if they aren't correct program won't work
this_prog_name = 'verif_temps3_for_mooc_v2.py'

# This is the working repertory that will be changed in last function (n°10)
repbase = "D:/Programmes/PYTHON/verif_temps3"

# This following folder needs to be created if it doesn't exist
repcible = "D:/Programmes/PYTHON/verif_temps3/Temp"

# This variable contains the path to file 'trigrammes.txt' (function n°6)
lien_trigrammes = "P:/Services/SINF/Trigrammes personnels/trigrammes.txt"

# These 2 following variables are used in function n°7 'verif_doublons'
rep_D8 = 'Y:\Data_Bruker_D8\Archives\Test_doublons_D8'
rep_D5005 = 'Y:\D5005\Data_D5005_Bruker\Archives\Test_doublons'

# If '*.py' file isn't in the correct folder
os.chdir (repbase)
print(os.getcwd())


###############################################################################
###############################  Function n°1  ################################
###############################################################################
def last_modification_file(this_prog_name):
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

    return
    

###############################################################################
###############################  Function n°2  ################################
###############################################################################
def input_file_xjob():
    """
    Asks user to type name of xjob file (without extension).
    Starts counting duration of this program after input, so we need a global
    variable 'start'. This value will be used at the end of the program.
    Then function 'verif_nom_fichier_xjob' is launched.
    """

    global start

    file_xjob = input("\nTaper le nom du fichier xjob sans l'extension: ")

    # Starts counting duration of this program
    start = time.time()

    file_xjob += '.xjob'

    
    verif_nom_fichier_xjob(file_xjob)


###############################################################################
###############################  Function n°3  ################################
###############################################################################
def verif_nom_fichier_xjob(file_xjob):
    """
    Checks if xjob filename exists in the specified directory.
    If it exists, 'open_file_xjob' is launched. Otherwise it returns an error
    message and function 'input_file_xjob' is launched again.
    """

    print(f"\n\n{' vérifie le nom du fichier xjob saisi '.center(78, '=')}\n")

    # Directory to modify if necessary: should contain all xjob files !
    liste_fichiers = (fichier for fichier in os.listdir(repbase)
                      if fichier.endswith('.xjob'))
    
    if file_xjob in liste_fichiers:
        print(file_xjob)
        open_file_xjob(file_xjob)
    else:
        print("Ooops! Le fichier tapé n'existe pas, recommençons.")
        input_file_xjob()


###############################################################################
###############################  Function n°4  ################################
###############################################################################
def open_file_xjob(file_xjob):
    """
    Opens *.xjob file after checking typed filename (if it exists). 
    Firstable, lines in *.xjob file are cleaned. Each value typed in
    "SamplePosition", "RawFile", "SampleID", "ExperimentFile", "Sample_holder",
    "User", "Group", "Price" and "Comment" are copied/pasted
    in 'cleaned2' list.
 
    Finally, function 'verif_characters' is launched.
    """
   
    with open(file_xjob) as f:
        # Beware! *.xjob file should be in the working directory. If it isn't,
        # an 'os.chdir' can be necessary.
        lines = f.readlines()
        clean_lines = (line.strip() for line in lines)

        # We need a better cleaning by removing '<CellValue>' and '</':
        cleaned2 = [elmt.strip('<CellValue>').strip('</')
                    for elmt in clean_lines
                    if elmt.startswith('<CellValue>')]


    # As a result: all sample numbers to test and *.bsml programs used are in
    # 'cleaned2' list.

    verif_characters(cleaned2)


###############################################################################
###############################  Function n°5  ################################
###############################################################################
def verif_characters(cleaned2):
    """
    Joins all characters from 'cleaned2' list to copy them into a new set 
    called 'set_all_cleaned2'.
    Checks if unwanted characters are present in 'set_all_cleaned2'.
    If it is the case, it returns an error message and this function starts
    counting errors (n_error variable is defined).

    Then function 'verif_numerotation' is launched.
    """

    result = set()
    n_errors = 0
    caracteres_speciaux = {'"', "'", "°", "à", "é", "è", "ù", "â", "ê", "î", 
"ô", "û", "ç", "ä", "ë", "ï", "ö", "ü", "@", "#", "&", "^", "~", "<", ">", 
"$", "€", "£", "¤", ";", "!"}


    print(f"\n\n{' vérifie les caractères spéciaux '.center(78, '=')}\n")

    set_all_cleaned2 = set([''.join(a.split()) for elmt in cleaned2
                            for a in elmt])

    result = caracteres_speciaux.intersection(set_all_cleaned2)
    
    if result != set():
        n_errors = len(result)
        print(f"{n_errors} erreur(s): {result}\n"
              "Merci de vérifier les caractères saisis dans la description "
              "de l'échantillon ou dans le nom de l'utilisateur.")
        print(f"\nCaractères non désirés: {caracteres_speciaux}")
    else:
        pass


    verif_numerotation(cleaned2, n_errors)
 

###############################################################################
###############################  Function n°6  ################################
###############################################################################
def verif_numerotation(cleaned2, n_errors):
    """
    Checks that programmed sample numbers comply with formats 'AAA-A-999-99-'
    or 'AAA-9-999-99-' with 'XRD-99' or 'HTD-99' extension,
    otherwise it returns an error message.
    
    Then if trigram (corresponding to the 3 first letters of each sample 
    number) is uppercased, opens 'trigrammes.txt' file and checks that
    all trigrams typed in '*.xjob' file exist.
    Otherwise it returns an error message.
    
    At the end, this function displays number of programmed analyses and 
    launches function 'verif_doublons'.
    """
    
    message_nbre_caracteres = "Erreur: mauvais nombre de caractères dans \
le nom de fichier ! Probablement 1 caractère en trop ou 1 caractère \
en moins... \n"
    message_non_conforme = "Erreur: au moins un des caractères saisis lors de \
la programmation de l'échantillon n'est pas conforme au format \
'AAA-A-999-99-' ou 'AAA-9-999-99-' avec l'extension 'XRD-99' ou 'HTD-99'. \n"
    message_trigramme_inconnu = "Erreur: le trigramme est inconnu ou \
appartient à une personne externe au laboratoire."


    print(f"""\n\n{" vérifie les numéros d'échantillon ".center(78, '=')}\n""")

    # 'liste_brml' contains all sample numbers of xjob file,
    # from trigram to '.brml' extension:
    liste_brml = [a[14:] for a in cleaned2 if a.startswith("D:\\raw_(brml)\\")]


    for filename in liste_brml:
        trigramme, num, ext = filename[:3], filename[3:19], filename[19:]

        if not trigramme[0].isupper() or not trigramme[1].isupper() \
           or not trigramme[2].isupper():
            pass
        
        else:
            with open(lien_trigrammes) as f:
                lines = f.readlines()

                liste_trigrammes = (line.strip('\n').split(', ')[0]
                                    for line in lines)
                
            if trigramme not in liste_trigrammes:
                n_errors += 1
                print(f"{trigramme} \n{message_trigramme_inconnu} \n")
  
            
        if len(filename) != 24:
            n_errors += 1
            print(filename)
            print(f"{message_nbre_caracteres}")

        elif (num[0] and num[2] and num[6] and num[9] and num[13]) is '-' \
           and (num[3:6] + num[7:9] + num[14:]).isdigit() \
           and (num[1] + trigramme).isupper() \
           and num[10:13] == ("XRD" or "HTD"):
            pass

        elif (num[0] and num[2] and num[6] and num[9] and num[13]) is '-' \
           and (num[1] + num[3:6] + num[7:9] + num[14:]).isdigit() \
           and trigramme.isupper() and num[10:13] == ("XRD" or "HTD"):
                pass

        else:
            n_errors += 1
            print(f"{filename} \n{message_non_conforme}")

        if filename[-5:] != '.brml':
            n_errors += 1
            print(filename)
            print(f"Erreur: l'extension rentrée '{ext}' est différente "
                  "de '.brml'. \n")

    print(' ')
    print(f"""{" compte le nombre d'analyses programmées ".center(78, '=')}"""
          f"""\n\nNombre d'analyses programmées: {len(liste_brml)}""")


    verif_doublons(liste_brml, cleaned2, n_errors)

                                 
###############################################################################
###############################  Function n°7  ################################
###############################################################################
def verif_doublons(liste_brml, cleaned2, n_errors):
    """
    Checks if sample numbers already exist on 'Y:\' server, in 'Test doublons'
    folders related to D5005 and D8 diffractometers.
    Otherwise it returns an error message.
    Then in all cases function 'verif_bsml' is launched.
    """

    print(f"\n\n{' vérifie les doublons '.center(78, '=')}\n")

    # All files ending with '.raw' from 'rep_D8' are pasted into this new list
    liste_analyses_D8_depuis_2010 = [file for file in os.listdir(rep_D8)
                                     if file.endswith('.raw')]

    # All filenames from 'rep_D5005' are pasted into this new list, but all
    # characters are capitalized
    liste_old_analyses_D5005 = [old_file.upper() for old_file
                                in os.listdir(rep_D5005)]
    
    # 'liste_brml2' is created with a generating expression (bit-efficient)
    liste_brml2 = (brml[:-5] for brml in liste_brml)

    for brml2 in liste_brml2:
        # If file already exists in rep_D8 directory
        if brml2 + '.raw' in liste_analyses_D8_depuis_2010:
            n_errors += 1
            print("Erreur: le numéro", brml2, "existe déjà dans la base de "
                  "données du D8. Merci d'en attribuer un autre ou "
                  "d'incrémenter l'extension après 'XRD'. \n")
            continue        # continues with the next iteration of the loop

        if brml2 + '.RAW' in liste_old_analyses_D5005:
            # = old diffractograms
            n_errors += 1
            print("Erreur: le numéro", brml2, "existe déjà dans la base de "
                  "données du D5005. Merci d'en attribuer un autre ou "
                  "d'incrémenter l'extension après 'XRD'. \n")


    verif_bsml(cleaned2, n_errors)


###############################################################################
###############################  Function n°8  ################################
###############################################################################
def verif_bsml(cleaned2, n_errors):
    """
    Firstable, this function checks that *.bsml program exists in the 
    specified directory, otherwise it returns an error message.
    
    Then it saves *.bsml filenames in a list called 'liste_bsml',
    but only if filenames are different from each other.
    Finally, function 'bsml_to_zip' is launched.
    """

    liste_bsml = []
    
    for a in cleaned2:
        # For each element 'a', we start looking for those which begin by
        # 'D:\Bruker_nov2012\'
        if a.startswith("D:\\Bruker_nov2012\\"):
            
            # String under format 'Prog_4-80-0,02-0,5_STANDARD_couteau-auto.'
            string_bsml = a.strip("D:\\Bruker_nov2012\\DIFFDAT\\bsml")
            
            # String under format
            # 'Prog_4-80-0,02-0,5_STANDARD_couteau-auto.bsml'
            string_bsml2 = string_bsml + "bsml"

            if string_bsml2 not in os.listdir(repbase):
                # This repertory needs to be modified when repertory
                # containing bsml files is changed
                n_errors += 1
                print(f"Erreur: le fichier {string_bsml2} n'existe pas dans "
                      f"le répertoire {repbase}.\n")
            else:
                # We add each string_bsml2 to 'liste_bsml' which contains all
                # programs
                liste_bsml.append(string_bsml2)


    bsml_to_zip(liste_bsml, n_errors)


###############################################################################
###############################  Function n°9  ################################
###############################################################################
def bsml_to_zip(liste_bsml, n_errors):
    """
    Firstable, different variables are created.
    'bsml' filenames with spaces are processed in this function because they're
    splitted into 2 elements in 'liste_bsml': one starting by 'Prog_' and
    one finishing by 'bsml'. These elements are joined together and
    the new element is added in 'liste_bsml'. Splitted elements are deleted.

    'liste_bsml' is converted into a set called 'set_bsml2'.
    By this way all doublons are deleted, which means that 'set_bsml2' only
    contains different 'bsml' files. Indeed, this function checks
    if these files (with '.zip' extension instead of 'bsml') already exist
    in the folder 'Temp'.
    
    Then this function copies '*.bsml' files from 'set_bsml2' to folder 'Temp'
    if these files don't already exist.
    '*.bsml' files are then converted into '*.zip'. 
    When it's done, function 'total_duration_time' is launched.
    """
    
    # Lists and variables
    liste_zip = []
    liste_zip_i = []
    a = 0
    bsml_tmp1 = ""
    bsml_tmp2 = ""

    
    bsml_temp = [bsml for bsml in liste_bsml if not (bsml.startswith("Prog")
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

        # Deletes bsml if it starts with "Prog_" but doesn't end with "bsml"
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
            
        # We remove '.bsml' extension of each 'bsml' file to convert it later
        # into '.zip'
        liste_file = [bsml.rstrip("bsml").rstrip(".") for bsml in set_bsml2]

        for file2 in liste_file:
            zip_file = file2 + ".zip"
            # Repertory + filename to rename
            bsml_dir = repcible + '/' + file2 + ".bsml"
            # Repertory + filename renamed
            zip_dir = repcible + '/' + zip_file 

            if (file2 + ".bsml") in os.listdir(repcible):
                # File *.bsml is renamed in *.zip to open it later
                os.rename(bsml_dir, zip_dir)


    ##### 2nd big condition: if there is at least 1 file in 'Temp' folder #####
    else:
        liste_zip.extend(os.listdir(repcible))

        for file in os.listdir(repcible):
            cible = pathlib.PurePosixPath(repcible, file)
            # Add filenames without extensions in 'liste_zip_i' from
            # repertory 'repcible':
            liste_zip_i.append('{}'.format(cible.stem))
            
        # We remove '.bsml' extension to convert the file into '.zip'
        liste_file = [bsml.rstrip("bsml").rstrip(".") for bsml in set_bsml2]
            
        # If file doesn't exist in 'liste_zip_i', so 'bsml' program has to copy
        # file in 'file3_bsml'
        file3_bsml = [file2 + ".bsml" for file2 in liste_file if file2 \
                      not in liste_zip_i]
                            
        for f in os.listdir(repbase):
            # src = 'repbase' repertory + filename
            src = pathlib.PurePosixPath(repbase, f)
            # cible = 'repcible' repertory + filename
            cible = pathlib.PurePosixPath(repcible, f)
            
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

                        
    total_duration_time(liste_bsml, set_bsml2, n_errors)
    
        
###############################################################################
###############################  Function n°10 ################################
###############################################################################
def total_duration_time(liste_bsml, set_bsml2, n_errors):
    """
    Firstable, this function counts number of errors occurred in this program
    and displays a message.
    
    Then it counts number of 'bsml' programs to use and put data
    in a dictionary.
    Next it opens *.zip files saved in folder 'Temp' to get the duration of
    each program, which is included in an XML file. This duration is multiplied
    by number of program uses and it is added to 'estimated_time' list.
    
    Constants are added to the duration of all analyses: loading/unloading of 
    each sample-holder, time to set work power on the diffractometer, time for
    arms of the goniometer to move down and be in position for the beginning 
    of the analyse...
    
    The current date and time are integrated to the function to determine the
    estimated end date & time of all analyses. This is displayed at the end.
    """

    #### Lists:
    estimated_time = []

    #### Constants:
    # Loading first sample (22s)
    load_1st_sample = 22
    # Time to set work power + arms of the goniometer moving in position (15s)
    setpower_et_gonio = 15
    # arms of the goniometer moving in position
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

    # Counts duplicates of programs in 'liste_bsml' and puts data in a dict:
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
    tot_duration = sum(estimated_time) + load_1st_sample + setpower_et_gonio \
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


    # Calculates end of analyses by adding all durations to current date/time
    endtime = date + timedelta(days=sum_days, hours=sum_hours,
                               minutes=sum_mins, seconds=sum_secs)

    print("Fin des analyses prévue le: "
          f"{endtime.strftime('%d/%m/%Y à %H:%M:%S')}")

    return endtime

   
#############################################################################
############################ Functions to launch ############################
#############################################################################
"""
Only 2 functions are launched to avoid using global variables.
At the end, the duration of this program execution is displayed (this will be
removed in the final program).

To exit this program, the user needs to press the 'Enter' key.
"""

last_modification_file(this_prog_name)
input_file_xjob()


# Displays program duration in seconds with 2 digits after the decimal point:
end = time.time()
print(f"\n\n\n\n\nDurée du programme = {round((end - start), 2)} secondes")


input("\nAppuyer sur la touche 'Entrée' pour quitter le programme...")


##################################    END    ##################################
