import Tkinter as tki # Tkinter -> tkinter in Python3
import tkFileDialog, tkMessageBox
from graphics import GraphWin
import subprocess, os

class IDE(object):

    def __init__(self):
        self.root = tki.Tk()
        self.filename = None
        # crea la ventana maximizada
        # self.root.state('zoomed')
        # self.root.wm_minsize(width=1000, height=600)
    # configure the Menu
        menu = tki.Menu(self.root)
        self.root.config(menu=menu)
        self.root.wm_title("Project Cobra")
        filemenu = tki.Menu(menu)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Open...", command=self.open_file)
        filemenu.add_command(label="Save", command=self.save, accelerator="Ctrl+s")
        filemenu.add_command(label="Save As...", command=self.save_as)
        filemenu.add_command(label="Exit", command=self.close)

        self.root.bind_all("<Control-s>", self.save)

        helpmenu = tki.Menu(menu)
        menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About...", command=self.about)

    # create a Frame for the Text and Scrollbar
        self.txt_frm = tki.Frame(self.root, width=1000, height=700, background="bisque")
        self.txt_frm.pack(fill=tki.BOTH)
    #     # ensure a consistent GUI size
        self.txt_frm.grid_propagate(False)
    #     # implement stretchability
        self.txt_frm.grid_rowconfigure(1, weight=1)
        self.txt_frm.grid_columnconfigure(0, weight=1)

    # # create a Text widget
        self.txt = tki.Text(self.txt_frm, borderwidth=3, relief="sunken")
        self.txt.config(font=("consolas", 12), undo=True, wrap='word')
        self.txt.grid(row=1, column=0, sticky="nsew")

    #  create a Scrollbar and associate it with txt
        scrollb = tki.Scrollbar(self.txt_frm, command=self.txt.yview)
        scrollb.grid(row=1, column=0, sticky='nsew')
        self.txt['yscrollcommand'] = scrollb.set

        redbutton = tki.Button(self.txt_frm, text="Run", fg="black",  height = 2, width = 10,  command=self.runCode)
        redbutton.grid(row=0, column=0, sticky='nsew')
        

        # define options for opening or saving a file
        self.file_opt = options = {}
        options['defaultextension'] = '.cbr'
        options['filetypes'] = [('Project Cobra Files', '.cbr')]
        options['initialdir'] = 'C:\\'
        options['initialfile'] = ''
        options['parent'] = self.root
        options['title'] = 'Select your file'

        # TODO: line number http://stackoverflow.com/questions/16369470/tkinter-adding-line-number-to-text-widget
    

    def open_file(self):
        # get filename
        self.filename = tkFileDialog.askopenfilename(**self.file_opt)
        
        # open file on your own
        if self.filename:
            archivo = open(self.filename, 'r')
            self.txt.delete("1.0", tki.END)
            self.txt.insert(tki.INSERT, archivo.read())
            archivo.close()
            self.filename = os.path.basename(self.filename)
            self.root.wm_title("Project Cobra - " + self.filename)

    def save_as(self):
        """Returns an opened file in write mode."""

        export = tkFileDialog.asksaveasfile(mode='w', **self.file_opt)
        self.filename = os.path.basename(export.name)
        self.root.wm_title("Project Cobra - " + self.filename)

    def save(self, event=None):

        """Returns an opened file in write mode.
        This time the dialog just returns a filename and the file is opened by your own code.
        """
        # open file on your own
        if self.filename:
            archivo = open(self.filename, 'w')
            archivo.write(self.txt.get("1.0", tki.END))
            archivo.close()
        else:
            self.save_as()

    def about(self):
        pass
        info = '''
        Compiladores
        Julio 
        Jose Fernando'''
        tkMessageBox.showinfo("About",info)

    def close(self):
        if tkMessageBox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            self.root.quit()

    def runCode(self):

    # obtener 
        nombre = "output.cbr"
        archivo = open(nombre, "w")
        archivo.write(self.txt.get("1.0", tki.END)) 
        archivo.close()
        subprocess.Popen('python parser.py '+ nombre)

app = IDE()
app.root.protocol("WM_DELETE_WINDOW", app.close)
app.root.mainloop()
