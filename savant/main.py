#!/usr/bin/python3

#########################################################################################
#Title: main.py
#Author: Douglas T.
#Creation Date: 02/01/2019
#Description: Main file for the whole Savant app.  This file combines the kivy front end
#             gui with the logical back end.  For Savant, the goal is to keep the gui
#             code free of the logical code
#
#Changelog:
#Name:          Date:       Change:
# Douglas T.    02/01/2019  Initial version 
#########################################################################################

import kivy
import brain

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.properties import ObjectProperty

kivy.require('1.10.1')

class FrontEnd(TabbedPanel):

    newegg = ObjectProperty(None)
    others = ObjectProperty(None)
    other1 = ObjectProperty(None)
    other2 = ObjectProperty(None)
    other3 = ObjectProperty(None)
    other4 = ObjectProperty(None)
    other5 = ObjectProperty(None)
    other6 = ObjectProperty(None)

    def search_go(self, search):
        if self.newegg.active:
            sites = 'Newegg, '
        if self.others.active:
            sites = sites + 'others, '
        if self.other1.active:
            sites = sites + 'other1, '
        if self.other2.active:
            sites = sites + 'other2, '
        if self.other3.active:
            sites = sites + 'other3, '
        if self.other4.active:
            sites = sites + 'other4, '
        if self.other5.active:
            sites = sites + 'other5, '
        if self.other6.active:
            sites = sites + 'other6'

        #Call
        brain.start(sites, search)
        #temp exit
        #exit(0)

    def text_refresh(self):

        self.ids.file_text.text = brain.file_read()

class SavantApp(App):

    def build(self):
        return FrontEnd()

if __name__ == '__main__':
    SavantApp().run()
