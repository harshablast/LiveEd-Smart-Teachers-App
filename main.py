from tkinter import *
from tkinter import ttk
from ttkthemes import themed_tk as tk
from tkinter.scrolledtext import ScrolledText

root = tk.ThemedTk()
root.get_themes()
root.set_theme("radiance")
f1 = Frame(root, height=1080, width=1920, bg="white")

f1.pack()
f1.pack_propagate(0)
nb = ttk.Notebook(f1, height=430, width=360)

style = ttk.Style()
style.theme_create("MyStyle", parent="alt", settings={
    "TNotebook": {"configure": {"tabmargins": [2, 2, 2, 0]}},
    "TNotebook.Tab": {"configure": {"padding": [100, 10]}, }})

style.theme_use("MyStyle")

# signup page
signup_page = ttk.Frame(nb)
sfname = Entry(signup_page)
sfname.insert(0, 'Name')
susername = Entry(signup_page)
susername.insert(0, 'Username')
seid = Entry(signup_page)
spw = Entry(signup_page)

sfname.place(relx=0.5,rely=0.3,anchor=CENTER)
susername.place(relx=0.5,rely=0.4,anchor=CENTER)
seid.place(relx=0.5,rely=0.5,anchor=CENTER)
spw.place(relx=0.5,rely=0.6,anchor=CENTER)


login_page = ttk.Frame(nb)

nb.add(signup_page, text='Sign Up')
nb.add(login_page, text='Login')
nb.pack(expand=1, anchor='center')

root.mainloop()
