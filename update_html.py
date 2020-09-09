#!/usr/bin/python
from bitcoinrpc.authproxy import AuthServiceProxy
import time
import datetime
import RPC_PASSWORDS as rp
import subprocess

siteDir = "/home/pi/repos/boomerNodeStats/"

def updatePricePage():
    ratehtml = subprocess.check_output(["curl", "rate.sx/btc"])
    html = ratehtml.split("<pre>")[1].split("begin")[0]

    with open(siteDir + "price.html", 'r') as f:
        siteContents = f.read()

    preContents, middle, postContents = siteContents.split('<!---splithere-->\n')

    splitLine = '<!---splithere-->\n'
    with open(siteDir + "price.html", 'w') as f:
        f.write(preContents + splitLine + html + splitLine + postContents)
    return


while True:
    try:
        rpc_connection = AuthServiceProxy("http://{}:{}@127.0.0.1:8332".format(rp.username,
                                                                               rp.password
                                                                               ))
        info = rpc_connection.getblockchaininfo()

        #print(info)

        with open(siteDir + "index.html", 'r') as f:
            siteContents = f.read()

        preContents, middle, postContents = siteContents.split('<!---splithere-->\n')

        middle = ""

        for infokey in ["blocks", "difficulty", "headers", "bestblockhash", "size_on_disk"]:
            statValue = info[infokey]
            middle += "<p><b>" + infokey + ": </b>" + str(statValue) + "</p>\n"

        now = datetime.datetime.now()
        middle += "<p><b>Last Updated<b>: " + now.strftime("%Y-%m-%d %H:%M:%S") + " AEST</p>\n"


        splitLine = '<!---splithere-->\n'
        with open(siteDir + "index.html", 'w') as f:
            f.write(preContents + splitLine + middle + splitLine + postContents)

        try:
            updatePricePage()
        except:
            continue

        try:
            subprocess.call(["rsync", "-a", siteDir, "root@202.182.97.180:/var/www/nodeStats/"])
        except Exception as e:
            print("rsync error: ")
            print(e)
            time.sleep(60*5)
            continue

        print(now.strftime("%Y-%m-%d %H:%M:%S"))
        print("sleeping")



    except Exception as e:
        print("main error: ")
        print(e)
        time.sleep(60*5)
        continue


    time.sleep(60)
