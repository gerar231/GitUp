import tkinter as tk
from tkinter import filedialog, ttk
from local_control import project_manager
from github_control import user_account

user = None
proj_manager = None
proj_name = None
proj_dir = None
repo = None

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
        global user
        print(user)
        tk.Label(self, text = "GitUp").pack()
        tk.Label (self, text = "v1.0.0").pack()
        if user == None:
            tk.Label(self, text = "No user").pack()
        else:
            tk.Label(self, text = user.get_name()).pack()
        tk.Button(self, text = "Login",
                command = lambda: master.switch_frame(LoginWindow)).pack()
        tk.Button(self, text = "Add Project",
                command = lambda: master.switch_frame(ExistingProjects)).pack()
        tk.Button(self, text = "View Project",
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
        self.password = tk.Entry(self, show='*')
        self.password.grid(column = 1, row = 1)
        tk.Button(self, text="Login",
                command = lambda: self.login(master)).grid(row = 2)
        tk.Button(self, text="Back",
                command = lambda: master.switch_frame(StartingMenu)).grid(column = 1, row=2)

    def login(self, master):
        if self.username.get() != "" and self.password.get != "":
            global user
            user = user_account.UserAccount(self.username.get(), self.password.get())
            print(user.get_name())
            print(user.get_profile_image_url())
            print(user.get_profile_url())
            print(user)
            global project_manager
            project_manager = project_manager.ProjectManager(user)
            master.switch_frame(StartingMenu)
'''
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
        project_manager.view_project_repo(projName + proj_loc)
        master.switch_frame(StartingMenu)
'''                

class ExistingProjects(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text = "Choose a project to restore:").pack()
        global user
        projs = [i[0] for i in user.get_remote_repos()]
        choose_proj = tk.ttk.Combobox(self, values = projs)
        choose_proj.pack()
        tk.Button(self, text = "Add Project",
                command = lambda: self.createFolder(master, choose_proj.get())).pack()
        tk.Button(self, text = "Back",
                command = lambda: master.switch_frame(StartingMenu)).pack()

    def createFolder(self, master, projName):
        proj_loc = filedialog.askdirectory()
        project_manager.restore_project_repo(proj_loc, projName)
        master.switch_frame(StartingMenu)

class OpenProjectMenu(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Button(self, text = "Back",
                command = lambda: master.switch_frame(StartingMenu)).pack()
        tk.Button(self, text = "Open Project",
            command = lambda: self.openProject(master)).pack()

    def openProject(self, master):
        global proj_dir
        proj_dir = filedialog.askdirectory(initialdir = "/")
        global project_manager
        #project_manager.view_project_repo(proj_dir)
        master.switch_frame(ProjectMenu)

class ProjectMenu(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Button(self, text = "View File",
                command = lambda: master.switch_frame(ViewFile)).pack()
        scrollbar = tk.Scrollbar(master)
        scrollbar.pack(side="right", fill="y")
        listbox = tk.Listbox(master, yscrollcommand=scrollbar.set)
        commits = ['1', '2', '3']
        for commit in commits:
            listbox.insert(tk.END, commit)
        scrollbar.config(command=listbox.yview)
        listbox.pack(side="left", fill="both", expand=1)

class ViewFile(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        global proj_dir
        filename =  filedialog.askopenfilename(initialdir = proj_dir,
                title = "Select file",filetypes = (("text files", "*.txt"),("all files","*.*")))
        tk.Label(self, text=filename).pack()
        with open(filename, "r") as f:
            tk.Label(self, text=f.read(), justify = 'left').pack()
        tk.Button(self, text = "Back",
                command = lambda: master.switch_frame(StartingMenu)).pack()
        
'''       
class FileView(tk.Frame):
    def __init__(self, master, file):
        tk.Frame.__init__(self, master)
        self.file = file
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        tk.Label(self, text="Old Version").grid()
        commits = self.getCommits()
        pre_version = tk.ttk.Combobox(self, values = tuple(commits))
        pre_version.grid(column = 1)
        tk.Label(self, text="New Version").grid(column = 2)
        post_version = tk.ttk.Combobox(self, values = tuple(commits))
        post_version.grid(column = 3)
        tk.Button(self, text = "Compare",
            command = lambda: compareVersions(file))

    def getCommits():
        #TODO: get list of all past versions of file
        return ["1", "2", "3"]

    def compareVersions(file):
        
        
'''
class DeleteProjectMenu(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text = "Choose a project:").pack()
        projs = ["None", "hah"] #TODO: Get List of names of projects GitUp is currently tracking
        options = tk.ttk.Combobox(self, values = tuple(projs)).pack()
        tk.Button(self, text = "Delete Project",
                command = project_manager.delete_project_repo(options.get()))
        tk.Button(self, text = "Back",
                command = lambda: master.switch_frame(StartingMenu)).pack()

if __name__ == "__main__":
    app = GitUpApp()
    app.mainloop()
