import os
import sys
import time
import signal
import resource
import subprocess


def save_code(code):
  index = str(int(time.time()))
  file_name = index
  dir_name = os.getcwd()
  file_path_NOEX = os.path.join(dir_name, 'submissions', file_name)
  file_path = file_path_NOEX + '.cpp'
  input_path = file_path_NOEX + '.inp'
  output_path = file_path_NOEX + '.out'

  with open(file_path, 'w') as fopen:
    fopen.write(code)

  return {
    "name" : file_name,
    "path_noex" : file_path_NOEX,
    "path": file_path,
    "code" : code,
    "input" : input_path,
    "output" : output_path,
    "result" : ''
  }
  
def compile(details):
  path = details["path"]
  exe = details["path_noex"]
  compilation = subprocess.Popen(["g++", path, '-o', exe])
  compilation.wait()

def execute_v0(details):
  exe = details["path_noex"]
  start_time = time.time()
  execution = subprocess.Popen([exe], stdout=subprocess.PIPE)
  execution.wait()
  details["result"] = execution.stdout.read()
  details["time"] = time.time() - start_time
  return

TIME_LIMIT = 2
MEM_LIMIT = 512 * 1024
def execute(details):
  exe = details["path_noex"]
  r, w = os.pipe()
  pid = os.fork()
  if not pid:
    os.close(r)
    os.dup2(w, sys.stdout.fileno())
    os.dup2(w, sys.stderr.fileno())
    resource.setrlimit(resource.RLIMIT_CPU, (TIME_LIMIT, TIME_LIMIT))
    resource.setrlimit(resource.RLIMIT_DATA, (MEM_LIMIT, MEM_LIMIT))
    print(time.time())
    os.execvp(exe, ["--"])
  else:
    os.close(w)
    process_out = os.fdopen(r)
    start_time = float(process_out.readline())
    def active_handler(sig ,stack):
      os.kill(pid, signal.SIGKILL)
    def passive_handler(sig ,stack):  
      pass
    signal.signal(signal.SIGALRM, active_handler)
    signal.alarm(TIME_LIMIT)
    _, sig = os.wait()
    if sig:
      print(signal.Signals(sig))
    signal.signal(signal.SIGALRM, passive_handler)
    details["result"] = process_out.read()
    details["time"] = time.time() - start_time
    process_out.close()

def cleanup(details):
  path = details["path"]
  exe = details["path_noex"]
  os.remove(exe)
  os.remove(path)

def run(code):
  details = save_code(code)
  compile(details)  
  execute(details)
  cleanup(details)
  output = details["result"]
  time = details["time"]
  return output

if __name__ == "__main__":
  with open('tests/hello.cpp', 'r') as fopen:
    code = fopen.read()
    run(code)