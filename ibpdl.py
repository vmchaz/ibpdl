import sys, os
import download_2ch_thread
import copy

def GetConfigFileName():
    script_full_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_full_path)
    config_path = os.path.join(script_dir, "ibpdl.conf")
    return config_path

def ParseConfigFile(file_name, dict):
    f = open(file_name, "r")
    lines = f.readlines()
    f.close()
    for l in lines:
        parts = l.split("=")
        if len(parts) >= 2:
            p1 = parts[0].strip()
            p2 = parts[1].strip()
            if len(p1) > 0 and len(p2) > 0:
                dict[p1] = p2

args = []
for k, v in enumerate(sys.argv):
    if k > 0:
        args.append(v)

if len(args) < 1:
    print("not enough args!")
    sys.exit(0)

address = args[0]
args = args[1:]


conf_path = GetConfigFileName()

conf = {}
ParseConfigFile(conf_path, conf)
    
if download_2ch_thread.DoesAddressMatch(address):
    download_2ch_thread.DownloadThread(address, args, conf)

