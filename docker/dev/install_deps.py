import sys
import subprocess
from distutils.core import run_setup

result = run_setup("/tmp/setup.py", stop_after="init")
requirements = result.install_requires
to_exec = [
    sys.executable,
    "-m",
    "pip",
    "install"
]
to_exec.extend(requirements)
subprocess.check_call(to_exec)