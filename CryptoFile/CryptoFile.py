import os
import tkinter as tk
from tkinter import messagebox, filedialog
import onetimepad
from Cryptodome import Random
from Cryptodome.Cipher import AES
from PIL import Image, ImageTk


class Encryptor:
    def __init__(self, key):
        self.key = key

    def pad(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

    def encrypt(self, message, key, key_size=256):
        message = self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message)

    def encrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            plaintext = fo.read()
        enc = self.encrypt(plaintext, self.key)
        with open(file_name + ".enc", 'wb') as fo:
            fo.write(enc)
        os.remove(file_name)

    def decrypt(self, ciphertext, key):
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b"\0")

    def decrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            ciphertext = fo.read()
        dec = self.decrypt(ciphertext, self.key)
        with open(file_name[:-4], 'wb') as fo:
            fo.write(dec)
        os.remove(file_name)

    def getAllFiles(self, file_name):
        dir_path = file_name
        dirs = []
        for dirName, subdirList, fileList in os.walk(dir_path):
            for fName in fileList:
                if fName != 'script.py' and fName != 'data.txt.enc':
                    dirs.append(dirName + "\\" + fName)
        return dirs

    def encrypt_all_files(self, file_name):
        dirs = self.getAllFiles(file_name)
        for file_name in dirs:
            self.encrypt_file(file_name)

    def decrypt_all_files(self, file_name):
        dirs = self.getAllFiles(file_name)
        for file_name in dirs:
            self.decrypt_file(file_name)


class FirstPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        load = Image.open("img1.jpg")
        photo = ImageTk.PhotoImage(load)
        label = tk.Label(self, image=photo)
        label.image = photo
        label.place(x=0, y=100)

        l1 = tk.Label(self, text="Username", font=("Arial Bold", 15), bg='ivory')
        l1.place(x=545, y=130)
        t1 = tk.Entry(self, width=30, bd=5)
        t1.place(x=545, y=170)
        l2 = tk.Label(self, text="Password", font=("Arial Bold", 15), bg='ivory')
        l2.place(x=545, y=210)
        t2 = tk.Entry(self, width=30, show='*', bd=5)
        t2.place(x=545, y=250)

        def encryptMessage():
            pt = e1.get()

            # inbuilt function to encrypt a message
            ct = onetimepad.encrypt(pt, 'random')
            e2.insert(0, ct)

        def decryptMessage():
            ct1 = e3.get()

            # inbuilt function to decrypt a message
            pt1 = onetimepad.decrypt(ct1, 'random')
            e4.insert(0, pt1)

        def verify():
            try:
                with open("credential.txt", "r") as f:
                    info = f.readlines()
                    i = 0
                    for e in info:
                        u, p = e.split(",")
                        if u.strip() == t1.get() and p.strip() == t2.get():
                            controller.show_frame(SecondPage)
                            i = 1
                            break
                    if i == 0:
                        messagebox.showinfo("Error", "Please provide correct username and password!!")
            except:
                messagebox.showinfo("Error", "Please provide correct username and password!!")

        b1 = tk.Button(self, text="Submit", font=("Arial", 15), cursor="hand2", command=verify)
        b1.place(x=654, y=325)

        def register():
            window = tk.Tk()
            window.resizable(0, 0)
            window.configure(bg="deep sky blue")
            window.title("Register")
            l1 = tk.Label(window, text="Username:", font=("Arial", 15), bg="deep sky blue")
            l1.place(x=10, y=10)
            t1 = tk.Entry(window, width=30, bd=5)
            t1.place(x=200, y=10)

            l2 = tk.Label(window, text="Password:", font=("Arial", 15), bg="deep sky blue")
            l2.place(x=10, y=60)
            t2 = tk.Entry(window, width=30, show="*", bd=5)
            t2.place(x=200, y=60)

            l3 = tk.Label(window, text="Confirm Password:", font=("Arial", 15), bg="deep sky blue")
            l3.place(x=10, y=110)
            t3 = tk.Entry(window, width=30, show="*", bd=5)
            t3.place(x=200, y=110)

            def check():
                if t1.get() != "" or t2.get() != "" or t3.get() != "":
                    if t2.get() == t3.get() and t2.get() != "":
                        with open("credential.txt", "a") as f:
                            f.write(t1.get() + "," + t2.get() + "\n")
                            messagebox.showinfo("Welcome", "You are registered successfully!!")
                            fn = 'credential.txt'
                            p = os.popen('attrib +h ' + fn)
                            t = p.read()
                            p.close()
                    else:
                        messagebox.showinfo("Error", "Your password didn't get match!!")
                else:
                    messagebox.showinfo("Error", "Please fill the complete field!!")
                window.destroy()

            b1 = tk.Button(window, text="Sign in", font=("Arial", 15), bg="#ffc22a", command=check)
            b1.place(x=315, y=150)

            window.geometry("470x220")
            window.mainloop()

        def shift():
            x1, y1, x2, y2 = canvas.bbox("marquee")
            if x2 < 0 or y1 < 0:
                x1 = canvas.winfo_width()
                y1 = canvas.winfo_height() // 2
                canvas.coords("marquee", x1, y1)
            else:
                canvas.move("marquee", -2, 0)
            canvas.after(1000 // fps, shift)

        f1 = tk.Frame(self, bg="yellow", width=800, height=100)
        f1.place(x=0, y=0)
        f1.update()
        l1 = tk.Label(f1, text="CryptoFile", bg="yellow", fg="#192249", font=("Arial Bold", 50))
        l1.place(x=360, y=39, anchor="center")
        l2 = tk.Label(f1, text="1.0.0", bg="yellow", fg="#192249", font=("Arial Bold", 13))
        l2.place(x=530, y=52)

        canvas = tk.Canvas(f1, bg='yellow')
        canvas.place(x=0, y=80)
        text_var = "Hey there .. !!  Register yourself to get access for the encryption " \
                   "and decryption of a particular file or the whole folder.."
        text = canvas.create_text(0, -2000, text=text_var, font=('Times New Roman', 12), fill='#192249',
                                  tags=("marquee",), anchor='w')
        x1, y1, x2, y2 = canvas.bbox("marquee")
        width = 648
        height = y2 - y1
        canvas['width'] = width
        canvas['height'] = height
        fps = 40  # Change the fps to make the animation faster/slower
        shift()

        b2 = tk.Button(f1, text="Register", bg="dark orange", font=("Arial", 15), cursor="hand2", command=register)
        b2.place(x=650, y=30)
        #############################################################################################################
        f2 = tk.Frame(self, bg="white", width=800, height=100)
        f2.place(x=0, y=400)
        f2.update()

        label1 = tk.Label(f2, text='plain text', bg="white")
        label1.place(x=80, y=10)
        label2 = tk.Label(f2, text='encrypted text', bg="white")
        label2.place(x=53, y=40)
        l3 = tk.Label(f2, text="cipher text", bg="white")
        l3.place(x=420, y=10)
        l4 = tk.Label(f2, text="decrypted text", bg="white")
        l4.place(x=400, y=40)

        # creating entries and positioning them on the grid
        e1 = tk.Entry(f2, bg='yellow')
        e1.place(x=150, y=10)
        e2 = tk.Entry(f2, bg='yellow')
        e2.place(x=150, y=40)
        e3 = tk.Entry(f2, bg='yellow')
        e3.place(x=500, y=10)
        e4 = tk.Entry(f2, bg='yellow')
        e4.place(x=500, y=40)

        # creating encryption button to produce the output
        ent = tk.Button(f2, text="encrypt", bg="red", fg="white", command=encryptMessage)
        ent.place(x=180, y=70)

        # creating decryption button to produce the output
        dec = tk.Button(f2, text="decrypt", bg="green", fg="white", command=decryptMessage)
        dec.place(x=530, y=70)


#######################################################################################################################


class SecondPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        load = Image.open("img2.jpg")
        load = load.resize((762, 500), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(load)
        label = tk.Label(self, image=photo)
        label.image = photo
        label.place(x=0, y=0)

        key = b'[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e'
        enc = Encryptor(key)
        clear = lambda: os.system('cls')

        def e_file():
            enc.encrypt_file(str(browseFiles()))

        def d_file():
            enc.decrypt_file(str(browseFiles()))

        def e_a_file():
            enc.encrypt_all_files(str(browseDir()))

        def d_a_file():
            enc.decrypt_all_files(str(browseDir()))

        def browseFiles():
            filename = filedialog.askopenfilename(initialdir="/",
                                                  title="Select a File",
                                                  filetypes=(("Text files",
                                                              "*.txt*"),
                                                             ("all files",
                                                              "*.*")))
            l1 = tk.Label(self, text="File Encrypted: " + filename, fg='black', font=("Arial", 10))
            l1.place(x=390, y=10)
            return filename

        def browseDir():
            filename = tk.filedialog.askdirectory()
            l1 = tk.Label(self, text="Folder Encrypted: " + filename, fg='black', font=("Arial", 10))
            l1.place(x=390, y=10)
            return filename

        button1 = tk.Button(self, text="Encrypt file", font=("Arial", 13), bg="blue", fg="white", command=e_file)
        button1.place(x=100, y=70)
        button2 = tk.Button(self, text="Decrypt file", font=("Arial", 13), bg="blue", fg="white", command=d_file)
        button2.place(x=100, y=140)
        button3 = tk.Button(self, text="Encrypt all files in the directory", font=("Arial", 13),
                            bg="blue", fg="white", command=e_a_file)
        button3.place(x=100, y=270)
        button4 = tk.Button(self, text="Decrypt all files in the directory", font=("Arial", 13),
                            bg="blue", fg="white", command=d_a_file)
        button4.place(x=100, y=340)

        button = tk.Button(self, text="About", font=("Arial", 15), command=lambda: controller.show_frame(ThirdPage))
        button.place(x=650, y=420)

        button = tk.Button(self, text="Back", font=("Arial", 15), command=lambda: controller.show_frame(FirstPage))
        button.place(x=100, y=420)


class ThirdPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        l1 = tk.Label(self, text="CryptoFile", font=("Arial Bold", 50))
        l1.place(x=360, y=39, anchor="center")

        var = tk.StringVar()
        label = tk.Message(self, textvariable=var, relief=tk.RAISED, font=('Times New Roman', 20), width=700)
        var.set("The Authors will not be responsible for any kind of loss of data "
                "so it is essential to have a Backup of Original Data you give as Input "
                "to Encrypt/Decrypt in the Software. Under no circumstances shall we be "
                "liable or responsible to you or any other person for any damages, "
                "loss of any of your useful data by using this Software. Read the "
                "LICENSE for more information.")
        label.place(x=25, y=140)

        l1 = tk.Label(self, text="Version : 1.0.0", font=('Arial', 15))
        l1.place(x=600, y=110)

        def openNewWindow():
            new_window = tk.Toplevel(self)
            new_window.title("LICENSE")
            new_window.geometry("400x450")

            my_var = tk.StringVar()
            my_label = tk.Message(new_window, textvariable=my_var, relief=tk.RAISED, font=('Arial', 10), width=350)
            my_var.set("Copyright (c) 2020 Kumar Rishi \n\n"
                       "Permission is hereby granted, free of charge, to any person obtaining a copy "
                       "of this software and associated documentation files (the ""Software""), to deal "
                       "in the Software without restriction, including without limitation the rights "
                       "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell "
                       "copies of the Software, and to permit persons to whom the Software is "
                       "furnished to do so, subject to the following conditions: \n"
                       "The above copyright notice and this permission notice shall be included in all "
                       "copies or substantial portions of the Software.\n"
                       "THE SOFTWARE IS PROVIDED ""AS IS"", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR "
                       "IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, "
                       "FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE "
                       "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER "
                       "LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, "
                       "OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE "
                       "SOFTWARE.")
            my_label.place(x=20, y=25)

        button = tk.Button(self, text="LICENSE", font=("Arial", 15), command=openNewWindow)
        button.place(x=643, y=375)

        button = tk.Button(self, text="Home", font=("Arial", 15), command=lambda: controller.show_frame(FirstPage))
        button.place(x=650, y=450)

        button = tk.Button(self, text="Back", font=("Arial", 15), command=lambda: controller.show_frame(SecondPage))
        button.place(x=100, y=450)


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # creating a window
        window = tk.Frame(self)
        window.pack()

        window.grid_rowconfigure(0, minsize=500)
        window.grid_columnconfigure(0, minsize=800)

        self.frames = {}
        for F in (FirstPage, SecondPage, ThirdPage):
            frame = F(window, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(FirstPage)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()
        self.title("CryptoFile")


app = Application()
app.maxsize(762, 500)
app.mainloop()
