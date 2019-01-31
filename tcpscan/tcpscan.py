from scapy.all import *
import optparse
import threading

def scan(ip,port):
    pkt=IP(dst=ip)/TCP(dport=int(port))
    res=sr1(pkt,timeout=0.1,verbose=0)
    try:
        if int(res[TCP].flags)==18:
            print(port,' is open')
    except:
        pass

def main():
    parser=optparse.OptionParser('%prog '+"xxx")
    parser.add_option('-t',dest='target',type='string',help='Target')
    parser.add_option('-p',dest='port',type='string',help='Port(eg:22,80    1-500)')
    (options,args)=parser.parse_args()
    target=options.target
    if(',' in options.port):
        ports=str(options.port).split(',')
        if ((target==None) or (ports[0]==None)):
            print('Please input target(-t) and port(-p)!')
            exit(0)
        for port in ports:
            t=threading.Thread(target=scan,args=(target,port))
            t.start()
    elif('-' in options.port):
        ports=str(options.port).split('-')
        for port in range(int(ports[0]),int(ports[1])):
            t=threading.Thread(target=scan,args=(target,port))
            t.start()

if __name__=='__main__':
    main()