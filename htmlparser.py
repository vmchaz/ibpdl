# coding:utf-8
import sys
import copy
import binaryreader
from binaryreader import TBinaryReader
import statemachine
from statemachine import cStates
from htmldocument import THTMLNode
import htmltags



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

    CTR = htmltags.cTags[lTag]
    if SMVars["OpeningTag"] == True:
        if CTR["Pairing"] == htmltags.cprStrict:
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

        elif CTR["Pairing"] == htmltags.cprTextMark:
            N = THTMLNode(NodeContainer.fDocument)
            N.fNodeType = lTag
            N.fTreeElementType = THTMLNode.cttOPENING
            N.fParentNode = NodeContainer.fNode
            N.fDepth = NodeContainer.fNode.fDepth + 1
            N.fAttributes = copy.deepcopy(AttrBuffer)
            NodeContainer.fNode.AddChildNode(N)

        elif CTR["Pairing"] == htmltags.cprStateChanging:
            pass

        elif CTR["Pairing"] == htmltags.cprNone:
            N = THTMLNode(NodeContainer.fDocument)
            N.fNodeType = lTag
            N.fParentNode = NodeContainer.fNode
            N.fDepth = NodeContainer.fNode.fDepth + 1
            N.fAttributes = copy.deepcopy(AttrBuffer)
            NodeContainer.fNode.AddChildNode(N)
        else:
            return -1


    elif SMVars["ClosingTag"] == True:
        if CTR["Pairing"] == htmltags.cprStrict:
            
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
                    
        elif CTR["Pairing"] == htmltags.cprTextMark:
            pass
        elif CTR["Pairing"] == htmltags.cprNone:
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


def SmartStripText(T):
    if len(T) == 0:
        return ""

    lFNSS = -1
    lLNSS = -1
    
    
    for i in range(len(T)):
        if T[i] in [" ", chr(9), "\n"]:
            pass
        else:
            if lFNSS == -1:
                lFNSS = i
            lLNSS = i

    if lFNSS >= 0:
        S = T[lFNSS:lLNSS+1]

        if lFNSS > 0:
            S = " " + S

        if lLNSS + 1 != len(T):
            S += " "

        return S
    else:
        return " "



def OnDoneReadingWildText(R, StateContainer, NodeContainer, Accumulators, SMVars, AttrBuffer, ErrorHandlers, DebugLines):
    if IsEmptyWildText(Accumulators[3]):
        pass
    else:
        N = THTMLNode(NodeContainer.fDocument)
        N.fParentNode = NodeContainer.fNode
        N.fNodeType = "wild"
        N.fText = SmartStripText(Accumulators[3])
        #if "TrimText" in SMVars:
        #    N.fText = N.fText.strip(" \n"+chr(9))
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
                if cSMEventHandlers[lOnEnter] is not None:
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

            if lOnLeave is not None:
                if lOnLeave in cSMEventHandlers:
                    if cSMEventHandlers[lOnLeave] is not None:
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

    lUseDebugBuffer = False
    if "UseDebugBuffer" in Parameters:
        lUseDebugBuffer = True

    R = TBinaryReader(Data, lUseDebugBuffer)
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

