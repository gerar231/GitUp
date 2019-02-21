import tkinter as tk
from tkinter import filedialog, ttk

proj_name = None
proj_dir = None

class GitUpApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry('600x350')
        self.title('GitUp')
        self._frame = None
        self.switch_frame(StartingMenu)

    def switch_frame(self, frame_class):
        if self._frame is not None:
            self._frame.destroy()
        self._frame = frame_class(self)
        self._frame.pack()

class StartingMenu(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text = "GitUp").pack()
        tk.Label (self, text = "v1.0.0").pack()
        tk.Button(self, text = "Login",
                command = lambda: master.switch_frame(LoginWindow)).pack()
        tk.Button(self, text = "Add Project",
                command = lambda: master.switch_frame(AddProjectMenu)).pack()
        tk.Button(self, text = "Open Project",
                command = lambda: master.switch_frame(OpenProjectMenu)).pack()
        tk.Button(self, text = "Remove Project",
                command = lambda: master.switch_frame(DeleteProjectMenu)).pack()

class LoginWindow(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text = "Username:").grid(column = 0, row = 0)
        tk.Label(self, text = "Password:").grid(column = 0, row = 1)
        self.username = tk.Entry(self)
        self.username.grid(column = 1, row = 0)
        self.password = tk.Entry(self)
        self.password.grid(column = 1, row = 1)
        tk.Button(self, text="Login",
                command = lambda: self.login(master)).grid(row = 2)
        tk.Button(self, text="Back",
                command = lambda: master.switch_frame(StartingMenu)).grid(column = 1, row=2)

    def login(self, master):
        if self.username.get() != "" and self.password.get != "":
            #TODO: Use username and password for OAuth
            master.switch_frame(StartingMenu)

class AddProjectMenu(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Button(self, text = "Back",
                command = lambda: master.switch_frame(StartingMenu))
        tk.Button(self, text = "Create New Project",
            command = lambda: master.switch_frame(CreateProject)).pack()
        tk.Button(self, text = "Add Existing Project",
            command = lambda: master.switch_frame(ExistingProjects)).pack()
        tk.Button(self, text = "Back",
                command = lambda: master.switch_frame(StartingMenu)).pack()

class CreateProject(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text = "Choose project name:").grid()
        self.name = tk.Entry(self)
        self.name.grid(column = 1, row = 0)
        tk.Button(self, text = "Create project",
            command = lambda: self.createFolder(master, self.name.get())).grid(row = 1)
        tk.Button(self, text = "Back",
                command = lambda: master.switch_frame(StartingMenu)).grid(column = 1, row = 1)

    def createFolder(self, master, projName):
        proj_loc = filedialog.askdirectory()
        #TODO: Create a repo on GitHub with name projName and clone it to proj_loc
        master.switch_frame(StartingMenu)
                

class ExistingProjects(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text = "Choose a project:").pack()
        projs = ["None", "hah"] #TODO: Get List of names of projects GitUp is currently tracking
        choose_proj = tk.ttk.Combobox(self, values = tuple(projs))
        choose_proj.pack()
        tk.Button(self, text = "Add Project",
                command = lambda: self.createFolder(master, choose_proj.get())).pack()
        tk.Button(self, text = "Back",
                command = lambda: master.switch_frame(StartingMenu)).pack()

    def createFolder(self, master, projName):
        proj_loc = filedialog.askdirectory()
        #TODO: clone the repo projName on GitHub to local at proj_loc
        master.switch_frame(StartingMenu)

class OpenProjectMenu(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Button(self, text = "Back",
                command = lambda: master.switch_frame(StartingMenu)).pack()
        tk.Label(self, text = "Choose a project:").pack()
        projs = ttk.Combobox(self, values = ("First project", "Second project"))
        projs.pack()
        tk.Button(self, text = "Open Project",
            command = lambda: self.openProject(master, projs.current())).pack()

    def fetchProjects(self):
        a = 1#TODO: Return a list of all the projects that are currently being tracked
    
    def openProject(self, master, projName):
        proj_dir = None #TODO: Get the full path to projName
        master.switch_frame(ProjectMenu)

class ProjectMenu(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Button(self, text = "View File",
                command = lambda: master.switch_frame(ViewFile)).pack()

class ViewFile(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        filename =  filedialog.askopenfilename(initialdir = proj_dir,
                title = "Select file",filetypes = (("text files", "*.txt"),("all files","*.*")))
        tk.Label(self, text=filename).pack()
        with open(filename, "r") as f:
            tk.Label(self, text=f.read(), justify = 'left').pack()
        tk.Button(self, text = "Back",
                command = lambda: master.switch_frame(StartingMenu)).pack()
        
        

class DeleteProjectMenu(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text = "Choose a project:").pack()
        projs = ["None", "hah"] #TODO: Get List of names of projects GitUp is currently tracking
        tk.ttk.Combobox(self, values = tuple(projs)).pack()
        tk.Button(self, text = "Back",
                command = lambda: master.switch_frame(StartingMenu)).pack()

if __name__ == "__main__":
    app = GitUpApp()
    app.mainloop()
