from urllib.request import urlopen
import htmlparser
from htmlparser import THTMLNode, THTMLDocument

html_resp = urlopen("https://2ch.hk/sci/res/398324.html")
html_raw_data = html_resp.read()
html_doc = THTMLDocument()
htmlparser.Parse(html_raw_data.decode("utf-8"), html_doc, [])

def PrintNode(Node, RecDepth):
    t = ""
    for i in range(RecDepth):
        t += "  "

    print(t, Node.fNodeType, Node.fText, Node.fAttributes)
    for E in Node.fChildNodes:
        PrintNode(E, RecDepth+1)

PrintNode(html_doc.fRootNode, 0)
