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

ctaWild = "W"
ctaQuote = "Q"
ctaBold = "B"
ctaCursive = "C"
ctaHidden = "H"
ctaStrike = "S"


def PrintException():
    pass
    # print(sys.exc_info())
    # print(dir(e))


def ExceptionToString():
    exc_type, exc_obj, tb = sys.exc_info()
    s1 = str(exc_type) + str(exc_obj) + str(tb)


gSiteAddress = "4chan.org"
gTitle = ""


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
        if Node.CheckAttribute("class", "quotelink"):
            return True

    return False


def ParseLLink(Node, Attributes, Post):
    lHREF = Node.GetAttribute("href")
    lText = lHREF
    if lText.startswith("#p"):
        lText = lText[2:]

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


def ParseImageBlock(Node, Post):
    for E in Node.fChildNodes:
        if E.fNodeType == "figure":
            if E.CheckAttribute("class", "image"):
                # try:
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

                    # except:
                    return -1
                    # print("ParseImageBlock exc")
                    # traceback.print_exc()
                    # print(sys.exc_info())
                    # PrintException()


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
    a0t, a0m = SplitStringByFirstSymbol(T, "&")
    a1 = a0t.split(" ")
    dp, dnp, tp = a1[0], a1[1], a1[2]
    d_arr = dp.split("/")
    t_arr = tp.split(":")
    lDay, lMonth, lYear = d_arr[0], d_arr[1], "20" + d_arr[2]
    lHour, lMinute, lSecond = t_arr[0], t_arr[1], t_arr[2]
    return lYear + "." + lMonth + "." + lDay + " " + lHour + ":" + lMinute + ":" + lSecond


class TIB2chParser(TAbstractParser):
    def Parse(self, HTMLDocument):
        global gTitle
        # try:

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
        ThreadNode.FindInChildren("div", "class", "postContainer opContainer", False, PNL)
        ThreadNode.FindInChildren("div", "class", "postContainer replyContainer", False, PNL)

        for PN in PNL:
            P = TPost()
            lRes = self.ParsePost(PN, P)
            self.fPosts.append(P)

            # except:
            #    print("Exception in TIB2chParser.Parse")
            #    return -1

    def ParsePost(PostNode, Post):
        lE = None
        #        try:


        PostNode2 = PostNode.FindFirstInChildren("div", "class", "post reply", False, False)
        if PostNode2 is None:
            PostNode2 = PostNode.FindFirstInChildren("div", "class", "post op", False, False)

        PosterID = ""

        lID = PostNode2.GetAttribute("data-num")
        BQ = PostNode2.FindFirstInChildren("blockquote", "class", "post-message", True, True)
        TS = PostNode.FindFirstInChildren("span", "class", "posttime", True, True)
        TST = TS.FindFirstInChildren("wild", "", "", False, True)
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
        Post.fDate = DateTimeToStandardFormat(TST.fText)

        ParsePostTextRec(BQ, [ctaWild], Post)

        # raise("qwer")

        for N in PostNode2.fChildNodes:
            if N.fNodeType == "div":
                a = N.GetAttribute("class")
                if a.startswith("images"):
                    ParseImageBlock(N, Post)
                    break

        return 0


# except:
#            return -1


cIMAGE_TYPES = ["png", "jpg", "gif"]
cVIDEO_TYPES = ["webm"]
cDOWNLOAD_IMAGES_PREVIEW = ["preview", "all"]
cDOWNLOAD_IMAGES_FULL = ["full", "all"]
cDOWNLOAD_VIDEOS_PREVIEW = ["preview", "all"]
cDOWNLOAD_VIDEOS_FULL = ["full", "all"]


def DownloadImages(Post, Images, DownloadImages, DownloadVideos):
    for I in Post.fImages:
        UID, Type, FileName, Source, Preview, PreviewSource = I[0], I[1], I[2], I[3], I[4], I[5]
        full_src = Protocol + SiteName + Source
        preview_src = Protocol + SiteName + PreviewSource

        if Type in cIMAGE_TYPES:
            if DownloadImages in cDOWNLOAD_IMAGES_PREVIEW:
                print("Downloading", preview_src)
                d = execute_http_request(preview_src)
                print("Downloading complete, data size =", len(d))
                Images[Preview] = d

            if DownloadImages in cDOWNLOAD_IMAGES_FULL:
                print("Downloading", full_src)
                d = execute_http_request(full_src)
                print("Downloading complete, data size =", len(d))
                Images[FileName] = d

        if Type in cVIDEO_TYPES:
            if DownloadVideos in cDOWNLOAD_VIDEOS_PREVIEW:
                print("Downloading", preview_src)
                d = execute_http_request(preview_src)
                print("Downloading complete, data size =", len(d))
                Images[Preview] = d

            if DownloadVideos in cDOWNLOAD_VIDEOS_FULL:
                print("Downloading", full_src)
                d = execute_http_request(full_src)
                print("Downloading complete, data size =", len(d))
                Images[FileName] = d


SaveImages = "all"
SaveVideos = "all"
SaveFormat = "tar"

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
NewThreadURL = Protocol + ThreadURL

print("Downloading", NewThreadURL)
lRawData = execute_http_request(NewThreadURL)
print("Downloading complete, data size =", len(lRawData))

lProcessedData = lRawData.decode("utf-8")
print("Parsing page...")

Doc = THTMLDocument()
htmlparser.Parse(lProcessedData, Doc, {}, [])

bp = TIB2chParser()
bp.Parse(Doc)

print("Parsing complete")

ThreadText = "@global source=\"" + NewThreadURL + "\" title=\"\"\n"
gImages = {}

for P in bp.fPosts:
    ThreadText += P.Print()

for P in bp.fPosts:
    DownloadImages(P, gImages, SaveImages, SaveVideos)

tarfn = ""
for c in NewThreadURL:
    if c in statemachine.cENG_LETTERS + statemachine.cDIGITS:
        tarfn += c
    else:
        tarfn += "_"

savefn = SiteName + " - _" + BoardName + "_ - " + ThreadNumber

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

