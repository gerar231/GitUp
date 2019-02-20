import tkinter as tk
from tkinter import filedialog, ttk

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

class LoginWindow(tk.frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text = "Username:").grid(column = 0, row = 0)
        tk.Label(self, text = "Password:").grid(column = 0, row = 1)
        self.username = tk.Entry(self).grid(column = 1, row = 0)
        self.password = tk.Entry(self).grid(column = 1, row = 1)
        tk.Button(self, text="Login",
            command = self.login()).grid(row = 2)

    def login(self):
        if self.username.get() == None:
            return false

class AddProjectMenu(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Button(self, text = "Back",
                command = lambda: master.switch_frame(StartingMenu))
        tk.Button(self, text = "Create New Project",
            command = self.createProject).pack()
        tk.Button(self, text = "Add Existing Project").pack()
        tk.Button(self, text = "Back",
                command = lambda: master.switch_frame(StartingMenu)).pack()
    def createProject(*args):
        tkFileDialog.askopenfilename(initialdir = "/",title = "Select file",filetypes =
                (("jpeg   files","*.jpg"),("all files","*.*")))

class OpenProjectMenu(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Button(self, text = "Back",
                command = lambda: master.switch_frame(StartingMenu)).pack()
        tk.Label(self, text = "Choose a project:").pack()
        projs = ttk.Combobox(self, values = ("First project", "Second project")).pack()
        tk.Button(self, text = "Open Project",
            command = self.openProject(projs.current()))

    def openProject(projName):
        a = 1
 
class ProjectViewMenu(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Button(self, text = "View File History",
                command = viewFileHistory)

    def viewFileHistory():
        tkFileDialog.askopenfilename(initialdir = proj_dir,title = "Select file to view history",
                filetypes = (("jpeg   files","*.jpg"),("all files","*.*")))
        

class DeleteProjectMenu(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Button(self, text = "Back",
                command = lambda: master.switch_frame(StartingMenu))
        tk.Label(self, text = "Choose a project:").pack()
        tk.ttk.Combobox(self, values = ("First project", "Second project")).pack()

if __name__ == "__main__":
    app = GitUpApp()
    app.mainloop()
