import os
import io
import pdb

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
            contents = f.readlines()
    except Exception as err:
        return False, err

    return True, contents

def insert_tag(html_file, tracking_tag, tag_insert_after, encodings):

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

            try:
                index = contents.index(tag_insert_after)
                contents.insert(index + 1, tracking_tag)
                contents = "".join(contents)
            except Exception as e:
                message = "Traking tag didn't insert in file {}, error: {}".format(html_file, e)
                ok, err = write_to_file('error.log', message, 'a')
                return
            break

    if not ok:
        message = "Error reading data from file {}: {}".format(html_file, contents)
        ok, err = write_to_file('error.log', message, 'a')
        return

    ok, err = write_to_file(html_file, contents, 'w')
    if err:
        message = "Error writing data to file {}: {}".format(html_file, err)
        ok, err = write_to_file('error.log', message, 'a')
    return 
    
def main():
    
    tracking_tag = """
    <!-- Global site tag (gtag.js) - Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=UA-152040304-1"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'UA-152040304-1');
    </script>
    """
    tag_insert_after = '<head>\n'
    path_html_files= '.'
    file_extension = 'html'

    encodings = ('utf-8', 'iso-8859-1')
    
    html_files = []
    for r, d, f in os.walk(path_html_files):
        for file in f:
            if file.endswith(file_extension):
                html_files.append(os.path.join(r, file))

    # pdb.set_trace()

    for html_file in html_files:
        print(html_file)
        insert_tag(html_file, tracking_tag, tag_insert_after, encodings)

if __name__ == "__main__":
    main()
