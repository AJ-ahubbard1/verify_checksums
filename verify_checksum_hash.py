from tkinter import * 
from tkinter.ttk import *
from tkinter.filedialog import askopenfile
import io, hashlib, hmac
BLOCKSIZE = 65536

# setup
window = Tk()
window.title("Verify Checksum")
window.geometry('460x270')

# globals
selectedHash = StringVar(window, "1")
labelFile1 = None
labelFile2 = None
labelResults = None
btnRun = None
btnReset  = None
file1 = None
checksum = None

label1 = Label(window, text="1. Select file to verify:")
label2 = Label(window, text="2. Select file with checksum value:")
label3 = Label(window, text="3. Select algorithm:")
label1.grid(row = 0, column = 0, sticky = W, pady = 5)
label2.grid(row = 2, column = 0, sticky = W, pady = 5)
label3.grid(row = 4, column = 0, sticky = W, pady = 5)

b1 = Radiobutton(window, text = "SHA1", 
                  variable = selectedHash,
                  value    = "1")
b2 = Radiobutton(window, text = "SHA224", 
                  variable = selectedHash,
                  value    = "2")
b3 = Radiobutton(window, text = "SHA256", 
                  variable = selectedHash,
                  value    = "3")
b4 = Radiobutton(window, text = "SHA512", 
                  variable = selectedHash,
                  value    = "4")
b5 = Radiobutton(window, text = "MD5", 
                  variable = selectedHash,
                  value    = "5")
b1.grid(row = 4, column = 3, sticky = W, padx = 2, pady = 5)
b2.grid(row = 4, column = 4, sticky = W, padx = 2, pady = 5)
b3.grid(row = 4, column = 5, sticky = W, padx = 2, pady = 5)
b4.grid(row = 5, column = 3, sticky = W, padx = 2, pady = 5)
b5.grid(row = 5, column = 4, sticky = W, padx = 2, pady = 5)

def open_file1():
  global file1
  global labelFile1
  file1 = askopenfile(mode = 'rb')
  if file1 is not None:
    name = str(file1.name)
    i = name.rfind("/")
    labelFile1 = Label(window, text = name[i:])
    labelFile1.grid(row = 1, column = 1, columnspan = 5, sticky = E, pady = 5)

btn1 = Button(window, text = "Browse..", command = lambda:open_file1())
btn1.grid(row = 1, column = 0, sticky = W, padx = 2, pady = 5)

def getHash():
  algorithm = selectedHash.get()
  if algorithm == "1":
    return hashlib.sha1()
  elif algorithm == "2":
    return hashlib.sha224()
  elif algorithm == "3":
    return hashlib.sha256()
  elif algorithm == "4":
    return hashlib.sha512()
  else:
    return hashlib.md5()

def reset():
  labelFile1.destroy()
  labelFile2.destroy()
  labelResults.destroy()
  btnRun.destroy()
  btnReset.destroy()

def addResetBtn():
  global btnReset
  btnReset = Button(window, text = "Reset", command = lambda:reset())
  btnReset.grid(row = 7, column = 0, sticky = W, padx = 2, pady = 5)

def verifyHash():
  global labelResults
  h = getHash()
  print(h)
  with file1 as afile:
    buf = afile.read(BLOCKSIZE)
    while len(buf) > 0:
      h.update(buf)
      buf = afile.read(BLOCKSIZE)
      h.hexdigest()
    hashValue = h.hexdigest() 

  if hashValue in checksum:
    resultText = "Success!"
  else:
    resultText = "FAILED"
  labelResults = Label(window, text = resultText)
  labelResults.grid(row = 6, column = 5, sticky = E, pady = 5)
  addResetBtn()

def open_file2():
  global checksum
  global labelFile2
  global btnRun
  file2 = askopenfile(mode = 'r')
  if file2 is not None:
    name = str(file2.name)
    i = name.rfind("/")
    labelFile2 = Label(window, text = name[i:])
    labelFile2.grid(row = 3, column = 1, columnspan = 5, sticky = E, pady = 5)
    checksum = file2.read()
    if file1 is not None:
      btnRun = Button(window, text = "Run: click once and wait", command = lambda: verifyHash())
      btnRun.grid(row = 6, column = 0, sticky = W, padx = 2, pady = 5)

btn2 = Button(window, text = "Browse..", command = lambda:open_file2())
btn2.grid(row = 3, column = 0, sticky = W, padx = 2, pady = 5)

window.mainloop()
