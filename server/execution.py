import os
import sys
import time
import signal
import resource
import subprocess


def save_code(code, inp):
  index = str(int(time.time()) % 1000)
  file_name = index
  dir_name = os.getcwd()
  file_path_NOEX = os.path.join(dir_name, 'submissions', file_name)
  file_path = file_path_NOEX + '.cpp'
  input_path = file_path_NOEX + '.inp'
  meta_path = file_path_NOEX + '.meta'

  with open(file_path, 'w') as fopen:
    fopen.write(code)
  with open(input_path, 'w') as fopen:
    fopen.write(inp)

  return {
    "id" : index,
    "name" : file_name,
    "path_noex" : file_path_NOEX,
    "path": file_path,
    "code" : code,
    "input" : input_path,
    "meta" : meta_path,
    "result" : None,
    "error" : None
  }
  
def compile(details):
  path = details["path"]
  exe = details["path_noex"]
  compiler = subprocess.Popen(["g++", path, '-o', exe], shell=False, stderr=subprocess.PIPE)
  compiler.wait()
  exitcode = compiler.returncode
  if exitcode:
    details["error"] = compiler.stderr.read().decode('utf-8').replace(path, "exe")
  else:
    assert os.path.isfile(exe)

TIME_LIMIT = 1 # s
MEM_LIMIT = 16 # mb
FSIZE_LIMIT = 1 # mb
def execute(details):
  exe = details["path_noex"]
  input_path = details["input"]
  meta_path = details["meta"]
  init = subprocess.Popen(["isolate", "--cg", "--box-id=" + details["id"], "--init"], shell=False, stdout=subprocess.PIPE)
  init.wait()
  details["sandbox"] = init.stdout.read().decode('utf-8').strip()
  box = details["sandbox"] + '/box'
  copy = subprocess.Popen(["cp", exe, box + '/exe'], shell=False, stdout=subprocess.PIPE)
  copy.wait()
  copy = subprocess.Popen(["cp", input_path, box + '/inp'], shell=False, stdout=subprocess.PIPE)
  copy.wait()
  run = subprocess.Popen(
    [
      "isolate",
      "--cg",
      "--box-id=" + details["id"],
      "-t", str(TIME_LIMIT),
      "-w", str(TIME_LIMIT + 0.5),
      "-m", str(MEM_LIMIT * 1024),
      "-f", str(FSIZE_LIMIT * 1024),
      "-i", "inp",
      "-o", "out",
      "-M", meta_path,
      "-p4",
      "--stderr-to-stdout",
      "--share-net",
      "-s",
      "-d", "/usr:noexec",
      "--run",
      "--",
      "exe"],
    shell=False
  )
  run.wait()
  with open(box + '/out', 'r') as fout:
    output = fout.read()
  with open(meta_path, 'r') as fout:
    meta = parse_meta(fout.read())
  if run.returncode:
    details["error"] = meta["message"]
  else:
    details["result"] = output

def parse_meta(meta):
  result = {}
  for line in meta.split('\n'):
    if ':' in line:
      key, value = line.split(':')
      result[key] = value

  if "status" in result:
    if result["status"] == "TO":
      result["message"] = "Time Limit Exceeded"
    if result["status"] == "SG":
      result["message"] = signal.Signals(int(result["exitsig"])).name

  return result

def cleanup(details):
  for file_path in [
    details["path"],
    details["input"],
    details["meta"],
    details["path_noex"],
  ]:
    if os.path.isfile(file_path):
      os.remove(file_path)
  if not "error" in details:
    iso_cleanup = subprocess.Popen(["isolate", "--box-id=" + details["id"], "--cleanup"], shell=False, stdout=subprocess.PIPE)
    iso_cleanup.wait()
    iso_cleanup = subprocess.Popen(["rm", "-rf", details["sandbox"]], shell=False, stdout=subprocess.PIPE)
    iso_cleanup.wait()
  
def run(code, inp):
  details = save_code(code, inp)
  compile(details)
  if not details["error"]:
    execute(details)
  cleanup(details)
  if details["error"]:
    output = details["error"]
  else:
    output = details["result"]
  return str(output)

if __name__ == "__main__":
  with open('tests/hello.cpp', 'r') as fopen:
    code = fopen.read()
    print(run(code))