from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import TCLink
import os


PORT = 6666

COUNT = 200

#Matrix full
#Buffer=(rate)*2*(latency)/1000*Bandwidth Example: 1 = 1 * 2 * 100/1000 * 100Mbps = 20Mb = 2.5 MB
#Bandwidth Mb/s Example: 100 = 100Mb/s
#Latency ms     Example: 100 = 100ms
'''
TCPCCAs=["BBR", "CUBIC"]
BUFFER1=[1.0, 0.8, 0.6, 0.5, 0.4, 0.2, 0.1]
BUFFER2=[1.0, 0.8, 0.6, 0.5, 0.4, 0.2, 0.1]
BANDWIDTH1=[1,10,50,100,200]
BANDWIDTH2=[1,10,50,100,200]
LATENCY1=[1,10,20,50,100,200]
LATENCY2=[1,10,20,50,100,200,500,1000]
'''


bw1 = None
bw2 = None
dl1 = None
dl2 = None
bf1 = None
bf2 = None

class MyTopo( Topo ): 
    def build( self ):
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        h1 = self.addHost('h1')
        h2 = self.addHost('h2')

        global bw1
        global bw2
        global dl1
        global dl2
        global bf1
        global bf2

        self.addLink(h1,s1, cls=TCLink, bw=bw1, delay=dl1, max_queue_size=bf1, loss=0, use_htb=True, use_fq=True)
        self.addLink(s1,s2, cls=TCLink, bw=bw2, delay=dl2, max_queue_size=bf2, loss=0, use_htb=True, use_fq=True)
        self.addLink(s2,h2, cls=TCLink, bw=bw1, delay=dl1, max_queue_size=bf1, loss=0, use_htb=True, use_fq=True)


def onetest(cca,buffer1,buffer2,bandwidth1,bandwidth2,latency1,latency2,cs,sc,fc,fs):


    os.system("sudo mn -c >/dev/null")

    global bw1
    global bw2
    global dl1
    global dl2
    global bf1
    global bf2

    #bandwidth unit: mb/s
    bw1=bandwidth1
    bw2=bandwidth2
    #delay unit: ms
    dl1=str(latency1)+"ms"
    dl2=str(latency2)+"ms"
    #buffer unit: packet
    bf1 = int(2*buffer2*bw2*(latency1+latency1+latency2)*1000/8/1500)
    bf2 = int(2*buffer2*bw2*(latency1+latency1+latency2)*1000/8/1500)
    print("bf1:"+str(bf1)+" bf2:"+str(bf2)+" bw1:"+str(bw1)+" bw2:"+str(bw2)+" dl1:"+str(dl1)+" dl2:"+str(dl2))
    #file.write("[MININET:] cca:"+ cca +" bf1:"+str(bf1)+" bf2:"+str(bf2)+" bw1:"+str(bw1)+" bw2:"+str(bw2)+" dl1:"+str(dl1)+" dl2:"+str(dl2)+"\n")

    print("2(dl1+dl2+dl1)=%d ms"%int(2*latency2+4*latency1))

    topo = MyTopo()
    net = Mininet(topo=topo, link=TCLink)
    net.start()
    h1 = net.get('h1')	
    h2 = net.get('h2')

    if cca == "BBR":
        h1.cmd("./set_bbr.sh")
        h2.cmd("./set_bbr.sh")
        if "bbr" not in h1.cmd("sysctl net.ipv4.tcp_congestion_control") :
            CLI(net)
        elif "bbr" not in h2.cmd("sysctl net.ipv4.tcp_congestion_control"):
            CLI(net)
    elif cca == "CUBIC":
        h1.cmd("./set_cubic.sh")
        h2.cmd("./set_cubic.sh")
        if "cubic" not in h1.cmd("sysctl net.ipv4.tcp_congestion_control") :
            CLI(net)
        elif "cubic" not in h2.cmd("sysctl net.ipv4.tcp_congestion_control"):
            CLI(net)
    

    fc.write("cca=%s, bf1=%d, bf2=%d, c2s=%d bytes, s2c=%d bytes, d1=%sms, d2=%sms, bw1=%dMbps, bw2=%dMbps\n"%(cca,bf1,bf2,cs,sc,dl1,dl2,bw1,bw2))
    fs.write("cca=%s, bf1=%d, bf2=%d, c2s=%d bytes, s2c=%d bytes, d1=%sms, d2=%sms, bw1=%dMbps, bw2=%dMbps\n"%(cca,bf1,bf2,cs,sc,dl1,dl2,bw1,bw2))
    fc.flush()
    fs.flush()                  

    CLIENT_CMD1="./client " 
    CLIENT_CMD2=" %d %d %d %d"%(PORT,COUNT,cs,sc)
    SERVER_CMD="./server %d %d %d %d > server_temp &"%(PORT,COUNT,cs,sc)
    #Server_result = h2.cmd(SERVER_CMD)
    h2.cmd(SERVER_CMD)
    #print(Server_result)
    #file.write(result)
    Client_result = h1.cmd(CLIENT_CMD1+str(h2.IP())+CLIENT_CMD2)
    #print(result)	
    #file.write(result)
    #result = h1.cmd("ping "+str(h2.IP())+" -c 20")
    #print(result)	
    #file.write(result)
    server_temp_file=open('server_temp','r')
    serverlines=server_temp_file.readlines()
    Server_result=""
    for serverline in serverlines:
        Server_result+=serverline
    print(Server_result)
    net.stop()
    return Server_result,Client_result


def main(TCPCCAs,BUFFER1,BUFFER2,BANDWIDTH1,BANDWIDTH2,LATENCY1,LATENCY2,SIZE_C2S,SIZE_S2C,client_file_name,server_file_name):
    filec = open(client_file_name,'w')
    files = open(server_file_name,'w')
    filecfull = open(client_file_name+"_full",'w')
    filesfull = open(server_file_name+"_full",'w')
    for c2s in SIZE_C2S:
        for s2c in SIZE_S2C:
            for dl1 in LATENCY1:
                for dl2 in LATENCY2:
                    for bw1 in BANDWIDTH1:
                        for bw2 in BANDWIDTH2:
                            for bf1 in BUFFER1:
                                filec.write("c2s=%d bytes, s2c=%d bytes, d1=%dms, d2=%dms, bw1=%dMbps, bw2=%dMbps\n"%(c2s,s2c,dl1,dl2,bw1,bw2))
                                files.write("c2s=%d bytes, s2c=%d bytes, d1=%dms, d2=%dms, bw1=%dMbps, bw2=%dMbps\n"%(c2s,s2c,dl1,dl2,bw1,bw2))
                                                                
                                for cca in TCPCCAs:
                                    client_upl_list=[]
                                    client_rtt_list=[]
                                    server_upl_list=[]
                                    server_rtt_list=[]
                                    for bf2 in BUFFER2:
                                        print("=====Start a Test=====")
                                        #file.write("=====Start a Test=====\n")
                                        print(cca,bf1,bf2,bw1,bw2,dl1,dl2)
                                        Server_result,Client_result=onetest(cca,bf1,bf2,bw1,bw2,dl1,dl2,c2s,s2c,filecfull,filesfull)
                                        print("=====End This Test=====")
                                        #file.write("=====End This Test=====\n\n\n\n")
                                        #file.flush()
                                        client_upl,client_rtt=get_upl_and_rtt(Client_result)
                                        server_upl,server_rtt=get_upl_and_rtt(Server_result)
                                        #
                                        client_upl_list.append(client_upl)
                                        client_rtt_list.append(client_rtt)
                                        #
                                        server_upl_list.append(server_upl)
                                        server_rtt_list.append(server_rtt)
                                        #
                                        filecfull.write(Client_result)
                                        filesfull.write(Server_result)

                                    filec.write(cca+"\n")
                                    files.write(cca+"\n")
                                    writeall(BUFFER2,filec)
                                    writeall(BUFFER2,files)
                                    #file.write(BUFFER2+"\n")
                                    writeall(client_upl_list,filec)
                                    writeall(server_upl_list,files)
                                    #file.write(upllist+"\n")
                                    writeall(client_rtt_list,filec)
                                    writeall(server_rtt_list,files)
                                    #file.write(rttlist+"\n\n\n\n")
    filec.close()
    files.close()
    filecfull.close()
    filesfull.close()

def writeall(alist,file):
    for item in alist:
        file.write(str(item)+" ")
    file.write("\n")

def get_upl_and_rtt(Client_result):
    rtt = None
    upl = None
    Client_lower = Client_result.split("[FINAL]:")[1]
    lines = Client_lower.split( )
    for oneline in lines:
        if "AverageUPL" in oneline:
            upl=oneline.split("=")[1]
        if "AverageRTT" in oneline:
            rtt=oneline.split("=")[1]
    return upl,rtt

def Figure1():
    PORT = 6666
    SIZE_C2S = [1]
    SIZE_S2C = [1000]
    COUNT = 200
    TCPCCAs=["BBR", "CUBIC"]
    BUFFER1=[1.0]
    BUFFER2=[0.25,0.5,1.0,2.0,4.0]
    BANDWIDTH1=[20]
    BANDWIDTH2=[10]
    LATENCY1=[1]
    LATENCY2=[100]
    filec = "f1c"
    files = "f1s"
    main(TCPCCAs,BUFFER1,BUFFER2,BANDWIDTH1,BANDWIDTH2,LATENCY1,LATENCY2,SIZE_C2S,SIZE_S2C,filec,files)
def Figure2():
    SIZE_C2S = [1]
    SIZE_S2C = [100000]
    TCPCCAs=["BBR", "CUBIC"]
    BUFFER1=[1.0]
    BUFFER2=[0.25,0.5,1.0,2.0,4.0]
    BANDWIDTH1=[20]
    BANDWIDTH2=[10]
    LATENCY1=[1]
    LATENCY2=[100]
    filec = "f2c"
    files = "f2s"
    main(TCPCCAs,BUFFER1,BUFFER2,BANDWIDTH1,BANDWIDTH2,LATENCY1,LATENCY2,SIZE_C2S,SIZE_S2C,filec,files)
def Figure3():
    SIZE_C2S = [1]
    SIZE_S2C = [1000]
    TCPCCAs=["BBR", "CUBIC"]
    BUFFER1=[1.0]
    BUFFER2=[0.25,0.5,1.0,2.0,4.0]
    BANDWIDTH1=[200]
    BANDWIDTH2=[100]
    LATENCY1=[1]
    LATENCY2=[100]
    filec = "f3c"
    files = "f3s"
    main(TCPCCAs,BUFFER1,BUFFER2,BANDWIDTH1,BANDWIDTH2,LATENCY1,LATENCY2,SIZE_C2S,SIZE_S2C,filec,files)
def Figure4():
    SIZE_C2S = [1]
    SIZE_S2C = [100000]
    TCPCCAs=["BBR", "CUBIC"]
    BUFFER1=[1.0]
    BUFFER2=[0.25,0.5,1.0,2.0,4.0]
    BANDWIDTH1=[200]
    BANDWIDTH2=[100]
    LATENCY1=[1]
    LATENCY2=[100]
    filec = "f4c"
    files = "f4s"
    main(TCPCCAs,BUFFER1,BUFFER2,BANDWIDTH1,BANDWIDTH2,LATENCY1,LATENCY2,SIZE_C2S,SIZE_S2C,filec,files)

def Figure5():
    SIZE_C2S = [1]
    SIZE_S2C = [1000000]
    TCPCCAs=["BBR", "CUBIC"]
    BUFFER1=[1.0]
    BUFFER2=[0.25,4.0]
    BANDWIDTH1=[100]
    BANDWIDTH2=[10]
    LATENCY1=[1]
    LATENCY2=[50]
    filec = "f5c"
    files = "f5s"
    main(TCPCCAs,BUFFER1,BUFFER2,BANDWIDTH1,BANDWIDTH2,LATENCY1,LATENCY2,SIZE_C2S,SIZE_S2C,filec,files)

def Figure6():
    SIZE_C2S = [1]
    SIZE_S2C = [1000000]
    TCPCCAs=["BBR", "CUBIC"]
    BUFFER1=[1.0]
    BUFFER2=[0.25,4.0]
    BANDWIDTH1=[100]
    BANDWIDTH2=[10]
    LATENCY1=[1]
    LATENCY2=[50]
    filec = "f6c"
    files = "f6s"
    main(TCPCCAs,BUFFER1,BUFFER2,BANDWIDTH1,BANDWIDTH2,LATENCY1,LATENCY2,SIZE_C2S,SIZE_S2C,filec,files)


def Figure10():
    SIZE_C2S = [1]
    SIZE_S2C = [1000000]
    TCPCCAs=["BBR", "CUBIC"]
    BUFFER1=[1.0]
    BUFFER2=[0.25,0.5,1.0,2.0,4.0]
    BANDWIDTH1=[100]
    BANDWIDTH2=[10]
    LATENCY1=[1]
    LATENCY2=[50]
    filec = "f10c"
    files = "f10s"
    main(TCPCCAs,BUFFER1,BUFFER2,BANDWIDTH1,BANDWIDTH2,LATENCY1,LATENCY2,SIZE_C2S,SIZE_S2C,filec,files)

def Figure11():
    SIZE_C2S = [1]
    SIZE_S2C = [1000000]
    TCPCCAs=["BBR", "CUBIC"]
    BUFFER1=[1.0]
    BUFFER2=[0.25,0.5,1.0,2.0,4.0]
    BANDWIDTH1=[100]
    BANDWIDTH2=[10]
    LATENCY1=[1]
    LATENCY2=[50]
    filec = "f11c"
    files = "f11s"
    main(TCPCCAs,BUFFER1,BUFFER2,BANDWIDTH1,BANDWIDTH2,LATENCY1,LATENCY2,SIZE_C2S,SIZE_S2C,filec,files)
if __name__ == '__main__':
    #Figure1()
    #Figure2()
    #Figure3()
    #Figure4()
    Figure10()
    Figure11()
