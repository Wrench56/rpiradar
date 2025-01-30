'''UDP communication tools'''

from typing import Any, Tuple

import socket

RECV_SIZE = 1024


def get_hostname() -> str:
    '''Get hostname'''
    return socket.gethostname()


def send_broadcast(ip: str, port: int, message: str) -> None:
    '''Send a UDP broadcast packet to all devices on the network'''
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        sock.sendto(message.encode(), (ip, port))
    except Exception as e:
        print(f'[!] Broadcast error: {e}')
        raise e
    finally:
        sock.close()


def receive_broadcast(port: int) -> Tuple[str, Tuple[Any]]:
    '''Receive UDP packets sent to a broadcast group in a blocking way'''
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind(('', port))
    sock.setblocking(False)

    while True:
        try:
            data, addr = sock.recvfrom(RECV_SIZE)
            if data != '':
                return (data.decode(), addr,)
        except BlockingIOError:
            pass


def send_until_receive(ip: str, port: int, msg: str) -> Tuple[str, Tuple[Any]]:
    '''Send a message until you receive a response'''
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind(('', port))
    sock.setblocking(False)

    while True:
        try:
            send_broadcast(ip, port, msg)
            data, addr = sock.recvfrom(RECV_SIZE)
            if data != '':
                return (data.decode(), addr,)
        except BlockingIOError:
            pass
