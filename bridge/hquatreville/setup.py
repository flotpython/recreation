# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

from cx_Freeze import setup, Executable
import sys

path = sys.path
base = None
if sys.platform == "win32":
    base = "Win32GUI"
    
icone = "Asdecoeur.ico"    
    
import os.path
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6') 
tcl_lib = os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll') 
tk_lib = os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll')   

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os", "tkinter", 'sys','PIL',
                                  'numpy','random','pickle'],
                     "includes" : [],
                     "include_files" : [tcl_lib,
                                        tk_lib,
                                        icone,                                        
                                    ],
                     "excludes": [],
                     "optimize" : 2,
                     "include_msvcr": True   #skip error msvcr100.dll missing
                     }



# On appelle la fonction setup
setup(
    name = "Bridge Bid Booster",
    version = "1.00",
    description = "Utilitaire pour bridgeur",
    options = {"build_exe": build_exe_options},
    executables = [Executable("bridgeutil.py", 
                              base=base, icon = icone)
                  ]
    )