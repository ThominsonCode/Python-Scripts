import socket
import optparse
import sys
import threading

from click import option

parser = optparse.OptionParser('Usage : ' + sys.argv[0] + ' -t <ip_target> -p <ports_list>')
parser.add_option('-t', '--target', dest='target_ip', type='string', help='specify the target ip')
parser.add_option('-p', '--ports', dest='target_ports', type='string', help='specify the port(s) separated by comma')

options, args = parser.parse_args()

if(options.target_ip == None) | (options.target_ports == None):
    print(parser.usage)
    exit(0)

ip = options.target_ip
ports_list = options.target_ports.split(',')

def scanPort(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex((ip, int(port)))
        if result == 0:
            print(f"{port} : open")
        else:
            print(f"{port} : close")
    except Exception as e:
        print(f"error : {e}")
    finally:
        s.close()

for port in ports_list:
    t = threading.Thread(target=scanPort, args=(ip, int(port)))
    t.start()
    # t.join()