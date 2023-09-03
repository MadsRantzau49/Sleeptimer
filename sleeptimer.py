# !/usr/bin/python3  
from time import time, sleep
import os
import tkinter as tk
from tkinter import messagebox
from math import *
import pyautogui 
import datetime



root = tk.Tk()  
#Layout
root.geometry("300x600")
root.title("Sleeptimer")

#funktion som bliver kaldt når man starter sleeptimeren.
def counter():
    #henter dataen fra user input
    m = int(minutes.get())
    h = int(hours.get())
    time = (m * 60) + (h*60*60)

    #overskriver data filen som er en fil med hvor lang tid der er tilbage til pc slukkes.
    my_file = open(os.path.dirname(__file__)+"/../data.txt", "w")
    my_file.write(str(time))
    my_file.close()

    #sætter check filen til true. Det gør den fordi at funkltionen bliver ved med at tælde nedaf men den shutdowner kun hvis tallet er 0 og check.txt = true :D. 
    my_check_file = open(os.path.dirname(__file__) + "/../check.txt", "w")
    my_check_file.write("true")
    my_check_file.close()

#loop som køres hvert sekund
def update():
    #læser hvor lang tid der er tilbage.
    my_new_file = open(os.path.dirname(__file__)+"/../data.txt", "r")
    data = my_new_file.read()
    list = data.split("\n")
    newTime = int(list[0])

    #laver nedtælingen:
    newTime -= 1  
    my_new_file.close()

    #overskriver det tidligere tal med det nye (altså 1 mindre)
    edit_new_file = open(os.path.dirname(__file__) + "/../data.txt", "w")
    edit_new_file.write(str(newTime))
    edit_new_file.close()
    
    #En lille warning når der er 60 sekunder tilbage for man kan nå at fortryde shutdown, men kun hvis check er true. 
    my_checker_file = open(os.path.dirname(__file__) + "/../check.txt", "r")
    check = my_checker_file.read()
    print(check)
    my_checker_file.close()

    #Opdatere uret visuelt
    if check == "true":
        newTimestr = str(datetime.timedelta(seconds=newTime))
        timeleft.config(text=newTimestr)
        #opretter sluk knap når check == true, sådan at man kan fortryde.
        slukButton.pack(anchor="c",pady=20)
        print(newTimestr)
    else:
        timeleft.config(text="")
        slukButton.pack_forget()

    if newTime == 60 and check == "true":
        #trykker win + d som gør at man går ud til desktop
        pyautogui.hotkey('winleft', 'd')
    
    
    #når tiden er gået ændre den check til false så når man åbner det næste gang så er den false og shutdowner ikke automatisk.
    if newTime <= 0 and check == "true":
        my_check_file = open(os.path.dirname(__file__)+"/../check.txt", "w")
        my_check_file.write("false")
        my_check_file.close()
        print("sluk")
        #Slukker computer:
        os.system("shutdown -s -t 1") 
    
    #gør at det bliver et loop 
    root.after(1000,update)



#når du trykker på krydset (luk app) så skal den ændre check til false først sådan at når man genåbner fortsætter den ikke hvor du slap
def quit():
    my_check_file = open(os.path.dirname(__file__) + "/../check.txt", "w")
    my_check_file.write("false")
    my_check_file.close()
    root.destroy()

#stopper tiden og sætter check til false
def turnoff():
    my_check_file = open(os.path.dirname(__file__) + "/../check.txt", "w")
    my_check_file.write("false")
    my_check_file.close()

#Minutes layoyt
labelM = tk.Label(root, text="Minutes: ",font=('Arial', 18))
labelM.pack(anchor="c")

#Minutes input
minutes = tk.Entry(root ,font=('Arial', 18))
#default value:
minutes.insert(0, "30")
minutes.pack(anchor="c")

#hours layout
labelH = tk.Label(root, text="Hours: ",font=('Arial', 18))
labelH.pack(anchor="c")

#hours input
hours = tk.Entry(root ,font=('Arial', 18))
#default value:
hours.insert(0, "0")
hours.pack(anchor="c")


#start knappen som sætter tiden.     
startButton = tk.Button(root, text="Start sleeptimer", command=counter,font=('Arial',20))
startButton.pack(anchor="c",pady=20)

#viser hvor lang tid der tilbage til den slukker
timeleft = tk.Label(root,text="",font=('Arial', 58))
timeleft.pack(anchor="c")

#start knappen som sætter tiden.     
slukButton = tk.Button(root, text="sluk sleeptimer", command=turnoff,font=('Arial',20))


#starter quit funktionen når man lukker appen. 
root.protocol("WM_DELETE_WINDOW",quit)
#kører loopet. 
root.after(1000,update)
root.mainloop()  
