#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK

## Dependencies:    mplayer, argparse, argcomplete, pyYAML
## Author:          Gijs Timmers: https://github.com/GijsTimmers

## Licence:         CC-BY-SA-4.0
##                  http://creativecommons.org/licenses/by-sa/4.0/

## This work is licensed under the Creative Commons
## Attribution-ShareAlike 4.0 International License. To  view a copy of
## this license, visit http://creativecommons.org/licenses/by-sa/4.0/ or
## send a letter to Creative Commons, PO Box 1866, Mountain View,
## CA 94042, USA.

from . import default           ## Superklasse
import sys                      ## Basislib

class Communicator(default.Communicator):
    def processIcy(self, regel):
        regel = self.checkIfIcyIsNew(regel)
        if regel:  
            if " - " in regel:
                ## Als er een liedje wordt afgespeeld (gekenmerkt door het
                ## streepje), wordt de string omgezet in kleine letters, be-
                ## ginnend met een hoofdletter.
                regel = regel.title()
                sys.stdout.write("\r" + " " * self.BREEDTE_TERMINAL)
                sys.stdout.write("\r" + "Info:         [{info}]".format(info=regel))
            
            else:
                sys.stdout.write("\r" + " " * self.BREEDTE_TERMINAL)
                sys.stdout.write("\r" + "Info:         [{info}]".
                format(info=regel))