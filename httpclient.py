#import urllib2
#from urllib.request import urlopen
import urllib.request



"""def execute_http_request(URL):
    try:
        html_resp = urlopen(URL)
        html_raw_data = html_resp.read()
        return html_raw_data.decode("utf-8")
    
    except:
        return "" """
        
def execute_http_request(URL, encoding = ""):
    #try:
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0'}
    req = urllib.request.Request(URL, data=None, headers=hdr)

    f = urllib.request.urlopen(req)
    raw_data = f.read()
    if encoding == "":
        return raw_data
    else:
        decoded_data = raw_data.decode(encoding)
        return decoded_data
    
    
def download_file(URL):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0'}
    req = urllib.request.Request(URL, data=None, headers=hdr)

    f = urllib.request.urlopen(req)
    raw_data = f.read()
    return raw_data

