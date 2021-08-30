from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import TCLink
import os

PORT = 6666
SIZE_C2S = 512
SIZE_S2C = 1024
COUNT = 10
CLIENT_CMD1="./client " 
CLIENT_CMD2=" %d %d %d %d"%(PORT,COUNT,SIZE_C2S,SIZE_S2C)
SERVER_CMD="./server %d %d %d &"%(PORT,SIZE_C2S,SIZE_S2C)
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
#Matrix test
#SIZE_C2S=[128,512,1024,2048,4096,8192]
#SIZE_S2C=[128,512,1024,2048,4096,8182]
TCPCCAs=["BBR", "CUBIC"]
BUFFER1=[1.0, 0.8, 0.5]
BUFFER2=[1.0, 0.8, 0.5]
BANDWIDTH1=[10,100]
BANDWIDTH2=[10,100]
LATENCY1=[1,10]
LATENCY2=[100,200]


bw1 = None
bw2 = None
dl1 = None
dl2 = None
bf1 = None
bf2 = None

file = open('UPLlog','w')

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
        print("bf1:"+str(bf1)+" bf2:"+str(bf2)+" bw1:"+str(bw1)+" bw2:"+str(bw2)+" dl1:"+str(dl1)+" dl2:"+str(dl2))
        file.write("[MININET:] bf1:"+str(bf1)+" bf2:"+str(bf2)+" bw1:"+str(bw1)+" bw2:"+str(bw2)+" dl1:"+str(dl1)+" dl2:"+str(dl2)+"\n")
        self.addLink(h1,s1, cls=TCLink, bw=bw1, delay=dl1, max_queue_size=bf1, loss=0, use_htb=True, use_fq=True)
        self.addLink(s1,s2, cls=TCLink, bw=bw2, delay=dl2, max_queue_size=bf2, loss=0, use_htb=True, use_fq=True)
        self.addLink(s2,h2, cls=TCLink, bw=bw1, delay=dl1, max_queue_size=bf1, loss=0, use_htb=True, use_fq=True)


def onetest(cca,buffer1,buffer2,bandwidth1,bandwidth2,latency1,latency2):

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


    topo = MyTopo()
    net = Mininet(topo=topo, link=TCLink)
    net.start()
    h1 = net.get('h1')	
    h2 = net.get('h2')
    result = h2.cmd(SERVER_CMD)
    print(result)
    file.write(result)
    result = h1.cmd(CLIENT_CMD1+str(h2.IP())+CLIENT_CMD2)
    print(result)	
    file.write(result)
    net.stop()


def main():
    print("=====Start a Test=====")
    file.write("=====Start a Test=====\n")
    onetest("BBR",1,1,10,100,10,100)
    print("=====End This Test=====")
    file.write("=====End This Test=====\n\n\n\n")
    file.flush()

if __name__ == '__main__':
    main()