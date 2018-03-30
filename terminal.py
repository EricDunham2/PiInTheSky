import subprocess, shlex

class Terminal :
    def __init__(self,root) :
        self.allow_root = root

    def execute(self,cmd) :
        if not self.allow_root :
            cmd = cmd.replace('sudo','nogosudotruedoe')
            args = shlex.split(cmd)
            return subprocess.check_output(args)
