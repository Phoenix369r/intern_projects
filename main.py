from tkinter import *
from tkinter import ttk,messagebox
import googletrans
from googletrans import Translator

root=Tk()
root.title("Google Translator 2.0")
root.minsize(width=1080, height=400)
root.resizable(False,False)
root.configure(background="white")

def label_change():
    c=combo1.get()
    c1=combo2.get()
    label1.configure(text=c)
    label2.configure(text=c1)
    root.after(1000,label_change)

def translate_now():
    try:
        text_=text1.get(1.0,END)
        if text_.strip():  # Check if there's text to translate
            t1=Translator()
            trans_text=t1.translate(text_,src=combo1.get(),dest=combo2.get())
            # Fixed: Use .text instead of .txt
            trans_text=trans_text.text

            text2.delete(1.0,END)
            text2.insert(END,trans_text)
        else:
            text2.delete(1.0,END)
            text2.insert(END, "Please enter text to translate")
    except Exception as e:
        text2.delete(1.0,END)
        text2.insert(END, f"Translation error: {str(e)}")
        print(f"Error: {e}")

# Note: You'll need to have these image files in your directory
# If you don't have them, comment out these lines
try:
    #icon
    image_icon=PhotoImage(file="google.png")
    root.iconphoto(False,image_icon)
except:
    print("google.png not found - skipping icon")

try:
    #arrow
    arrow_image=PhotoImage(file="arrow.png")
    image_label=Label(root,image=arrow_image,width=150)
    image_label.place(x=460,y=50)
except:
    print("arrow.png not found - skipping arrow image")
    # Create a simple arrow label instead
    image_label=Label(root,text="→",font=("Arial", 20),width=10,bg="white")
    image_label.place(x=460,y=50)

language=googletrans.LANGUAGES
languageV=list(language.values())
lang1=language.keys()

#first combobox
combo1=ttk.Combobox(root,values=languageV,font="Algerian",state="r")
combo1.place(x=110,y=20)
combo1.set("english")  # Changed to lowercase to match googletrans format

label1=Label(root,text="ENGLISH",font="TimesNewRoman",bg="white",width=18,bd=5,relief=GROOVE)
label1.place(x=140,y=50)

#second combobox
combo2=ttk.Combobox(root,values=languageV,font="Algerian",state="r")
combo2.place(x=700,y=20)
combo2.set("spanish")  # Set a default target language

label2=Label(root,text="SPANISH",font="TimesNewRoman",bg="white",width=18,bd=5,relief=GROOVE)
label2.place(x=730,y=50)

#first frame
f=Frame(root,bg="Black",bd=5)
f.place(x=10,y=118,width=440,height=210)

text1=Text(f,font="Algerian",bg="white",relief=GROOVE,wrap=WORD)
text1.place(x=0,y=0,width=430,height=200)
scrollbar1=Scrollbar(f)
scrollbar1.pack(side="right",fill='y')
scrollbar1.configure(command=text1.yview)
text1.configure(yscrollcommand=scrollbar1.set)

#second frame
f1=Frame(root,bg="Black",bd=5)
f1.place(x=630,y=118,width=440,height=210)

text2=Text(f1,font="Algerian",bg="white",relief=GROOVE,wrap=WORD)
text2.place(x=0,y=0,width=430,height=200)
scrollbar2=Scrollbar(f1)
scrollbar2.pack(side="right",fill='y')
scrollbar2.configure(command=text2.yview)
text2.configure(yscrollcommand=scrollbar2.set)

#translate button
translate=Button(root,text="Translate",font="Algerian",activebackground="white",cursor="hand2",
                 bd=1,width=10,height=2,bg="black",fg="white",command=translate_now)
translate.place(x=476,y=250)

label_change()
root.mainloop()