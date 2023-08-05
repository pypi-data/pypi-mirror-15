# What is PhIDE?

A misnomer and a mess. The IDE I want for doing knowledge work doesn't exist. 
IPython (i.e [Jupyter](http://jupyter.org/)) does a lot of what I want. But, 
for say, writing a dissertation, there are missing tools. Right now, PhIDE 
is me writing little utilities that work good enough, kicking the quality can 
down the road. You probably shouldn't use this library yet. I mean, it works, 
but it's not systematically tested. (But, I do use it daily, and I have not 
hand any accidental `rm -rf /` incidents -- yet.)

# Installation

`$ pip install phide`

# Commands

## `phide-simple-html`

### What it does now?

Recursively walks the file system -- starting from the current directory -- 
for IPython notebooks. Following the PhIDE convention, it skips processing of 
files or directories which start with a `.` or `_`. Ordering is lexicographic. 
(I use a convention of naming notebooks as `###_name.ipynb`.) When it reads a 
markdown cell, it concatenates it to the output Pandoc flavored markdown file 
(`_phide_output/extract.md`). When it encounters an SVG output, it serializes 
it (to `_phide_output/media/#.svg`) and insert an image into the markdown 
file. Then, it runs pandoc.

Usage: `$ phide-simple-html`

### What should it do?

I need to add support for pandoc compilation into alternative formats 
(e.g. latex). I especially want support for citations via IPython's data-cite 
convention.

It should also support more than just SVG files. And, I want it to support 
latex-style referencing and figures.

Oh, and templating.

## `phide-paper-sync`

### What it does now?

Often, I want to read PDF files on my iPad using GoodReader. GoodReader 
offers DropBox synchronization. This script syncs PDF files used in my 
dissertation with those on a Dropbox. It obeys the following rules:

1. If the dropbox file is newer, overwrite the dissertation one. 
2. If the dissertation file is newer, overwrite the dropbox one.
3. If there is no equivalent file in the dropbox directory, copy it.

Note, this script "unpacks" `_cited_docs`. For example, if you are working on 
your thesis you may have a: 
`/thesis/intro/_cited_docs/transformative_hermeneutics.pdf` it syncs with 
`/sync_folder/intro/transformative_hermeneutics.pdf`.

**WARNING**: *Modern Academia is a mostly a closed-source community, built upon 
the idea that sharing is bad (for your CV). Part of this paradigm depends upon 
journals, or tenure justifiers. These institutions do not like it when you 
share research, and will prosecute those who do. Remember to add 
`_citeddocs` to your `.gitignore`*.

Usage: `$ phide-paper-sync sync-dir`

### What should it do?

Probably something more robust than modified time comparisons. That seems 
dangerous. Also, I want it to be executable correctly from any project 
sub-dir, like git. 

