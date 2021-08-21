//UPL Simple Socket Client
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>  //struct used in socket
#include <netinet/in.h> //Linux IPv4 protocol implementation
#include <arpa/inet.h>  //convert IP address from text to binary
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
    if (argc != 6 ){
        printf("client [IP ADDRESS] [PORT] [COUNT] [SIZEc2s] [SIZEs2c] \nExample: ./client 10.10.10.1 80 2 1024 2048\n");
        return 0;
    }
    else{
        strcpy(IPADDR,argv[1]);
        PORT = atoi(argv[2]);
        COUNT = atoi(argv[3]);
        SIZEc2s = atoi(argv[4]);
        SIZEs2c = atoi(argv[5]);
    }

    struct sockaddr_in SERVER;
    memset(&SERVER, 0, sizeof(SERVER));
    inet_pton(AF_INET, IPADDR, SERVER.sin_addr.s_addr);
    SERVER.sin_port = PORT;
    SERVER.sin_family = AF_INET;

    char WBuffer[102400], RBuffer[102400];

    int MySocket;
    MySocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if(connect(MySocket,(struct sockaddr*) &SERVER, sizeof(SERVER))<0){
        printf("[CLIENT]: Connect failed.\n");
        exit(1);
    }

    int cnt = 0;
    for(cnt = 0; cnt < COUNT; cnt++){
        gettimeofday(&StartTime, NULL);

        write(MySocket,WBuffer,SIZEc2s);

        read (MySocket,RBuffer,SIZEs2c);

        gettimeofday(&EndTime, NULL);
        
        printf("[CLIENT]: Client's [No.%d] UPL Time is [%ld Second, %ld Microsecond].\n", 
                                    cnt+1, (EndTime.tv_sec-StartTime.tv_sec), (EndTime.tv_usec-StartTime.tv_usec));
    }
    return 0;
}
