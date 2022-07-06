import os
import tkinter as tk
from PIL import ImageTk, Image
 
# To get the dialog box to open when required
from tkinter import filedialog

import cv2
import agedetector
boje={
    "zuta":"#F6BD60",
    "bela":"#F7EDE2",
    "zelena":"#84A59D",
    "crvena":"#F28482"
}

class MainMenu():
    def __init__(self): 
        self.root=tk.Tk()
        self.root.config(bg=boje["bela"])
        self.root.geometry("1280x960")
        self.root.resizable(height = None, width = None)
        self.mainframe=tk.Frame()
        self.mainframe.config(bg=boje["zelena"])
        self.itemframe=tk.Frame(bg=boje["bela"])
        slika=tk.Button(self.mainframe,text="Dodaj sliku",command=self.addItem,width=15,height=2,font=("Helvetica",15),bg=boje["zuta"],fg=boje["zelena"],border=0,activebackground=boje["zelena"],activeforeground=boje["zuta"])
        slika.grid(row=0,column=0,pady=10,padx=10)

        self.mainframe.pack(fill="y", side="left")
        self.itemframe.pack()
        self.root.mainloop()
    
    
    def resetItemFrame(self):
        self.itemframe.destroy()
        self.itemframe=tk.Frame(bg=boje["bela"])
    
    def addItem(self):
        
        self.resetItemFrame()
        
        ocitaj=tk.Button(self.itemframe,text="Učitaj sliku",command=lambda :self.inputPhoto(panel),width=15,height=2,font=("Helvetica",15),bg=boje["zuta"],fg=boje["zelena"],border=0,activebackground=boje["zelena"],activeforeground=boje["zuta"])
        ocitaj.grid(row=0,column=0,columnspan=4,pady=10,padx=10)
        dothework=tk.Button(self.itemframe,text="Primeni",command=lambda :self.izvrsiAlg(panel.cget("text")),width=15,height=2,font=("Helvetica",15),bg=boje["zuta"],fg=boje["zelena"],border=0,activebackground=boje["zelena"],activeforeground=boje["zuta"])
        dothework.grid(row=3,column=0,columnspan=4,padx=10,pady=10)
        panel=tk.Label(self.itemframe)
        panel.config(bg=boje["bela"])
        panel.grid(row=2)
        self.itemframe.pack()
    
    def inputPhoto(self,panel):
        
        x = filedialog.askopenfilename(filetypes=[(".png",".jpg",".png")])
        filepath = os.path.abspath(x)
    # opens the image
        img = Image.open(x)
        
        # resize the image and apply a high-quality down sampling filter
        img = img.resize((360,320), Image.ANTIALIAS)
    
        # PhotoImage class is used to add image to widgets, icons etc
        img = ImageTk.PhotoImage(img)
    
        # create a label
        print(filepath)
        panel.config(image=img,text=str(filepath))
        # set the image as img
        panel.image = img
        panel.grid(row = 2)
    
    
    def izvrsiAlg(self,slika):

        img=agedetector.doStuff(slika)
        if len(img)==1 and img[0]==0:
            prikaz=tk.Label(self.itemframe,text="Nema lica na slici")
            prikaz.grid(row=2,column=3)
        else:    
        #cv2.imshow("DA",img)
        #img=cv2.imread(img)
            img = cv2.resize(img, (360, 320))
            blue,green,red = cv2.split(img)
            img = cv2.merge((red,green,blue))
            im = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=im)
            
            prikaz=tk.Label(self.itemframe,image=imgtk)
            prikaz.image=imgtk
            prikaz.grid(row=2,column=3)
    
    
    
def main():
    e=MainMenu()
    
    
if __name__=="__main__":
    main()