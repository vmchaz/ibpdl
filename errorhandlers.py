def handle_unexpected_td_closing(ErrorType, CTR, StateContainer, NodeContainer, Accumulators, AttrBuffer, SMVars, DebugLines):
    if ErrorType == "ClosingTagMismatch":
        opening_tag = NodeContainer.fNode.fNodeType
        closing_tag = Accumulators[0].lower()
        
        if (opening_tag == "td") and (closing_tag == "tr"):
            PN = NodeContainer.fNode.fParentNode
            if PN is not None:
                if PN.fNodeType == "tr":
                    GPN = PN.fParentNode                    
                    NodeContainer.fNode = GPN
                    return True

    return False
