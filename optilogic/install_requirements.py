
import os
import subprocess

def ensure_requirements():
    result = subprocess.run(f'pip3 install -r "{os.getcwd()}/requirements.txt"', shell=True, capture_output=True)
    result.check_returncode()
    print(result.stdout.decode('utf-8'))