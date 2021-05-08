#include <unistd.h>

#include <iostream>
using namespace std;

int main() {
  char* cwd;
  cwd = (char*)malloc(BUFSIZ * sizeof(char));
  getcwd(cwd, BUFSIZ);
  cout << cwd << endl;
}