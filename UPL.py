from mininet.topo import Topo
from mininet.net import Mininet

SERVER_NAME="h2"
PORT = 6666
SIZE_C2S = 128
SIZE_S2C = 512
COUNT = 100

CLIENT_CMD="./client %s %d %d %d %d > log"%(SERVER_NAME,PORT,COUNT,SIZE_C2S,SIZE_S2C)
SERVER_CMD="./server %d %d %d & > log "%(PORT,SIZE_C2S,SIZE_S2C)

class MyTopo( Topo ):
    def build( self ):
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        h1 = self.addHost('h1')
        h2 = self.addHost('h2')

        #h1----1000mbps, 1ms------(S1)----100mbps,10ms-----(S2)-----1000mbps,1ms------h2
        self.addLink(h1,s1,
                    bw=1000, delay='1ms', loss=0, use_htb=True)
        self.addLink(s1,s2,
                    bw=100, delay='100ms', loss=0, use_htb=True)
        self.addLink(s2,h2,
                    bw=1000, delay='1ms', loss=0, use_htb=True)

def main():
    topo = MyTopo()
    net = Mininet(topo=topo)
    net.start()
    h1 = net.get('h1')	
    h2 = net.get('h2')
    h2.cmdPrint(SERVER_CMD)
    h1.cmdPrint(CLIENT_CMD)	
    net.stop()

if __name__ == '__main__':
    main()