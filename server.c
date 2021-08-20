//UPL Simple Socket Server
//UPL Simple Socket Client
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>  //struct used in socket
#include <netinet/in.h> //Linux IPv4 protocol implementation
#include <arpa/inet.h>  //convert IP address from text to binary


FILE fp;
int save_one_log(int cnt, clock_t UPL){

}

int main(int argc, char** argv)
{
    int PORT;
    int SIZE;
    if (argc != 3 || strlen(argv[1]>30) ){
        printf("server [PORT] [SIZE]\nExample: ./server 80 1024\n");
        return 0;
    }
    else{
        PORT = atoi(argv[1]);
        SIZE = atoi(argv[2]);
    }

    struct sockaddr_in SERVER, CLIENT;
    memset(&SERVER, 0, sizeof(SERVER));
    SERVER.sin_addr.s_addr = INADDR_ANY;
    SERVER.sin_port = PORT;
    SERVER.sin_family = AF_INET;

    char WBuffer[8], RBuffer[1024]; memset(WBuffer, 1, sizeof(WBuffer));
    int ListenSocket, ResponseSocket;
    socklen_t CLIENT_LEN;
    int cnt = 0;
    while(1){
        ListenSocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
        if(bind(ListenSocket, (struct sockaddr*) &SERVER, sizeof(SERVER))<0){
            printf("bind failed.\n");
            exit(1);
        }

        listen(ListenSocket,5);
        CLIENT_LEN = sizeof(CLIENT);
        ResponseSocket=accept(ListenSocket, (struct sockaddr*) &CLIENT, &CLIENT_LEN);


        while(read(ResponseSocket,RBuffer,1000)==0){
            ;
        }
        int i;
        for (i=0;i<SIZE;i++){
            write(ResponseSocket, WBuffer, strlen(WBuffer));
        }

        close(ListenSocket);
        close(ResponseSocket);
    }
    return 0;
}
