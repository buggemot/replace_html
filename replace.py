import os
import io
# import pdb

def write_to_file(html_file, contents, mode, encoding='utf-8'):
    err = None
    try:
        with io.open(html_file, mode, encoding=encoding) as f:
            f.write(contents)
    except Exception as err:
        return False, err
        
    return True, err

def read_file(html_file, mode, encoding='utf-8'):
    contents = None
    try:
        with io.open(html_file, mode, encoding=encoding) as f:
            contents = f.read()
    except Exception as err:
        return False, err

    return True, contents

def replace(html_file, find_content, replace_to, encodings):

    # try:
    #     for line in fileinput.FileInput(html_file, inplace=True):
    #         if after_tag in line:
    #             line=line.replace(line, line+tracking_tag)
    # except Exception as e:
    #     print("Tag didn't insert in file {}. Error: {}".format(html_file, e))

    ok = False
    for encoding in encodings:
        ok, contents = read_file(html_file, 'r', encoding)
        if ok:
            contents = contents.replace(find_content, replace_to)
            ok, err = write_to_file(html_file, contents, 'w')
            if err:
                message = "Error writing data to file {}: {}".format(html_file, err)
                ok, err = write_to_file('error.log', message, 'a', 'utf-8')
            break

    if not ok:
        message = "Error reading data from file {}: {}".format(html_file, contents)
        ok, err = write_to_file('repalce_error.log', message, 'a', 'utf-8')
                
    return 

def main():

    encodings = ('utf-8', 'iso-8859-1')
    
    find_content = "UA-1051809-1"
    replace_to = ""

    path_html_files= '.'
    file_extension = 'html'

    html_files = []
    for r, d, f in os.walk(path_html_files):
        for file in f:
            if file.endswith(file_extension):
                html_files.append(os.path.join(r, file))

    # pdb.set_trace()

    for html_file in html_files:
        print(html_file)
        replace(html_file, find_content, replace_to, encodings)

if __name__ == "__main__":
    main()
