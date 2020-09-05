#!/usr/bin/python
from bitcoinrpc.authproxy import AuthServiceProxy
import time
import RPC_PASSWORDS as rp

rpc_connection = AuthServiceProxy("http://{}:{}@127.0.0.1:8332".format(rp.username,
                                                               rp.password
                                                               ))
info = rpc_connection.getblockchaininfo()

print(info)

with open("index.html", 'r') as f:
    siteContents = f.read()

preContents, middle, postContents = siteContents.split('<!---splithere-->')

middle = ""

for infokey in ["blocks", "difficulty", "headers", "bestblockhash", "size_on_disk"]:
    statValue = info[infokey]
    middle += "<p><b>" + infokey + ": </b>" + str(statValue) + "</p>\n"


splitLine = '<!---splithere-->\n'
with open("index.html", 'w') as f:
    f.write(preContents + splitLine + middle + splitLine + postContents)
