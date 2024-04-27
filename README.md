# accubooks

## developers:
### create txt from .venv (if activated) of libs used in project
`pip3 freeze > requirements.txt`

### recreate exe file with configs
`pyinstaller accubooks.spec`

## create new environment
`python3 -m venv .venv`

### activate venv
`source .venv/bin/activate`

## to uninstall all packages except for pip itself
`pip3 freeze | grep -v "^pip3==" | xargs pip3 uninstall -y`


## to run:
```
1. from src directory:
run pyinstaller accubooks.spec

2. build and dist/accubooks.exe will be built.
open accubooks.exe from finder. double click to run.

note: must have JRE in your computer to run.
```