# accubooks

### create txt from .venv (if activated) of libs used in project
`pip3 freeze > requirements.txt`

### recreate exe file with configs
`pyinstaller accubooks.spec`

### create new environment
`python3 -m venv .venv`

### activate venv
`source .venv/bin/activate`

### To uninstall all packages except for pip itself
`pip3 freeze | grep -v "^pip3==" | xargs pip3 uninstall -y`


