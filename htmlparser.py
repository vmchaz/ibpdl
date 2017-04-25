import sys
import copy
import binaryreader
from binaryreader import TBinaryReader
import statemachine
from statemachine import cStates
from htmldocument import THTMLNode

ctCOMMENT_OPEN = "<!--"
ctCOMMENT_CLOSE = "-->"

ctSCRIPT_START = "<script"
ctSCRIPT_FINISH = "</script>"

ctSTYLE_START = "<style"
ctSTYLE_FINISH = "</style>"

#=========================================================================
#=========================================================================
#=========================================================================
#=========================================================================

class TNodeContainer:
    def __init__(self):
        self.fNode = None
        self.fDocument = None

class TStateContainer:
    def __init__(self):
        self.fState = 0
        self.fPrevState = 0
        self.fIsNewState = False
        self.fStateIteration = 0
        self.fDone = False

    def SetState(self, State):
        self.fPrevState = self.fState
        self.fState = State
        self.fIsNewState = True
        self.fStateIteration = 0







#=========================================================================
#=========================================================================
#=========================================================================
#=========================================================================

cENG_LOCASE_LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
cENG_UPCASE_LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
cENG_LETTERS = cENG_LOCASE_LETTERS + cENG_UPCASE_LETTERS
cDIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
cUNDERSCORE = ['_']
cMINUS = ['-']
cSPACE = [' ']
cTAGSTART = ['<']
cTAGFINISH = ['>']
cSLASH = ['/']
cEQUALS = ['=']
cEXC = ['!']
cSINGLEQUOTE = ["'"]
cDOUBLEQUOTE = ['"']
cDIVIDE = ["/"]
cMULTIPLY = ["*"]
cMINUS = ["-"]

cprNone = 0
cprStrict = 1
cprTextMark = 2
cprStateChanging = 3

cTags = {
    "a":{"Pairing":cprStrict},
    "abbr":{"Pairing":cprStrict},
    "acronym":{"Pairing":cprStrict},
    "address":{"Pairing":cprStrict},
    "applet":{"Pairing":cprStrict},
    "area":{"Pairing":cprStrict},
    "article":{"Pairing":cprStrict},
    "aside":{"Pairing":cprStrict},
    "audio":{"Pairing":cprStrict},
    "b":{"Pairing":cprStrict},
    "base":{"Pairing":cprStrict},
    "basefont":{"Pairing":cprStrict},
    "bdi":{"Pairing":cprStrict},
    "bdo":{"Pairing":cprStrict},
    "big":{"Pairing":cprStrict},
    "blockquote":{"Pairing":cprStrict},
    "body":{"Pairing":cprStrict},
    "br":{"Pairing":cprNone},
    "button":{"Pairing":cprStrict},
    "canvas":{"Pairing":cprStrict},
    "caption":{"Pairing":cprStrict},
    "center":{"Pairing":cprStrict},
    "cite":{"Pairing":cprStrict},
    "code":{"Pairing":cprStrict},
    "col":{"Pairing":cprStrict},
    "colgroup":{"Pairing":cprStrict},
    "datalist":{"Pairing":cprStrict},
    "dd":{"Pairing":cprStrict},
    "del":{"Pairing":cprStrict},
    "details":{"Pairing":cprStrict},
    "dfn":{"Pairing":cprStrict},
    "dialog":{"Pairing":cprStrict},
    "dir":{"Pairing":cprStrict},
    "div":{"Pairing":cprStrict},
    "dl":{"Pairing":cprStrict},
    "dt":{"Pairing":cprStrict},
    "em":{"Pairing":cprStrict},
    "embed":{"Pairing":cprStrict},
    "fieldset":{"Pairing":cprStrict},
    "figcaption":{"Pairing":cprStrict},
    "figure":{"Pairing":cprStrict},
    "font":{"Pairing":cprStrict},
    "footer":{"Pairing":cprStrict},
    "form":{"Pairing":cprStrict},
    "frame":{"Pairing":cprStrict},
    "frameset":{"Pairing":cprStrict},
    "h1":{"Pairing":cprStrict},
    "h2":{"Pairing":cprStrict},
    "h3":{"Pairing":cprStrict},
    "h4":{"Pairing":cprStrict},
    "h5":{"Pairing":cprStrict},
    "h6":{"Pairing":cprStrict},
    "head":{"Pairing":cprStrict},
    "header":{"Pairing":cprStrict},
    "hr":{"Pairing":cprNone},
    "html":{"Pairing":cprStrict},
    "i":{"Pairing":cprStrict},
    "iframe":{"Pairing":cprStrict},
    "img":{"Pairing":cprNone},
    "input":{"Pairing":cprNone},
    "ins":{"Pairing":cprStrict},
    "kbd":{"Pairing":cprStrict},
    "keygen":{"Pairing":cprStrict},
    "label":{"Pairing":cprStrict},
    "legend":{"Pairing":cprStrict},
    "li":{"Pairing":cprStrict},
    "link":{"Pairing":cprNone},
    "main":{"Pairing":cprStrict},
    "map":{"Pairing":cprStrict},
    "mark":{"Pairing":cprStrict},
    "menu":{"Pairing":cprStrict},
    "menuitem":{"Pairing":cprStrict},
    "meta":{"Pairing":cprNone},
    "meter":{"Pairing":cprStrict},
    "nav":{"Pairing":cprStrict},
    "nobr":{"Pairing":cprStrict},
    "noframes":{"Pairing":cprStrict},
    "noscript":{"Pairing":cprStrict},
    "object":{"Pairing":cprStrict},
    "ol":{"Pairing":cprStrict},
    "optgroup":{"Pairing":cprStrict},
    "option":{"Pairing":cprStrict},
    "output":{"Pairing":cprStrict},
    "p":{"Pairing":cprStrict},
    "param":{"Pairing":cprStrict},
    "pre":{"Pairing":cprStrict},
    "progress":{"Pairing":cprStrict},
    "q":{"Pairing":cprStrict},
    "rp":{"Pairing":cprStrict},
    "rt":{"Pairing":cprStrict},
    "ruby":{"Pairing":cprStrict},
    "s":{"Pairing":cprStrict},
    "samp":{"Pairing":cprStrict},
    "script":{"Pairing":cprStateChanging},
    "section":{"Pairing":cprStrict},
    "select":{"Pairing":cprStrict},
    "small":{"Pairing":cprStrict},
    "source":{"Pairing":cprStrict},
    "span":{"Pairing":cprStrict},
    "strike":{"Pairing":cprStrict},
    "strong":{"Pairing":cprStrict},
    "style":{"Pairing":cprStrict},
    "sub":{"Pairing":cprStrict},
    "summary":{"Pairing":cprStrict},
    "sup":{"Pairing":cprStrict},
    "table":{"Pairing":cprStrict},
    "tbody":{"Pairing":cprStrict},
    "td":{"Pairing":cprStrict},
    "textarea":{"Pairing":cprStrict},
    "tfoot":{"Pairing":cprStrict},
    "th":{"Pairing":cprStrict},
    "thead":{"Pairing":cprStrict},
    "time":{"Pairing":cprStrict},
    "title":{"Pairing":cprStrict},
    "tr":{"Pairing":cprStrict},
    "track":{"Pairing":cprStrict},
    "tt":{"Pairing":cprStrict},
    "u":{"Pairing":cprStrict},
    "ul":{"Pairing":cprStrict},
    "var":{"Pairing":cprStrict},
    "video":{"Pairing":cprStrict},
    "wbr":{"Pairing":cprNone}
}

def OnReadTagStart(R, StateContainer, NodeContainer, Accumulators, AttrBuffer, SMVars, ErrorHandlers, DebugLines):
    #print("OnReadTagStart")
    AttrBuffer.clear()
    return 0


def OnDoneReadingTagName(R, StateContainer, NodeContainer, Accumulators, AttrBuffer, SMVars, ErrorHandlers, DebugLines):
    #print("OnDoneReadingTagName", "Tag:", Accumulators[0])
    return 0


def OnDoneAttributeValue(R, StateContainer, NodeContainer, Accumulators, AttrBuffer, SMVars, ErrorHandlers, DebugLines):
    #print("OnDoneAttributeValue", "Tag:", Accumulators[0], "Attribute:", Accumulators[1], Accumulators[2])
    lN = Accumulators[1]
    lV = Accumulators[2]
    AttrBuffer[lN] = lV
    Accumulators[1] = ""
    Accumulators[2] = ""
    return 0


def OnDoneReadingTagFinish(R, StateContainer, NodeContainer, Accumulators, AttrBuffer, SMVars, ErrorHandlers, DebugLines):
    lRes = 0
    #print("OnDoneReadingTagFinish TagName:", Accumulators[0], "Attributes:", AttrBuffer, "SMVars:", SMVars)

    lTag = Accumulators[0].lower()

    CTR = cTags[lTag]
    if SMVars["OpeningTag"] == True:
        if CTR["Pairing"] == cprStrict:
            #print("Entering new level")

            N = THTMLNode(NodeContainer.fDocument)

            N.fParentNode = NodeContainer.fNode
            N.fNodeType = lTag
            N.fAttributes = copy.deepcopy(AttrBuffer)
            N.fDepth = NodeContainer.fNode.fDepth + 1
            N.fDebug = R.GetDebugBuffer()
            NodeContainer.fNode.fChildNodes.append(N)

            NodeContainer.fNode = N

            pass

        elif CTR["Pairing"] == cprTextMark:
            N = THTMLNode(NodeContainer.fDocument)
            N.fNodeType = lTag
            N.fTreeElementType = THTMLNode.cttOPENING
            N.fParentNode = NodeContainer.fNode
            N.fDepth = NodeContainer.fNode.fDepth + 1
            N.fAttributes = copy.deepcopy(AttrBuffer)
            NodeContainer.fNode.AddChildNode(N)

        elif CTR["Pairing"] == cprStateChanging:
            pass

        elif CTR["Pairing"] == cprNone:
            N = THTMLNode(NodeContainer.fDocument)
            N.fNodeType = lTag
            N.fParentNode = NodeContainer.fNode
            N.fDepth = NodeContainer.fNode.fDepth + 1
            N.fAttributes = copy.deepcopy(AttrBuffer)
            NodeContainer.fNode.AddChildNode(N)
        else:
            return -1


    elif SMVars["ClosingTag"] == True:
        if CTR["Pairing"] == cprStrict:
            
            if NodeContainer.fNode.fNodeType == lTag:
                NodeContainer.fNode = NodeContainer.fNode.fParentNode
            else:
                                    
                lErrorIsHandled = False
                #DebugLines.append("ERROR! Node type doesnt match!")

                for EH in ErrorHandlers:
                    lErrorIsHandled = EH("ClosingTagMismatch", CTR, StateContainer, NodeContainer, Accumulators, AttrBuffer, SMVars, DebugLines)
                    if lErrorIsHandled:
                        break
                    
                if lErrorIsHandled:
                    DebugLines.append("Error ClosingTagMismatch is successfully handled")
                else:
                    DebugLines.append("============ ERROR! Node type doesnt match! =====================")
                    DebugLines.append("Opening: "+NodeContainer.fNode.fNodeType)
                    DebugLines.append("Closing: "+lTag)
                    DebugLines.append("Stack:")
                    N = NodeContainer.fNode
                    while N is not None:
                        DebugLines.append(N.fNodeType+" "+N.fAttributes.__str__())
                        N = N.fParentNode
                                    
                    d1 = NodeContainer.fNode.fDebug
                    d2 = R.GetDebugBuffer()
                    DebugLines.append("OpeningBuffer:"+d1)
                    DebugLines.append("")
                    DebugLines.append("ClosingBuffer:"+d2)
                    DebugLines.append("")
                    lRes = -1
                    
        elif CTR["Pairing"] == cprTextMark:
            pass
        elif CTR["Pairing"] == cprNone:        
            pass
        else:
            pass

    elif SMVars["FastClosingTag"] == True:
        N = THTMLNode(NodeContainer.fDocument)
        N.fDocument = NodeContainer.fDocument
        N.fNodeType = lTag
        N.fParentNode = NodeContainer.fNode
        N.fDepth = NodeContainer.fNode.fDepth + 1
        NodeContainer.fNode.AddChildNode(N)

    return lRes


def IsEmptyWildText(T):
    lRes = True
    for C in T:
        if not( C in [" ", chr(9), "\n"]):
            lRes = False

    return lRes


def OnDoneReadingWildText(R, StateContainer, NodeContainer, Accumulators, SMVars, AttrBuffer, ErrorHandlers, DebugLines):
    if IsEmptyWildText(Accumulators[3]):
        pass
    else:
        N = THTMLNode(NodeContainer.fDocument)
        N.fParentNode = NodeContainer.fNode
        N.fNodeType = "wild"
        N.fText = Accumulators[3]
        if "TrimText" in SMVars:
            N.fText = N.fText.strip(" \n"+chr(9))
        N.fDepth = NodeContainer.fNode.fDepth + 1
        NodeContainer.fNode.AddChildNode(N)
    return 0

cSMEventHandlers = {
    "OnReadTagStart": OnReadTagStart,
    "OnDoneReadingTagName": OnDoneReadingTagName,
    "OnDoneAttributeValue": OnDoneAttributeValue,
    "OnDoneReadingTagFinish": OnDoneReadingTagFinish,
    "OnDoneReadingWildText": OnDoneReadingWildText
}



def Step(NodeContainer, R, State, Accumulators, AttrBuffer, SMVars, ErrorHandlers, DebugLines):

    lRes = 0

    lState = State.fState
    lStateIteration = State.fStateIteration

    if lState in cStates:
        STR = cStates[lState]
    else:
        print ("Wrong state " + lState)
        raise "Wrong state"

    ECList = STR["ExitConditions"]

    lAccumulate = STR["Accumulate"]
    lAccNumber = STR["AccNumber"]
    lLimit = STR["Limit"]
    lOnEnter = STR["OnEnter"]
    lOnLeave = STR["OnLeave"]

    if lStateIteration == 0:
        P = None
        if lOnEnter is not None:
            if lOnEnter in cSMEventHandlers:
                if cSMEventHandlers[lOnEnter] != None:
                    P = cSMEventHandlers[lOnEnter]

        if P is not None:
            lRes = P(R, State, NodeContainer, Accumulators, AttrBuffer, SMVars, ErrorHandlers, DebugLines)
            if lRes != 0:
                return lRes

    for V in STR["Vars"]:
        VN = V[0]
        VA = V[1]

        if VA == statemachine.cvaSet:
            SMVars[VN] = True
        elif VA == statemachine.cvaReset:
            SMVars[VN] = False


    if lAccumulate:
        if State.fStateIteration == 0:
            Accumulators[lAccNumber] = R.fLast
        else:
            Accumulators[lAccNumber] += R.fLast

    Ch = R.Read()

    if Ch != "":
        State.fNewState = -1

        FND = False

        for EC in ECList:
            if FND == False:

                lECOperation = EC["LogicalOperation"]
                lECSymbols = EC["Symbols"]
                lECNewState = EC["NewState"]
                lACL = EC["AdditionalConditions"]


                # Проверка основного условия
                MainCM = False
                if lECOperation == "In":
                    if Ch in lECSymbols:
                        MainCM = True
                elif lECOperation == "NotIn":
                    if not(Ch in lECSymbols):
                        MainCM = True
                elif lECOperation == "Limit":
                    if lLimit + 1 >= lStateIteration:
                        MainCM = True
                elif lECOperation == "Default":
                    MainCM = True

                # Проверка дополнительных условий
                ACM = True
                if len(lACL) > 0:
                    for ACE in lACL:
                        if ACE[0] == "Var":
                            lVN = ACE[2]
                            lVV = ACE[3]
                            if ACE[1] == "EQ":
                                if SMVars[lVN] == lVV:
                                    pass
                                else:
                                    ACM = False
                            elif ACE[1] == "NEQ":
                                if SMVars[lVN] != lVV:
                                    pass
                                else:
                                    ACM = False
                            else:
                                ACM = False
                        else:
                            ACM = False


                if MainCM and ACM:
                    FND = True
                    State.fNewState = lECNewState

        if FND:
            P = None

            lCSOL = STR["CSOL"]
            if len(lCSOL) > 0:
                q0 = 1
                for R1 in lCSOL:
                    V1 = Accumulators[R1[0]].upper()
                    V2 = R1[1].upper()
                    if V1 == V2:
                        SMVars[R1[2]] = R1[3]

            if lOnLeave != None:
                if lOnLeave in cSMEventHandlers:
                    if cSMEventHandlers[lOnLeave] != None:
                        P = cSMEventHandlers[lOnLeave]

            if P is not None:
                lRes = P(R, State, NodeContainer, Accumulators, AttrBuffer, SMVars, ErrorHandlers, DebugLines)
                if lRes != 0:
                    return lRes

            STR2 = cStates[lECNewState]
            #print ("Entering state "+STR2["name"])

            State.SetState(State.fNewState)
    else:
        State.fDone = True

    return 0

def CutComments(S):
    ps = S.find(ctCOMMENT_OPEN)
    while ps >= 0:
        pe = S.find(ctCOMMENT_CLOSE, ps)
        if pe >= 0:
            S = S[:ps] + S[pe+len(ctCOMMENT_CLOSE):]
            ps = S.find(ctCOMMENT_OPEN)
        else:
            return S

    return S


def CutScripts(S):
    ps = S.find(ctSCRIPT_START)
    while ps >= 0:
        pe = S.find(ctSCRIPT_FINISH, ps)
        if pe >= 0:
            S = S[:ps] + S[pe + len(ctSCRIPT_FINISH):]
            ps = S.find(ctSCRIPT_START)
        else:
            return S

    return S

def CutStyles(S):
    ps = S.find(ctSTYLE_START)
    while ps >= 0:
        pe = S.find(ctSTYLE_FINISH, ps)
        if pe >= 0:
            S = S[:ps] + S[pe + len(ctSTYLE_FINISH):]
            ps = S.find(ctSTYLE_START)
        else:
            return S

    return S








def Parse(Data, Document, Parameters, ErrorHandlers):
    lState = TStateContainer()
    lAccumulators = ["", "", "", "", ""]
    lAttrBuffer = {}
    lSMVars = {}
    lDebugLines = []

    lSMVars["StrictTagMatch"] = True

    for PN, PV in Parameters.items():
        lSMVars[PN] = PV


    lNodeContainer = TNodeContainer()
    lNodeContainer.fDocument = Document
    lNodeContainer.fNode = Document.fRootNode

    R = TBinaryReader(Data)
    R.Read()

    if R.fLast in cTAGSTART:
        lState.fState = statemachine.cscReadTagStart
    else:
        lState.fState = statemachine.cscReadWildText

    #try:
    lRes = 0
    while (lState.fDone == False) and (lRes == 0):
        lRes = Step(lNodeContainer, R, lState, lAccumulators, lAttrBuffer, lSMVars, ErrorHandlers, lDebugLines)

        if lRes == 0:
            if lState.fIsNewState == True:
                lState.fIsNewState = False
            else:
                lState.fStateIteration += 1

            if lState.fState == statemachine.cscError:
                print ("fState = Error! Debug buffer:", R.GetDebugBuffer())
                print ("gState.fPrevState:", lState.fPrevState)
                raise "Error state"
        else:
            print("lRes == ", lRes)

    
    if Parameters.get("Debug"):
        for L in lDebugLines:
            print(L)
    #print("Position (Current/Max):", R.fPosition, len(lProcessedData))

    #except:
    #   print(sys.exc_info()[0])
    #   print("Stopped at position ", R.fPosition)
