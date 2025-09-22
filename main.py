import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import os
import time
from urllib import request
from urllib import error

class Emoji:
    def __init__(self, name:str, id:int, isAnim:bool):
        self.name = name
        self.id = id
        self.isAnim = isAnim
    def __repr__(self):
        return f"Emoji: (name: {str(self.name)}, id: {str(self.id)}, isAnim: {str(self.isAnim)})"

line = ""

def addHeader():
    def saveAndClose():
        global headers, reminder
        headers = {"User-Agent":entry.get()}
        with open("savefile.txt", 'w') as f:
            f.write(entry.get())
        headerWindow.destroy()
        if headers == {"User-Agent":""}:
            tk.messagebox.showinfo("No Header", "please add a web request header before continuing :(")
            return
    headerWindow = tk.Toplevel(main)
    headerWindow.title("Add Header")
    frm2 = ttk.Frame(headerWindow, padding=40)
    frm2.grid()
    ttk.Label(frm2, text="Please input a web request header.").grid(column=0, row=0)
    entry = ttk.Entry(frm2, width=50)
    entry.grid(column=0, row=1,padx=10,pady=10)
    ttk.Button(frm2, text="Save and Close", command=lambda: saveAndClose()).grid(column=0, row=2)

def getMini():
    def saveAndClose():
        global line
        line = entry.get()
        miniWindow.destroy()
        if line == "":
            tk.messagebox.showinfo("No Input", "please input a string of consecutive Discord emoji IDs :(")
            return
        pairEmotes(line)
    miniWindow = tk.Toplevel(main)
    miniWindow.title("Mini Input")
    frm3 = ttk.Frame(miniWindow, padding=40)
    frm3.grid()
    ttk.Label(frm3, text="Please input a string of consecutive Discord emoji IDs.").grid(column=0, row=0)
    entry = ttk.Entry(frm3, width=50)
    entry.grid(column=0, row=1,padx=10,pady=10)
    ttk.Button(frm3, text="Save and Close", command=lambda: saveAndClose()).grid(column=0, row=2)

# requests txt file from user
def getFile():
    if headers == {"User-Agent":""}:
        tk.messagebox.showinfo("No Header", "please add a web request header before continuing. :(")
        return
    global line
    filePath = filedialog.askopenfile(filetypes=[("Text files", "*.txt")])
    time.sleep(.25)
    if filePath is None:
        return
    with open(filePath.name, 'r') as f:
        # Split the extension from the path and normalise it to lowercase.
        ext = os.path.splitext(filePath.name)[-1].lower()
        # Now we can simply use == to check for equality, no need for wildcards.
        line = f.read().rstrip()
    pairEmotes(line)

def pairEmotes(text: str):
    brokenList = []
    while text != "":
        start_index = text.find('<')
        end_index = text.find('>')
        if start_index != -1 and end_index != -1 and start_index < end_index:
            brokenList.append(text[start_index + 1 : end_index])
            text = text[end_index+1:]
        else:
            tk.messagebox.showinfo("Error", "there was an error processing your file :( \n please ensure it is formatted correctly.")
            return
    newList = []
    for each in brokenList:
        if each.startswith("a"):
            anim = True
            each1 = each[2:]
        else:
            anim = False
            each1 = each[1:]
        breakIndex = each1.find(":")
        name = each1[:breakIndex]
        id = int(each1[breakIndex+1:])
        newList.append(Emoji(name,id,anim))
    fetchEmojis(newList)

def fetchEmojis(emojis: list):
    folderPath = filedialog.askdirectory(title="Select a folder for emoji location")
    time.sleep(.25)
    if folderPath is None:  # Check if a folder was actually selected
        return
    for each in emojis:
        if each.isAnim: fileType = "gif"
        else: fileType = "png"
        url = f"https://cdn.discordapp.com/emojis/{str(each.id)}.{fileType}"
        fileName = f"{each.name}.{fileType}"
        try:
            req = request.Request(url, headers=headers)
            with request.urlopen(req) as response:
                image_data = response.read()
            with open(os.path.join(folderPath,fileName), "wb") as f:
                f.write(image_data)
            print(f"Image downloaded successfully to {fileName}")
        except error.URLError as e:
            print(f"Error fetching image: {e.reason}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    tk.messagebox.showinfo("all done!", "all files downloaded successfully :3")

if not os.path.exists("savefile.txt"):
    with open("savefile.txt", 'w') as f:
        f.write("")
        headers = {"User-Agent":""}
else:
    with open("savefile.txt", 'r') as f:
        headers = {"User-Agent":f.read()}

# opens window
main = tk.Tk()
frm = ttk.Frame(main, padding=40)
frm.grid()
main.title("Kip's Discord Emoji Extracter En Masse")
ttk.Label(frm, text="please input a .txt file of consecutive Discord emoji IDs, no spaces or lines").grid(column=0, row=0)
ttk.Label(frm, text="example: <emoji1name:emoji1id><emoji1name:emoji2id>").grid(column=0, row=1)
if headers == {"User-Agent":""}:
    reminder = ttk.Label(frm , text="also, add a web request header using the 'Add Header' button if you haven't already!").grid(column=0, row=2)
else:
    reminder = ttk.Label(frm , text="header added successfully! you can now continue :D").grid(column=0, row=2)
ttk.Button(frm, text="input", command=lambda: getFile()).grid(column=0, row=3)
ttk.Button(frm, text="mini input", command=lambda: getMini()).grid(column=0, row=4)
if headers == {"User-Agent":""}:
    headerButton = ttk.Button(frm, text="add header", command=lambda: addHeader()).grid(column=0, row=5)
else:
    headerButton = ttk.Button(frm, text="change header", command=lambda: addHeader()).grid(column=0, row=5)
ttk.Button(frm, text="exit", command=lambda: main.destroy()).grid(column=0, row=6)
ttk.Button(frm, text="credits", command=lambda: tk.messagebox.showinfo("Credits", "made by 'kipikii' on discord :3")).grid(column=0, row=7)

main.mainloop()