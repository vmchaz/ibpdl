class TBinaryReader:
    def __init__(self, Data):
        self.fData = Data
        self.fPosition = 0
        self.fPushBackBuffer = []
        self.fLast = ""
        self.fDebugBuffer = []
        self.fMaxLen = 200

    def Read(self):
        if(self.fPosition < len(self.fData)):
            Ch = self.fData[self.fPosition]
            self.fPosition += 1
            self.fLast = Ch

            #if Ch != "\n":
            if len(self.fDebugBuffer) > self.fMaxLen:
                del self.fDebugBuffer[0]
            self.fDebugBuffer.append(Ch)

            return Ch
        else:
            return ""
            #raise self.fPosition

    def PushBack(self, Ch):
        if self.fPosition > 0:
            self.fPosition -= 1

    def GetDebugBuffer(self):
        S = "".join(self.fDebugBuffer)
        return S
