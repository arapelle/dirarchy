# `temgen`

 A tool generating a directory architecture or a file, from a template.

# Example
A template example stored to path/to/template.xml:
```XML
<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
        <var name="message" type="str" />
    </vars>
    <dir path="{project_root_dir}">
        <file path="data.txt">
"{message}"
        </file>
    </dir>
</template>
```
It is used with temgen simply like that:
```commandline
temgen path/to/template.xml
```
For project_root_dir = "project" and message = "coucou", temgen will generate the following dir architecture:
```
project
 `-- data.txt (contents:coucou\n)
```

# Install

Clone the project (if it is not already the case):
```commandline
cd $(mktemp -d) && git clone https://github.com/arapelle/temgen.git
```

To install a specific version of temgen:\
**- Release:**
```commandline
cd $(mktemp -d) && git clone https://github.com/arapelle/temgen.git -b release/0.6.0 
```
**- Dev:**
```commandline
cd $(mktemp -d) && git clone https://github.com/arapelle/temgen.git -b develop/0.x 
```

## Linux & MacOS
Create a virtual env and use pyinstaller (adapt the path to `cli_temgen.py` if needed):
```commandline
python -m venv venv
venv/bin/pip install semver pyinstaller
venv/bin/pyinstaller -F --clean --optimize 2 -n temgen --distpath bin  temgen/cli_temgen.py
```
The path to the compiled executable is: `bin/temgen`\
(Move it where you prefer. ex: */usr/local/bin*)

## Windows
Create a virtual env and use pyinstaller (adapt the path to `cli_temgen.py` if needed):
```commandline
python -m venv venv
venv/bin/pip install semver pyinstaller
venv/bin/pyinstaller --clean --optimize 2 -n temgen --distpath bin  temgen/cli_temgen.py
```
The compiled executable with its dependencies are in: `bin/temgen`\
(Move `bin/temgen/temgen.exe` and `bin/temgen/_internal` where you prefer.)
 
# License

[MIT License](./LICENSE.md) © temgen
