cscReadTagStart = 1
cscReadSpacesBeforeOpeningTagName = 2
cscReadSlashBeforeClosingTagName = 3
cscReadOpeningTagName = 4
cscReadSpacesBetweenAttributes = 5
cscReadFastCloseSlash = 6
cscReadAttributeName = 7
cscReadEqualsBeforeAttributeValue = 8
cscReadStartQuote = 9
cscReadAttributeValue = 10
cscReadFinishQuote = 11
cscReadStartSingleQuote = 12
cscReadSQAttributeValue = 13
cscReadFinishSingleQuote = 14
cscReadUQAttributeValue = 100
cscReadClosingTagName = 15
cscReadTagFinish = 16
cscReadWildText = 17
cscReadExcAfterTagStart = 18
cscReadDoctype = 19
cscReadDoctypeTagFinish = 20

cscJS_Wild = 21
cscJS_SQ_Start = 22
cscJS_SQ_Text = 23
cscJS_SQ_Finish = 24
cscJS_DQ_Start = 25
cscJS_DQ_Text = 26
cscJS_DQ_Finish = 27
cscJS_Divide = 28
cscJS_DivMul = 29
cscJS_Comment = 30
cscJS_Comment_Mul = 31
cscJS_Comment_MulDiv = 32
cscJS_TagStart = 33
cscJS_TagStart_ReadSlash_Done_WaitFor_L1 = 34
cscJS_TagStart_L1_Done_WaitFor_L2 = 35
cscJS_TagStart_L2_Done_WaitFor_L3 = 36
cscJS_TagStart_L3_Done_WaitFor_L4 = 37
cscJS_TagStart_L4_Done_WaitFor_L5 = 38
cscJS_TagStart_L5_Done_WaitFor_L6 = 39
cscJS_TagStart_L6_Done_WaitFor_TagFinish = 40
cscJS_TagFinish = 41

cscCommentBegin_M1Done_M2Wait = 42
cscCommentBegin_M2Done = 43
cscComment = 44
cscCommentEnd_M1Done_M2Wait = 45
cscCommentEnd_M2Done_TagFinishWait = 46
cscCommentEnd_TagFinishDone = 47

cscError = 48



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



#======================================================================================================
#======================================================================================================
#======================================================================================================



cprNone = 0
cprStrict = 1
cprTextMark = 2


#======================================================================================================
#======================================================================================================
#======================================================================================================


cvaSet = 1
cvaReset = 2
cvaIncrement = 3
cvaDecrement = 4

cCSOL_ReadOpeningTagName = [
    [0, "script", "Script", True],
    [0, "style", "Style", True]
]


cStates = {

cscReadTagStart:{"name":"ReadTagStart", "Vars":[("OpeningTag", cvaReset), ("ClosingTag", cvaReset), ("FastClosingTag", cvaReset), ("Script", cvaReset), ("Style", cvaReset)], "Accumulate":False, "AccNumber":-1, "OnEnter":None, "OnLeave":"OnReadTagStart", "Limit":0, "Stop":False, "CSOE":[], "CSOL":[], "ExitConditions":[
    {"LogicalOperation":"In", "Symbols":cSPACE, "AdditionalConditions":[], "NewState":cscReadSpacesBeforeOpeningTagName},
    {"LogicalOperation":"In", "Symbols":cENG_LETTERS, "AdditionalConditions":[], "NewState":cscReadOpeningTagName},
    {"LogicalOperation":"In", "Symbols":cSLASH, "AdditionalConditions":[], "NewState":cscReadSlashBeforeClosingTagName},
    {"LogicalOperation":"In", "Symbols":cEXC, "AdditionalConditions":[], "NewState":cscReadExcAfterTagStart}
    ]},

cscReadSpacesBeforeOpeningTagName:{"name":"ReadSpacesBeforeOpeningTagName", "Accumulate":False, "AccNumber":-1, "Vars":[], "OnEnter":None, "OnLeave":None, "Limit":0, "Stop":False, "CSOE":[], "CSOL":[], "ExitConditions":[
    {"LogicalOperation":"In", "Symbols":cENG_LETTERS, "AdditionalConditions":[], "NewState":cscReadOpeningTagName}
    ]},

cscReadSlashBeforeClosingTagName:{"name":"ReadSlashBeforeClosingTagName", "Accumulate":False, "AccNumber":-1, "Vars":[], "OnEnter":None, "OnLeave":None, "Limit":0, "Stop":False, "CSOE":[], "CSOL":[], "ExitConditions":[
    {"LogicalOperation":"In", "Symbols":cENG_LETTERS, "AdditionalConditions":[], "NewState":cscReadClosingTagName}
    ]},

cscReadOpeningTagName:{"name":"ReadOpeningTagName", "Accumulate":True, "AccNumber":0, "Vars":[("OpeningTag", cvaSet)], "OnEnter":None, "OnLeave":"OnDoneReadingTagName", "Limit":0, "Stop":False, "CSOE":[], "CSOL":cCSOL_ReadOpeningTagName, "ExitConditions":[
    {"LogicalOperation":"In", "Symbols":cSPACE, "AdditionalConditions":[], "NewState":cscReadSpacesBetweenAttributes},
    {"LogicalOperation":"In", "Symbols":cSLASH, "AdditionalConditions":[], "NewState":cscReadFastCloseSlash},
    {"LogicalOperation":"In", "Symbols":cTAGFINISH, "AdditionalConditions":[], "NewState":cscReadTagFinish}
    ]},

cscReadSpacesBetweenAttributes:{"name":"ReadSpacesBetweenAttributes", "Accumulate":False, "AccNumber":-1, "Vars":[], "OnEnter":None, "OnLeave":None, "Limit":0, "Stop":False, "CSOE":[], "CSOL":[], "ExitConditions":[
    {"LogicalOperation":"In", "Symbols":cENG_LETTERS, "AdditionalConditions":[], "NewState":cscReadAttributeName},
    {"LogicalOperation":"In", "Symbols":cSLASH, "AdditionalConditions":[], "NewState":cscReadFastCloseSlash},
    {"LogicalOperation":"In", "Symbols":cTAGFINISH, "AdditionalConditions":[], "NewState":cscReadTagFinish}
    ]},

cscReadFastCloseSlash:{"name":"ReadFastCloseSlash", "Accumulate":False, "AccNumber":-1, "Vars":[("OpeningTag", cvaReset), ("ClosingTag", cvaReset), ("FastClosingTag", cvaSet)], "OnEnter":None, "OnLeave":None, "Limit":0, "Stop":False, "CSOE":[], "CSOL":[], "ExitConditions":[
    {"LogicalOperation":"In", "Symbols":cTAGFINISH, "AdditionalConditions":[], "NewState":cscReadTagFinish}
    ]},

cscReadAttributeName:{"name":"ReadAttributeName", "Accumulate":True, "AccNumber":1, "Vars":[], "OnEnter":None, "OnLeave":None, "Limit":0, "Stop":False, "CSOE":[], "CSOL":[], "ExitConditions":[
    {"LogicalOperation":"In", "Symbols":cEQUALS, "AdditionalConditions":[], "NewState":cscReadEqualsBeforeAttributeValue},
    {"LogicalOperation":"In", "Symbols":cTAGFINISH, "AdditionalConditions":[], "NewState":cscReadTagFinish},
    ]},

cscReadEqualsBeforeAttributeValue:{"name":"ReadEqualsBeforeAttributeValue", "Accumulate":False, "AccNumber":0, "Vars":[], "OnEnter":None, "OnLeave":None, "Limit":0, "Stop":False, "CSOE":[], "CSOL":[], "ExitConditions":[
    {"LogicalOperation":"In", "Symbols":cDOUBLEQUOTE, "AdditionalConditions":[], "NewState":cscReadStartQuote},
    {"LogicalOperation":"In", "Symbols":cSINGLEQUOTE, "AdditionalConditions":[], "NewState":cscReadStartSingleQuote},
    {"LogicalOperation":"In", "Symbols":cENG_LETTERS+cDIGITS+cUNDERSCORE+cMINUS, "AdditionalConditions":[], "NewState":cscReadUQAttributeValue},
    {"LogicalOperation":"Default", "Symbols":[], "AdditionalConditions":[], "NewState":cscError},
    ]},

cscReadStartQuote:{"name":"ReadStartQuote", "Accumulate":False, "AccNumber":-1, "Vars":[], "OnEnter":None, "OnLeave":None, "Limit":1, "Stop":False, "CSOE":[], "CSOL":[], "ExitConditions":[
    {"LogicalOperation":"In", "Symbols":cDOUBLEQUOTE, "AdditionalConditions":[], "NewState":cscReadFinishQuote},
    {"LogicalOperation":"Limit", "Symbols":[], "AdditionalConditions":[], "NewState":cscReadAttributeValue},
    ]},

cscReadAttributeValue:{"name":"ReadAttributeValue", "Accumulate":True, "AccNumber":2, "Vars":[], "OnEnter":None, "OnLeave":None, "Limit":0, "Stop":False, "CSOE":[], "CSOL":[], "ExitConditions":[
    {"LogicalOperation":"In", "Symbols":cDOUBLEQUOTE, "AdditionalConditions":[], "NewState":cscReadFinishQuote},
    ]},

cscReadFinishQuote:{"name":"ReadFinishQuote", "Accumulate":False, "AccNumber":-1, "Vars":[], "OnEnter":None, "OnLeave":"OnDoneAttributeValue", "Limit":1, "Stop":False, "CSOE":[], "CSOL":[], "ExitConditions":[
    {"LogicalOperation":"In", "Symbols":cSPACE, "AdditionalConditions":[], "NewState":cscReadSpacesBetweenAttributes},
    {"LogicalOperation":"In", "Symbols":cSLASH, "AdditionalConditions":[], "NewState":cscReadFastCloseSlash},
    {"LogicalOperation":"In", "Symbols":cTAGFINISH, "AdditionalConditions":[], "NewState":cscReadTagFinish},
    {"LogicalOperation":"Limit", "Symbols":[], "AdditionalConditions":[], "NewState":cscError},
    ]},
    


cscReadStartSingleQuote:{"name":"ReadStartSingleQuote", "Accumulate":False, "AccNumber":-1, "Vars":[], "OnEnter":None, "OnLeave":None, "Limit":1, "Stop":False, "CSOE":[], "CSOL":[], "ExitConditions":[
    {"LogicalOperation":"In", "Symbols":cSINGLEQUOTE, "AdditionalConditions":[], "NewState":cscReadFinishSingleQuote},
    {"LogicalOperation":"Limit", "Symbols":[], "AdditionalConditions":[], "NewState":cscReadSQAttributeValue},
    ]},

cscReadSQAttributeValue:{"name":"ReadSQAttributeValue", "Accumulate":True, "AccNumber":2, "Vars":[], "OnEnter":None, "OnLeave":None, "Limit":0, "Stop":False, "CSOE":[], "CSOL":[], "ExitConditions":[
    {"LogicalOperation":"In", "Symbols":cSINGLEQUOTE, "AdditionalConditions":[], "NewState":cscReadFinishSingleQuote},
    ]},

cscReadFinishSingleQuote:{"name":"ReadFinishSingleQuote", "Accumulate":False, "AccNumber":-1, "Vars":[], "OnEnter":None, "OnLeave":"OnDoneAttributeValue", "Limit":1, "Stop":False, "CSOE":[], "CSOL":[], "ExitConditions":[
    {"LogicalOperation":"In", "Symbols":cSPACE, "AdditionalConditions":[], "NewState":cscReadSpacesBetweenAttributes},
    {"LogicalOperation":"In", "Symbols":cSLASH, "AdditionalConditions":[], "NewState":cscReadFastCloseSlash},
    {"LogicalOperation":"In", "Symbols":cTAGFINISH, "AdditionalConditions":[], "NewState":cscReadTagFinish},
    {"LogicalOperation":"Limit", "Symbols":[], "AdditionalConditions":[], "NewState":cscError},
    ]},
    
cscReadUQAttributeValue:{"name":"ReadUQAttributeValue", "Accumulate":True, "AccNumber":2, "Vars":[], "OnEnter":None, "OnLeave":"OnDoneAttributeValue", "Limit":0, "Stop":False, "CSOE":[], "CSOL":[], "ExitConditions":[
    {"LogicalOperation":"In", "Symbols":cSPACE, "AdditionalConditions":[], "NewState":cscReadSpacesBetweenAttributes},
    {"LogicalOperation":"In", "Symbols":cSLASH, "AdditionalConditions":[], "NewState":cscReadFastCloseSlash},
    {"LogicalOperation":"In", "Symbols":cTAGFINISH, "AdditionalConditions":[], "NewState":cscReadTagFinish},
    ]},


cscReadClosingTagName:{"name":"ReadClosingTagName", "Accumulate":True, "AccNumber":0, "Vars":[("ClosingTag", cvaSet)], "OnEnter":None, "OnLeave":None, "Limit":0, "Stop":False, "CSOE":[], "CSOL":[], "ExitConditions":[
    {"LogicalOperation":"In", "Symbols":cTAGFINISH, "AdditionalConditions":[], "NewState":cscReadTagFinish}
    ]},

cscReadTagFinish:{"name":"ReadTagFinish", "Accumulate":False, "AccNumber":-1, "Vars":[], "OnEnter":None, "OnLeave":"OnDoneReadingTagFinish", "Limit":1, "Stop":False, "CSOE":[], "CSOL":[], "ExitConditions":[
    {"LogicalOperation":"In", "Symbols":cTAGSTART, "AdditionalConditions":[["Var", "EQ", "Script", True]], "NewState":cscJS_TagStart},
    {"LogicalOperation":"In", "Symbols":cTAGSTART, "AdditionalConditions":[], "NewState":cscReadTagStart},
    {"LogicalOperation":"Limit", "Symbols":[], "AdditionalConditions":[["Var", "EQ", "Script", True]], "NewState":cscJS_Wild},
    {"LogicalOperation":"Limit", "Symbols":[], "AdditionalConditions":[], "NewState":cscReadWildText}
    ]},

cscReadWildText:{"name":"ReadWildText", "Accumulate":True, "AccNumber":3, "Vars":[], "OnEnter":None, "OnLeave":"OnDoneReadingWildText", "Limit":0, "Stop":False, "CSOE":[], "CSOL":[], "ExitConditions":[
    {"LogicalOperation":"In", "Symbols":cTAGSTART, "AdditionalConditions":[], "NewState":cscReadTagStart},
    ]},




cscReadExcAfterTagStart:{"name": "ReadExcAfterTagStart", "Accumulate":False, "AccNumber":-1, "Vars":[], "OnEnter":None, "OnLeave":None, "Limit":1, "Stop":False, "CSOE":[], "CSOL":[], "ExitConditions":[
    {"LogicalOperation":"In", "Symbols":cMINUS, "AdditionalConditions":[], "NewState":cscCommentBegin_M1Done_M2Wait},
    {"LogicalOperation":"Limit", "Symbols":[], "AdditionalConditions":[], "NewState":cscReadDoctype}
    ]},

cscReadDoctype:{"name":"ReadDoctype", "Accumulate":False, "AccNumber":-1, "Vars":[], "OnEnter":None, "OnLeave":None, "Limit":0, "Stop":False, "CSOE":[], "CSOL":[], "ExitConditions":[
    {"LogicalOperation":"In", "Symbols":cTAGFINISH, "AdditionalConditions":[], "NewState":cscReadDoctypeTagFinish}
    ]},

cscReadDoctypeTagFinish:{"name":"ReadDoctypeTagFinish", "Accumulate":False, "AccNumber":-1, "Vars":[], "OnEnter":None, "OnLeave":None, "Limit":1, "Stop":False, "CSOE":[], "CSOL":[], "ExitConditions":[
    {"LogicalOperation":"In", "Symbols":cTAGSTART, "AdditionalConditions":[], "NewState":cscReadTagStart},
    {"LogicalOperation":"Limit", "Symbols":[], "AdditionalConditions":[], "NewState":cscReadWildText}
    ]},


cscJS_Wild:{"name":"JS_Wild", "Accumulate":False, "AccNumber":-1, "Vars":[], "OnEnter":None, "OnLeave":None, "Limit":0, "Stop":False, "CSOE":[], "CSOL":[], "ExitConditions":[
    {"LogicalOperation":"In", "Symbols":cSINGLEQUOTE, "AdditionalConditions":[], "NewState":cscJS_SQ_Start},
    {"LogicalOperation":"In", "Symbols":cDOUBLEQUOTE, "AdditionalConditions":[], "NewState":cscJS_DQ_Start},
    {"LogicalOperation":"In", "Symbols":cTAGSTART, "AdditionalConditions":[], "NewState":cscJS_TagStart},
    {"LogicalOperation":"In", "Symbols":cDIVIDE, "AdditionalConditions":[], "NewState":cscJS_Divide},
    ]},

cscJS_SQ_Start:{"name":"JS_SQ_Start", "Accumulate":False, "AccNumber":-1, "Vars":[], "OnEnter":None, "OnLeave":None, "Limit":1, "Stop":False, "CSOE":[], "CSOL":[], "ExitConditions":[
    {"LogicalOperation":"In", "Symbols":cSINGLEQUOTE, "AdditionalConditions":[], "NewState":cscJS_SQ_Finish},
    {"LogicalOperation":"Limit", "Symbols":[], "AdditionalConditions":[], "NewState":cscJS_SQ_Text},
    ]},

cscJS_SQ_Text:{"name":"JS_SQ_Text", "Accumulate":False, "AccNumber":-1, "Vars":[], "OnEnter":None, "OnLeave":None, "Limit":0, "Stop":False, "CSOE":[], "CSOL":[], "ExitConditions":[
    {"LogicalOperation":"In", "Symbols":cSINGLEQUOTE, "AdditionalConditions":[], "NewState":cscJS_SQ_Finish},
    ]},

cscJS_SQ_Finish:{"name":"JS_SQ_Finish", "Accumulate":False, "AccNumber":-1, "Vars":[], "OnEnter":None, "OnLeave":None, "Limit":1, "Stop":False, "CSOE":[], "CSOL":[], "ExitConditions":[
    {"LogicalOperation":"In", "Symbols":cDOUBLEQUOTE, "AdditionalConditions":[], "NewState":cscJS_DQ_Start},
    {"LogicalOperation":"In", "Symbols":cSINGLEQUOTE, "AdditionalConditions":[], "NewState":cscJS_SQ_Start},
    {"LogicalOperation":"In", "Symbols":cTAGSTART, "AdditionalConditions":[], "NewState":cscJS_TagStart},
    {"LogicalOperation":"In", "Symbols":cDIVIDE, "AdditionalConditions":[], "NewState":cscJS_Divide},
    {"LogicalOperation":"Limit", "Symbols":[], "AdditionalConditions":[], "NewState":cscJS_Wild}
    ]},



cscJS_DQ_Start:{"name":"JS_DQ_Start", "Accumulate":False, "AccNumber":-1, "Vars":[], "OnEnter":None, "OnLeave":None, "Limit":1, "Stop":False, "CSOE":[], "CSOL":[], "ExitConditions":[
    {"LogicalOperation":"In", "Symbols":cDOUBLEQUOTE, "AdditionalConditions":[], "NewState":cscJS_DQ_Finish},
    {"LogicalOperation":"Limit", "Symbols":[], "AdditionalConditions":[], "NewState":cscJS_DQ_Text},
    ]},

cscJS_DQ_Text:{"name":"JS_DQ_Text", "Accumulate":False, "AccNumber":-1, "Vars":[], "OnEnter":None, "OnLeave":None, "Limit":0, "Stop":False, "CSOE":[], "CSOL":[], "ExitConditions":[
    {"LogicalOperation":"In", "Symbols":cDOUBLEQUOTE, "AdditionalConditions":[], "NewState":cscJS_DQ_Finish},
    ]},

cscJS_DQ_Finish:{"name":"JS_DQ_Finish", "Accumulate":False, "AccNumber":-1, "Vars":[], "OnEnter":None, "OnLeave":None, "Limit":1, "Stop":False, "CSOE":[], "CSOL":[], "ExitConditions":[
    {"LogicalOperation":"In", "Symbols":cDOUBLEQUOTE, "AdditionalConditions":[], "NewState":cscJS_DQ_Start},
    {"LogicalOperation":"In", "Symbols":cSINGLEQUOTE, "AdditionalConditions":[], "NewState":cscJS_SQ_Start},
    {"LogicalOperation":"In", "Symbols":cDIVIDE, "AdditionalConditions":[], "NewState":cscJS_Divide},
    {"LogicalOperation":"In", "Symbols":cTAGSTART, "AdditionalConditions":[], "NewState":cscJS_TagStart},
    {"LogicalOperation":"Limit", "Symbols":[], "AdditionalConditions":[], "NewState":cscJS_Wild}
    ]},


cscJS_Divide:{"name":"JS_Divide", "Accumulate":False, "AccNumber":-1, "Vars":[], "OnEnter":None, "OnLeave":None, "Limit":1, "Stop":False, "CSOE":[], "CSOL":[], "ExitConditions":[
    {"LogicalOperation":"In", "Symbols":cMULTIPLY, "AdditionalConditions":[], "NewState":cscJS_DivMul},
    {"LogicalOperation":"In", "Symbols":cDIVIDE, "AdditionalConditions":[], "NewState":cscJS_Divide},
    {"LogicalOperation":"Limit", "Symbols":[], "AdditionalConditions":[], "NewState":cscJS_Wild},
    ]},

cscJS_DivMul:{"name":"JS_DivMul", "Accumulate":False, "AccNumber":-1, "Vars":[], "OnEnter":None, "OnLeave":None, "Limit":1, "Stop":False, "CSOE":[], "CSOL":[], "ExitConditions":[
    {"LogicalOperation":"In", "Symbols":cMULTIPLY, "AdditionalConditions":[], "NewState":cscJS_Comment_Mul},
    {"LogicalOperation":"Limit", "Symbols":[], "AdditionalConditions":[], "NewState":cscJS_Comment},
    ]},

cscJS_Comment:{"name":"JS_Comment", "Accumulate":False, "AccNumber":-1, "Vars":[], "OnEnter":None, "OnLeave":None, "Limit":0, "Stop":False, "CSOE":[], "CSOL":[], "ExitConditions":[
    {"LogicalOperation":"In", "Symbols":cMULTIPLY, "AdditionalConditions":[], "NewState":cscJS_Comment_Mul}
    ]},

cscJS_Comment_Mul:{"name":"JS_Comment_Mul", "Accumulate":False, "AccNumber":-1, "Vars":[], "OnEnter":None, "OnLeave":None, "Limit":1, "Stop":False, "CSOE":[], "CSOL":[], "ExitConditions":[
    {"LogicalOperation":"In", "Symbols":cDIVIDE, "AdditionalConditions":[], "NewState":cscJS_Comment_MulDiv},
    {"LogicalOperation":"In", "Symbols":cMULTIPLY, "AdditionalConditions":[], "NewState":cscJS_Comment_Mul},
    {"LogicalOperation":"Limit", "Symbols":[], "AdditionalConditions":[], "NewState":cscJS_Comment},
    ]},

cscJS_Comment_MulDiv:{"name":"JS_Comment_MulDiv", "Accumulate":False, "AccNumber":-1, "Vars":[], "OnEnter":None, "OnLeave":None, "Limit":1, "Stop":False, "CSOE":[], "CSOL":[], "ExitConditions":[
    {"LogicalOperation": "In", "Symbols": cDOUBLEQUOTE, "AdditionalConditions": [], "NewState": cscJS_DQ_Start},
    {"LogicalOperation": "In", "Symbols": cSINGLEQUOTE, "AdditionalConditions": [], "NewState": cscJS_SQ_Start},
    {"LogicalOperation": "In", "Symbols": cTAGSTART, "AdditionalConditions": [], "NewState": cscJS_TagStart},
    {"LogicalOperation": "In", "Symbols": cDIVIDE, "AdditionalConditions": [], "NewState": cscJS_Divide},
    {"LogicalOperation": "Limit", "Symbols": [], "AdditionalConditions": [], "NewState": cscJS_Wild}
    ]},

cscJS_TagStart:{"name":"JS_TagStart", "Accumulate":False, "AccNumber":-1, "Vars":[], "OnEnter":None, "OnLeave":None, "Limit":1, "Stop":False, "CSOE":[], "CSOL":[], "ExitConditions":[
    {"LogicalOperation":"In", "Symbols":cSLASH, "AdditionalConditions":[], "NewState":cscJS_TagStart_ReadSlash_Done_WaitFor_L1},

    {"LogicalOperation": "In", "Symbols": cDOUBLEQUOTE, "AdditionalConditions": [], "NewState": cscJS_DQ_Start},
    {"LogicalOperation": "In", "Symbols": cSINGLEQUOTE, "AdditionalConditions": [], "NewState": cscJS_SQ_Start},
    {"LogicalOperation": "In", "Symbols": cTAGSTART, "AdditionalConditions": [], "NewState": cscJS_TagStart},
    {"LogicalOperation": "In", "Symbols": cDIVIDE, "AdditionalConditions": [], "NewState": cscJS_Divide},

    {"LogicalOperation":"Limit", "Symbols":[], "AdditionalConditions":[], "NewState":cscJS_Wild},
    ]},

cscJS_TagStart_ReadSlash_Done_WaitFor_L1: {"name": "JS_TagStart", "Accumulate": False, "AccNumber": -1, "Vars": [], "OnEnter": None, "OnLeave": None, "Limit": 1, "Stop": False, "CSOE":[], "CSOL":[], "ExitConditions": [
    {"LogicalOperation": "In", "Symbols": ["s", "S"], "AdditionalConditions": [], "NewState": cscJS_TagStart_L1_Done_WaitFor_L2},
    {"LogicalOperation": "In", "Symbols": cDOUBLEQUOTE, "AdditionalConditions": [], "NewState": cscJS_DQ_Start},
    {"LogicalOperation": "In", "Symbols": cSINGLEQUOTE, "AdditionalConditions": [], "NewState": cscJS_SQ_Start},
    {"LogicalOperation": "In", "Symbols": cTAGSTART, "AdditionalConditions": [], "NewState": cscJS_TagStart},
    {"LogicalOperation": "In", "Symbols": cDIVIDE, "AdditionalConditions": [], "NewState": cscJS_Divide},

    {"LogicalOperation": "Limit", "Symbols": [], "AdditionalConditions": [], "NewState": cscJS_Wild},
    ]},


cscJS_TagStart_L1_Done_WaitFor_L2:{"name":"JS_TagStart_L1_Done_WaitFor_L2", "Accumulate":False, "AccNumber":-1, "Vars":[], "OnEnter":None, "OnLeave":None, "Limit":1, "Stop":False, "CSOE":[], "CSOL":[], "ExitConditions":[
    {"LogicalOperation": "In", "Symbols": ["c", "C"], "AdditionalConditions": [], "NewState": cscJS_TagStart_L2_Done_WaitFor_L3},
    {"LogicalOperation": "Limit", "Symbols": [], "AdditionalConditions": [], "NewState": cscError}
    ]},

cscJS_TagStart_L2_Done_WaitFor_L3:{"name":"JS_TagStart_L2_Done_WaitFor_L3", "Accumulate":False, "AccNumber":-1, "Vars":[], "OnEnter":None, "OnLeave":None, "Limit":1, "Stop":False, "CSOE":[], "CSOL":[], "ExitConditions":[
    {"LogicalOperation": "In", "Symbols": ["r", "R"], "AdditionalConditions": [], "NewState": cscJS_TagStart_L3_Done_WaitFor_L4},
    {"LogicalOperation": "Limit", "Symbols": [], "AdditionalConditions": [], "NewState": cscError}
    ]},

cscJS_TagStart_L3_Done_WaitFor_L4:{"name":"JS_TagStart_L3_Done_WaitFor_L4", "Accumulate":False, "AccNumber":-1, "Vars":[], "OnEnter":None, "OnLeave":None, "Limit":1, "Stop":False, "CSOE":[], "CSOL":[], "ExitConditions":[
    {"LogicalOperation": "In", "Symbols": ["i","I"], "AdditionalConditions": [], "NewState": cscJS_TagStart_L4_Done_WaitFor_L5},
    {"LogicalOperation": "Limit", "Symbols": [], "AdditionalConditions": [], "NewState": cscError}
    ]},

cscJS_TagStart_L4_Done_WaitFor_L5:{"name":"JS_TagStart_L4_Done_WaitFor_L5", "Accumulate":False, "AccNumber":-1, "Vars":[], "OnEnter":None, "OnLeave":None, "Limit":1, "Stop":False, "CSOE":[], "CSOL":[], "ExitConditions":[
    {"LogicalOperation": "In", "Symbols": ["p", "P"], "AdditionalConditions": [], "NewState": cscJS_TagStart_L5_Done_WaitFor_L6},
    {"LogicalOperation": "Limit", "Symbols": [], "AdditionalConditions": [], "NewState": cscError}
    ]},

cscJS_TagStart_L5_Done_WaitFor_L6:{"name":"JS_TagStart_L5_Done_WaitFor_L6", "Accumulate":False, "AccNumber":-1, "Vars":[], "OnEnter":None, "OnLeave":None, "Limit":1, "Stop":False, "CSOE":[], "CSOL":[], "ExitConditions":[
    {"LogicalOperation": "In", "Symbols": ["t", "T"], "AdditionalConditions": [], "NewState": cscJS_TagStart_L6_Done_WaitFor_TagFinish},
    {"LogicalOperation": "Limit", "Symbols": [], "AdditionalConditions": [], "NewState": cscError}
    ]},

cscJS_TagStart_L6_Done_WaitFor_TagFinish:{"name":"JS_TagStart_L6_Done_WaitFor_TagFinish", "Accumulate":False, "AccNumber":-1, "Vars":[], "OnEnter":None, "OnLeave":None, "Limit":1, "Stop":False, "CSOE":[], "CSOL":[], "ExitConditions":[
    {"LogicalOperation": "In", "Symbols": cTAGFINISH, "AdditionalConditions": [], "NewState": cscJS_TagFinish},
    {"LogicalOperation": "Limit", "Symbols": [], "AdditionalConditions": [], "NewState": cscError}
    ]},

cscJS_TagFinish:{"name":"JS_TagFinish", "Accumulate":False, "AccNumber":-1, "Vars":[], "OnEnter":None, "OnLeave":None, "Limit":1, "Stop":False, "CSOE":[], "CSOL":[], "ExitConditions":[
    {"LogicalOperation":"In", "Symbols":cTAGSTART, "AdditionalConditions":[], "NewState":cscReadTagStart},
    {"LogicalOperation":"Limit", "Symbols":[], "AdditionalConditions":[], "NewState":cscReadWildText}
    ]},



cscCommentBegin_M1Done_M2Wait:{"name":"CommentBegin_M1Done_M2Wait", "Accumulate":False, "AccNumber":-1, "Vars":[], "OnEnter":None, "OnLeave":None, "Limit":1, "Stop":False, "CSOE":[], "CSOL":[], "ExitConditions":[
    {"LogicalOperation":"In", "Symbols":cMINUS, "AdditionalConditions":[], "NewState":cscCommentBegin_M2Done},
    {"LogicalOperation":"Limit", "Symbols":[], "AdditionalConditions":[], "NewState":cscError}
    ]},

cscCommentBegin_M2Done:{"name":"CommentBegin_M2Done", "Accumulate":False, "AccNumber":-1, "Vars":[], "OnEnter":None, "OnLeave":None, "Limit":1, "Stop":False, "CSOE":[], "CSOL":[], "ExitConditions":[
    {"LogicalOperation":"In", "Symbols":cMINUS, "AdditionalConditions":[], "NewState":cscCommentEnd_M1Done_M2Wait},
    {"LogicalOperation":"Limit", "Symbols":[], "AdditionalConditions":[], "NewState":cscComment}
    ]},

cscComment:{"name":"Comment", "Accumulate":False, "AccNumber":-1, "Vars":[], "OnEnter":None, "OnLeave":None, "Limit":1, "Stop":False, "CSOE":[], "CSOL":[], "ExitConditions":[
    {"LogicalOperation":"In", "Symbols":cMINUS, "AdditionalConditions":[], "NewState":cscCommentEnd_M1Done_M2Wait}
    ]},

cscCommentEnd_M1Done_M2Wait:{"name":"CommentEnd_M1Done_M2Wait", "Accumulate":False, "AccNumber":-1, "Vars":[], "OnEnter":None, "OnLeave":None, "Limit":1, "Stop":False, "CSOE":[], "CSOL":[], "ExitConditions":[
    {"LogicalOperation":"In", "Symbols":cMINUS, "AdditionalConditions":[], "NewState":cscCommentEnd_M2Done_TagFinishWait},
    {"LogicalOperation":"Limit", "Symbols":[], "AdditionalConditions":[], "NewState":cscComment}
    ]},

cscCommentEnd_M2Done_TagFinishWait:{"name":"CommentEnd_M2Done_TagFinishWait", "Accumulate":False, "AccNumber":-1, "Vars":[], "OnEnter":None, "OnLeave":None, "Limit":1, "Stop":False, "CSOE":[], "CSOL":[], "ExitConditions":[
    {"LogicalOperation":"In", "Symbols":cTAGFINISH, "AdditionalConditions":[], "NewState":cscCommentEnd_TagFinishDone},
    {"LogicalOperation":"In", "Symbols":cMINUS, "AdditionalConditions":[], "NewState":cscCommentEnd_M1Done_M2Wait},
    {"LogicalOperation":"Limit", "Symbols":[], "AdditionalConditions":[], "NewState":cscComment}
    ]},

cscCommentEnd_TagFinishDone:{"name":"CommentEnd_TagFinishDone", "Accumulate":False, "AccNumber":-1, "Vars":[], "OnEnter":None, "OnLeave":None, "Limit":1, "Stop":False, "CSOE":[], "CSOL":[], "ExitConditions":[
    {"LogicalOperation":"In", "Symbols":cTAGSTART, "AdditionalConditions":[], "NewState":cscReadTagStart},
    {"LogicalOperation":"Limit", "Symbols":[], "AdditionalConditions":[], "NewState":cscReadWildText}
    ]},

cscError:{"name":"Error", "Accumulate":False, "AccNumber":-1, "Vars":[], "OnEnter":None, "OnLeave":None, "Limit":0, "Stop":True, "CSOE":[], "CSOL":[], "ExitConditions":[
    ]}
}
