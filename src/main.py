'''Main file'''

import signal
import sys
import time
import udp

BROADCAST_IP = '10.1.255.255'
PORT = 5005


def main() -> None:
    '''Entry point'''
    signal.signal(signal.SIGINT, lambda signum, _: _handle_interrupt())
    print('[*] Online')
    if len(sys.argv) == 1:
        hostname = udp.get_hostname()
        while True:
            msg, _ = udp.receive_broadcast(PORT)
            if msg != 'WKE':
                continue
            for _ in range(10):
                if _broadcast_hostname(hostname):
                    # Wait until you send hostname again
                    time.sleep(10.0)
                    break
                print('[!] Retrying to broadcast hostname...')
    else:
        if sys.argv[1].lower() == 'recv':
            print(f'[*] Listening to {BROADCAST_IP}:{PORT}...')
            print('[*] Receiving hostnames:')
            recv_ips = set()
            while True:
                msg, addr = udp.send_until_receive(BROADCAST_IP, PORT, 'WKE', wait=0.01)
                if msg[0:3] == 'BDC':
                    hostname = msg[3:].strip()
                    if addr[0] in recv_ips:
                        udp.send_broadcast(BROADCAST_IP, PORT, f'ACK @{hostname}')
                        continue
                    print(f'[@]     {hostname} at {addr[0]}')
                    udp.send_broadcast(BROADCAST_IP, PORT, f'ACK @{hostname}')
                    recv_ips.add(addr[0])
                else:
                    if msg == 'WKE':
                        continue
                    print(f'[!]     Invalid message received: "{msg}"')
        else:
            print(f'[!] Invalid argument: "{sys.argv[1]}"')
            sys.exit(1)


def _handle_interrupt():
    print('[!] Interrupted. Exiting gracefully.')
    sys.exit(1)


def _broadcast_hostname(hostname: str) -> bool:
    print(f'[*] Sending broadcast data to group {BROADCAST_IP}:{PORT}...')
    while True:
        msg, _ = udp.send_until_receive(BROADCAST_IP, PORT, f'BDC {hostname}', wait=0.1)
        if msg == f'ACK @{hostname}':
            print('[*] Verfied!')
            return True
        return False


if __name__ == '__main__':
    main()
