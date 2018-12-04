# -*- coding: utf-8 -*-
#!/usr/bin/python3.6
# Program "verif_temps3_for_mooc.py"

# Preamble:
"""
This is a cleaned version of my program to show you my code because I'm sure
it can be improved (maybe with classes?).
I already removed many 'global' variables and I reduced pieces of this code.
I modified this code by learning from the excellent MOOC on Python :-)

Please don't hesitate to criticize/review this code and ask for everything
you find weird !
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

This program contains 12 functions and only the 2 first are launched at the end
because other functions are launched from the second one.
I don't know if it's the best solution in terms of bit-efficiency, but in the
first version of this program I launched all functions at the end.

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

# 12 functions:
"""
- First function only displays last modification of this file
- In second one we ask user to type 'xjob' filename without its extension and
we start counting duration of the program
- Then third function checks the existence of this 'xjob' filename
- 4th function opens this file and cleans lines
- Functions 5, 6 and 7 check unwanted characters, sample numbers formats and
trigrams
- Functions 8 and 9 check the existence of these numbers in our database and
'bsml' experiment files
- Function 10 fix an error when 'bsml' filename has a space, copy 'bsml' files
in a folder and convert them into 'zip' files. There are 2 conditions because
if the folder is empty (at the beginning) it doesn't work.
- Function 11 calculates durations of each program, adds them with constants
to current date and time to determine the estimated end date & time
of all analyses.
- Function 12 is used to display the result of last function under format:
"Fin des analyses prévue le: dd/mm/yyyy, vers HH:MM:SS"
with minutes and seconds on 2 digits, because I had only 1 digit
when minutes or seconds were lower than 10. I don't mind for hours.
I know this can be improved with hour formats but I don't know exactly how.
- At the end: programs counts and displays its duration (between 1.5 and
2 seconds) on my computer

I will add a display of my program when it's well-executed (with errors).
"""


# Different imports:
import os
import sys
import shutil
import pathlib
import time

from zipfile import ZipFile
from datetime import datetime

os.chdir ('D:/Programmes/PYTHON/verif_temps3')

print(f"\n{23*'='}  Démarrage du programme *.py  {24*'='}\n")
print(os.getcwd())


###############################################################################
###############################  Function n°1  ################################
###############################################################################
def last_modification_file():
    """
    Displays last modification of *.py file
    """
    
    path = pathlib.Path('verif_temps3_for_mooc.py')
    mtime = path.stat().st_mtime
    mtime_datetime = datetime.fromtimestamp(mtime)
    
    print(f"Dernière modification du fichier *.py le {mtime_datetime:%d/%m}/20"
          f"{mtime_datetime:%y} ({mtime_datetime:%H:%M}) \n")
    

###############################################################################
###############################  Function n°2  ################################
###############################################################################
def input_file_xjob():
    """
    Asks user to type name of xjob file (without extension). 
    If user presses the 'Enter' key, program ends. 
    Otherwise 'verif_nom_fichier_xjob()' is launched.
    """
    
    global start

    file_xjob = input("\nTaper le nom du fichier xjob sans l'extension\n"
                      "(Appuyer sur 'Entrée' pour quitter le programme): ")

    if file_xjob is '':    # If user presses the 'Enter' key, program ends
        exit()
    else:
        file_xjob += '.xjob'
        # Starts counting duration of this program
        start = time.time()
        verif_nom_fichier_xjob(file_xjob)


###############################################################################
###############################  Function n°3  ################################
###############################################################################
def verif_nom_fichier_xjob(file_xjob):
    """
    Checks if xjob filename exists in the specified directory.
    If it exists, 'open_file_xjob()' is launched. Otherwise it returns an error
    message and function 'saisir_file_xjob()' is launched again.
    """

    print(f"\n\n{19*'='}  vérifie le nom du fichier xjob saisi  {19*'='}\n")

    # Directory to modify if necessary: should contain all xjob files !
    liste_fichiers = (fichier for fichier
                      in os.listdir('/Programmes/PYTHON/verif_temps3')
                      if fichier.endswith('.xjob'))
    
    if file_xjob in liste_fichiers:
        print(file_xjob)
        open_file_xjob(file_xjob)
    else:
        print("Ooops! Le fichier tapé n'existe pas, recommençons.")
        saisir_file_xjob()


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
 
    Finally, 'verif_characters()' is launched.
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
    Checks if unwanted characters are present in 'cleaned2' list.
    If it is the case, it returns an error message.
    
    n_error variable is defined to start counting errors.
    Then in all cases, 'verif_numerotation()' is launched.
    """
    
    n_errors = 0
    caracteres_speciaux = {'"', "'", "°", "à", "é", "è", "ù", "â", "ê", "î", 
"ô", "û", "ç", "ä", "ë", "ï", "ö", "ü", "@", "#", "&", "^", "~", "<", ">", 
"$", "€", "£", "¤", ";", "!"}

    print(f"\n\n{21*'='}  vérifie les caractères spéciaux  {22*'='}\n")

    for carac in caracteres_speciaux:
        for a in cleaned2:
            # cleaned2 list contains all positions, sample numbers and programs
            # repertories, sample descriptions, sample-holder numbers, user
            # first/last names and team, price, comment (automatic knife) and
            # 'ANR' name if it is filled.
            if carac in a:
                print(f"{carac} dans '{a}'")
                n_errors += 1
                
    if n_errors > 0:
        print("\nErreur: merci de vérifier les caractères saisis dans la "
              "description de l'échantillon ou dans le nom de l'utilisateur.")
        print(f"\nCaractères non désirés: {caracteres_speciaux}")

            
    verif_numerotation(cleaned2, n_errors)
 

###############################################################################
###############################  Function n°6  ################################
###############################################################################
def verif_numerotation(cleaned2, n_errors):
    """
    Checks that programmed sample numbers comply with formats 'AAA-A-999-99-'
    or 'AAA-9-999-99-' with 'XRD-99' or 'HTD-99' extension,
    otherwise it returns an error message.
    
    Then, if trigram (corresponding to the 3 first letters of each sample
    number) is uppercased, function 'verif_trigramme()' is launched.
    At the end, 'verif_numerotation()' counts number of programmed analyses
    and launches function 'verif_doublons()'.
    """
    
    message_nbre_caracteres = "Erreur: mauvais nombre de caractères dans \
le nom de fichier ! Probablement 1 caractère en trop ou 1 caractère \
en moins... \n"
    message_non_conforme = "Erreur: au moins un des caractères saisis lors de \
la programmation de l'échantillon n'est pas conforme au format \
'AAA-A-999-99-' ou 'AAA-9-999-99-' avec l'extension 'XRD-99' ou 'HTD-99'. \n"


    print(f"\n\n{20*'='}  vérifie les numéros d'échantillon  {21*'='}\n")

    # 'liste_brml' contains all sample numbers of xjob file,
    # from trigram to '.brml' extension:
    liste_brml = [a[14:] for a in cleaned2 if a.startswith("D:\\raw_(brml)\\")]


    for filename in liste_brml:
        trigramme, num, ext = filename[:3], filename[3:19], filename[19:]

        if not trigramme[0].isupper() or not trigramme[1].isupper() \
           or not trigramme[2].isupper():
            pass
        else:
            verif_trigramme(trigramme)
            
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

    print(f"\n\n{17*'='}  compte le nombre d'analyses programmées  {18*'='}\n"
          f"\nNombre d'analyses programmées: {len(liste_brml)} \n")

    
    verif_doublons(liste_brml, cleaned2, n_errors, trig_error)
    
    
###############################################################################
###############################  Function n°7  ################################
###############################################################################
def verif_trigramme(trigramme):
    """
    Opens 'trigrammes.txt' file and checks that all trigrams
    typed in '*.xjob' file exist, otherwise it returns an error message.
    """

    global trig_error

    trig_error = 0
    message_trigramme_inconnu = "Erreur: le trigramme est inconnu ou \
appartient à une personne externe au laboratoire."
	
    with open("P:/Services/SINF/Trigrammes personnels/trigrammes.txt") as f:
        lines = f.readlines()
        liste_trigrammes = (line.strip('\n').split(', ')[0] for line in lines)
	
    if trigramme not in liste_trigrammes:
        trig_error += 1
        print(f"{trigramme} \n{message_trigramme_inconnu} \n")

                                 
###############################################################################
###############################  Function n°8  ################################
###############################################################################
def verif_doublons(liste_brml, cleaned2, n_errors, trig_error):
    """
    Checks if sample numbers already exist on 'Y:\' server, in 'Test doublons'
    folders related to D5005 and D8 diffractometers.
    Otherwise it returns an error message.
    Then in all cases 'verif_bsml()' is launched.
    """

    rep_D8 = 'Y:\Data_Bruker_D8\Archives\Test_doublons_D8'
    rep_D5005 = 'Y:\D5005\Data_D5005_Bruker\Archives\Test_doublons'

    print(f"\n\n{27*'='}  vérifie les doublons  {27*'='}\n")

    # All files ending with '.raw' from 'rep_D8' are pasted into this new list
    liste_analyses_D8_depuis_2010 = [file for file in os.listdir(rep_D8)
                                     if file.endswith('.raw')]

    # All filenames from 'rep_D5005' are pasted into this new list, but all
    # characters are capitalized
    liste_old_analyses_D5005 = [old_file.upper() for old_file
                                in os.listdir(rep_D5005)]
    
    # 'liste_brml2' is created with a generating expression (bit-efficient)
    liste_brml2 = (brml[:-4] for brml in liste_brml)

    for brml2 in liste_brml2:
        # If file already exists in rep_D8 directory
        if brml2 + 'raw' in liste_analyses_D8_depuis_2010:
            n_errors += 1
            print("Erreur: le numéro", brml2, "existe déjà dans la base de "
                  "données du D8. Merci d'en attribuer un autre ou "
                  "d'incrémenter l'extension après 'XRD'. \n")
            continue

        if brml2 + 'RAW' in liste_old_analyses_D5005:
            # = old diffractograms
            n_errors += 1
            print("Erreur: le numéro", brml2, "existe déjà dans la base de "
                  "données du D5005. Merci d'en attribuer un autre ou "
                  "d'incrémenter l'extension après 'XRD'. \n")


    verif_bsml(cleaned2, n_errors, trig_error)


###############################################################################
###############################  Function n°9  ################################
###############################################################################
def verif_bsml(cleaned2, n_errors, trig_error):
    """
    Firstable, this function checks that *.bsml program exists in the 
    specified directory, otherwise it returns an error message.
    
    Then it saves *.bsml filenames in a list called 'liste_bsml',
    but only if filenames are different from each other.
    Finally, 'bsml_to_zip()' is launched.
    """
    
    liste_bsml = []

    print(f"\n\n{18*'='}  vérifie l'existence des fichiers bsml  {19*'='}\n")
    
    for a in cleaned2:
        # For each element 'a', we start looking for those which begin by
        # 'D:\Bruker_nov2012\'
        if a.startswith("D:\\Bruker_nov2012\\"):
            
            # String under format 'Prog_4-80-0,02-0,5_STANDARD_couteau-auto.'
            string_bsml = a.strip("D:\\Bruker_nov2012\\DIFFDAT\\bsml")
            
            # String under format
            # 'Prog_4-80-0,02-0,5_STANDARD_couteau-auto.bsml'
            string_bsml2 = string_bsml + "bsml"

            if string_bsml2 not in \
               os.listdir('D:/Programmes/PYTHON/verif_temps3'):
                # This repertory needs to be modified when repertory
                # containing bsml files is changed
                n_errors += 1
                print("Erreur: le fichier", string_bsml2, "n'existe pas dans "
                      "le répertoire 'D:\\Programmes\\PYTHON\\verif_temps3.\n")
            else:
                # We add each string_bsml2 to 'liste_bsml' which contains all
                # programs
                liste_bsml.append(string_bsml2)


    bsml_to_zip(liste_bsml, n_errors, trig_error)


###############################################################################
##############################  Function n°10  ################################
###############################################################################
def bsml_to_zip(liste_bsml, n_errors, trig_error):
    """
    Firstable, different variables are created.
    'bsml' filenames with spaces are processed in this function because they're
    splitted into 2 elements in 'liste_bsml': one starting by 'Prog_' and
    one finishing by 'bsml'. These elements are joined and the new element is
    added in 'liste_bsml'. Splitted elements are deleted.

    'liste_bsml' is converted into a set called 'set_bsml2'.
    By this way all doublons are deleted, which means that 'set_bsml2' only
    contains different 'bsml' files. Indeed, this function checks
    if these files (with '.zip' extension instead of 'bsml') already exist
    in the folder 'Temp'.
    
    Then this function copies '*.bsml' files from 'set_bsml2' to 'Temp'
    folder if these files don't already exist.
    '*.bsml' files are then converted into '*.zip'. 
    When it's done, 'total_duration_time()' is launched.
    """
    
    # Lists and variables
    liste_zip = []
    liste_zip_i = []
    a = 0
    bsml_tmp1 = ""
    bsml_tmp2 = ""
    repbase = "D:/Programmes/PYTHON/verif_temps3"
    # This following folder needs to be created if it doesn't exist:
    repcible = "D:/Programmes/PYTHON/verif_temps3/Temp"

    
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
        if not bsml.startswith("Prog_"):
            liste_bsml.remove(bsml)

    for bsml in liste_bsml:
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

        """These last few lines replaced this piece of code:
        liste_zip_i = [os.path.splitext(file)[0] for file in \
                       os.listdir(repcible)]"""
            
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
        # print("Des fichiers sont présents dans le dossier Temp.\n")
        liste_zip.extend(os.listdir(repcible))
        # print("liste_zip =", liste_zip, "\n")

        for file in os.listdir(repcible):
            cible = pathlib.PurePosixPath(repcible, file)
            # Add filenames without extensions in 'liste_zip_i' from
            # repertory 'repcible':
            liste_zip_i.append('{}'.format(cible.stem))
        
        # liste_zip_i = ['stem : {}'.format(cible.stem) for cible in \
                       # os.listdir(repcible)]
        # print(f"liste_zip_i = {liste_zip_i}\n")
            
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

                        
    total_duration_time(liste_bsml, repcible, n_errors, set_bsml2, trig_error)
    
        
###############################################################################
###############################  Function n°11 ################################
###############################################################################
def total_duration_time(liste_bsml, repcible, n_errors, set_bsml2, trig_error):
    """
    Firstable, this function counts number of errors occurred in this program
    and displays a message.
    
    Then it counts number of 'bsml' programs to use and put data
    in a dictionary.
    Next it opens *.zip files saved in folder 'Temp' to get the duration of
    each program, which is included in an XML file. This duration is multiplied
    by number of program uses and is added to 'estimated_time' list.
    
    Constants are added to the duration of all analyses: loading/unloading of 
    each sample-holder, time to set work power on the diffractometer, time for
    arms of the goniometer to move down and be in position for the beginning 
    of the analyse...
    
    The current date and time are integrated to the function to determine the
    estimated end date & time of all analyses.
    Finally this function launches the last function of this program
    which is called 'conditions_hour_min_sec'.
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
    

    os.chdir ('D:/Programmes/PYTHON/verif_temps3/Temp')

    print(f"\n\n{22*'='}  estime la date/l'heure de fin  {23*'='}\n")
    
    if (n_errors + trig_error) == 0:
        print('Aucune erreur détectée, bravo!!! \n')
    elif (n_errors + trig_error) > 0:
        print("ATTENTION: nombre d'erreurs détectées = "
              f"{n_errors + trig_error} \nMerci de vérifier et corriger "
              "les erreurs avant de lancer les jobs...\n\n")


    # Counts duplicates of programs in 'liste_bsml' and puts data in a dict:
    compteur = {f: liste_bsml.count(f) for f in set(liste_bsml)}

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
    sum_days = float(tot_duration / (3600 * 24))
    sum_hours = float(tot_duration / 3600 - (int(sum_days) * 24))
    sum_mins = float((tot_duration / 60) - (int(sum_hours) * 60) - \
                     (int(sum_days) * 24 * 60))
    sum_secs = float(tot_duration - (int(sum_mins) * 60) - \
                     (int(sum_hours) * 3600) - (int(sum_days) * 3600 * 24))

    # Displays current date and hour:
    date = datetime.now()
    year = date.year
    month = date.month
    day = date.day
    hour = date.hour
    minute = date.minute
    second = date.second
    print(f"Date actuelle = {day}/{month}/{year}, "
          f"heure = {date.strftime('%H:%M:%S')}\n\n")

    if int(sum_days) is 0:
        print("Les analyses doivent se terminer dans:", int(sum_hours),
              "heure(s)", int(sum_mins), "minutes", int(sum_secs),
              "secondes.\n")
    elif int(sum_hours) is 0:
        print("Les analyses doivent se terminer dans:", int(sum_mins),
              "minutes", int(sum_secs), "secondes.\n")
    else:
        print("Les analyses doivent se terminer dans:", int(sum_days),
              "jour(s)", int(sum_hours), "heure(s)", int(sum_mins), "minutes",
              int(sum_secs), "secondes.\n")


    # Adds previous sums to current day/hour/minute/second, these new variables
    # will be used in next function 'conditions_hour_min_sec()':
    sum_secs2 = second + int(sum_secs)

    sum_mins2 = minute + int(sum_mins) + 1 if (sum_secs2 >= 60) \
                else minute + int(sum_mins)    # = conditional expression

    sum_hours2 = hour + int(sum_hours) + 1 if (sum_mins2 >= 60) \
                 else hour + int(sum_hours)

    sum_days2 = day + int(sum_days) + 1 if (sum_hours2 >= 24) \
                else day + int(sum_days)


    ##########################################################################
    ### If current month is: JANUARY, MARCH, MAY, JULY, AUGUST, OCTOBER or ###
    ### DECEMBER                                                           ###
    ##########################################################################
    for chiffre in [1, 3, 5, 7, 8, 10, 12]:
        if month == chiffre:
        ### If analyses finish next month in: FEBRUARY, APRIL, JUNE,
            ### SEPTEMBER or NOVEMBER
            if sum_days2 > 31:
                month += 1
                conditions_hour_min_sec(sum_secs2, sum_mins2, sum_hours2,
                                        sum_days2, month, year)
            
            ### If current month is: JANUARY, MARCH, MAY, JULY, AUGUST, OCTOBER
            ### or DECEMBER
            else:
                conditions_hour_min_sec(sum_secs2, sum_mins2, sum_hours2,
                                        sum_days2, month, year)

    ###########################################################################
    ###################### If current month is: FEBRUARY ######################
    ###########################################################################
    if month is 2:
        ### If FEBRUARY is a leap year this year
        if year % 400 is 0 or (year % 4 is 0 and year % 100 != 0): 
            # print("L'année actuelle est bissextile. Ce mois a 29 jours.")
            conditions_hour_min_sec(sum_secs2, sum_mins2, sum_hours2,
                                    sum_days2, month, year)

        ### If FEBRUARY isn't a leap year this year
        else:
            # print("L'année actuelle n'est pas bissextile. Ce mois a
            # 28 jours.")
            conditions_hour_min_sec(sum_secs2, sum_mins2, sum_hours2,
                                        sum_days2, month, year)

    ###########################################################################
    ######### If current month is: APRIL, JUNE, SEPTEMBER or NOVEMBER #########
    ###########################################################################
    for chiffre in [4, 6, 9, 11]:
        if month == chiffre:
        ### If analyses finish next month in: MAY, JULY, OCTOBER or DECEMBER
            if sum_days2 > 30:
                month += 1
                for chiffre2 in [5, 7, 10, 12]:
                    if month == chiffre2:
                        # print("Ce mois a 31 jours")
                        conditions_hour_min_sec(sum_secs2, sum_mins2,
                                                sum_hours2, sum_days2,
                                                month, year)
         
            ### If current month is: APRIL, JUNE, SEPTEMBER or NOVEMBER
            else:
                # print("Ce mois a 30 jours\n")
                conditions_hour_min_sec(sum_secs2, sum_mins2, sum_hours2,
                                        sum_days2, month, year)
            

###############################################################################
###############################  Function n°12 ################################
###############################################################################
def conditions_hour_min_sec(sum_secs2, sum_mins2, sum_hours2, sum_days2,
                            month, year):
    """
    Tests conditions on hours/minutes/seconds for days of each month of
    the current year, to display the estimated end date of all analyses under
    format 'dd/mm/yyyy' and end time under format 'HH:MM:SS'.
    """

    # 2 conditional expressions to avoid display problems of seconds or minutes
    # on 1 digit (when < 10):
    sum_mins3 = '0' + str(sum_mins2 - 60) if 0 <= (sum_mins2 - 60) < 10 else \
        ('0' + str(sum_mins2) if sum_mins2 < 10 else sum_mins2)

    sum_secs3 = '0' + str(sum_secs2 - 60) if 0 <= (sum_secs2 - 60) < 10 else \
        ('0' + str(sum_secs2) if sum_secs2 < 10 else sum_secs2)


    #1 = beginning of first condition "if"
    #1f = end of first condition "else"
    
    if sum_hours2 < 24: #1
        print("Fin des analyses prévue le:",
              f"{sum_days2}/{month}/{year}", end = " ")
        if sum_mins2 < 60: #2
            if sum_mins2 < 10: #3
                if sum_secs2 < 60: #4
                    if sum_secs2 < 10: #5
                        print(f"vers {sum_hours2}:{sum_mins3}:{sum_secs3}")
                    else: #5f
                        print(f"vers {sum_hours2}:{sum_mins3}:{sum_secs2}")
                else: #4f
                    seconde = sum_secs2 - 60
                    if seconde < 10: #5
                        print(f"vers {sum_hours2}:{sum_mins3}:{sum_secs3}")
                    else: #5f
                        print(f"vers {sum_hours2}:{sum_mins3}:{seconde}")
            else: #3f
                if sum_secs2 < 60: #4
                    if sum_secs2 < 10: #5
                        print(f"vers {sum_hours2}:{sum_mins2}:{sum_secs3}")
                    else: #5f
                        print(f"vers {sum_hours2}:{sum_mins2}:{sum_secs2}")
                else: #4f
                    seconde = sum_secs2 - 60
                    if seconde < 10: #5
                        print(f"vers {sum_hours2}:{sum_mins2}:{sum_secs3}")
                    else: #5f
                        print(f"vers {sum_hours2}:{sum_mins2}:{seconde}")
        else: #2f
            minute = sum_mins2 - 60
            if minute < 10: #3
                if sum_secs2 < 60: #4
                    if sum_secs2 < 10: #5
                        print(f"vers {sum_hours2}:{sum_mins3}:{sum_secs3}")
                    else: #5f
                        print(f"vers {sum_hours2}:{sum_mins3}:{sum_secs2}")
                else: #4f
                    seconde = sum_secs2 - 60
                    if seconde < 10: #5
                        print(f"vers {sum_hours2}:{sum_mins3}:{sum_secs3}")
                    else: #5f
                        print(f"vers {sum_hours2}:{sum_mins3}:{seconde}") 
            else: #3f
                if sum_secs2 < 60: #4
                    if sum_secs2 < 10: #5
                        print(f"vers {sum_hours2}:{minute}:{sum_secs3}")
                    else: #5f
                        print(f"vers {sum_hours2}:{minute}:{sum_secs2}")
                else: #4f
                    seconde = sum_secs2 - 60
                    if seconde < 10: #5
                        print(f"vers {sum_hours2}:{minute}:{sum_secs3}")
                    else: #5f
                        print(f"vers {sum_hours2}:{minute}:{seconde}")
                           
    else: #1f
        heure = sum_hours2 - 24
        print("Fin des analyses prévue le:",
              f"{sum_days2}/{month}/{year}", end = " ")
        if sum_mins2 < 60: #2
            if sum_mins2 < 10: #3
                if sum_secs2 < 60: #4
                    if sum_secs2 < 10: #5
                        print(f"vers {heure}:{sum_mins3}:{sum_secs3}")
                    else: #5f
                        print(f"vers {heure}:{sum_mins3}:{sum_secs2}")
                else: #4f
                    seconde = sum_secs2 - 60
                    if seconde < 10: #5
                        print(f"vers {heure}:{sum_mins3}:{sum_secs3}")
                    else: #5f
                        print(f"vers {heure}:{sum_mins3}:{seconde}")
            else: #3f
                if sum_secs2 < 60: #4
                    if sum_secs2 < 10: #5
                        print(f"vers {heure}:{sum_mins2}:{sum_secs3}")
                    else: #5f
                        print(f"vers {heure}:{sum_mins2}:{sum_secs2}")
                else: #4f
                    seconde = sum_secs2 - 60
                    if seconde < 10: #5
                        print(f"vers {heure}:{sum_mins2}:{sum_secs3}")
                    else: #5f
                        print(f"vers {heure}:{sum_mins2}:{seconde}")
        else: #2f
            minute = sum_mins2 - 60
            if minute < 10: #3
                if sum_secs2 < 60: #4
                    if sum_secs2 < 10: #5
                        print(f"vers {heure}:{sum_mins3}:{sum_secs3}")
                    else: #5f
                        print(f"vers {heure}:{sum_mins3}:{sum_secs2}")
                else: #4f
                    seconde = sum_secs2 - 60
                    if seconde < 10: #5
                        print(f"vers {heure}:{sum_mins3}:{sum_secs3}")
                    else: #5f
                        print(f"vers {heure}:{sum_mins3}:{seconde}")
            else: #3f
                if sum_secs2 < 60: #4
                    if sum_secs2 < 10: #5
                        print(f"vers {heure}:{minute}:{sum_secs3}")
                    else: #5f
                        print(f"vers {heure}:{minute}:{sum_secs2}")
                else: #4f
                    seconde = sum_secs2 - 60
                    if seconde < 10: #5
                        print(f"vers {heure}:{minute}:{sum_secs3}")
                    else: #5f
                        print(f"vers {heure}:{minute}:{seconde}")

   
#############################################################################
############################ Functions to launch ############################
#############################################################################

last_modification_file()
input_file_xjob()


end = time.time()
# Displays program duration in seconds with 2 digits after the decimal point:
print(f"\n\n\n\n\nDurée du programme = {round((end - start), 2)} secondes")


input("\nAppuyer sur la touche 'Entrée' pour quitter le programme...")


##################################    END    ##################################
