

class THTMLDocument:
    def __init__(self):
        self.fRootNode = THTMLNode(self)
        self.fRootNode.fDepth = 0
        self.fRootNode.fNodeType = "root"
        self.fNodes = []

class THTMLNode:

    cttNONE = 0
    cttOPENING = 1
    cttCLOSING = 2
    cttMARKOPENING = 3
    cttMARKCLOSING = 4

    def __init__(self, Document):
        self.fAttributes = {}
        self.fNodeType = ""
        self.fParentNode = None
        self.fText = ""
        self.fChildNodes = []
        self.fDepth = 0
        self.fDebug = ""
        self.fErrorFlag = False
        self.fTreeElementType = self.cttNONE
        self.fDocument = Document
        pass

    def AddAttribute(self, Name, Value):
        self.fAttributes[Name] = Value

    def AddChildNode(self, N):
        self.fChildNodes.append(N)
        self.fDocument.fNodes.append(N)

    def FindInChildrenEx(self, SearchParameters, Recursive, NodeList):

        lFindType = False
        if "Type" in SearchParameters:
            lFindType = True
            lType = SearchParameters["Type"]

        lFindAttributeName = False
        if "AttributeName" in SearchParameters:
            lFindAttributeName = True
            lAttributeName = SearchParameters["AttributeName"]

        lFindAttributeValue = False
        if "AttributeValue" in SearchParameters:
            lFindAttributeValue = True
            lAttributeValue = SearchParameters["AttributeValue"]

        for N in self.fChildNodes:
            Match = True

            if lFindType:
                if N.fNodeType == lType:
                    pass
                else:
                    Match = False

            if lFindAttributeName:
                if lAttributeName in N.fAttributes:
                    if lFindAttributeValue:
                        if N.fAttributes[lAttributeName] == lAttributeValue:
                            pass
                        else:
                            Match = False
                    pass
                else:
                    Match = False

            if Match:
                NodeList.append(N)

            if Recursive:
                N.FindInChildrenEx(SearchParameters, Recursive, NodeList)

    def FindInChildren(self, NodeType, AttributeName, AttributeValue, Recursive, NodeList):
        SearchParameters = {}
        if NodeType != "":
            SearchParameters["Type"] = NodeType

        if AttributeName != "":
            SearchParameters["AttributeName"] = AttributeName

        if AttributeValue != "":
            SearchParameters["AttributeValue"] = AttributeValue

        self.FindInChildrenEx(SearchParameters, Recursive, NodeList)

    def FindFirstInChildrenEx(self, SearchParameters, Recursive, RaiseErrorOnNotFound):
        L = []
        self.FindInChildrenEx(SearchParameters, Recursive, L)
        if len(L) > 0:
            return L[0]
        else:
            if RaiseErrorOnNotFound:
                raise "No matching child elements found for node " + str(self)
                #raise "No matching child elements found for node " + str(self) + " options:(NodeType:" + NodeType + ", AttributeName:" + AttributeName + ", AttributeValue:" + AttributeValue + ")"
            return None

    def FindFirstInChildren(self, NodeType, AttributeName, AttributeValue, Recursive, RaiseErrorOnNotFound):
        SearchParameters = {}
        if NodeType != "":
            SearchParameters["Type"] = NodeType

        if AttributeName != "":
            SearchParameters["AttributeName"] = AttributeName

        if AttributeValue != "":
            SearchParameters["AttributeValue"] = AttributeValue

        if Recursive:
            SearchParameters["Recursive"] = True

        L = []
        self.FindInChildrenEx(SearchParameters, Recursive, L)
        if len(L) > 0:
            return L[0]
        else:
            if RaiseErrorOnNotFound:
                print("No matching child elements found for node " + str(self) + " options:(NodeType:" + NodeType + ", AttributeName:" + AttributeName + ", AttributeValue:" + AttributeValue + ")")
                #raise "No matching child elements found for node " + str(self) + " options:(NodeType:" + NodeType + ", AttributeName:" + AttributeName + ", AttributeValue:" + AttributeValue + ")"
                raise "No matching child elements found!" # for node " + str(self) + " options:(NodeType:" + NodeType + ", AttributeName:" + AttributeName + ", AttributeValue:" + AttributeValue + ")"
            return None

    def CheckAttribute(self, AttributeName, AttributeValue):
        if AttributeName in self.fAttributes:
            if self.fAttributes[AttributeName] == AttributeValue:
                return True
        return False

    def GetAttribute(self, AttributeName):
        if AttributeName in self.fAttributes:
            return self.fAttributes[AttributeName]
        else:
            return ""

    """def CreateChildNode(self):
        N = THTMLNode()
        N.fParentNode = self
        N.fDocument = self.fDocument
        N.fDepth = self.fDepth + 1
        self.fChildNodes.append(N)
        return N"""