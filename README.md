# dirarchy

Generates directory architecture based on a template.

### TODO

```
<if expr="" />
<var regex=''/>

{$PROGRAM_DIR}, {$CANONICAL_PROGRAM_DIR}, {$CURRENT_SOURCE_DIR}, {$TREE_ROOT_DIR}, {$CURRENT_TREE_ROOT_DIR}
template="TemplateName"  look for TemplateName or TemplateName.xml in directories of templates.
  Where are the dir of templates ? envar DIRARCHY_PATH ?

<then /> and <else />
<match expr=""><case value="" /></match>
<file copy="path/to/file_to_copy.txt" />

argparse [--no-window] [-C working_dir] [-v var=value] [-Vvar_list_path] path/to/dirarchy.xml

Gui: Pattern Strategy
terminal
tkinter
? curses

<execute script="./pyscript.py">...</execute>
<execute lang="py">...</execute>
```
