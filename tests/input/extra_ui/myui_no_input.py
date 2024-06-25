import json
import sys

if __name__ == '__main__':
    variables = dict()
    variables["message"] = "coucou"
    variables["end_message"] = "end"
    output_var_fpath = sys.argv[1]
    with open(output_var_fpath, 'w') as var_file:
        json.dump(variables, var_file, indent=4)
