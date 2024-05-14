import random
import string
import pyperclip
import time
import tkinter
from tkinter import PhotoImage
from tkinter import Canvas
from tkinter import font
from tkinter import messagebox
import pandas
import json

#Colour Pallete
BACKGROUND_COLOR = "#FF3FA4"
FRONT_COLOR = "#FFC8C8"
BACK_COLOR = "#57375D"
ACCENT_COLOR = "#FF9B82"


#Create window
window = tkinter.Tk()
window.title("Flash Cards")
window.config(padx=5, pady=50, bg = BACKGROUND_COLOR)
window.minsize(400,350)

#String variable to determine if answer is known or not
response = tkinter.StringVar()


#Read in csv data

#Try to read in the saved file of words that have not yet been learned
try:
    data = pandas.read_csv(r"\Users\Alienware 15\Documents\Udemy Projects\Project 14 - Afrikaans flash cards\wordsToLearn.csv")

#Otherwise read in the fill frequency list
except:
    data = pandas.read_csv(r"\Users\Alienware 15\Documents\Udemy Projects\Project 14 - Afrikaans flash cards\afrikaans_frequency_list.csv")

#Create dictionary out of data from csv
Afrikaans_Dict = data.to_dict()

#Create dataframe from the dictionary of csv data
frequencyList_df = pandas.DataFrame(Afrikaans_Dict)


#------------------------------------Functions-------------------------------------------------#

#Method to flip the card on the screen from the english side to afrikaans side and vice versa
def flipCard(word):
    global cardState

    if cardState == "f":
        canvas.itemconfig(cardFace, image = cardBack)
        canvas.itemconfig(LanguageLabel,text = "English", fill = ACCENT_COLOR)
        canvas.itemconfig(wordGuess, fill = ACCENT_COLOR, text = word)
        cardState = "b"

    else:
        canvas.itemconfig(cardFace, image = cardFront)
        canvas.itemconfig(LanguageLabel,text = "Afrikaans", fill = BACK_COLOR)
        canvas.itemconfig(wordGuess, fill = BACK_COLOR, text = word)
        cardState = "f"
    
#Method to run the program
def start():
    global cardState
    global frequencyList_df
    cardState = "b"
    for row in frequencyList_df.itertuples(index = True, name = None):
        
        index = row[0]
        afrWord = row[1]
        engWord = row[2]
        
        flipCard(afrWord)
        window.update()
        time.sleep(3)

        flipCard(engWord)
        window.update()
        
        #Await user input from buttons
        global response 
        response.set("")
        window.wait_variable(response)

        #If user knows the answer then remove it from list and save file
        if response.get() == "Yes":
            frequencyList_df = frequencyList_df.drop(index)
            frequencyList_df.to_csv(r"\Users\Alienware 15\Documents\Udemy Projects\Project 14 - Afrikaans flash cards\wordsToLearn.csv", index = False)
       
#Method to be triggered on the green button press           
def rightSet():
    global response
    response.set("Yes")

#Method to be triggered on the red button press
def wrongSet():
    global response
    response.set("No")

#------------------UI DESIGN------------------#

#Create flash card front
cardFront = PhotoImage(file=r"\Users\Alienware 15\Documents\Udemy Projects\Project 14 - Afrikaans flash cards\images\front_pic.PNG")
canvas = Canvas(width = 535, height=250,highlightthickness=0, bg=  BACKGROUND_COLOR)
cardBack = PhotoImage(file=r"\Users\Alienware 15\Documents\Udemy Projects\Project 14 - Afrikaans flash cards\images\back_pic.PNG")
cardFace = canvas.create_image(270,100,image = cardFront)

LanguageLabel = canvas.create_text(264,30, text ="Afrikaans" ,fill= BACK_COLOR, font=font.Font(family ="adlam display", size=25))
wordGuess = canvas.create_text(264,100, text ="Poes" ,fill= BACK_COLOR, font=font.Font(family ="adlam display", size=40))

#Create green button
ticImg = PhotoImage(file=r"\Users\Alienware 15\Documents\Udemy Projects\Project 14 - Afrikaans flash cards\images\right.PNG")

rightBtn = tkinter.Button(window, image = ticImg, borderwidth= 0, highlightthickness= 0, command= rightSet)
rightBtn.grid(column = 3, row = 3)

#create red button
crossImg = PhotoImage(file=r"\Users\Alienware 15\Documents\Udemy Projects\Project 14 - Afrikaans flash cards\images\wrong.PNG")

wrongBtn = tkinter.Button(window, image = crossImg, borderwidth= 0, highlightthickness= 0, command= wrongSet)
wrongBtn.grid(column = 1, row = 3)


canvas.grid(column=1,row=1, columnspan=3)


#Trigger the main program logic
while True: 
    start() 

window.mainloop()

