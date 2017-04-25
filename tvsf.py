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
    
cstReadSpacesBeforeName = 0
cstReadName = 1
cstReadSpacesAfterName = 2
cstReadEq = 3
cstReadSpacesAfterEq = 4
cstReadOpeningQuote = 5
cstReadValue = 6
cstReadClosingQuote = 7
cstReadUQValue = 8
cstError = 9

def ParseParametersString(S, Parameters):
    if len(S) == 0:
        return
        
    S += " "
    
    st = 0
    p = ""
    v = ""
    qs = []
    lENG_LOCASE_LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    lENG_UPCASE_LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    lENG_LETTERS = lENG_LOCASE_LETTERS + lENG_UPCASE_LETTERS
    lDIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    lUNDERSCORE = ['_']
    lDOT = ['.']
    lQUOTE = ['"']
    lMINUS = ['-']

    lNAMESYM = lENG_LETTERS + lDIGITS + lUNDERSCORE + lMINUS + lDOT
    lSPACESYM = [" ", chr(9)]
    lEQSYM = ["="]
    
    if S[0] in lNAMESYM:
        st = cstReadSpacesBeforeName
    elif S[0] in lSPACESYM:
        st = cstReadName
    else:
        st = cstError
    
    for C in S:
        if st == cstReadSpacesBeforeName:
            if C in lSPACESYM:
                pass
            elif C in lNAMESYM:
                p += C
                st = cstReadName
            else:
                st = cstError
                break
                                
        elif st == cstReadName:
            if C in lNAMESYM:
                p += C
            elif C in lSPACESYM:
                st = cstReadSpacesAfterName
            elif C in lEQSYM:
                st = cstReadEq
            else:
                st = cstError
                break
                
        elif st == cstReadSpacesAfterName:
            if C in lSPACESYM:
                pass
            elif C in lEQSYM:
                st = cstReadEq
            else:
                st = cstError
                break
                
        elif st == cstReadEq:
            if C in lSPACESYM:
                st = cstReadSpacesAfterEq
            elif C in lQUOTE:
                st = cstReadOpeningQuote
            elif C in lNAMESYM:                
                v += C
                st = cstReadUQValue                
            else:
                st = cstError
                break
                
        elif st == cstReadSpacesAfterEq:
            if C in lSPACESYM:
                pass
            elif C in lQUOTE:
                st = cstReadOpeningQuote
            elif C in lNAMESYM:
                v += C
                st = cstReadUQValue
            else:
                st = cstError
                break
                
        elif st == cstReadOpeningQuote:
            if C in lQUOTE:
                v = ""
                st = cstReadClosingQuote
            else:
                v += C
                st = cstReadValue
                
        elif st == cstReadValue:
            if C in lQUOTE:
                st = cstReadClosingQuote
                if len(p) > 0:
                    Parameters[p] = v
                p = ""
                v = ""
            else:
                v += C
                
        elif st == cstReadClosingQuote:
            if C in lSPACESYM:
                st = cstReadSpacesBeforeName
            else:
                st = cstError
                break
                
        elif st == cstReadUQValue:
            if C in lNAMESYM:
                v += C
            elif C in lSPACESYM:
                if len(p) > 0:
                    Parameters[p] = v
                v = ""
                p = ""
                st = cstReadSpacesBeforeName
            else:
                st = cstError
            
        elif st == cstError:
            pass
            
    if st == cstError:
        return -1
    
    return 0
    
    
s0, s1 = SplitStringByFirstSymbol('@data format="png" source="1234.png" preview="1234s.jpg" v=3 b=1', " ")
d0 = {}


r = ParseParametersString(s1, d0)
print(r, "["+s0+"]", "["+s1+"]", d0)

