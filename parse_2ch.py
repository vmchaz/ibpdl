import sys
import htmlparser
from io import BytesIO
from htmldocument import THTMLNode, THTMLDocument
from abstractparser import TPost, TAbstractParser
from httpclient import execute_http_request

ctaWild = "W"
ctaQuote = "Q"
ctaBold = "B"
ctaCursive = "C"
ctaHidden = "H"
ctaStrike = "S"


def PrintException():
    pass
    #print(sys.exc_info())
    #print(dir(e))    


def ExceptionToString():
    exc_type, exc_obj, tb = sys.exc_info()
    s1 = str(exc_type) + str(exc_obj) + str(tb)
    print
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    return s1 + filename + str(lineno)
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    return 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)




gSiteAddress = "2ch.hk"



  
        



def IsSkippableBlock(Node):
    return False
    


def IsWildText(Node):
    if Node.fNodeType == "wild":
        return True
    return False       


def ParseWildText(Node, Attributes, Post):
    Post.AddElement("wild", Node.fText, "".join(Attributes), "")




def IsLLink(Node):
    if Node.fNodeType == "a":
        if Node.CheckAttribute("class", "post-reply-link"):
            return True
                    
    return False
        

def ParseLLink(Node, Attributes, Post):
    lHREF = Node.GetAttribute("href")
    lText = Node.GetAttribute("data-num")
    Post.AddElement("llink", ">>"+lText, Attributes, lHREF)
    
    
    

def IsCommonLink(Node):
    if Node.fNodeType == "a":
        if not Node.CheckAttribute("class", "post-reply-link"):
            return True
                    
    return False
        

def ParseCommonLink(Node, Attributes, Post):
    href = Node.GetAttribute("href")
    Post.AddElement("ext_link", "", Attributes, href)
    
    
    

def IsQuote(Node):
    if Node.fNodeType == "span":
        if Node.CheckAttribute("class", "unkfunc"):
            return True
    return False
    

def ParseQuote(Node, Attributes, Post):
    A = Attributes[:] + [ctaQuote]
    ParsePostTextRec(Node, A, Post)
    


def IsBold(Node):
    if Node.fNodeType == "strong":
        return True
    return False
    

def ParseBold(Node, Attributes, Post):
    A = Attributes[:] + [ctaBold]
    ParsePostTextRec(Node, A, Post)
    
   
    
    
def IsStrikeText(Node):
    if Node.fNodeType == "span":
        if Node.CheckAttribute("class", "s"):
            return True
    return False
    

def ParseStrikeText(Node, Attributes, Post):
    A = Attributes[:] + [ctaStrike]
    ParsePostTextRec(Node, A, Post)
    
    
    
def IsBR(Node):
    if Node.fNodeType == "br":
        return True
    return False
    
    
def ParseBR(Node, Attributes, Post):
    Post.AddElement("br", "", "".join(Attributes), "")
    
        



def ParsePostTextRec(PostTextNode, Attributes, Post):
    for E in PostTextNode.fChildNodes:
    
        if IsSkippableBlock(E):            
            pass
        
        if IsWildText(E):
            ParseWildText(E, Attributes, Post)
        
        elif IsLLink(E):
            ParseLLink(E, Attributes, Post)
            
        elif IsCommonLink(E):
            ParseCommonLink(E, Attributes, Post)
            
        elif IsBR(E):
            ParseBR(E, Attributes, Post)
        
        elif IsStrikeText(E):
            ParseStrikeText(E, Attributes, Post)
            
        elif IsQuote(E):            
            ParseQuote(E, Attributes, Post)
            
        elif IsBold(E):            
            ParseBold(E, Attributes, Post)
            
            
            
def ParseImageBlock(Node, Post):
    for E in Node.fChildNodes:
        if E.fNodeType == "figure":
            if E.CheckAttribute("class", "image"):
                #try:
                D = E.FindFirstInChildren("div", "class", "image-link", True, False)
                if D is not None:
                    UID = D.GetAttribute("id").split("-")[-1]
                    A = D.FindFirstInChildren("a", "", "", False, False)
                    if A is not None:
                        href = A.GetAttribute("href")
                        #frmt = href.split(".")[-1]
                        fname = href.split("/")[-1]
                        Post.AddImage(UID, href, fname)
                    else:
                        print("a (:) not found!")
                    
                else:
                    print("div (class:image-link) not found!")
                    
                #except:
                    return -1
                    #print("ParseImageBlock exc")
                    #traceback.print_exc()
                    #print(sys.exc_info())
                    #PrintException()

                        
        
class TIB2chParser(TAbstractParser):
    def Parse(self, HTMLDocument):
        #try:
        ThreadNode = Doc.fRootNode.FindFirstInChildren("div", "class", "thread", True, True)
        PNL = []
        ThreadNode.FindInChildren("div", "class", "oppost-wrapper", False, PNL)
        ThreadNode.FindInChildren("div", "class", "post-wrapper", False, PNL)

        for PN in PNL:
            P = TPost()                
            lRes = self.ParsePost(PN, P)
            self.fPosts.append(P)
                
        #except:            
        #    print("Exception in TIB2chParser.Parse")
        #    return -1

    
    
    def ParsePost(self, PostNode, Post):
        lE = None
#        try:
            
        PostNode2 = PostNode.FindFirstInChildren("div", "", "", True, True)
        
        lID = PostNode2.GetAttribute("data-num")
        BQ = PostNode2.FindFirstInChildren("blockquote", "class", "post-message", True, True)
        
        Post.fNumber = lID
        
        ParsePostTextRec(BQ, [ctaWild], Post)
        
        #raise("qwer")
        
        for N in PostNode2.fChildNodes:
            if N.fNodeType == "div":
                a = N.GetAttribute("class")
                if a.startswith("images"):
                    ParseImageBlock(N, Post)
                    break
                    
        return 0
#        except:            
#            return -1
        


if len(sys.argv) <= 2:
    print("not enough args!")
    sys.exit(0)
    
if sys.argv[1] == "url":
    lRawData = execute_http_request(sys.argv[2])
    print("Parsing URL ", sys.argv[2])
    
elif sys.argv[1] == "file":
    print("# Parsing file", sys.argv[2])
    f = open(sys.argv[2], "r", encoding="utf8")
    lRawData = f.read()
    lProcessedData = lRawData
    f.close()
else:
    print("Wrong source", sys.argv[1])
    sys.exit(0)

Doc = THTMLDocument()
htmlparser.Parse(lRawData, Doc, {}, [])

bp = TIB2chParser()
bp.Parse(Doc)
print("@header", "site="+'"'+gSiteAddress+'"')
for P in bp.fPosts:
    P.Print()
    pass
