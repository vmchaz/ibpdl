from html.parser import HTMLParser
from httpclient import execute_http_request, download_file
import sys
import os

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        #print("Encountered a start tag:", tag, attrs)
        if tag == "a":
            #print("[a] tag:", attrs)
            fnd  = False
            href = ""
            for attr in attrs:
                if attr[0] == "href":
                    href = attr[1]
                    
                if attr[0] == "class" and attr[1] == "post__image-link":
                    fnd = True
                    
            if fnd:
                self.links.append("https://2ch.hk"+href)
                #print(href)
                

    def handle_endtag(self, tag):
        #print("Encountered an end tag :", tag)
        pass

    def handle_data(self, data):
        #print("Encountered some data  :", data)
        pass
        
def save_to_tar(files:dict, tarfn):
    if not tarfn.endswith(".tar"):
        tarfn = tarfn + ".tar"

    print("Saving data to", tarfn)

    tar = tarfile.open(tarfn, "w")
    for PN, PV in files:
        fb = BytesIO(PV)
        ti = tarfile.TarInfo(name=PN)
        ti.size = len(PV)
        ti.mtime = time.time()
        tar.addfile(tarinfo=ti, fileobj=fb)

    #ThreadTextData = ThreadText.encode("utf-8")
    #fb = BytesIO(ThreadTextData)
    #ti = tarfile.TarInfo(name="index.txt")
    #ti.size = len(ThreadTextData)
    #ti.mtime = time.time()
    #tar.addfile(tarinfo=ti, fileobj=fb)

    fb = BytesIO(lRawData)
    ti = tarfile.TarInfo(name="index.html")
    ti.size = len(lRawData)
    ti.mtime = time.time()
    tar.addfile(tarinfo=ti, fileobj=fb)

    tar.close()
    print("Saving complete")
    

def main():
    if len(sys.argv) < 3:
        print("Not enough arguments")
        return
                    
    htmldata = execute_http_request(sys.argv[1], RetryCount=1, encoding="utf8")
    targetdir = sys.argv[2]
    
    f = open(os.path.join(targetdir, "index.html"), "w")
    f.write(, htmldata)
    f.close()

    parser = MyHTMLParser()
    parser.links = []
    parser.feed(htmldata)
    
        
    
    for l in parser.links:
        fn = l.split("/")[-1]
        
        if not os.path.isfile(fn):
            print("Downloading file", l)
            fd = download_file(l)
            f = open(fn, "wb")
            f.write(os.path.join(targetdir, fd))
            f.close()
            print("Done")
            

if __name__=="__main__":
    main()
