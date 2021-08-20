//UPL Simple Socket Client
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>  //struct used in socket
#include <netinet/in.h> //Linux IPv4 protocol implementation
#include <arpa/inet.h>  //convert IP address from text to binary
#include <time.h>

FILE fp;
int save_one_log(int cnt, clock_t UPL){

}
/*
int MySend(int fd, int Bytes){
    if(Bytes>0){
    char WBuffer1 = "11111111";
    char WBuffer2 = "cltend==";
    int cnt;
    for (cnt=0;cnt<Bytes-1;cnt++){
        write(fd,WBuffer1,strlen(WBuffer1));
    }
    write(fd,WBuffer2,strlen(WBuffer1));
    }
}

int MyReceive(int fd){
    char RBuffer [1024];
    memset(RBuffer,0,sizeof(RBuffer));
    while(read())

}*/

int main(int argc, char** argv)
{
    char* IPADDR = malloc(sizeof(char)*128);
    int PORT;
    int COUNT;
    int SIZE;
    clock_t StartClock, EndClock, UPLTime;
    if (argc != 5 || strlen(argv[1]>30) ){
        printf("client [IP ADDRESS] [PORT] [COUNT] [SIZE]\nExample: ./client 10.10.10.1 80 2 1024\n");
        return 0;
    }
    else{
        strcpy(IPADDR,argv[1]);
        PORT = atoi(argv[2]);
        COUNT = atoi(argv[3]);
        SIZE = atoi(argv[4]);
    }

    struct sockaddr_in SERVER;
    memset(&SERVER, 0, sizeof(SERVER));
    //TODO
    SERVER.sin_addr.s_addr = IPADDR;
    //TODO
    SERVER.sin_port = PORT;
    SERVER.sin_family = AF_INET;

    char WBuffer[8], RBuffer[1024]; memset(WBuffer, 1, sizeof(WBuffer));
    int MySocket;
    int cnt = 0;
    for( cnt = 0; cnt < COUNT; cnt++){

        StartClock = clock();

        MySocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
        if(connect(MySocket,(struct sockaddr*) &SERVER, sizeof(SERVER))<0){
            printf("Connect failed.\n");
            exit(1);
        }

        int i;
        for (i=0;i<SIZE;i++){
            write(MySocket,WBuffer,strlen(WBuffer));
        }

        while(read(MySocket,RBuffer,1000)==0){
            ;
        }


//TODO
        EndClock = clock();
        UPLTime = EndClock - StartClock;
        printf("UPL is %d\n",UPLTime);
    }
    return 0;
}
