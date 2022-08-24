# GUI related libraries
import tkinter as tk
from tkinter.ttk import Progressbar

# system management
import pwd, os, subprocess

from tkinter.ttk import Progressbar
# the skeleton of this is ripped directly from the answer to this stack overflow question
# https://stackoverflow.com/questions/63017238/how-to-switch-between-different-tkinter-canvases-from-a-start-up-page-and-return

class StartingBlock(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._mainCanvas = None
        self.title("StartingBlock")
        # The dictionary to hold the class type to switch to
        # Each new class passed here, will only have instance or object associated with it (i.e the result of the Key)
        self._allCanvases = dict()
        # Switch (and create) the single instance of StartUpPage
        self.switch_Canvas(StartUpPage)

    def switch_Canvas(self, Canvas_class):

        # Unless the dictionary is empty, hide the current Frame (_mainCanvas is a frame)
        if self._mainCanvas:
            self._mainCanvas.pack_forget()

        # is the Class type passed one we have seen before?
        canvas = self._allCanvases.get(Canvas_class, False)

        # if Canvas_class is a new class type, canvas is False
        if not canvas:
            # Instantiate the new class
            canvas = Canvas_class(self)
            # Store it's type in the dictionary
            self._allCanvases[Canvas_class] = canvas

            # Pack the canvas or self._mainCanvas (these are all frames)
        canvas.pack(pady=60)
        # and make it the 'default' or current one.
        self._mainCanvas = canvas

class StartUpPage(tk.Canvas):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.canvas = tk.Canvas(self, height=200, width=430)

        Explanation = tk.Label(self.canvas,
                               text="Welcome to StartingBlock! \n This program was made to help setting up a Gitlab Runner that much easier \n Click Get Started to download dependencies")
        Explanation.pack()

        def installPackages():
            list = ["curl", "git"]
            for i in list:
                subprocess.run(["apt-get", "install", "-y", i])
                pb["value"] += 50
                self.canvas.update_idletasks()
                txt["text"] = pb['value'], '%'
                self.canvas.update_idletasks()

        pb = Progressbar(self.canvas, orient=tk.HORIZONTAL, length=100, mode="determinate")
        pb.pack()

        txt = tk.Label(self.canvas, text="0%", bg="#345", fg="#fff")
        txt.pack()

        StartDownload = tk.Button(self.canvas,
                                  text="Install required packages and move on to the next step",
                                  command=lambda: [installPackages(), master.switch_Canvas(CreateUser)])
        StartDownload.pack()

        self.canvas.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

class CreateUser(tk.Canvas):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.canvas = tk.Canvas(self, height=200, width=430)

        UsernameExplanation = tk.Label(self.canvas,
                                       text="Next up, we need to create user account explicitly for the Gitlab Runner software")
        UsernameExplanation.pack()

        self.canvas.usernameEntry = tk.Entry(self.canvas)
        self.canvas.usernameEntry.pack()

        PasswordExplanation = tk.Label(self.canvas, text="Enter a password below")
        PasswordExplanation.pack()

        self.canvas.passwordEntry = tk.Entry(self.canvas)
        self.canvas.passwordEntry.pack()

        def CreateUser():
            special_characters = ["\"", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "+", "?", "=",
                                  ",", "<", ">", "/"]

            username = self.canvas.usernameEntry.get()

            if any(c in special_characters for c in username):
                WarnUser()

            username = self.canvas.usernameEntry.get()
            subprocess.run(["sudo", "useradd", "--comment", username, "--create-home", username, "--shell",
                            "/bin/bash"])

        def CreatePassword():
            password = self.canvas.passwordEntry.get()
            username = self.canvas.usernameEntry.get()

            # encode string for use as a psuedo file to pass as stdin to passwd commmand below

            changePassword = subprocess.Popen(["passwd", username], stdin=subprocess.PIPE)
            # I had to use the same line of code twice below because the passwd command asks for password change confirmation
            changePassword.stdin.write('{}\n'.format(password).encode('utf-8'))
            changePassword.stdin.write('{}\n'.format(password).encode('utf-8'))
            changePassword.stdin.flush()

        def PermissionSet():
            username = self.canvas.usernameEntry.get()
            sudoerfileLocation = "/etc/sudoers/"
            sudoerfile = open(sudoerfileLocation, "a")
            PermString = username + " ALL=(ALL) NOPASSWD: /usr/bin/apt, /usr/bin/snap"
            sudoerfile.write(PermString)
            sudoerfile.close()

        def CreateSSHKey():
            username = self.canvas.usernameEntry.get()
            password = self.canvas.usernameEntry.get()
            # changing to gitlab-runner user to create ssh key
            uid = pwd.getpwnam(username)[2]
            os.setuid(uid)

            SSHLoc = "/home/" + username + "/ssh_key"

            subprocess.run(["ssh-keygen", "-t", "rsa", "-b", "2048", "-P", password, "-f", SSHLoc])

        def startSSH(cls) -> 'SshAgent':
            username = self.canvas.usernameEntry.get()
            SSHLoc = "/home/" + username + "/ssh_key"
            print("Starting ssh-agent")
            output = subprocess.check_output(['ssh-agent', '-s'])
            agent_env = cls.parse_agent_env(output)
            subprocess.run(["ssh-add", SSHLoc])
            return cls(agent_env)

        def WarnUser():
            self.canvas.Warning = tk.Label(
                text="An Ubuntu username can contain only the _ and - special characters. \n Please try again")
            self.canvas.Warning.pack()

        CreateAccountButton = tk.Button(self, text="Create Account and Move On",
                                        command=lambda: [CreateUser(), CreatePassword(), PermissionSet(), CreateSSHKey(), startSSH(),
                                                         master.switch_Canvas(InstallGitlab)])
        CreateAccountButton.pack()

        self.canvas.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

class InstallGitlab(tk.Canvas):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.canvas = tk.Canvas(self, height=200, width=430)

        Explanation = tk.Label(self.canvas, text="Next, we need to install Gitlab and set job concurrency. \n"
                                                 "Enter how many jobs you would like this runner to process at once.")
        Explanation.pack()

        def DownloadInstall():
            subprocess.run(["sudo", "curl", "-L", "--output", "/usr/local/bin/gitlab-runner",
                            "https://gitlab-runner-downloads.s3.amazonaws.com/latest/binaries/gitlab-runner-linux-amd64"])
            pb["value"] += 45
            txt["text"] = pb['value'], '%'
            self.canvas.update_idletasks()

            subprocess.run(["sudo", "chmod", "+x", "/usr/local/bin/gitlab-runner"])
            pb["value"] += 5
            txt["text"] = pb['value'], '%'
            self.canvas.update_idletasks()

            # for some reason I need to add the shell=True part would love to know why
            subprocess.run(["cd", "/usr/local/bin/"], shell=True)
            pb["value"] += 5
            txt["text"] = pb['value'], '%'
            self.canvas.update_idletasks()

            subprocess.run(["sudo", "gitlab-runner", "install", "--user=gitlab-runner",
                            "--working-directory=/home/gitlab-runner"])
            pb["value"] += 45
            txt["text"] = pb['value'], '%'
            self.canvas.update_idletasks()


        NumJobs = tk.Entry(self.canvas)
        NumJobs.pack()

        def Concurrency():
            ConcurrentJobs = NumJobs.get()

            print(ConcurrentJobs)

            with open("/etc/gitlab-runner/config.toml", 'r') as fin:
                data = fin.read().splitlines(True)
            with open('/etc/gitlab-runner/config.toml', 'w') as fout:
                fout.writelines(data[1:])
                fout.writelines("\n concurrent = " + ConcurrentJobs)


        pb = Progressbar(self.canvas, orient=tk.HORIZONTAL, length=100, mode="determinate")
        pb.pack()

        txt = tk.Label(self.canvas, text="0%", bg="#345", fg="#fff")
        txt.pack()

        self.canvas.DownloadInstallButton = tk.Button(self.canvas,
                                                      text="Click me to download and install Gitlab",
                                                      command=lambda: [DownloadInstall(), Concurrency(),
                                                                       master.switch_Canvas(GetRegKey)])
        self.canvas.DownloadInstallButton.pack()


        self.canvas.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

class GetRegKey(tk.Canvas):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.canvas = tk.Canvas(self, height=200, width=430)

        Explanation = tk.Label(self.canvas,
                               text="Now we need to register this runner, copy and paste the URL and token in the appropriate entry boxes")
        Explanation.pack()

        URLExplanation = tk.Label(self.canvas, text="Enter the Gitlab(?) URL in below:")
        URLExplanation.pack()
        self.canvas.URLEntry = tk.Entry(self.canvas)
        self.canvas.URLEntry.pack()

        TokenExplanation = tk.Label(text="Enter the token below")
        TokenExplanation.pack()
        self.canvas.TokenEntry = tk.Entry(self.canvas)
        self.canvas.TokenEntry.pack()

        def DownloadInstall():
            URL = self.canvas.URLEntry.get()
            Token = self.canvas.TokenEntry.get()

            subprocess.run(
                ["sudo", "gitlab-runner", "register", "--url", URL, "--registration-token", Token])

        RegisterRunner = tk.Button(self.canvas, text="Register!", command=lambda: [DownloadInstall()])
        RegisterRunner.pack()

        self.canvas.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)











