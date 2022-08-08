#!/usr/bin/env python3

"""
Convert a C++ project directory into a markdown book.
Comments are turned into regular text, and all the code into code blocks.
Tested on linear-cpp tutorial.

USAGE:

    ./cpp2mkd.py <project directory>

Will create a new file <project directory>_ebook.md
"""


import glob
import sys
import os
import os.path as op
import re


START_REGEX = re.compile(r'/\*')
END_REGEX = re.compile(r'\*/')
MKD_ESCAPE = re.compile('([#_<>])')
TXT_EXTENSIONS = ('.md', '.txt', '.mkd')
CODE_EXTENSIONS = ('.cpp', '.cc', '.h', '.hpp')


def debug(*args, end=None):
    pass


def mkd_esc(line):
    indent = re.search(r'\S|$', line).start()
    if indent < 4:
        return MKD_ESCAPE.sub(r'\\\1', line)
    else:
        return line


def mkd_increment(lines, level=1):
    """Increment titles"""
    for line in lines:
        if line.startswith('#'):
            line = '#'*level + line
            if line.rstrip().endswith('#'):
                line = line.rstrip() + '#'*level + '\n'
        yield line


def code2mkd(lines):
    mkd = ""

    in_comment = 0  # nesting depth of being inside /* ... */ comments.
    star_indent = None  # save the index of the asterisque used to format comments.

    code = ""      # current code block content. Not written if empty
    
    for lineno, line in enumerate(lines):
        line = line.rstrip()
        column = 0
        debug(lineno, end='. ')
        while True:
            begin = 0
            end = None
            if in_comment:
                debug('in+=', end='')
                match = END_REGEX.search(line)
                indent = 0
                if column == 0 and line.startswith(star_indent):
                    begin = len(star_indent)
                else:
                    # Unindent
                    begin = re.search(r'\S', line).start()
                if match:
                    end = match.start()
                    in_comment -= 1
                debug('%s-%s' % (begin, end), end=' ')
                mkd += mkd_esc(line[begin:end]) + '\n'  # necessary newline
            else:
                debug('code', end=' ')
                match = START_REGEX.search(line)
                if match:
                    end = match.start()
                    in_comment += 1
                    star_indent = ' '*end + ' *'
                    if line[:end].rstrip():
                        code += line[:end].rstrip()
                        debug('+=-%s' % (end), end=' ')
                    if code.strip():
                        if mkd:
                            mkd += '\n'
                        mkd += '```cpp\n' + code.lstrip('\n').rstrip() + '\n```\n\n'
                        debug(' >blk.', end=' ')
                        code = ""
                else:
                    code += line.rstrip() + '\n'
                    debug('+=-', end=' ')
                    break
            if match is None:
                break
            line = line[match.end():]
            column += match.end()
        debug('')
    if code.strip():
        debug('Post.', end=' ')
        if mkd:
            mkd += '\n'
        mkd += '```cpp\n' + code.rstrip() + '\n```\n'
    
    return mkd


def codefile2mkd(codefile):
    """Return the markdown text"""
    if codefile == '-':
        return code2mkd(sys.stdin)
    else:
        with open(codefile) as f:
            return code2mkd(f)

def ls(directory):
    content = [name for name in sorted(os.listdir(directory)) if not name.startswith('.')]
    if 'README.md' in content:
        content.remove('README.md')
        content.insert(0, 'README.md')
    return content


def project2mkd(directory):
    """Convert the hierarchy of directories into a hierarchy of chapters"""
    level = 1
    parents = [directory]
    dircontent = {1: ls(directory)}  # at level one
    with open(directory + '_ebook.md', 'w') as out:
        out.write('% ' + directory + '\n%\n%\n\n')
        
        while level:
            try:
                element = dircontent[level].pop(0)
            except IndexError:
                level -= 1
                parents.pop()
                continue

            path = op.join(*parents, element)
            if op.isfile(path):
                out.write('\n' + '#' * level + ' ' + element + '\n\n')
                ext = op.splitext(element)[1]
                if ext in TXT_EXTENSIONS:
                    with open(path) as f:
                        for line in mkd_increment(f):
                            out.write(line)
                elif ext in CODE_EXTENSIONS:
                    out.write(codefile2mkd(path))
            elif op.isdir(path):
                out.write('\n' + '#'*level + ' ' + element + '\n\n')
                level += 1
                parents.append(element)
                if level > 6:
                    print('WARNING: directories deeper than 7 levels are not explored.', file=sys.stderr)
                    out.write('\n- '.join('`%s`' % e for e in ls(path)) + '\n')
                dircontent[level] = ls(path)
            else:
                print('WARNING: Ignored: not a regular file or dir:', element, file=sys.stderr)
    
    

def main():
    try:
        if sys.argv[1] in ('-h', '--help'):
            print(__doc__)
            sys.exit()

        if sys.argv[1] in ('-d', '--debug'):
            global debug
            def debug(*args, end=None): print(*args, end=end, file=sys.stderr)
            directory = sys.argv[2]
        else:
            directory = sys.argv[1]

    except IndexError:
        print(__doc__)
        sys.exit(2)

    project2mkd(directory)


if __name__ == '__main__':
    main()
