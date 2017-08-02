import sys
import htmlparser
import uuid
import tarfile
import statemachine
import time
from io import BytesIO
from htmldocument import THTMLNode, THTMLDocument
from abstractparser import TPost, TAbstractParser
from httpclient import execute_http_request
from os import listdir
import os.path

ctaWild = "W"
ctaQuote = "Q"
ctaBold = "B"
ctaCursive = "C"
ctaHidden = "H"
ctaStrike = "S"
ctaReplacedColored = "R"

gRetryCount = 3
gCacheDir = ""

class TCache:
    def __init__(self):
        self.fDirectory = ""
        self.fFiles = {}
        self.fEnabled = False
        #Сканирование каталога кэша

    def SetDirectory(self, Directory):
        self.fDirectory = Directory

    def EnableCache(self):
        self.fEnabled = True

    def ScanDirectory(self):
        if not self.fEnabled:
            return

        for fn in listdir(self.fDirectory):
            full_fn = os.path.join(self.fDirectory, fn)
            if os.path.isfile(full_fn):
                f = open(full_fn, "rb")
                data = f.read()
                self.fFiles[fn] = data

    def CheckFile(self, FileName):
        if self.fEnabled:
            return FileName in self.fFiles
        else:
            return False

    def GetFile(self, FileName):
        if self.fEnabled:
            return self.fFiles[FileName]

    def AddFile(self, FileName, Data):
        if not self.fEnabled:
            return

        if not self.CheckFile(FileName):
            full_fn = os.path.join(self.fDirectory, FileName)
            f = open(full_fn, "wb")
            f.write(Data)
            f.close()




gSiteAddress = "2ch.hk"
gTitle = ""
gCache = TCache()

  




def IsSkippableBlock(Node):
    return False
    


def IsWildText(Node):
    if Node.fNodeType == "wild":
        return True
    return False       


def ParseWildText(Node, Attributes, Post):
    Post.AddElement("text", Node.fText, "".join(Attributes), "")




def IsLLink(Node):
    if Node.fNodeType == "a":
        if Node.CheckAttribute("class", "post-reply-link"):
            return True
                    
    return False
        

def ParseLLink(Node, Attributes, Post):
    lHREF = Node.GetAttribute("href")
    lText = Node.GetAttribute("data-num")
    Post.AddElement("llink", lText, Attributes, lHREF)
    
    
    

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
    

def ParseHiddenText(Node, Attributes, Post):
    A = Attributes[:] + [ctaHidden]
    ParsePostTextRec(Node, A, Post)
    
    
def IsHiddenText(Node):
    if Node.fNodeType == "span":
        if Node.CheckAttribute("class", "spoiler"):
            return True
    return False
    

def ParseStrikeText(Node, Attributes, Post):
    A = Attributes[:] + [ctaStrike]
    ParsePostTextRec(Node, A, Post)


def IsReplacedColoredText(Node):
    if Node.fNodeType == "span":
        s = Node.GetAttribute("style")
        if s.startswith("color:"):
            return True
    return False


def ParseReplacedColoredText(Node, Attributes, Post):
    A = Attributes[:] + [ctaReplacedColored]
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
            
        elif IsHiddenText(E):
            ParseHiddenText(E, Attributes, Post)            
            
        elif IsQuote(E):            
            ParseQuote(E, Attributes, Post)
            
        elif IsBold(E):            
            ParseBold(E, Attributes, Post)

        elif IsReplacedColoredText(E):
            ParseReplacedColoredText(E, Attributes, Post)
            

            
def ParseImageBlock(Node, Post):
    for E in Node.fChildNodes:
        if E.fNodeType == "figure":
            if E.CheckAttribute("class", "image"):
                #try:
                D = E.FindFirstInChildren("div", "class", "image-link", True, False)
                if D is not None:
                    UUID = str(uuid.uuid4())
                    A = D.FindFirstInChildren("a", "", "", False, False)
                    if A is not None:
                        full_src = A.GetAttribute("href")
                        full_fname = full_src.split("/")[-1]
                        img_type = full_fname.split(".")[-1]
                        preview_src = ""
                        preview_fname = ""
                        
                        PV = A.FindFirstInChildren("img", "", "", False, False)
                        if PV is not None:
                            preview_src = PV.GetAttribute("src")
                            preview_fname = preview_src.split("/")[-1]
                        else:
                            print("\"img\" tag not found!")
                            
                        Post.AddImage(UUID, img_type, full_fname, full_src, preview_fname, preview_src)
                    else:
                        print("\"a\" tag not found!")
                    
                else:
                    print("div (class:image-link) not found!")
                    
                #except:
                    return -1
                    #print("ParseImageBlock exc")
                    #traceback.print_exc()
                    #print(sys.exc_info())
                    #PrintException()
                    
                    
def SplitStringByFirstSymbol(S, Sym):
    sm = False
    rs = ["", ""]
    for C in S:
        if C != Sym:
            rs[int(sm)] += C
        else:
            if sm == False:
                sm = True
            else:
                rs[int(sm)] += C
                
    return rs[0], rs[1]                    

                        
def DateTimeToStandardFormat(T):
    try:
        a0t, a0m = SplitStringByFirstSymbol(T, "&")
        a1 = a0t.split(" ")
        dp, dnp, tp = a1[0], a1[1], a1[2]
        d_arr = dp.split("/")
        t_arr = tp.split(":")
        lDay, lMonth, lYear = d_arr[0], d_arr[1], "20"+d_arr[2]
        lHour, lMinute, lSecond = t_arr[0], t_arr[1], t_arr[2]
        return lYear+"."+lMonth+"."+lDay+" "+lHour+":"+lMinute+":"+lSecond
    except:
        print ("DateTime conversion exception")


class TIB2chParser(TAbstractParser):
    def Parse(self, HTMLDocument):
        global gTitle
        #try:
        
        T1Node = Doc.fRootNode.FindFirstInChildren("html", "", "", False, False)
        if T1Node is not None:
            T2Node = T1Node.FindFirstInChildren("head", "", "", False, False)
            if T2Node is not None:
                T3Node = T2Node.FindFirstInChildren("title", "", "", False, False)
                if T3Node is not None:
                    T4Node = T3Node.FindFirstInChildren("wild", "", "", False, False)
                    if T4Node is not None:
                        gTitle = T4Node.fText
                
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
            
        PostNode2 = PostNode.FindFirstInChildren("div", "", "", False, True)
        PosterID = ""
        
        lID = PostNode2.GetAttribute("data-num")
        BQ = PostNode2.FindFirstInChildren("blockquote", "class", "post-message", True, True)

        # Get post datetime
        lPostDateTime = "0000.00.00 00:00:00"
        TS = PostNode.FindFirstInChildren("span", "class", "posttime", True, True)
        if TS is not None:
            TST = TS.FindFirstInChildren("wild", "", "", False, True)
            lPostDateTime = DateTimeToStandardFormat(TST.fText)

        PIN1 = PostNode.FindFirstInChildren("span", "class", "ananimas", True, False)
        if PIN1 is not None:
            PIN2 = PIN1.FindFirstInChildren("span", "", "", False, False)
            if PIN2 is not None:
                PIN3 = PIN2.FindFirstInChildren("wild", "", "", False, False)
                if PIN3 is not None:
                    PosterID = PIN3.fText
                    
        OP1 = PostNode.FindFirstInChildren("span", "class", "ophui", True, False)
        if OP1 is not None:
            OP2 = OP1.FindFirstInChildren("wild", "", "", False, False)
            if OP2 is not None:
                PosterID = "OP"
        
        Post.fNumber = lID
        Post.fPosterID = PosterID
        Post.fDate = lPostDateTime

        
        ParsePostTextRec(BQ, [], Post)
        
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


cIMAGE_TYPES = ["png", "jpg", "gif"]
cVIDEO_TYPES = ["webm"]
cDOWNLOAD_IMAGES_PREVIEW = ["preview", "all"]
cDOWNLOAD_IMAGES_FULL = ["full", "all"]
cDOWNLOAD_VIDEOS_PREVIEW = ["preview", "all"]
cDOWNLOAD_VIDEOS_FULL = ["full", "all"]


def ProcessFileURL(FileName, FileSource, Cache, Images, RetryCount):
    print("Downloading", FileSource)
    if Cache.CheckFile(FileName):
        print("File", FileName, "found in cache")
        Images[FileName] = Cache.GetFile(FileName)
    else:
        try:
            d = execute_http_request(FileSource, RetryCount)
            print("Downloading complete, data size =", len(d))
            Cache.AddFile(FileName, d)
            Images[FileName] = d

        except:
            if IgnoreErrors:
                print("Error downloading", FileSource)
            else:
                raise


def DownloadImages(Post, Images, Cache, DownloadImages, DownloadVideos, IgnoreErrors, RetryCount):
    for I in Post.fImages:
        UID, Type, FileName, Source, PreviewFileName, PreviewSource = I[0], I[1], I[2], I[3], I[4], I[5]
        full_src = Protocol + SiteName + Source
        full_preview_src = Protocol + SiteName + PreviewSource
        

        if Type in cIMAGE_TYPES:
            if DownloadImages in cDOWNLOAD_IMAGES_PREVIEW:
                ProcessFileURL(PreviewFileName, full_preview_src, Cache, Images, RetryCount)

            if DownloadImages in cDOWNLOAD_IMAGES_FULL:
                ProcessFileURL(FileName, full_src, Cache, Images, RetryCount)
                
        if Type in cVIDEO_TYPES:
            if DownloadVideos in cDOWNLOAD_VIDEOS_PREVIEW:
                ProcessFileURL(PreviewFileName, full_preview_src, Cache, Images, RetryCount)
                
            if DownloadVideos in cDOWNLOAD_VIDEOS_FULL:
                ProcessFileURL(FileName, full_src, Cache, Images, RetryCount)

    return 0

        
SaveImages = "all"
SaveVideos = "all"
SaveFormat = "tar"
IgnoreErrors = False

if len(sys.argv) < 2:
    print("not enough args!")
    sys.exit(0)
    
arg_p = []
if len(sys.argv) >= 3:
    arg_p = sys.argv[2:]
    
    
for a in arg_p:
    if a.startswith("--images="):
        SaveImages = a[len("--images="):]
        
    if a.startswith("--videos="):
        SaveVideos = a[len("--videos="):]

    if a.startswith("--ignore-errors"):
        IgnoreErrors = True

    if a.startswith("--cache="):
        gCacheDir = a[len("--cache="):]
        gCache.SetDirectory(gCacheDir)
        gCache.EnableCache()

        
    if a.startswith("--format="):
        SaveFormat = a[len("--format="):]
        if SaveFormat == "tar":
            pass
        if SaveFormat == "txt":
            SaveImages = "None"
            SaveVideos = "None"
        

ThreadURL = sys.argv[1]
if ThreadURL.startswith("http://"):
    ThreadURL = ThreadURL[7:]
    
if ThreadURL.startswith("https://"):
    ThreadURL = ThreadURL[8:]

ThreadURLParts = ThreadURL.split("/")
SiteName = ThreadURLParts[0]
BoardName = ThreadURLParts[1]
ThreadNumber = ThreadURLParts[-1].split(".")[0]
Protocol = "https://"
NewThreadURL = Protocol+ThreadURL

print("Downloading", NewThreadURL)
lRawData = execute_http_request(NewThreadURL, gRetryCount)
print("Download complete, data size =", len(lRawData))

lProcessedData = lRawData.decode("utf-8")
print("Parsing page...")

Doc = THTMLDocument()
htmlparser.Parse(lProcessedData, Doc, {}, [])

bp = TIB2chParser()
bp.Parse(Doc)

print("Parsing complete")

ThreadText = "@global source=\""+NewThreadURL+"\" title=\""+gTitle+"\"\n"
gImages = {}

for P in bp.fPosts:
    ThreadText += P.Print()

if gCache.fEnabled:
    gCache.ScanDirectory()

for P in bp.fPosts:
    DownloadImages(P, gImages, gCache, SaveImages, SaveVideos, IgnoreErrors, gRetryCount)
    
tarfn = ""
for c in NewThreadURL:
    if c in statemachine.cENG_LETTERS + statemachine.cDIGITS:
        tarfn += c
    else:
        tarfn += "_"
        

savefn = SiteName+" - _"+BoardName+"_ - "+ThreadNumber

if SaveFormat == "tar":
    tarfn = savefn + ".tar"
   
    print("Saving data to", tarfn)

    tar = tarfile.open(tarfn, "w")
    for PN, PV in gImages.items():
        fb = BytesIO(PV)
        ti = tarfile.TarInfo(name=PN)
        ti.size = len(PV)
        ti.mtime = time.time()
        tar.addfile(tarinfo=ti, fileobj=fb)
        
    ThreadTextData = ThreadText.encode("utf-8")
    fb = BytesIO(ThreadTextData)
    ti = tarfile.TarInfo(name="index.txt")
    ti.size = len(ThreadTextData)
    ti.mtime = time.time()
    tar.addfile(tarinfo=ti, fileobj=fb)
    
    fb = BytesIO(lRawData)
    ti = tarfile.TarInfo(name="index.html")
    ti.size = len(lRawData)
    ti.mtime = time.time()
    tar.addfile(tarinfo=ti, fileobj=fb)

    tar.close()
    print("Saving complete")
    
elif SaveFormat == "txt":
    txtfn = savefn + ".txt"
    print("Saving data to", txtfn)
    ThreadTextData = ThreadText.encode("utf-8")
    fxt = open(txtfn, "wb")
    fxt.write(ThreadTextData)
    fxt.close()
    print("Saving complete")

