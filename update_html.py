#!/usr/bin/python
from bitcoinrpc.authproxy import AuthServiceProxy
import time
import datetime
import RPC_PASSWORDS as rp
import subprocess

while True:

    rpc_connection = AuthServiceProxy("http://{}:{}@127.0.0.1:8332".format(rp.username,
                                                                           rp.password
                                                                           ))
    info = rpc_connection.getblockchaininfo()

    print(info)

    with open("index.html", 'r') as f:
        siteContents = f.read()

    preContents, middle, postContents = siteContents.split('<!---splithere-->\n')

    middle = ""

    for infokey in ["blocks", "difficulty", "headers", "bestblockhash", "size_on_disk"]:
        statValue = info[infokey]
        middle += "<p><b>" + infokey + ": </b>" + str(statValue) + "</p>\n"
    
    now = datetime.datetime.now()
    middle += "<p><b>Last Updated<b>: " + now.strftime("%Y-%m-%d %H:%M:%S") + " AEST</p>\n"


    splitLine = '<!---splithere-->\n'
    with open("index.html", 'w') as f:
        f.write(preContents + splitLine + middle + splitLine + postContents)

    
    try:
        subprocess.call(["rsync", "-a", "./index.html", "root@202.182.97.180:/var/www/nodeStats/index.html"])
    except Exception as e:
        print("Error: " + e)

    print("sleeping")
    time.sleep(60)
