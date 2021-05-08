// Client side C/C++ program to demonstrate Socket programming
#include <arpa/inet.h>
#include <bits/stdc++.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>
#define PORT 80

int main(int argc, char const *argv[]) {
  int sock = 0, valread;
  struct sockaddr_in serv_addr;
  char *hello =
      "GET / HTTP/1.1\r\nHost: cse.iitj.ac.in\r\nAccept: text/html\r\n\r\n";
  char buffer[1024] = {0};
  if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
    printf("\n Socket creation error \n");
    return 0;
  }

  serv_addr.sin_family = AF_INET;
  serv_addr.sin_port = htons(PORT);

  // Convert IPv4 and IPv6 addresses from text to binary form
  if (inet_pton(AF_INET, "14.139.37.148", &serv_addr.sin_addr) <= 0) {
    printf("\nInvalid address\n");
    return 0;
  }

  if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
    printf("\nConnection Failed \n");
    return 0;
  }
  send(sock, hello, strlen(hello), 0);
  std::string end = "</html>";
  while ((valread = read(sock, buffer, 1024)) > 0) {
    buffer[valread] = '\0';
    std::string s(buffer);
    std::cout << s << std::endl;
    if (s.find(end) != std::string::npos) break;
  }
  return 0;
}