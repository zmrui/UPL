#! /bin/bash

sed -i '/net\.core\.default_qdisc/d' /etc/sysctl.conf
sed -i '/net\.ipv4\.tcp_congestion_control/d' /etc/sysctl.conf
echo 'net.core.default_qdisc=fq' >> /etc/sysctl.conf
echo 'net.ipv4.tcp_congestion_control=cubic' >> /etc/sysctl.conf
sysctl -p
