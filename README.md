jtitles
=======

> A paper fan in BibTeX hell.

A little utility for managing those pesky journal abbreviations in bibtex.
When you have a ton of slightly different journal naming schemes in your references file, this should help out.
Usage is simple:

    jtitles.py refs.bib --makelist > mapfile

will print a list of all the unique journal titles in your references file to stdout.
I suggest piping this to a new file, because you have to manually define a standard naming scheme for each journal (sorry!), e.g.

```
phrevlett
Phys. Rev. Lett.
Physical Review Letters
Phys Rev Lett

ploscompbio
PLoS Comp. Bio.
PLOS COMP BIO
PLOS Computational Biology
```

Every journal group is separated by two newlines. The first line in the group defines a unique macro and the following lines define all the possible journal names.
The first name following the macro will become the standard, i.e. all the titles for that journal will be replaced with this.

Updating
--------

If you update your bib file, it's a simple case of running jtitles again:

    jtitles.py refs_updated.bib --makelist --map mapfile > newmapfile

This does a number of useful things:

* Any new journal titles that aren't mapped already will be output at the end of the file.
* If you have multiple groups with the same macro the titles will be concatenated (means you don't have to rearrange new stuff).
* Concatenated and cleaned up journal groups will be output alphabetically.

So you may have to do a few repeated sweeps when you add new entries.

Generating new BibTeX
---------------------

This is the important part. To generate the mapped bibtex files, just run

    jtitles.py refs.bib --makebib --map mapfile

Two new files: refs_mapd.bib and refs_macro.bib will be generated if all goes well.
Use these in place of your original bibliography include:

    \bibliography{refs_macro,refs_mapd}

