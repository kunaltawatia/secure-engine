#include <dirent.h>
#include <unistd.h>

#include <iostream>
using namespace std;

int main() {
  char *cwd;
  cwd = (char *)malloc(BUFSIZ * sizeof(char));
  getcwd(cwd, BUFSIZ);

  DIR *dir;
  struct dirent *ent;
  if ((dir = opendir(cwd)) != NULL) {
    while ((ent = readdir(dir)) != NULL) {
      printf("%s\n", ent->d_name);
    }
    closedir(dir);
  } else {
    printf("Couldn't access directory\n");
  }
}