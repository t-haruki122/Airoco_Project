import sys
import time

isLog = True
isWait = False

def log(message):
    if not isLog: return
    if isWait: print()
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}", file=sys.stdout)
    set_isWait(False)

def log_wait(message):
    if not isLog: return
    if isWait: print()
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}", file=sys.stdout, end=" ")
    set_isWait(True)

def log_result(message):
    if not isLog: return
    if isWait:
        print(f"{message}", file=sys.stdout)
    else:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}", file=sys.stdout)
    set_isWait(False)



def set_isLog(bool_value):
    global isLog
    isLog = bool_value

def set_isWait(bool_value):
    global isWait
    isWait = bool_value



if __name__ == "__main__":
    print("This is a library module.")