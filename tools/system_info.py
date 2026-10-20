import platform
import socket
import psutil
import uuid
import re
def system_info() -> str:
    try:
        info={}
        info['platform']=platform.system()
        info['platform-release']=platform.release()
        info['platform-version']=platform.version()
        info['architecture']=platform.machine()
        info['hostname']=socket.gethostname()
        info['ip-address']=socket.gethostbyname(socket.gethostname())
        info['mac-address']=':'.join(re.findall('..', '%012x' % uuid.getnode()))
        info['processor']=platform.processor()
        info['ram']=str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
        return str(info)
    except Exception as e:
        return str(e)

SCHEMA = {
    "type": "function",
    "function": {
        "name": "system_info",
        "description": "Provide system info"
        }
    }


if __name__ == '__main__':
    print(system_info())