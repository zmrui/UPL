//UPL Simple Socket Server
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>  //struct used in socket
#include <netinet/in.h> //Linux IPv4 protocol implementation
#include <arpa/inet.h>  //convert IP address from text to binary
#include <netinet/tcp.h>
#include <sys/time.h>

int main(int argc, char** argv)
{
    //printf("[SERVER]: Server Started.\n");
    int PORT;
    int SIZEc2s, SIZEs2c,COUNT;
    struct timeval StartTime, EndTime;
    struct timeval BeginTime, FinishTime;    

    struct tcp_info TCPInfo;
    socklen_t tcp_info_length = sizeof(TCPInfo);
    int ret;


    unsigned int RTTSum = 0;
    unsigned int RTT = 0;
    unsigned int RTTVAR = 0;
    long UPLSum = 0;
    long UPL = 0;


    if (argc != 5){
        printf("server [PORT] [COUNT] [SIZEc2s] [SIZEs2c]\nExample: ./server 80 5 1024 2048\n");
        return 0;
    }
    else{
        PORT = atoi(argv[1]);
        COUNT = atoi(argv[2]);
        SIZEc2s = atoi(argv[3]);
        SIZEs2c = atoi(argv[4]);
        //printf("[SERVER]: Parameters: Port:%d c2s:%d s2c:%d\n",PORT,SIZEc2s,SIZEs2c);
    }

    struct sockaddr_in SERVER, CLIENT;
    memset(&SERVER, 0, sizeof(SERVER));
    SERVER.sin_addr.s_addr = INADDR_ANY;
    SERVER.sin_port = PORT;
    SERVER.sin_family = AF_INET;

    char WBuffer[102400], RBuffer[102400]; memset(WBuffer,2,sizeof(WBuffer));
    //printf("[SERVER]: Server Initialized.\n");
    int ListenSocket, ResponseSocket;
    socklen_t CLIENT_LEN;
    ListenSocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if(bind(ListenSocket, (struct sockaddr*) &SERVER, sizeof(SERVER))<0){
        printf("[SERVER]: bind failed.\n");
        exit(1);
    }
//    printf("[SERVER]: Bind Succed.\n");

    listen(ListenSocket,5);
    CLIENT_LEN = sizeof(CLIENT);
    ResponseSocket=accept(ListenSocket, (struct sockaddr*) &CLIENT, &CLIENT_LEN);
    if(ResponseSocket>0){
        //printf("[SERVER]: Socket to client established.\n");
        ;
    }
    else{
        printf("[SERVER]: Failed to establish socket to client.\n");
        exit(1);
    }

    gettimeofday(&BeginTime, NULL);
    gettimeofday(&StartTime, NULL);
    int cnt = 0;
    for(cnt=0;cnt<COUNT;cnt++){
        int c2s=0, flag=0;
        gettimeofday(&StartTime, NULL);
        while(c2s<SIZEc2s){
            c2s+=read (ResponseSocket, RBuffer, SIZEc2s);
            //if(flag==0){gettimeofday(&StartTime, NULL);flag+=1;}
        }
        

        write(ResponseSocket, WBuffer, SIZEs2c);

        gettimeofday(&EndTime, NULL);

        

        getsockopt(ResponseSocket, SOL_TCP, TCP_INFO, &TCPInfo, &tcp_info_length);
        
        if(cnt>=100){
            RTT = TCPInfo.tcpi_rtt;
            RTTVAR = TCPInfo.tcpi_rttvar;

            RTTSum += RTT;
            
            UPL = 1000000*(EndTime.tv_sec-StartTime.tv_sec)+(EndTime.tv_usec-StartTime.tv_usec);
            UPLSum += UPL;

            printf("%d %lf %lf %u\n", cnt+1, UPL/1000.0, RTT/1000.0, RTTVAR);
        }

    }

    gettimeofday(&FinishTime, NULL);

    close(ResponseSocket);
    close(ListenSocket);

    double throughput;
    throughput = COUNT*SIZEs2c/((FinishTime.tv_sec-BeginTime.tv_sec)+(FinishTime.tv_usec-BeginTime.tv_usec)/1000000.0);

    printf("[FINAL]:\nServer Throughput=%lf Byte/s\n",throughput);
    
    double av_RTT, av_UPL;
    av_RTT = RTTSum/(COUNT-100)/1000.0;
    av_UPL = UPLSum/(COUNT-100)/1000.0;

    unsigned char tcpi_retransmits;
    unsigned int tcpi_rto,tcpi_lost,tcpi_retrans,tcpi_snd_cwnd,tcpi_snd_ssthresh,tcpi_total_retrans;

    tcpi_retransmits = TCPInfo.tcpi_retransmits;
    tcpi_rto = TCPInfo.tcpi_rto;
    tcpi_lost = TCPInfo.tcpi_lost;
    tcpi_retrans = TCPInfo.tcpi_retrans;
    tcpi_snd_cwnd = TCPInfo.tcpi_snd_cwnd;
    tcpi_snd_ssthresh = TCPInfo.tcpi_snd_ssthresh;
    tcpi_total_retrans = TCPInfo.tcpi_total_retrans;


    
    printf("AverageUPL=%lf\n\
    AverageRTT=%lf\n\
    tcpi_retransmits=%d\n\
    tcpi_rto=%u\n\
    tcpi_lost=%u\n\
    tcpi_retrans=%u\n\
    tcpi_snd_cwnd=%u\n\
    tcpi_snd_ssthresh=%u\n\
    tcpi_total_retrans=%u\n",
    av_UPL,
    av_RTT,
    tcpi_retransmits,
    tcpi_rto,
    tcpi_lost,
    tcpi_retrans,
    tcpi_snd_cwnd,
    tcpi_snd_ssthresh,
    tcpi_total_retrans);


    return 0;
}
