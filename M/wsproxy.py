#!/usr/bin/env python
# encoding: utf-8
# CRAZY By @Crazy_vpn - Enhanced Multi-Port Support
import socket, threading, thread, select, signal, sys, time, getopt
MSG = 'WebSocket'
COR = '<font color="null">'
FTAG = '</font>'
PASS = ''
LISTENING_ADDR = '0.0.0.0'
LISTENING_PORTS = []
try:
   # Support both single port and comma-separated ports
   port_arg = sys.argv[1]
   if ',' in port_arg:
       LISTENING_PORTS = [int(p.strip()) for p in port_arg.split(',')]
   else:
       LISTENING_PORTS = [int(port_arg)]
except:
   LISTENING_PORTS = [80]
BUFLEN = 8196 * 8
TIMEOUT = 60
DEFAULT_HOST = "127.0.0.1:22"
RESPONSE = 'HTTP/1.1 101 '+str(COR)+str(MSG)+str(FTAG)+' \r\n\r\n'
 
class Server(threading.Thread):
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.running = False
        self.host = host
        self.port = port
        self.threads = []
        self.threadsLock = threading.Lock()
        self.logLock = threading.Lock()

    def run(self):
        self.soc = socket.socket(socket.AF_INET)
        self.soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.soc.settimeout(2)
        try:
            self.soc.bind((self.host, self.port))
            self.soc.listen(0)
            self.running = True
            print("WebSocket server started on port %d" % self.port)
        except Exception as e:
            print("Failed to start server on port %d: %s" % (self.port, str(e)))
            return

        try:                    
            while self.running:
                try:
                    c, addr = self.soc.accept()
                    c.setblocking(1)
                except socket.timeout:
                    continue
                
                conn = ConnectionHandler(c, self, addr)
                conn.start();
                self.addConn(conn)
        finally:
            self.running = False
            self.soc.close()
            
    def printLog(self, log):
        self.logLock.acquire()
        print("[Port %d] %s" % (self.port, log))
        self.logLock.release()
	
    def addConn(self, conn):
        try:
            self.threadsLock.acquire()
            if self.running:
                self.threads.append(conn)
        finally:
            self.threadsLock.release()
                    
    def removeConn(self, conn):
        try:
            self.threadsLock.acquire()
            self.threads.remove(conn)
        finally:
            self.threadsLock.release()
                
    def close(self):
        try:
            self.running = False
            self.threadsLock.acquire()
            
            threads = list(self.threads)
            for c in threads:
                c.close()
        finally:
            self.threadsLock.release()
			

class ConnectionHandler(threading.Thread):
    def __init__(self, socClient, server, addr):
        threading.Thread.__init__(self)
        self.clientClosed = False
        self.targetClosed = True
        self.client = socClient
        self.client_buffer = ''
        self.server = server
        self.log = 'Connection: ' + str(addr)

    def close(self):
        try:
            if not self.clientClosed:
                self.client.shutdown(socket.SHUT_RDWR)
                self.client.close()
        except:
            pass
        finally:
            self.clientClosed = True
            
        try:
            if not self.targetClosed:
                self.target.shutdown(socket.SHUT_RDWR)
                self.target.close()
        except:
            pass
        finally:
            self.targetClosed = True

    def run(self):
        try:
            self.client_buffer = self.client.recv(BUFLEN)
        
            hostPort = self.findHeader(self.client_buffer, 'X-Real-Host')
            
            if hostPort == '':
                hostPort = DEFAULT_HOST

            split = self.findHeader(self.client_buffer, 'X-Split')

            if split != '':
                self.client.recv(BUFLEN)
            
            if hostPort != '':
                passwd = self.findHeader(self.client_buffer, 'X-Pass')
				
                if len(PASS) != 0 and passwd == PASS:
                    self.method_CONNECT(hostPort)
                elif len(PASS) != 0 and passwd != PASS:
                    self.client.send('HTTP/1.1 400 WrongPass!\r\n\r\n')
                elif hostPort.startswith('127.0.0.1') or hostPort.startswith('localhost'):
                    self.method_CONNECT(hostPort)
                else:
                    self.client.send('HTTP/1.1 403 Forbidden!\r\n\r\n')
            else:
                print('- No X-Real-Host!')
                self.client.send('HTTP/1.1 400 NoXRealHost!\r\n\r\n')

        except Exception as e:
            self.log += ' - error: ' + str(e)
            self.server.printLog(self.log)
            pass
        finally:
            self.close()
            self.server.removeConn(self)

    def findHeader(self, head, header):
        aux = head.find(header + ': ')
    
        if aux == -1:
            return ''

        aux = head.find(':', aux)
        head = head[aux+2:]
        aux = head.find('\r\n')

        if aux == -1:
            return ''

        return head[:aux];

    def connect_target(self, host):
        i = host.find(':')
        if i != -1:
            port = int(host[i+1:])
            host = host[:i]
        else:
            if self.method=='CONNECT':
                port = 443
            else:
                port = 80

        (soc_family, soc_type, proto, _, address) = socket.getaddrinfo(host, port)[0]

        self.target = socket.socket(soc_family, soc_type, proto)
        self.targetClosed = False
        self.target.connect(address)

    def method_CONNECT(self, path):
        self.log += ' - CONNECT ' + path
        
        self.connect_target(path)
        self.client.sendall(RESPONSE)
        self.client_buffer = ''

        self.server.printLog(self.log)
        self.doCONNECT()

    def doCONNECT(self):
        socs = [self.client, self.target]
        count = 0
        error = False
        while True:
            count += 1
            (recv, _, err) = select.select(socs, [], socs, 3)
            if err:
                error = True
            if recv:
                for in_ in recv:
                    try:
                        data = in_.recv(BUFLEN)
                        if data:
                            if in_ is self.target:
                                self.client.send(data)
                            else:
                                while data:
                                    byte = self.target.send(data)
                                    data = data[byte:]

                            count = 0
                        else:
                            break
                    except:
                        error = True
                        break
            if count == TIMEOUT:
                error = True

            if error:
                break


class MultiPortManager:
    def __init__(self, host, ports):
        self.host = host
        self.ports = ports
        self.servers = []
        
    def start_all(self):
        for port in self.ports:
            server = Server(self.host, port)
            server.start()
            self.servers.append(server)
            time.sleep(0.1)  # Small delay between server starts
            
    def stop_all(self):
        for server in self.servers:
            server.close()

def print_usage():
    print('Use: wsproxy.py <port1,port2,port3>')
    print('     wsproxy.py -p <port1,port2,port3>')
    print('     wsproxy.py -b <ip> -p <port1,port2,port3>')
    print('     wsproxy.py -b 0.0.0.0 -p 80,2082,8080')
    print('     wsproxy.py 80,2082,8080')

def parse_args(argv):
    global LISTENING_ADDR
    global LISTENING_PORTS
    
    try:
        opts, args = getopt.getopt(argv,"hb:p:","bind=","port=")
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print_usage()
            sys.exit()
        elif opt in ("-b", "--bind"):
            LISTENING_ADDR = arg
        elif opt in ("-p", "--port"):
            if ',' in arg:
                LISTENING_PORTS = [int(p.strip()) for p in arg.split(',')]
            else:
                LISTENING_PORTS = [int(arg)]
    

def main(host=LISTENING_ADDR, ports=LISTENING_PORTS):
    
    print("\033[0;34m━"*8,"\033[1;32m PROXY WEBSOCKET MULTI-PORT","\033[0;34m━"*8,"\n")
    print("\033[1;33mIP:\033[1;32m " + LISTENING_ADDR)
    print("\033[1;33mPORTS:\033[1;32m " + ", ".join(map(str, LISTENING_PORTS)) + "\n")
    print("\033[0;34m━"*10,"\033[1;32m CRAZY MULTI","\033[0;34m━\033[1;37m"*11,"\n")
    
    manager = MultiPortManager(LISTENING_ADDR, LISTENING_PORTS)
    manager.start_all()

    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        print('\nStopping all servers...')
        manager.stop_all()
    
if __name__ == '__main__':
    parse_args(sys.argv[1:])
    main()

