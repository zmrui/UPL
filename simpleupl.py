from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import TCLink
import os

PORT = 6666
SIZE_C2S = 2048
SIZE_S2C = 2048
COUNT = 10
CLIENT_CMD1="./client " 
CLIENT_CMD2=" %d %d %d %d"%(PORT,COUNT,SIZE_C2S,SIZE_S2C)
SERVER_CMD="./server %d %d %d %d &"%(PORT,COUNT,SIZE_C2S,SIZE_S2C)


class MyTopo( Topo ): 

    def build( self ):
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        h1 = self.addHost('h1')
        h2 = self.addHost('h2')

        self.addLink(h1,s1, bw=10, delay='10ms', max_queue_size=8, loss=0, use_htb=True, use_fq=True)
        self.addLink(s1,s2, bw=100, delay='100ms', max_queue_size=856, loss=0, use_htb=True, use_fq=True)
        self.addLink(s2,h2, bw=10, delay='10ms', max_queue_size=8, loss=0, use_htb=True, use_fq=True)


def onetest():
    topo = MyTopo()
    net = Mininet(topo=topo, link=TCLink)
    net.start()
    h1 = net.get('h1')	
    h2 = net.get('h2')
    result = h2.cmd(SERVER_CMD)
    print(result)
    result = h1.cmd(CLIENT_CMD1+str(h2.IP())+CLIENT_CMD2)
    print(result)	
    net.stop()


def main():
    onetest()


if __name__ == '__main__':
    main()