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

import subprocess               ## Om programma's uit te voeren vanuit Python
import html                     ## Ndz voor decoderen van zgn. HTML-entities
import sys                      ## Basislib
import os                       ## Basislib
import re                       ## Regex

class Radio(object):
    def __init__(self):
        if os.name == "posix":
            self.cmd = "mplayer"
        else:
            self.cmd = "mplayer.exe"
        
    def afspelen(self, zender, url, co, q):
        self.co = co
        self.q  = q
        try:        
            self.stream = subprocess.Popen([self.cmd, url], \
            stdin=subprocess.PIPE, \
            stdout=subprocess.PIPE, \
            stderr=subprocess.STDOUT, \
            bufsize=1)
            
        except OSError:
            print("Kon geen mplayer-executable vinden in $PATH.")
            print("Installeer deze eerst:")
            print("Ubuntu:  sudo apt-get install mplayer2")
            print("Arch:    sudo pacman -S mplayer")
            print("Windows: http://sourceforge.net/projects/mplayer-win32/")
            self.q.put("stop")
        
        self.co.processChannelName(zender)
                
        for regel in iter(self.stream.stdout.readline, ''):
            ## Omzetten van bytes naar gewone string
            regel = regel.decode("utf-8", errors='ignore')

            #print("\r" + regel)
            ## Per nieuwe entry in stdout.readline wordt door deze loop
            ## gegaan. Als bijvoorbeeld de ICY-info verandert, wordt er
            ## opnieuw geprint: ICY Info: ... Dat wordt opgepakt door de if,
            ## en doorgegeven aan de communicator. Zo hebben we iedere keer
            ## de recentste info te pakken.
            
            if re.match("^ICY", regel):
                regel = re.findall(
                "(?<=ICY Info: StreamTitle=').*?(?=';)", regel
                                        )[0].strip()[:64]
                
                ## Omzetten van zgn. HTML-entities in plaintext. Anders zien we
                ## symbolen als &#40; in de ICY-info verschijnen.
                regel = html.unescape(regel)
                self.co.processIcy(regel)
            
            elif re.match("Server returned 404: File Not Found", regel):
                sys.stdout.write("\rKan niet afspelen: stream offline\n")
                sys.stdout.flush()
                q.put("404")
                break                
            
            elif re.match("^Exiting...", regel):
                break
                
        return()
            
    def volumeUp(self):
        ## raise volume by 4 steps: emulates user pressing on 0 for 4 times
        self.stream.stdin.write(b"000")
        self.stream.stdin.flush()
        
        self.co.processVolumeUp()
        
    def volumeDown(self):
        ## lower volume by 4 steps: emulates user pressing on 9 for 4 times
        self.stream.stdin.write(b"99999")
        self.stream.stdin.flush()
        
        self.co.processVolumeDown()
        
    def stoppen(self):
        ## Terminaltitel opnieuw instellen op "Terminal"
        if os.name == "posix":
            sys.stdout.write("\x1b]2;Terminal\x07")
        
        ## Stuur de toetsindruk Q naar de stream. mplayer reageert op q
        ## door te stoppen. Bij het stoppen print mplayer "Exiting...". In
        ## de thread t loopt een for-loop, welke deze string opvangt. Als 
        ## reactie stopt de for-loop ('break'), en komen we aan bij het
        ## return()-statenment. De thread is nu beëindigd.
        
        self.stream.stdin.write(b"q")
        self.stream.stdin.flush()
        
