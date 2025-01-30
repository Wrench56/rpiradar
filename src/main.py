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
    if len(sys.argv) == 1:
        hostname = udp.get_hostname()
        for _ in range(10):
            if _broadcast_hostname(hostname):
                break
            print('[!] Retrying to broadcast hostname...')
        print('[*] Exiting')
        sys.exit(0)
    else:
        if sys.argv[1].lower() == 'recv':
            print(f'[*] Listening to {BROADCAST_IP}:{PORT}...')
            print('[*] Receiving hostnames:')
            while True:
                data, addr = udp.receive_broadcast(PORT)
                if data == '':
                    time.sleep(0.1)
                    continue

                if data[0:3] == 'BDC':
                    hostname = data[3:].strip()
                    print(f'[@]     {hostname} at {addr[0]}')
                    udp.send_broadcast(BROADCAST_IP, PORT, f'ACK @{hostname}')
                else:
                    print(f'[!]     Invalid message received: "{data}"')
        else:
            print(f'[!] Invalid argument: "{sys.argv[1]}"')
            sys.exit(1)


def _handle_interrupt():
    print('[!] Interrupted. Exiting gracefully.')
    sys.exit(1)


def _broadcast_hostname(hostname: str) -> bool:
    print(f'[*] Sending broadcast data to group {BROADCAST_IP}:{PORT}...')
    while True:
        udp.send_broadcast(BROADCAST_IP, PORT, f'BDC {hostname}')
        msg, _ = udp.receive_broadcast(PORT)
        if msg != '':
            break
        time.sleep(0.5)
    if msg == f'ACK @{hostname}':
        print('[*] Verfied!')
        return True
    return False


if __name__ == '__main__':
    main()
