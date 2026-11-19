# -*- coding: utf-8 -*-
# Run with OpenOffice's own Python 2.7: "C:\Program Files (x86)\OpenOffice 4\program\python.exe" aoo_convert.py in.docx out.odt out.pdf
# Apache OpenOffice 4 has no -convert-to (that is LibreOffice); this starts it headless and converts over UNO.
import os
import subprocess
import sys
import time

PROGRAM = r"C:\Program Files (x86)\OpenOffice 4\program"
sys.path.insert(0, PROGRAM)
os.environ["PATH"] = PROGRAM + os.pathsep + os.environ.get("PATH", "")
os.environ.setdefault("URE_BOOTSTRAP", "vnd.sun.star.pathname:" + os.path.join(PROGRAM, "fundamental.ini"))

import uno
from com.sun.star.beans import PropertyValue

SOFFICE = r"C:\Program Files (x86)\OpenOffice 4\program\soffice.exe"
PORT = 2002


def prop(name, value):
    p = PropertyValue()
    p.Name, p.Value = name, value
    return p


def url(path):
    return uno.systemPathToFileUrl(os.path.abspath(path))


def restore_bookmark_names(src, doc):
    """AOO imports DOCX bookmarks as Bookmark, Bookmark1... in document order; give back the real names
    so that the internal links of the table of contents keep working."""
    import re
    import zipfile
    xml = zipfile.ZipFile(src).read("word/document.xml").decode("utf-8")
    names = re.findall(r'<w:bookmarkStart [^>]*w:name="([^"]+)"', xml)
    marks = doc.getBookmarks()
    for i, real in enumerate(names):
        generic = "Bookmark" if i == 0 else "Bookmark%d" % i
        if marks.hasByName(generic):
            marks.getByName(generic).setName(real)
    print("bookmarks: " + ", ".join(marks.getElementNames()))


def main():
    src, outs = sys.argv[1], sys.argv[2:]
    proc = subprocess.Popen([SOFFICE, "-headless", "-invisible", "-norestore", "-nofirststartwizard",
                             "-accept=socket,host=127.0.0.1,port=%d;urp;" % PORT])
    local = uno.getComponentContext()
    resolver = local.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", local)
    ctx = None
    for _ in range(60):
        try:
            ctx = resolver.resolve("uno:socket,host=127.0.0.1,port=%d;urp;StarOffice.ComponentContext" % PORT)
            break
        except Exception:
            time.sleep(1)
    if ctx is None:
        print("could not connect to OpenOffice")
        return 1
    desktop = ctx.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
    doc = desktop.loadComponentFromURL(url(src), "_blank", 0, (prop("Hidden", True),))
    restore_bookmark_names(src, doc)
    filters = {".odt": "writer8", ".pdf": "writer_pdf_Export"}
    for out in outs:
        doc.storeToURL(url(out), (prop("FilterName", filters[os.path.splitext(out)[1]]),))
        print("written " + out)
    doc.close(True)
    try:
        desktop.terminate()
    except Exception:
        pass
    proc.wait()
    return 0


if __name__ == "__main__":
    sys.exit(main())
