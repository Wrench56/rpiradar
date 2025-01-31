# RPiRadar

A tool made for discovering the local IP address of Raspberry Pi-s

On your Raspberry Pi-s, use `python3 main.py`. On your laptop, use `python3 main.py recv`. (This will be your "monitor")
The Raspberry Pi shares it's hostname and IP address through UDP broadcast.
You will end up seeing something like:

```sh
[*] Online
[*] Listening to 10.1.255.255:5005...
[*] Receiving hostnames:
[@]     raspberrypi-main at 10.1.6.253
[!] Interrupted. Exiting gracefully.
```

To not flood the router with UDP messages, a `WKE` (wake) packets gets sent once the monoitor runs. The clients respond by sending out `BDC {hostname}` messages where `{hostname}` is the client's hostname. At this point the monitor receives these packets, sends an acknowledge (`ACK @{hostname}`) and lists the hosntame along with the IP address that sent the package.

This project is unlikely to get substantial upgrade in the future. If you have any bugs, please report it [here](https://github.com/Wrench56/rpiradar/issues). The project will remain maintained.
