import customtkinter
import os
from tkinter import messagebox
from tkinter import filedialog
import pickle
customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('green')
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.models import Word2Vec
import numpy as np
import string
import joblib
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import ISRIStemmer
from tkinter import Tk, Label, Text, Button, Menu
import random

import os
import re
import json
import camel_tools
import nltk
import pandas as pd
from pathlib import Path
import qalsadi.lemmatizer
from camel_tools.ner import NERecognizer
from camel_tools.tokenizers.word import simple_word_tokenize
from camel_tools.utils.dediac import dediac_ar, dediac_bw


class MainGUI():
    
    @staticmethod
    def Preprocess_Text(text):
        pass
    
    def predict_category():
        pass
        
                
    def copy():
        Main.clipboard_append(Input_Textbox.selection_get())

    def paste():
        Input_Textbox.insert(Main.INSERT, Main.clipboard_get())
    
    menu = Menu(customtkinter.CTk(), tearoff=0)
    menu.add_command(label="Copy", command=copy)
    menu.add_command(label="Paste", command=paste) 
          
    def DestroyAll():
        widgets = Main.winfo_children()
        for widget in widgets:
            widget.destroy()
                
    def Continue():
        MainGUI.DestroyAll()
        MainGUI.Train_Test_Form()
    
    def ResetWindow():
        Main.destroy()
        os.startfile(r"MainGUI.py")
    
    def ClearText():
        Input_Textbox.delete('1.0', 'end')

    def TrainClassifierPage():
        MainGUI.DestroyAll()
        
        global classifierComboBox
      
        ConfirmButton = customtkinter.CTkButton(Main, text="Confirm", command=lambda: MainGUI.Go_Train(), width=100, height=50, font=("System", 30, "bold"), fg_color="darkgreen")
        QuitButton = customtkinter.CTkButton(Main, text="Quit", command=quit, width=100, height=50, font=("System", 30, "bold"), fg_color="darkgreen")

        classifierComboBox.place(x=Main.winfo_screenwidth()/2 - 520, y=Main.winfo_screenheight()/2 - 250, anchor="center")
        ConfirmButton.place(x=Main.winfo_screenwidth()/2 - 220, y=Main.winfo_screenheight() /2 - 250, anchor="center")
        QuitButton.place(x=Main.winfo_screenwidth()/2 - 120,y=Main.winfo_screenheight() / 2 - 50, anchor="center")

    def Train_Test_Form():
        MainGUI.DestroyAll()
        ChooseButtonLabel = customtkinter.CTkLabel(Main, text="Would like to train or test?", font=("System", 40, "bold"))
        TrainButton = customtkinter.CTkButton(Main, text="Train", width=500, height=125, font=("System", 40, "bold"), fg_color="darkgreen", command=lambda: MainGUI.TrainClassifierPage())
        TestButton = customtkinter.CTkButton(Main, text="Test", width=500, height=125, font=("System", 40, "bold"), fg_color="darkgreen", command=lambda: MainGUI.Create_Test_Form())
        ChooseButtonLabel.place(x=Main.winfo_screenwidth()/2 - 450, y=Main.winfo_screenheight()/2 - 400, anchor="center")
        TrainButton.place(x=Main.winfo_screenwidth()/2 - 450,y=Main.winfo_screenheight() / 2 - 250, anchor="center")
        TestButton.place(x=Main.winfo_screenwidth()/2 -450 ,y=Main.winfo_screenheight() / 2 - 100, anchor="center")

    def Create_Test_Form():
        MainGUI.DestroyAll()
        ChooseFileLabel = customtkinter.CTkLabel(Main, text="Input An Article", font=("System", 40, "bold"))
        classifierLabel = customtkinter.CTkLabel(Main, text="AraBERT", font=("System", 10, "bold"))
        Classify_Button = customtkinter.CTkButton(Main, text="Classify",width=200, height=62, font=("System", 30, "bold"), fg_color="darkgreen", command=lambda:MainGUI.predict_category())
        Clear_Btn = customtkinter.CTkButton(Main, text="Clear",width=180, height=62, font=("System", 30, "bold"), fg_color="darkgreen", command=lambda:MainGUI.ClearText())

        global Input_Textbox
        Input_Textbox = customtkinter.CTkTextbox(Main, width=600, height=300, font=("System", 20, "bold"))
        ChooseFileLabel.place(x=Main.winfo_screenwidth()/2 - 450,y=Main.winfo_screenheight()/2 - 450, anchor="center")
        Input_Textbox.place(x=Main.winfo_screenwidth()/2 - 600,y=Main.winfo_screenheight()/2 - 200, anchor="center")
        Classify_Button.place(x=Main.winfo_screenwidth()/2 - 125,y=Main.winfo_screenheight()/2 - 300, anchor="center")
        classifierLabel.place(x=Main.winfo_screenwidth()/2 - 480, y=Main.winfo_screenheight() - 550, anchor="center")
        Clear_Btn.place(x=Main.winfo_screenwidth()/2 - 125, y=Main.winfo_screenheight() - 650, anchor="center")

Main = customtkinter.CTk()
Main.title("Arabic Text Summarization")
Main.attributes("-topmost", True)

ScreenWidth = Main.winfo_screenwidth()
ScreenHeight = Main.winfo_screenheight()
Main.geometry("1000x580".format(ScreenWidth, ScreenHeight))

WelcomeLabel = customtkinter.CTkLabel(Main, text="Welcome to the\nMain Page", font=("System", 40, "bold"))
ContinueButton = customtkinter.CTkButton(Main, text="Continue", command=lambda: MainGUI.Continue(),  width=500, height=125, font=("System", 40, "bold"), fg_color="darkgreen")
QuitButton = customtkinter.CTkButton(Main, text="Quit", command=quit, width=500, height=125, font=("System", 40, "bold"), fg_color="darkgreen")
WelcomeLabel.place(x=ScreenWidth/2-450, y=ScreenHeight/2 - 450, anchor="center")
ContinueButton.place(x=ScreenWidth/2 - 450, y=ScreenHeight/2 - 250, anchor="center")
QuitButton.place(x=ScreenWidth/2 - 450, y=ScreenHeight/2 - 100, anchor="center")

Main.mainloop()
