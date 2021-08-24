//UPL Simple Socket Server
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>  //struct used in socket
#include <netinet/in.h> //Linux IPv4 protocol implementation
#include <arpa/inet.h>  //convert IP address from text to binary

int main(int argc, char** argv)
{
    printf("[SERVER]: Server Started.\n");
    int PORT;
    int SIZEc2s, SIZEs2c;
    if (argc != 4){
        printf("server [PORT] [SIZEc2s] [SIZEs2c]\nExample: ./server 80 1024 2048\n");
        return 0;
    }
    else{
        PORT = atoi(argv[1]);
        SIZEc2s = atoi(argv[2]);
        SIZEs2c = atoi(argv[3]);
        printf("[SERVER]: Parameters: Port:%d c2s:%d s2c:%d\n",PORT,SIZEc2s,SIZEs2c);
    }

    struct sockaddr_in SERVER, CLIENT;
    memset(&SERVER, 0, sizeof(SERVER));
    SERVER.sin_addr.s_addr = INADDR_ANY;
    SERVER.sin_port = PORT;
    SERVER.sin_family = AF_INET;

    char WBuffer[102400], RBuffer[102400]; memset(WBuffer,1,sizeof(WBuffer));
    printf("[SERVER]: Server Initialized.\n");
    int ListenSocket, ResponseSocket;
    socklen_t CLIENT_LEN;
    ListenSocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if(bind(ListenSocket, (struct sockaddr*) &SERVER, sizeof(SERVER))<0){
        printf("[SERVER]: bind failed.\n");
        exit(1);
    }
    printf("[SERVER]: Bind Succed.\n");

    listen(ListenSocket,5);
    CLIENT_LEN = sizeof(CLIENT);
    ResponseSocket=accept(ListenSocket, (struct sockaddr*) &CLIENT, &CLIENT_LEN);
    if(ResponseSocket>0){
        printf("[SERVER]: Socket to client established.\n");
    }
    else{
        printf("[SERVER]: Failed to establish socket to client.\n");
        exit(1);
    }


    int cnt = 0;
    while(1){
        read (ResponseSocket, RBuffer, SIZEc2s);
        write(ResponseSocket, WBuffer, SIZEs2c);
    }
    return 0;
}
