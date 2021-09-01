from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import TCLink
import os
import matplotlib.pyplot as plt


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

#file = open('UPLlog','w')

def setBBR():
    os.system("sed -i '/net\.core\.default_qdisc/d' /etc/sysctl.conf")
    os.system("sed -i '/net\.ipv4\.tcp_congestion_control/d' /etc/sysctl.conf")
    os.system("echo 'net.core.default_qdisc=fq' >> /etc/sysctl.conf")
    os.system("echo 'net.ipv4.tcp_congestion_control=bbr' >> /etc/sysctl.conf")
    os.system("sysctl -p")

def setCUBIC():
    os.system("sed -i '/net\.core\.default_qdisc/d' /etc/sysctl.conf")
    os.system("sed -i '/net\.ipv4\.tcp_congestion_control/d' /etc/sysctl.conf")
    os.system("echo 'net.core.default_qdisc=fq' >> /etc/sysctl.conf")
    os.system("echo 'net.ipv4.tcp_congestion_control=cubic' >> /etc/sysctl.conf")
    os.system("sysctl -p")
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


def onetest(cca,buffer1,buffer2,bandwidth1,bandwidth2,latency1,latency2,cs,sc):

    os.system("sudo mn -c >/dev/null")
    if cca == "BBR":
        setBBR()
    elif cca == "CUBIC":
        setCUBIC()
    
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
    bf1 = int(2*buffer1*bw1*latency1*1000/8/1460)
    bf2 = int(2*buffer2*bw2*latency2*1000/8/1460)
    print("bf1:"+str(bf1)+" bf2:"+str(bf2)+" bw1:"+str(bw1)+" bw2:"+str(bw2)+" dl1:"+str(dl1)+" dl2:"+str(dl2))
    #file.write("[MININET:] cca:"+ cca +" bf1:"+str(bf1)+" bf2:"+str(bf2)+" bw1:"+str(bw1)+" bw2:"+str(bw2)+" dl1:"+str(dl1)+" dl2:"+str(dl2)+"\n")

    print("2(dl1+dl2+dl1)=%d ms"%int(2*latency2+4*latency1))

    topo = MyTopo()
    net = Mininet(topo=topo, link=TCLink)
    net.start()
    h1 = net.get('h1')	
    h2 = net.get('h2')
    CLIENT_CMD1="./client " 
    CLIENT_CMD2=" %d %d %d %d"%(PORT,COUNT,cs,sc)
    SERVER_CMD="./server %d %d %d %d &"%(PORT,COUNT,cs,sc)
    Server_result = h2.cmd(SERVER_CMD)
    print(Server_result)
    #file.write(result)
    Client_result = h1.cmd(CLIENT_CMD1+str(h2.IP())+CLIENT_CMD2)
    #print(result)	
    #file.write(result)
    #result = h1.cmd("ping "+str(h2.IP())+" -c 20")
    #print(result)	
    #file.write(result)
    net.stop()
    return Server_result,Client_result


def main(TCPCCAs,BUFFER1,BUFFER2,BANDWIDTH1,BANDWIDTH2,LATENCY1,LATENCY2,SIZE_C2S,SIZE_S2C):
    for c2s in SIZE_C2S:
        for s2c in SIZE_S2C:
            for bf1 in BUFFER1:
                for dl1 in LATENCY1:
                    for dl2 in LATENCY2:
                        for bw1 in BANDWIDTH1:
                            for bw2 in BANDWIDTH2:
                                for cca in TCPCCAs:
                                    upllist=[]
                                    rttlist=[]
                                    for bf2 in BUFFER2:
                                        print("=====Start a Test=====")
                                        #file.write("=====Start a Test=====\n")
                                        print(cca,bf1,bf2,bw1,bw2,dl1,dl2)
                                        Server_result,Client_result=onetest(cca,bf1,bf2,bw1,bw2,dl1,dl2,c2s,s2c)
                                        print("=====End This Test=====")
                                        #file.write("=====End This Test=====\n\n\n\n")
                                        #file.flush()
                                        upl,rtt=get_upl_and_rtt(Client_result)
                                        upllist.append(upl)
                                        rttlist.append(rtt)
                                    plt.plot(BUFFER2,upllist,label="UPL")
                                    plt.plot(BUFFER2,rttlist,label="RTT")
                                    plt.savefig("./"+cca+".jpg")
                                    plt.show()


def get_upl_and_rtt(Client_result):
    rtt = None
    upl = None
    Client_lower = Client_result.split("[CLIENT_FINAL]:")[1]
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
    main(TCPCCAs,BUFFER1,BUFFER2,BANDWIDTH1,BANDWIDTH2,LATENCY1,LATENCY2,SIZE_C2S,SIZE_S2C)
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
    main(TCPCCAs,BUFFER1,BUFFER2,BANDWIDTH1,BANDWIDTH2,LATENCY1,LATENCY2,SIZE_C2S,SIZE_S2C)
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
    main(TCPCCAs,BUFFER1,BUFFER2,BANDWIDTH1,BANDWIDTH2,LATENCY1,LATENCY2,SIZE_C2S,SIZE_S2C)
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
    main(TCPCCAs,BUFFER1,BUFFER2,BANDWIDTH1,BANDWIDTH2,LATENCY1,LATENCY2,SIZE_C2S,SIZE_S2C)
if __name__ == '__main__':
    Figure1()