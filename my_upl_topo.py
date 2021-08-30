"""Custom topology example

Two directly connected switches plus a host for each switch:

   host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

from mininet.topo import Topo

class MyTopo( Topo ):
    "Simple topology example."

    def build( self ):
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        '''
        self.addLink(h1,s1,bw=100, delay='500ms', loss=0, use_htb=True)
        self.addLink(s1,s2,bw=10, delay='1000ms', loss=0, use_htb=True)
        self.addLink(s2,h2,bw=100, delay='500ms', loss=0, use_htb=True)
	    '''
        self.addLink(h1,s1, bw=10, delay='1ms', max_queue_size=20000, loss=0, use_htb=True, use_fq=True)
        self.addLink(s1,s2, bw=100, delay='100ms', max_queue_size=20000000, loss=0, use_htb=True, use_fq=True)
        self.addLink(s2,h2, bw=10, delay='1ms', max_queue_size=20000, loss=0, use_htb=True, use_fq=True)


topos = { 'mytopo': ( lambda: MyTopo() ) }
