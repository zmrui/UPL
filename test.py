text='''
1111[CLIENT_FINAL]:Client Throughput=[34.336002] Byte/s\r\nAverageUPL=[26.489000]\r\n    AverageRTT=[26.998000]\r\n    tcpi_retransmits=[0]\r\n    tcpi_rto=[224000]\r\n    tcpi_lost=[0]\r\n    tcpi_retrans=[0]\r\n    tcpi_snd_cwnd=[18]\r\n    tcpi_snd_ssthresh=[2147483647]\r\n    tcpi_total_retrans=[0]\r\n
'''

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

upl,rtt=get_upl_and_rtt(text)
print(upl,rtt)