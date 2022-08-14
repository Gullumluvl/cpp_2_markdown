Exporter of a C++ tutorial to read later
=========================================

Convert C++ project into a single book (markdown format):

1. organize folders and files into chapters; if a README is found, it is placed first.
2. put code and inline comments inside fenced code blocks.
3. turn multiline comments into paragraphs;
    * symbols like # _ \< \> and \\n or \\t are escaped
    * preserve indentation for comments formatted with a leading asterisk:
      - indent > 5 spaces after the asterisk is preserved, thus becoming
        valid markdown indented code block, if preceeded by a blank line;
      - if not preceeded by a blank line, it is turned into inline code;
      - indent > 3 spaces is interpreted as list item; same if line startswith
        an hyphen or asterisk (excluding the comment format asterisk)



This aimed at converting the awesome C++ tutorial
<https://github.com/jesyspa/linear-cpp> into an ebook (epub).
Otherwise untested.


Produces a single markdown file, in this case `linear-cpp_ebook.md`

### Commands for making an epub:

    ./cpp_2_markdown.py linear-cpp
    
    pandoc -M author=jesyspa --standalone -V 'header-includes="<style>pre > code.sourceCode {white-space: pre-wrap !important;}</style>" --toc --toc-depth=1 -o linear-cpp.epub linear-cpp_ebook.md

