#include <fstream>
#include <iostream>
using namespace std;

int main() {
  fstream fin;
  fin.open("./reveal_content.cpp", fstream::in);
  string line;
  while (fin >> line) cout << line << " ";
}