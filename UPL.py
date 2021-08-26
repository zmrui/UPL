from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
import time

PORT = 6666
SIZE_C2S = 512
SIZE_S2C = 512
COUNT = 1

CLIENT_CMD1="./client " 
CLIENT_CMD2=" %d %d %d %d"%(PORT,COUNT,SIZE_C2S,SIZE_S2C)
SERVER_CMD="./server %d %d %d &"%(PORT,SIZE_C2S,SIZE_S2C)

class MyTopo( Topo ):
    def build( self ):
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        h1 = self.addHost('h1')
        h2 = self.addHost('h2')

        #h1----200mbps, 1ms------(S1)----20mbps,10ms-----(S2)-----200mbps,1ms------h2
        self.addLink(h1,s1,
                    bw=200, delay='1ms', loss=0, use_htb=True)
        self.addLink(s1,s2,
                    bw=20, delay='100ms', loss=0, use_htb=True)
        self.addLink(s2,h2,
                    bw=200, delay='1ms', loss=0, use_htb=True)

def main():
    topo = MyTopo()
    net = Mininet(topo=topo)
    net.start()
    time.sleep(1)
    h1 = net.get('h1')	
    h2 = net.get('h2')
    print(h2.IP())
    result = h2.cmd(SERVER_CMD)
    print(result)
    result = h1.cmd(CLIENT_CMD1+str(h2.IP())+CLIENT_CMD2)
    print(result)	
    net.stop()

if __name__ == '__main__':
    main()