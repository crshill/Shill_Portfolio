# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 15:14:54 2019

@author: LGC0069
"""

import tkinter as ttk
import sys

class CoreGUI(object):
    def __init__(self, parent):
        text_box = ttk.Text(parent, state=ttk.DISABLED)
        text_box.pack()
        
        sys.stdout = StdRedirector(text_box)
        sys.stderr = StdRedirector(text_box)

        yes_button = ttk.Button(parent, text="Yes", command=self.return_T('Y'))
        yes_button.pack()
        no_button = ttk.Button(parent, text="No", command=self.main('N'))
        no_button.pack()

    def main(self, yn):
        if yn == 'Y' :
            print('Saving file to Downloads folder.')
            return True
        if yn == 'N' :
            print('exit')
            return False
        self.destroy

class StdRedirector(object):
    def __init__(self, text_widget):
        self.text_space = text_widget

    def write(self, string):
        self.text_space.config(state=ttk.NORMAL)
        self.text_space.insert("end", string)
        self.text_space.see("end")
        self.text_space.config(state=ttk.DISABLED)
        

