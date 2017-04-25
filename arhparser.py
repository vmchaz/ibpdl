import sys
import htmlparser
from htmlparser import THTMLNode, THTMLDocument
from abstractparser import TPost, TAbstractParser
#from parser import THTMLDocument

if len(sys.argv) <= 1:
    print("no args!")
    sys.exit(0)

print("Parsing file ", sys.argv[1])

f = open(sys.argv[1], "r", encoding="utf8")
lRawData = f.read()
#lProcessedData = CutStyles(CutScripts(CutComments(lRawData)))
lProcessedData = lRawData
f.close()

Doc = THTMLDocument()
htmlparser.Parse(lRawData, Doc, {})

def PrintRec(Node):
    S = "|"
    for i in range(Node.fDepth):
        S += "    "

    S += '[' + Node.fNodeType + ']'

    for a in Node.fAttributes:
        S += a + ':"' + Node.fAttributes[a] + '", '
    #print (Node.fAttributes)
    #for an, av in Node.fAttributes:
    #    SA = an + '"' + av + '"'
        #S += an + '"' + av + '"' + ', '

    S += 'Text:"' + Node.fText + '"'

    print(S)

    for N in Node.fChildNodes:
        PrintRec(N)

def CallRec(Node, NodeList):
    if Node.fNodeType == "div":
        if "class" in Node.fAttributes:
            if Node.fAttributes["class"] == "post":
                NodeList.append(Node)

    for N in Node.fChildNodes:
        CallRec(N)

def AssembleTuple(ElementType, ElementOptions, ElementText):
    return (ElementType, ElementOptions, ElementText)



def IsLLink(LinkNode):
    lHREF = LinkNode.GetAttribute("href")
    if len(lHREF) > 0:
        if lHREF[0] == "#":
            return True
    return False



def ParseLLink(LinkNode, PostData):
    lHREF = LinkNode.GetAttribute("href")
    lHREF2 = lHREF[1:]
    lText = ""

    for E in LinkNode.fChildNodes:
        if E.fNodeType == "wild":
            if lText == "":
                lText = E.fText
            else:
                lText += lText + " " + E.fText

    PostData.append(AssembleTuple("_llink", "href="+lHREF2, lText))



def IsImgLink(LinkNode):
    imgfn = LinkNode.GetAttribute("img_filename")
    if len(imgfn) > 0:
        return True
    return False

def ParseImgLink(LinkNode, PostData):
    lHREF = LinkNode.GetAttribute("href")
    lText = ""

    for E in LinkNode.fChildNodes:
        if E.fNodeType == "wild":
            lText = E.fText

    PostData.append(AssembleTuple("_img", "src="+lHREF, lText))

ctaWild = "W"
ctaQuote = "Q"
ctaBold = "B"
ctaCursive = "C"
ctaHidden = "H"


def ParsePostTextRec(PostTextNode, PostData, Attributes):

    for E in PostTextNode.fChildNodes:
        if E.fNodeType == "wild":
            PostData.append(AssembleTuple("wild", "".join(Attributes) , E.fText))
        elif E.fNodeType == "br":
            PostData.append(AssembleTuple("br", "", ""))
        elif E.fNodeType == "span":
            if E.CheckAttribute("class", "spoiler"):
                A = Attributes[:] + [ctaHidden]
                ParsePostTextRec(E, PostData, A)
            elif E.CheckAttribute("class", "unkfunc"):
                A = Attributes[:] + [ctaQuote]
                ParsePostTextRec(E, PostData, A)

        elif E.fNodeType == "a":
            if IsLLink(E):
                ParseLLink(E, PostData)
            elif IsImgLink(E):
                ParseImgLink(E, PostData)


def ParsePostHeader(PostNode, PostData):
    pass

def ParsePostText(PostNode, PostData):
    pass


class TArhParser(TAbstractParser):
    def Parse(self, HTMLDocument):
        ThreadNode = Doc.fRootNode.FindFirstInChildren("div", "class", "thread_inner", True, True)
        PNL = []
        ThreadNode.FindInChildren("div", "class", "post", False, PNL)
        PD = []
        for PN in PNL:
            lRes = self.ParsePost(PN, PD)
            if lRes == -1:
                print("Post parse error")

    def ParsePost(PostNode, PostData):
        lE = None
        try:
            lID = PostNode.GetAttribute("postid")
            PostData.append(AssembleTuple("_post", "id="+lID, ""))

            PostHeadDiv = PostNode.FindFirstInChildren("div", "class", "post_head", False, True)
            PostCommentSpan = PostNode.FindFirstInChildren("span", "class", "post_comment", False, True)
            PostCommentBodyDiv = PostCommentSpan.FindFirstInChildren("div", "class", "post_comment_body", False, True)
            PostImageBlock = PostCommentSpan.FindFirstInChildren("div", "class", "post_image_block", False, False)

            if PostImageBlock != None:
                for E in PostImageBlock.fChildNodes:
                    if (E.fNodeType == "a") and (E.CheckAttribute("class", "img_filename")):
                        lT = ""
                        for E2 in E.fChildNodes:
                            if E2.fNodeType == "wild":
                                lT = E2.fText

                        img_src = E.GetAttribute("href")
                        PostData.append(AssembleTuple("img", "src="+img_src, lT))

            lAttributes = [ctaWild]
            ParsePostTextRec(PostCommentBodyDiv, PostData, lAttributes)

            return 0
        except:
            print(sys.exc_info())
            return -1

f = open("out.txt", "w", encoding="utf8")

for E in PD:
    if E[0] == "_post":
        f.write("\n\n\n")

    S = E[0]+" ("+E[1]+") "+E[2] + "\n"
    f.write(S)

f.close()

    #print(PN.fNodeType, PN.fAttributes)
