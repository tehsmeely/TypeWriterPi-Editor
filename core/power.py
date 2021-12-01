import sys, os

_win_shutdown = "shutdown /s /t 0"
_win_restart = "shutdown /r /t 0"
_linux_shutdown = "shutdown now"
_linux_restart = "reboot"


def shutdown():
    if sys.platform == "win32":
        cmd = _win_shutdown
    else:
        cmd = _linux_shutdown
    print("Issuing: {}".format(cmd))
    os.system(cmd)


def restart():
    if sys.platform == "win32":
        cmd = _win_restart
    else:
        cmd = _linux_restart
    print("Issuing: {}".format(cmd))
    os.system(cmd)
