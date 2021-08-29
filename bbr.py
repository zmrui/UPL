import os
os.system("sed -i '/net\.core\.default_qdisc/d' /etc/sysctl.conf")
os.system("sed -i '/net\.ipv4\.tcp_congestion_control/d' /etc/sysctl.conf")
os.system("echo 'net.core.default_qdisc=fq' >> /etc/sysctl.conf")
os.system("echo 'net.ipv4.tcp_congestion_control=bbr' >> /etc/sysctl.conf")
os.system("sysctl -p")