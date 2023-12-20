import sys

if __name__ == '__main__':
    var_fpath = sys.argv[1]
    with open(var_fpath, 'w') as var_file:
        var_file.write("""{
"other_text": "here is a tale" 
}""")
    pass
