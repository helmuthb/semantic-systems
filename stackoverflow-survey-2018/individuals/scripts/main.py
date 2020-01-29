import os, os.path
import errno
from csv2ttl import main as ttl_main
from csv2devroles import main as devroles_main
from csv2complangs import main as complangs_main
from csv2countries import main as countries_main
from csv2genders import main as gender_main
from csv2ages import main as ages_main

"""

This script generates everything that is needed for the stackoverflow survey 2018 results:
- developer roles
- computer languages
- .ttl file

"""

# Taken from https://stackoverflow.com/a/600612/119527
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def main():
    mkdir_p('../generated')
    devroles_main()
    complangs_main()
    countries_main()
    gender_main()
    ages_main()
    ttl_main()

if __name__ == "__main__":
    main()