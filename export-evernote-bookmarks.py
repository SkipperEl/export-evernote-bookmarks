#!/usr/bin/env python
"""
export-evernote-bookmarks.py

Creates a HTML Bookmarks file from your evernote database, making a bookmark for each note with a URL, suitable for import into any browser or your favorite online bookmarking service.

Created by Joel Carranza on 2011-06-25.
joel.carranza@gmail.com  
http://carranza-collective.com/joel.html  

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>
"""

import sys
import os.path
import datetime
import codecs
import sqlite3
import codecs
import getopt
from optparse import OptionParser
from xml.etree.ElementTree import Element,ElementTree,SubElement

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
EVERNOTE_DIR = os.path.join(os.path.expanduser("~"), "Library", "Application Support", "Evernote", "data")
# this might be different, depending on the Evernote version
EVERNOTE_DIR = os.path.join(EVERNOTE_DIR, "101370")
EVERNOTE_DB_PATH = os.path.join(EVERNOTE_DIR, "Evernote.sql")

def get_article_tags(conn,pk):
    c = conn.cursor()
    c.execute("""
    SELECT e.zname2 
    FROM Z_12TAGS t, 
    ZENATTRIBUTEDENTITY e 
    WHERE  e.z_ent = 17 and t.z_17tags = e.z_pk
    and t.z_12notes = ?
    """,(pk,))
    tags = []
    for row in c:
      tags.append(row[0])
    c.close()
    return tags

def read_url(path):
    if not os.path.exists(path):
      raise Exception("Evernote database file does not exist at: %s" % path)
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("SELECT Z_PK,ZTITLE, ZSOURCEURL  FROM Zenattributedentity where Z_ENT=12 and ZSOURCEURL IS NOT NULL")
    data = []
    for pk,title,url in c:
      tags = get_article_tags(conn,pk)
      data.append((title,url,tags))
    conn.close()
    return data

def write_bookmarks(data,fname):
  dl = Element("DL")
  for title,url,tags in data:
    dt = SubElement(dl,"DT")
    a = SubElement(dt,"A",attrib=dict(HREF=url,TAGS=",".join(tags)))
    a.text = title
    dt.tail = "\n"
  file = codecs.open(fname,"w","UTF-8")
  file.write("""<!DOCTYPE NETSCAPE-Bookmark-file-1>\n""")
  file.write("""<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">\n""")
  file.write("""<TITLE>Evernote Bookmarks</TITLE>\n""")
  ElementTree(dl).write(file)

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-i", dest="dbpath",default=EVERNOTE_DB_PATH,
                    help='Evernote sqlite database. Defaults to %default', metavar="FILE")
    parser.add_option("-o", dest="out",default="bookmarks.html",
                  help="write bookmarks to FILE. Defaults to %default", metavar="FILE")
    parser.add_option("-t", dest="tag",
                  help="additional tag to add to all bookmarks", metavar="TAG")

    (options, args) = parser.parse_args()
    urls = read_url(options.dbpath)
    if options.tag:
      for u in urls:
        u[2].append(options.tag)
    write_bookmarks(urls,options.out)