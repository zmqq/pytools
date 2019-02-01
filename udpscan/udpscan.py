from scapy.all import *
import optparse
import threading

def scan(target,port):
    pkt=IP(dst=target)/UDP(dport=int(port))
    res=sr1(pkt,timeout=0.1,verbose=0)
    if res==None:
        print(port,' is online')

def main():
    parser=optparse.OptionParser("%prog"+"-t <target> -p <port>")
    parser.add_option('-t',dest='target',type='string',help='Target')
    parser.add_option('-p',dest='port',type='string',help='Port(split with \',\')')
    (options,args)=parser.parse_args()
    target=options.target
    ports=str(options.port).split(',')
    if(target==None) or (ports[0]==None):
        print('Please input target(-t) and port(-p)!')
        exit(0)
    for port in ports:
        t=threading.Thread(target=scan,args=(target,port))
        t.start()

if __name__=='__main__':
    main()