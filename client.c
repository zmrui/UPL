//UPL Simple Socket Client
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>  //struct used in socket
#include <netinet/in.h> //Linux IPv4 protocol implementation
#include <arpa/inet.h>  //convert IP address from text to binary
#include <netinet/tcp.h> //TCP
#include <sys/time.h>

FILE fp;
int save_one_log(int cnt, clock_t UPL){

}

int main(int argc, char** argv)
{
    char* IPADDR = malloc(sizeof(char)*128);
    int PORT;
    int COUNT;
    int SIZEc2s, SIZEs2c;
    struct timeval StartTime, EndTime;
    struct timeval BeginTime, FinishTime;
    if (argc != 6 ){
        printf("client [IP ADDRESS] [PORT] [COUNT] [SIZEc2s] [SIZEs2c] \nCOUNT>200\nExample: ./client 10.10.10.1 80 2 1024 2048\n");
        return 0;
    }
    else{
        strcpy(IPADDR,argv[1]);
        PORT = atoi(argv[2]);
        COUNT = atoi(argv[3]);
        SIZEc2s = atoi(argv[4]);
        SIZEs2c = atoi(argv[5]);
        //printf("[CLIENT]: Parameters: IP:%s Port:%d COUNT:%d c2s:%d s2c:%d\n",IPADDR, PORT, COUNT, SIZEc2s, SIZEs2c);
    }

    struct sockaddr_in SERVER;
    memset(&SERVER, 0, sizeof(SERVER));
    inet_pton(AF_INET, IPADDR, &SERVER.sin_addr.s_addr);
    SERVER.sin_port = PORT;
    SERVER.sin_family = AF_INET;
    
    char WBuffer[102400], RBuffer[102400]; memset(WBuffer,1,sizeof(WBuffer));


    int MySocket;
    MySocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if(connect(MySocket,(struct sockaddr*) &SERVER, sizeof(SERVER))<0){
        printf("[CLIENT]: %d Connect failed.\n",connect(MySocket,(struct sockaddr*) &SERVER, sizeof(SERVER)));
        exit(1);
    }
    //printf("[CLIENT]: Connected.\n");


    struct tcp_info TCPInfo;
    socklen_t tcp_info_length = sizeof(TCPInfo);
    int ret;
    
    unsigned int RTTSum = 0;
    unsigned int RTT = 0;
    unsigned int RTTVAR = 0;
    long UPLSum = 0;
    long UPL = 0;

    int cnt = 0;
    gettimeofday(&BeginTime, NULL);
    for(cnt = 0; cnt < COUNT; cnt++){
        gettimeofday(&StartTime, NULL);

        write(MySocket,WBuffer,SIZEc2s);

        int s2c=0;
        while(s2c<SIZEs2c){
            s2c += read (MySocket,RBuffer,SIZEs2c);
        }
        gettimeofday(&EndTime, NULL);

        getsockopt(MySocket, SOL_TCP, TCP_INFO, &TCPInfo, &tcp_info_length);
        
        if(cnt>=100){
            RTT = TCPInfo.tcpi_rtt;
            RTTVAR = TCPInfo.tcpi_rttvar;

            RTTSum += RTT;
            
            UPL = 1000000*(EndTime.tv_sec-StartTime.tv_sec)+(EndTime.tv_usec-StartTime.tv_usec);
            UPLSum += UPL;

            printf("%d %lf %lf %u\n", cnt+1, UPL/1000.0, RTT/1000.0, RTTVAR);
//          printf("[CLIENT]:[%d]UPL:[%lf ms]RTT:[%lf ms]RTTVAR:[%u]\n", cnt+1, UPL/1000.0, RTT/1000.0, RTTVAR);
        }
    }

    gettimeofday(&FinishTime, NULL);

    close(MySocket);

    double av_RTT, av_UPL;
    av_RTT = RTTSum/(COUNT-100)/1000.0;
    av_UPL = UPLSum/(COUNT-100)/1000.0;

    double throughput;
    throughput = COUNT*SIZEc2s/((FinishTime.tv_sec-BeginTime.tv_sec)+(FinishTime.tv_usec-BeginTime.tv_usec)/1000000.0);

    printf("[CLIENT_FINAL]:\nClient Throughput=[%lf] Byte/s\n",throughput);

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
    tcpi_snd_ssthresh[%u\n\
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
