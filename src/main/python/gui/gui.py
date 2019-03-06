import tkinter as tk
from tkinter import filedialog, ttk
from local_control import project_manager
from github_control import user_account
import git
from git import Repo
from git import Commit
import time

user = None
proj_manager = None
proj_name = None
proj_dir = None
repo = None

# Main Application
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
            tk.Label(self, text = user.get_id()).pack()
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
        global repo
        repo = Repo(proj_dir)
        global project_manager
        #project_manager.view_project_repo(proj_dir)
        master.switch_frame(ProjectMenu)

class ProjectMenu(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        print("yo")
        tk.Button(self, text = "View File",
                command = lambda: master.switch_frame(ViewFile)).grid()
        scrollbar = tk.Scrollbar(self)
        scrollbar.grid(column= 1, sticky='ns')
        listbox = tk.Listbox(self, yscrollcommand=scrollbar.set)
        self.commits = {
                    "1/24":["14:23", "15:32"],
                    "1/22":["2:42"]
                }
        for group in self.commits.keys():
            listbox.insert(tk.END, group)
        scrollbar.config(command=listbox.yview)
        listbox.grid(row=1)
        listbox.bind('<Double-1>', lambda x: self.viewDetailedCommits(listbox.get(listbox.curselection())))

    def viewDetailedCommits(self, groupName):
        commitWindow = tk.Toplevel()
        scrollbar = tk.Scrollbar(commitWindow)
        scrollbar.grid(column= 1, sticky='ns')
        listbox = tk.Listbox(commitWindow, yscrollcommand=scrollbar.set)
        for commit in self.commits[groupName]:
            listbox.insert(tk.END, commit)
        # listbox.insert(tk.END, "BACK")
        scrollbar.config(command=listbox.yview)
        listbox.grid(row=1)
        # listbox.bind('<Double-1>', lambda x: self.getFileViewer())

class ViewFile(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        global proj_dir
        print(proj_dir)
        global project_manager
        self.filename =  filedialog.askopenfilename(initialdir = proj_dir,
                title = "Select file",filetypes = (("text files", "*.txt"),("all files","*.*")))
        self.filename = self.filename.replace(proj_dir, '')
        tk.Button(self, text = "Back",
                command = lambda: master.switch_frame(StartingMenu)).grid()
        #tk.Label(self, text=filename).grid(column=1)
        self.commits = repo.iter_commits('--all', paths=proj_dir + "/" + self.filename)
        commit_dates = [time.strftime("%a, %d %b %Y %H:%M", time.localtime(commit.committed_date)) for commit in self.commits]
        tk.Label(self, text = "Old Version").grid(row = 1)        
        self.pre_version = tk.ttk.Combobox(self, values = commit_dates)
        self.pre_version.grid(row = 1, column = 1)
        tk.Label(self, text="New Version").grid(row = 1, column = 2)
        self.post_version = tk.ttk.Combobox(self, values = commit_dates)
        self.post_version.grid(row = 1, column = 3)
        text = tk.Text(self)
        text.tag_config("del", background="#fcc9c9", foreground="red")
        text.tag_config("add", background="#ccfcc9", foreground="#1e9e16")
        with open(proj_dir + "/" + self.filename, "r") as f:
            file_contents = f.read().splitlines()
            for line in file_contents:
                if len(line) > 0 and line[0] == 'd':
                    text.insert(tk.END, line + '\n', 'del')
                elif len(line) > 0 and line[0] == 'm':
                    text.insert(tk.END, line + '\n', 'add')
                else:
                    text.insert(tk.END, line + '\n')
        scrollbar = tk.Scrollbar(self, command=text.yview)
        scrollbar.grid(row = 2, column= 4, sticky='ns')
        text.config(state = tk.DISABLED)
        text.grid(row = 2, columnspan = 4)
        text['yscrollcommand'] = scrollbar.set
        self.pre_version.bind("<<ComboboxSelected>>", self.getDiff())
        self.post_version.bind("<<ComboboxSelected>>", self.getDiff())

    def getDiff(self):
        return "1"        
        self.commits = ["1"]
        pre_commit = self.commits[self.pre_version.current()].hexsha
        post_commit = self.commits[self.post_version.current()].hexsha
        diff_contents = "hi!" # GET DIFF CONTENTS HERE
        diff_lines = diff_contents.splitlines()
        for line in file_contents:
            if len(line) > 0 and line[0] == '-':
                text.insert(tk.END, line + '\n', 'del')
            elif len(line) > 0 and line[0] == '+':
                text.insert(tk.END, line + '\n', 'add')
            else:
                text.insert(tk.END, line + '\n')
        
        
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
