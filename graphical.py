#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tkinter

fenetre = tkinter.Tk()

label = tkinter.Label(fenetre, text="Salut")
label.pack()

bouton = tkinter.Button(fenetre, text="Fermer", command=fenetre.quit)
bouton.pack()

value = tkinter.StringVar()
value.set("Default")
s = ""
entree = tkinter.Entry(fenetre, textvariable=s, width=30)
entree.pack()

fenetre.mainloop()