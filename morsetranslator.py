import cv2
import os
from twilio.rest import Client
# from python-dotenv import load_dotenv
from dotenv import dotenv_values
from tkinter import *
from PIL import Image, ImageTk
from HandTrackingModule import HandDetector
from tkinter import filedialog
from gtts import gTTS
from playsound import playsound
import os
import string

Morse={'.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D',
        '.': 'E', '..-.': 'F', '--.': 'G', '....': 'H', 
        '..': 'I', '.---': 'J', '-.-': 'K', '.-..': 'L',
        '--': 'M', '-.': 'N', '---': 'O', '.--.': 'P', 
        '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T', 
        '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X',
        '-.--': 'Y', '--..': 'Z', '':' '}

win = Tk()
win.title("Morsocter")
win.geometry("670x600+200+30")

Main_Frame = Frame(win, width=670, height=700, bg="#ffd9cc").place(x=0, y=0)
cap = cv2.VideoCapture(0)

buttonX=10
buttonY=450
w = 300
h = 200
Main_Label = Label(Main_Frame, width=w, height=h)
Main_Label.place(x=180, y=220)

words=""
Y_Cordinate_Checker=False
X_Cordinate_Checker=False
Thumb_Checker=False

Video_One=StringVar()
Video_Two=StringVar()
Video_One.set("")
Video_Two.set("")

bVideo_One=''
bVideo_Two=''

Words=StringVar()
Words.set("")

TTSsave='OutputFile'

Maximum_Videos=0

def delChar():
    global Words
    n=str(Words.get())
    m=''
    if(len(n)>0):
        for i in range(len(n)-1):
            m+=n[i]
    Words.set(m)

def Help():
    os.startfile("Help.txt")

def Play():
    global TTSsave
    language = 'en'
    n=Words.get()
    #####################
    temp = dotenv_values(".env")
    TWILIO_ACCOUNT_SID=temp["TWILIO_ACCOUNT_SID"]
    TWILIO_AUTH_TOKEN=temp["TWILIO_AUTH_TOKEN"]
    client=Client(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN)
    message = client.messages \
    .create(
         body='The translation text for the Morse code is '+n,
         from_='+17073833609',
         to='+917848961952'
     )
    print(message.sid)
    #####################
    if(set(n).intersection(string.ascii_uppercase) != set()):
        myobj = gTTS(text=n, lang=language, slow=False)
    else:
        myobj = gTTS(text="Please enter some text first", lang=language, slow=False)
    TTSsave+='s'
    myobj.save('audio/'+TTSsave+'.mp3')
    playsound('audio/'+TTSsave+'.mp3')

def maxLim():
    global TTSsave
    language = 'en'
    n="Maximum Limit Reached"
    myobj = gTTS(text=n, lang=language, slow=False)
    TTSsave+='s'
    myobj.save('audio/'+TTSsave+'.mp3')
    playsound('audio/'+TTSsave+'.mp3')

def DelVid():
    global Maximum_Videos, bVideo_One, bVideo_Two, Video_One, Video_Two
    if(isinstance(bVideo_Two,Button)):
        bVideo_Two.place_forget()
        bVideo_Two=''
        Video_Two.set("")
        Maximum_Videos-=1
    elif(isinstance(bVideo_One,Button)):
        bVideo_One.place_forget()
        bVideo_One=''
        Video_One.set("")
        Maximum_Videos-=1

def Live():
    global cap, detector
    cap = cv2.VideoCapture(0)
    detector = HandDetector(detectionCon=0.5, maxHands=2)
    Words.set("")

def Recordings(num):
    global cap, detector
    if(num==1):
        if(".mp4" not in Video_One.get()):
            m=Video_One.get()
            n=''
            o=''
            for i in range(-1, -len(m), -1):
                if m[i]=='/':
                    break
                n+=m[i]
            for i in range(-1, -len(n)-1, -1):
                o+=n[i]
            m+=("/"+str(o)+".mp4")
            Video_One.set(m)
        cap = cv2.VideoCapture(Video_One.get())
        detector = HandDetector(detectionCon=0.5, maxHands=2)
        Words.set("")
    elif(num==2):
        if(".mp4" not in Video_Two.get()):
            m=Video_Two.get()
            n=''
            o=''
            for i in range(-1, -len(m), -1):
                if m[i]=='/':
                    break
                n+=m[i]
            for i in range(-1, -len(n)-1, -1):
                o+=n[i]
            m+=("/"+str(o)+".mp4")
            Video_Two.set(m)
        cap = cv2.VideoCapture(Video_Two.get())
        detector = HandDetector(detectionCon=0.5, maxHands=2)
        Words.set("")

def Video_Adder_Func():
    global Video_One, Video_Two, bVideo_One, bVideo_Two
    global Maximum_Videos
    filename = filedialog.askdirectory()
    if(filename!=""):
        if(Maximum_Videos<2):
            if(Video_One.get()==""):
                Video_One.set(filename)
                filename=""
                bVideo_One = Button(Main_Frame,text='1st Video', height=1, width=10, relief=RAISED, cursor="hand2", command= lambda : Recordings(1))
                bVideo_One.place(x=(buttonX+400), y=buttonY)
            elif(Video_Two.get()==""):
                Video_Two.set(filename)
                filename=""
                bVideo_Two = Button(Main_Frame,text='2nd Video', height=1, width=10, relief=RAISED, cursor="hand2", command= lambda : Recordings(2))
                bVideo_Two.place(x=(buttonX+500), y=buttonY)
        else:
            maxLim()
        if(Maximum_Videos<=1):
            Maximum_Videos+=1

def Button_Selector():
    bAdd = Button(Main_Frame,text='Add Videos', height=1, width=15, relief=RAISED,cursor="hand2", command=Video_Adder_Func)
    bAdd.place(x=(buttonX+200), y=buttonY)
    Main_Label = Label(Main_Frame, text="Videos Limit : 5",width=13, height=1, bg="#ffd9cc")
    Main_Label.place(x=(buttonX+220), y=(buttonY+30))

def Image_selector():
    global Thumb_Checker, X_Cordinate_Checker, Y_Cordinate_Checker, Words, words, cap, detector
    success, img = cap.read()
    if(success==False):
        cap = cv2.VideoCapture(0)
        Image_selector()
    img=cv2.flip(img, 1)
    hands, img = detector.findHands(img,flipType=False) 
    img = cv2.resize(img, (w, h))
    if hands:
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  # List of 21 Landmark points
        Index_tipY=lmList1[8][1] #8 for tip of index finger, 1 for y coordinate
        Index_dipY=lmList1[7][1] #7 for dip of index finger, 1 for y coordinate
        Middle_tipY=lmList1[12][1] #12 for tip of middle finger, 1 for y coordinate
        Middle_dipY=lmList1[11][1] #11 for dip of middle finger, 1 for y coordinate
        Thumb_tipX=lmList1[4][0] #4 for tip of thumb, 0 for x coordinate
        Thumb_ipX=lmList1[3][0] #3 for ip of thumb, 0 for x coordinate
        if (Index_tipY>Index_dipY):
            Y_Cordinate_Checker=True
        if Index_tipY<Index_dipY and Y_Cordinate_Checker :
            words+='-'
            Y_Cordinate_Checker=False
        if (Middle_tipY>Middle_dipY):
            X_Cordinate_Checker=True
        if Middle_tipY<=Middle_dipY and X_Cordinate_Checker :
            words+='.'
            X_Cordinate_Checker=False
        if(Thumb_tipX>Thumb_ipX):
            Thumb_Checker=True
        if Thumb_tipX<=Thumb_ipX and Thumb_Checker:
            p=str(Words.get())
            n=p+str(Morse.get(words,''))
            Words.set(n)
            words=''
            Thumb_Checker=False
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(imgRGB)
    finalImage = ImageTk.PhotoImage(image)
    Main_Label.configure(image=finalImage)
    Main_Label.image = finalImage
    win.after(1, Image_selector)

detector = HandDetector(detectionCon=0.5, maxHands=2)

label2= Label(Main_Frame, text="Welcome to Morsocter", bg="#ffd9cc", font=('Times', '14', 'bold') ).place(x=0,y=2)
label3= Label(Main_Frame, text="TEXT : ", bg="#ffd9cc").place(x=0,y=28)
label4= Label(Main_Frame, text="Developed by: Ujjawal Kumar, Anand Chourasiya", bg="#e6fff2", font=('Times', '10', 'bold')).place(x=400,y=570)
textlabel= Label(Main_Frame, textvariable=Words, width=92, height=10, relief=RIDGE)
textlabel.place(x=10, y=50)
b1 = Button(Main_Frame,text='Recorded Videos', bg="#ffffe6", height=1, width=20, relief=RAISED, cursor="hand2", command=Button_Selector)
b1.place(x=buttonX, y=buttonY)
b2 = Button(Main_Frame,text='Live Video', bg="#ffffe6", height=1, width=20, relief=RAISED, cursor="hand2", command=Live)
b2.place(x=buttonX, y=(buttonY+40))
b3 = Button(Main_Frame,text='Delete Video', bg="#ffffe6", height=1, width=20, relief=RAISED, cursor="hand2", command=DelVid)
b3.place(x=buttonX, y=(buttonY+80))
b4 = Button(Main_Frame,text='Play', bg="#ffffe6", height=1, width=5, relief=RAISED, cursor="hand2", command=Play)
b4.place(x=10, y=220)
b5 = Button(Main_Frame,text='Help', bg="#ffffe6", height=1, width=5, relief=RAISED, cursor="hand2", command=Help)
b5.place(x=600, y=220)
b6 = Button(Main_Frame,text='Delete Character', bg="#ffffe6", height=1, width=13, relief=RAISED, cursor="hand2", command=delChar)
b6.place(x=492, y=220)
Image_selector()
win.mainloop()