

class TPostElement:
    def __init__(self, Type, Text, Attributes, Source, SaveText, SaveAttributes, SaveSource):
        self.fElementType = Type
        self.fElementText = Text
        self.fElementAttributes = Attributes
        self.fElementSource = Source
        self.fSaveText = SaveText
        self.fSaveAttributes = SaveAttributes
        self.fSaveSource = SaveSource

class TPost:
    def __init__(self):
        self.fNumber = 0
        self.fDate = 0
        self.fIsOP = False
        self.fElements = []
        self.fImages = []
        self.fDate = ""
        self.fSaveAttributes = True
        self.fSaveText = True
        self.fSaveSource = True
        self.fPosterID = ""


    def AddElement(self, Type, Text, Attributes, Source):
        save_attr = True
        save_text = True
        save_src = True
        if Type == "br":
            save_attr = False
            save_text = False
            save_src = False
            
        if Type == "text":
            save_src = False
            
        self.fElements.append(TPostElement(Type, Text, Attributes, Source, save_text, save_attr, save_src))
        

        
    def AddImage(self, UID, Type, FileName, Source, PreviewFileName, PreviewSource):
        self.fImages.append( (UID, Type, FileName, Source, PreviewFileName, PreviewSource) )
        
    def Print(self):
        s = ""
        s += "# ======== Post #"+str(self.fNumber)+" ================= \n"
        s += "@post\n"
        s += "@local post=\""+str(self.fNumber)+"\" date=\""+self.fDate+"\" poster_id=\""+self.fPosterID+"\"\n"
        
        for E in self.fElements:
            s_attr = ""
            s_src = ""
            s_text = ""
            if E.fSaveText:
                s_text = "text=\""+E.fElementText+"\""
            if E.fSaveAttributes:
                s_attr = "attr=\""+"".join(E.fElementAttributes)+"\""
            if E.fSaveSource:
                s_src = "source=\""+E.fElementSource+"\""
                
            s += E.fElementType + " "+s_attr+" "+s_src+" "+s_text+"\n"
            
        if len(self.fImages) > 0:
            s += "# Images:\n"
            for I in self.fImages:
                UID, Type, FileName, Source, PreviewFileName, PreviewSource = I[0], I[1], I[2], I[3], I[4], I[5]                
                #s += "img uid=\""+UID+"\" type=\""+Type+"\" filename=\""+FileName+"\" preview=\""+PreviewFileName+"\"\n"
                s += "img type=\""+Type+"\" filename=\""+FileName+"\" preview=\""+PreviewFileName+"\"\n"
                
        s += "@endpost\n"
        s += "\n"
        
        return s
            

class TPostList:
    def __init__(self):
        self.fPosts = []

    def AddPost(self, Post):
        self.fPosts.append(Post)

class TAbstractParser:
    def __init__(self):
        self.fPosts = []

    def Parse(self):
        pass

    def Clear(self):
        self.fPosts.clear()
