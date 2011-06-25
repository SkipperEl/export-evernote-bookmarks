Creates a [HTML Bookmarks][bookmarks] file from your evernote database, making a bookmark for each note with a URL, suitable for import into your browser, or a bookmarking service like [pinboard.in][pinboard].

[pinboard]:http://pinboard.in/
[bookmarks]:http://msdn.microsoft.com/en-us/library/aa753582(v=vs.85).aspx

Joel Carranza  
joel.carranza@gmail.com  
http://carranza-collective.com/joel.html  

Based on a sample script by [kjk][] and a little info from blogpost by [mengwong][]

[kjk]:https://github.com/kjk/web-blog/blob/master/scripts/evernote-to-file.py
[mengwong]:http://mengwong.livejournal.com/84064.html

# Usage #

    Usage: export-evernote-bookmarks.py [options]

    Options:
      -h, --help  show this help message and exit
      -i FILE     Evernote sqlite database. Defaults to
                  /Users/joelcarranza/Library/Application
                  Support/Evernote/data/101370/Evernote.sql
      -o FILE     write bookmarks to FILE. Defaults to bookmarks.html
  

# License #

Licensed under the Unlicense. See the UNLICENSE file for more info.