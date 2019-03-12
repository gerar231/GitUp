import sys
import os
import tkinter as tk
from tkinter import filedialog, ttk
import git
from git import Repo
from git import Commit
import time
sys.path.append(os.path.normpath(os.path.join(os.path.realpath(__file__), "..", "..")))
from local_control import project_manager
from github_control import user_account

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
        global user   
        try:
            user = user_account.UserAccount("/tmp/gitup/token.txt")
            self.switch_frame(StartingMenu)
        except ValueError:
            self.switch_frame(LoginWindow)
 
    def switch_frame(self, frame_class):
        if self._frame is not None:
            self._frame.destroy()
        self._frame = frame_class(self)
        self._frame.pack()


class StartingMenu(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        global user
        global proj_manager
        if proj_manager is None:
            proj_manager = project_manager.ProjectManager(user)
        tk.Label(self, text = "GitUp").pack()
        tk.Label (self, text = "v1.0.0").pack()
        tk.Label(self, text = "Welcome " + user.get_login() + "!").pack()
        tk.Button(self, text = "Logout",
                command = lambda: master.switch_frame(LoginWindow)).pack()
        tk.Button(self, text = "Add Project",
                command = lambda: master.switch_frame(ExistingProjects)).pack()
        tk.Button(self, text = "View Project",
                command = lambda: master.switch_frame(OpenProjectMenu)).pack()
        tk.Button(self, text = "Remove Project", state = tk.DISABLED,
                command = lambda: master.switch_frame(DeleteProjectMenu)).pack()

# Login window for GitUp
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
            user = user_account.UserAccount(self.username.get(), self.password.get(), "/tmp/gitup/token.txt")
            master.switch_frame(StartingMenu)
          

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
        proj_manager.restore_project_repo(proj_loc, projName)
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
        global proj_manager
        repo = proj_manager.find_project_repo(proj_dir)
        if repo is None:
            repo = proj_manager.view_project_repo(proj_dir)
        #repo = Repo(proj_dir)
        master.switch_frame(ProjectMenu)

class ProjectMenu(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Button(self, text = "View File",
                command = lambda: master.switch_frame(ViewFile)).grid()
        '''
        scrollbar = tk.Scrollbar(self)
        scrollbar.grid(column= 1, sticky='ns')
        listbox = tk.Listbox(self, yscrollcommand=scrollbar.set)
        commitlist = list(repo.iter_commits('--all'))
        for commit in commitlist:
            time = time.localtime(commit.committed_date)
            key = "%a, %d %b %Y %H:%M"
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
        '''

class ViewFile(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        global proj_dir
        global proj_manager
        self.filename =  filedialog.askopenfilename(initialdir = proj_dir,
                title = "Select file",filetypes = (("text files", "*.txt"),("all files","*.*")))
        self.filename = self.filename.replace(proj_dir, '')
        tk.Button(self, text = "Back",
                command = lambda: master.switch_frame(StartingMenu)).grid()
        compare = tk.Button(self, text = "Compare",
                command = lambda: self.getDiff()).grid(row=1,column=4)
        #tk.Label(self, text=filename).grid(column=1)
        self.commits = list(repo.iter_commits('--all', paths=proj_dir + "/" + self.filename))
        commit_dates = [time.strftime("%a, %d %b %Y %H:%M", time.localtime(commit.committed_date)) for commit in self.commits]
        tk.Label(self, text = "Old Version").grid(row = 1)        
        self.pre_version = tk.ttk.Combobox(self, values = commit_dates)
        self.pre_version.grid(row = 1, column = 1)
        self.pre_version.current(0)
        tk.Label(self, text="New Version").grid(row = 1, column = 2)
        self.post_version = tk.ttk.Combobox(self, values = commit_dates)
        self.post_version.grid(row = 1, column = 3)
        self.text = tk.Text(self)
        self.text.tag_config("del", background="#fcc9c9", foreground="red")
        self.text.tag_config("add", background="#ccfcc9", foreground="#1e9e16")
        scrollbar = tk.Scrollbar(self, command=self.text.yview)
        scrollbar.grid(row = 2, column= 4, sticky='ns')
        self.text.config(state = tk.DISABLED)
        self.text.grid(row = 2, columnspan = 4)
        self.text['yscrollcommand'] = scrollbar.set
        self.post_version.current(0)
        self.getDiff()

    def getDiff(self):       
        global repo
        global proj_dir
        self.text.config(state = tk.NORMAL)
        self.text.delete('1.0', tk.END)
        if self.pre_version.current() == self.post_version.current():
            with open(proj_dir + "/" + self.filename, "r") as f:
                self.text.insert(tk.END, f.read())
        diff_contents = repo.git.diff(self.commits[self.pre_version.current()], self.commits[self.post_version.current()], proj_dir + "/" + self.filename)
        diff_lines = diff_contents.splitlines()
        for line in diff_lines[4:]:
            if len(line) > 0 and line[0] == '-':
                self.text.insert(tk.END, line + '\n', 'del')
            elif len(line) > 0 and line[0] == '+':
                self.text.insert(tk.END, line + '\n', 'add')
            elif len(line) > 0 and line[:2] != '@@':
                self.text.insert(tk.END, line + '\n')
        self.text.config(state = tk.DISABLED)
        
        
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
                command = proj_manager.delete_project_repo(options.get()))
        tk.Button(self, text = "Back",
                command = lambda: master.switch_frame(StartingMenu)).pack()

if __name__ == "__main__":
    app = GitUpApp()
    app.mainloop()
