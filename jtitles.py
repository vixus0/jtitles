#!/usr/bin/env python

import sys, re
from argparse import ArgumentParser, RawTextHelpFormatter

def parse_map(mapf):
  txt = re.split(r'[\r\n]{2,}', open(mapf).read())
  if txt[-1].strip() == '':
    txt.pop()
  l_to_m = {}
  m_to_l = {}
  for grp in txt:
    lin = grp.split('\n')
    macro = lin[0].replace(" ","")
    if macro == "UNMAPPED":
      continue
    if macro in m_to_l.keys():
      sys.stderr.write("Warning: macro", macro, "defined twice!\n")
    else:
      m_to_l[macro] = []
    for l in lin[1:]:
      l_to_m[l] = macro
      m_to_l[macro].append(l)
  return l_to_m, m_to_l

if __name__ == "__main__":
  epi="""
Format for map files:

  macro
  title that defines replacement
  title to replace
  ...

for each journal.
  """

  ap = ArgumentParser(description="A paper fan in BibTeX hell.", epilog=epi, formatter_class=RawTextHelpFormatter)
  ap.add_argument('bib', help='Bibtex file')
  ap.add_argument('--db', help='Pickled database', default='jtitles.db')
  ap.add_argument('--makelist', help='Make list of unique journal titles', action='store_true')
  ap.add_argument('--makebib', help='Make the mapped bibtex file and macro file', action='store_true')
  ap.add_argument('--map', help='Map file')

  args = ap.parse_args()

  bibf = [l.strip() for l in open(args.bib).readlines()]

  if args.map:
    titles_macro, macro_long = parse_map(args.map)
  else:
    titles_macro, macro_long = {}, {}

  if args.makelist:
    scan = []
    
    for l in bibf:
      if l.startswith("journal"):
        clean = l.split("=")[-1].strip('{}", ')
        if clean not in titles_macro.keys():
          scan.append(clean)
          titles_macro[clean] = True
    
    if args.map:
      for m in sorted(macro_long.keys()):
        print m
        sys.stdout.writelines([l+'\n' for l in macro_long[m]])
        print

      if len(scan)>0:
        print "\nUNMAPPED"

    titles = sorted(scan, key=lambda x: x.replace(".", "").replace("The","").strip())
    sys.stdout.writelines([t+'\n' for t in titles])
      
  elif args.makebib:
    bibo = open(args.bib.replace(".bib","")+"_mapd.bib", "w")

    for l in bibf:
      if l.startswith("journal"):
        clean = l.split("=")[-1].strip('{}", ')
        macro = titles_macro[clean]
        bibo.write('journal = '+macro+',\n')
      else:
        bibo.write(l+'\n')

    bibm = open(args.bib.replace(".bib","")+"_macro.bib", "w")
    for k,v in macro_long.items():
      bibm.write('@string{%s="%s"}\n' % (k,v[0]))

    print "done."
    print "Mapped bibtex in "+args.bib+"_mapd.bib"
    print "Macros in "+args.bib+"_macro.bib"

