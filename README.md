# `temgen`

 A tool generating a directory architecture or a file based on a template.

# Install

Clone the project (if it is not already the case):
```commandline
cd $(mktemp -d)
git clone https://github.com/arapelle/temgen.git
```
Create a virtual env and use pyinstaller (adapt the path to `cli_temgen.py` if needed):
```commandline
python -m venv virtualenv
virtualenv/bin/pip install semver pyinstaller
virtualenv/bin/pyinstaller -F --clean --optimize 2 -n temgen --distpath bin  temgen/cli_temgen.py
```
The path to the compiled executable is: `bin/temgen`\
(Move it where you prefer. ex: /usr/local/bin)
 
# License

[MIT License](./LICENSE.md) © temgen
