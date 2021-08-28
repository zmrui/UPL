from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import TCLink

PORT = 6666
SIZE_C2S = 512
SIZE_S2C = 512
COUNT = 1
CLIENT_CMD1="./client " 
CLIENT_CMD2=" %d %d %d %d"%(PORT,COUNT,SIZE_C2S,SIZE_S2C)
SERVER_CMD="./server %d %d %d &"%(PORT,SIZE_C2S,SIZE_S2C)
#Matrix full
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
TCPCCAs=["BBR", "CUBIC"]
BUFFER1=[1.0, 0.8, 0.5]
BUFFER2=[1.0, 0.8, 0.5]
BANDWIDTH1=[1,10]
BANDWIDTH2=[1,10]
LATENCY1=[1,10]
LATENCY2=[100,200]

class MyTopo( Topo,  cca,buffer1,buffer2,bandwidth1,bandwidth2,latency1,latency2):
    def build( self, cca,buffer1,buffer2,bandwidth1,bandwidth2,latency1,latency2):
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        h1 = self.addHost('h1')
        h2 = self.addHost('h2')


        bw1 = bandwidth1
        bw2 = bandwidth2
        dl1 = str(latency1)+"ms"
        dl2 = str(latency2)+"ms"
        bf1 = int(buffer1*bw1*dl1*2)
        bf2 = int(buffer2*bw2*dl2*2)

        self.addLink(h1,s1, bw=bw1, delay=dl1, max_queue_size=bf1, loss=0, use_htb=True)
        self.addLink(s1,s2, bw=bw2, delay=dl2, max_queue_size=bf2, loss=0, use_htb=True)
        self.addLink(s2,h2, bw=bw1, delay=dl1, max_queue_size=bf1, loss=0, use_htb=True)


def onetest(cca,buffer1,buffer2,bandwidth1,bandwidth2,latency1,latency2):
    topo = MyTopo(cca,buffer1,buffer2,bandwidth1,bandwidth2,latency1,latency2)
    net = Mininet(topo=topo, link=TCLink)
    net.start()
    h1 = net.get('h1')	
    h2 = net.get('h2')
    print(h2.IP())
    result = h2.cmd(SERVER_CMD)
    print(result)
    result = h1.cmd(CLIENT_CMD1+str(h2.IP())+CLIENT_CMD2)
    print(result)	
    net.stop()


def main():
    for cca in TCPCCAs:
        for bf1 in BUFFER1:
            for bf2 in BUFFER2:
                for bw1 in BANDWIDTH1:
                    for bw2 in BANDWIDTH2:
                        for dl1 in LATENCY1:
                            for dl2 in LATENCY2:
                                onetest(cca,bf1,bf2,bw1,bw2,dl1,dl2)

if __name__ == '__main__':
    main()