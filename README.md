Exporter of a C++ tutorial to read later
=========================================

Convert C++ project into a single book (markdown format):

- turn multiline comments into paragraphs;
- put code and inline comments into code blocks;
- organize folders into chapters.


This aimed at converting the awesome C++ tutorial
<https://github.com/jesyspa/linear-cpp> into an ebook (epub). Otherwise
untested.


Produces a single markdown file, in this case `linear-cpp_ebook.md`

### Commands for making an epub:

    ./cpp_2_markdown.py linear-cpp
    
    pandoc -M author=jesyspa --standalone --toc --toc-depth=1 -o linear-cpp.epub linear-cpp_ebook.md
