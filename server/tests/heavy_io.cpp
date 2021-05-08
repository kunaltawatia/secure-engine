#include <iostream>
using namespace std;

int main(int argc, char **argv) {
  for (int i = 0; i < 256; i++) putc('-', stdout);
  fflush(stdout);
}