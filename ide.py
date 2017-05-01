import Tkinter as tk # Tkinter -> tkinter in Python3
import tkFileDialog, tkMessageBox
from graphics import GraphWin
import subprocess, os


class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        '''redraw line numbers'''
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2,y,anchor="nw", text=linenum)
            i = self.textwidget.index("%s+1line" % i)

class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

        self.tk.eval('''
            proc widget_proxy {widget widget_command args} {

                # call the real tki widget command with the real args
                set result [uplevel [linsert $args 0 $widget_command]]

                # generate the event for certain types of commands
                if {([lindex $args 0] in {insert replace delete}) ||
                    ([lrange $args 0 2] == {mark set insert}) || 
                    ([lrange $args 0 1] == {xview moveto}) ||
                    ([lrange $args 0 1] == {xview scroll}) ||
                    ([lrange $args 0 1] == {yview moveto}) ||
                    ([lrange $args 0 1] == {yview scroll})} {

                    event generate  $widget <<Change>> -when tail
                }

                # return the result from the real widget command
                return $result
            }
            ''')
        self.tk.eval('''
            rename {widget} _{widget}
            interp alias {{}} ::{widget} {{}} widget_proxy {widget} _{widget}
        '''.format(widget=str(self)))

class EditCont(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.text = CustomText(self)
        self.vsb = tk.Scrollbar(orient="vertical", command=self.text.yview)
        self.linenumbers = TextLineNumbers(self, width=30)
        self.linenumbers.attach(self.text)

        self.vsb.pack(side="right", fill="y")
        self.linenumbers.pack(side="left", fill="y")
        self.text.pack(side="right", fill="both", expand=True)

        self.text.bind("<<Change>>", self._on_change)
        self.text.bind("<Configure>", self._on_change)


    def _on_change(self, event):
        self.linenumbers.redraw()
    
    def insert(self, texto):
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.INSERT, texto)

    def getText(self):
        return self.text.get("1.0", tk.END)

class IDE(object):

    def __init__(self):
        self.root = tk.Tk()
    
        self.filename = None
        self.closing = False
        
        # self.root.wm_minsize(width=1000, height=600)
    # configure the Menu
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        self.root.wm_title("Project Cobra")
        filemenu = tk.Menu(menu)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Open...", command=self.open_file)
        filemenu.add_command(label="Save", command=self.save, accelerator="Ctrl+s")
        filemenu.add_command(label="Save As...", command=self.save_as)
        filemenu.add_command(label="Exit", command=self.close)
    
    # shortcuts
        self.root.bind_all("<Control-s>", self.save)

        helpmenu = tk.Menu(menu)
        menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About...", command=self.about)

        self.editContainer = EditCont(self.root)
        self.editContainer.pack(side="bottom", fill="both", expand=True)
        redbutton = tk.Button(self.root, text="Run", fg="white", bg="#263238", command=self.runCode)
        redbutton.pack(side="top", fill="both",  padx=10, pady=5)


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
            self.editContainer.insert(archivo.read())
            archivo.close()
            self.filename = os.path.basename(self.filename)
            self.root.wm_title("Project Cobra - " + self.filename)

    def save_as(self):
        """Returns an opened file in write mode."""

        export = tkFileDialog.asksaveasfile(mode='w', **self.file_opt)
        # open file on your own
        if export:
            archivo = open(self.filename, 'w')
            archivo.write(self.editContainer.getText())
            archivo.close()
            return archivo
            self.filename = os.path.basename(export.name)
            self.root.wm_title("Project Cobra - " + self.filename)

        return export

    def save(self, event=None):

        """Returns an opened file in write mode.
        This time the dialog just returns a filename and the file is opened by your own code.
        """
        # open file on your own
        print self.filename
        if self.filename:
            archivo = open(self.filename, 'w')
            archivo.write(self.editContainer.getText())
            archivo.close()
        else:
            self.save_as()

    def about(self):
        pass
        info = '''
                        Tec de Monterrey                    
                
                        Compilers Design
                            Mayo 2017
                       Maestra: Elda Quiroga
                
                        Desarrollado por:
                        
                        Julio Cesar Aguilar 
                        Jose Fernando Davila 
        
        '''
        tkMessageBox.showinfo("About",info)

    def close(self):

        if tkMessageBox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            self.root.quit()

    def runCode(self):

    # Guarda el codigo en un archivo y lo ejecuta
        nombre = "output.cbr"
        archivo = open(nombre, "w")
        archivo.write(self.editContainer.getText()) 
        archivo.close()
        subprocess.Popen('python parser.py '+ nombre)

app = IDE()
app.root.protocol("WM_DELETE_WINDOW", app.close)
app.root.mainloop()
