from scapy.all import *
import optparse

def is_zombie(target,zombie):
    pktz=IP(dst=zombie)/TCP(flags='SA')
    pktt=IP(src=zombie,dst=target)/TCP(flags='S')
    res1=sr1(pktz,timeout=1,verbose=0)
    send(pktt,verbose=0)
    res2=sr1(pktz,timeout=1,verbose=0)
    try:
        if res2[IP].id-2==res1[IP].id:
            print('It is a zombie.')
            return 1
        else:
            print('It isn\'t a zombie.')
            return 0
    except:
        print('It isn\'t a zombie.')

def scan(target,zombie,port):
    pktz=IP(dst=zombie)/TCP(flags='SA',dport=int(port))
    pktt=IP(src=zombie,dst=target)/TCP(flags='S',dport=int(port))
    start=sr1(pktz,timeout=1,verbose=0)
    send(pktt,verbose=0)
    end=sr1(pktz,timeout=1,verbose=0)
    if end[IP].id-2==start[IP].id:
        print(port,' is online')

def main():
    parser=optparse.OptionParser("%prog "+'-t <target> -z <zombie> -p <port>')
    parser.add_option('-t',dest='target',type='string',help='Target')
    parser.add_option('-z',dest='zombie',type='string',help='Zombie')
    parser.add_option('-p',dest='port',type='string',help='Port(eg:22,80    or  1-100)')
    (options,args)=parser.parse_args()
    target=options.target
    zombie=options.zombie
    if(target==None) or (zombie==None):
        print('Please input target(-t) and zombie(-z)!')
        exit(0)
    res=is_zombie(target,zombie)
    if res==1:
        if(',' in options.port):
            ports=str(options.port).split(',')
            if ports[0]==None:
                print('Please input port(-p)!')
                exit(0)
            for port in ports:
                scan(target,zombie,port)
        elif('-' in options.port):
            ports=str(options.port).split('-')
            if ports[0]==None:
                print('Please input port(-p)!')
                exit(0)
            for port in range(int(ports[0]),int(ports[1])):
                scan(target,zombie,port)
    else:
        pass

if __name__=='__main__':
    main()