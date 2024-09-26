#include <iostream>
#include <cstring>
#include <chrono>
#include <thread>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>

const char* HOST = "127.0.0.1";
const int PORT = 65432;
const int TIMEOUT = 2;
const char* MESSAGE = "some message";

int main() {
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) {
        std::cerr << "Failed to create socket\n";
        return 1;
    }

    sockaddr_in server_addr;
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);
    
    if (inet_pton(AF_INET, HOST, &server_addr.sin_addr) <= 0) {
        std::cerr << "Invalid address/Address not supported\n";
        return 1;
    }

    if (connect(sock, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        std::cerr << "Connection failed\n";
        return 1;
    }

    auto now = std::chrono::system_clock::now();
    
    send(sock, MESSAGE, strlen(MESSAGE), 0);
    
    char buffer[2048] = {0};
    int valread = read(sock, buffer, 2048);
    
    std::this_thread::sleep_for(std::chrono::seconds(TIMEOUT));
    
    std::cout << "Received message = " << buffer << std::endl;

    close(sock);
    return 0;
}
