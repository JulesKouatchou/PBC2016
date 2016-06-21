#!/usr/bin/env python
# FileName: mymodule.py

def sayhi(myname):
    print "Hi from %s: this is mymodule speaking." %(myname)

version = '1.0'

if __name__ == "__main__":
  import sys
  try:
     sayhi(str(sys.argv[1]))
  except:
     print 'Usage: %s string' % sys.argv[0]
     sys.exit(0)
  print 'Version', version

# End of mymodule.py

