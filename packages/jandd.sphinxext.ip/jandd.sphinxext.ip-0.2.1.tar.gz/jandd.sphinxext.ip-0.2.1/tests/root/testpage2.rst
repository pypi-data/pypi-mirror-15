Test page 2
===========

This page contains IP addresses :ip:v4:`127.0.0.1`, :ip:v4:`192.168.0.1` and
:ip:v6:`2001:dead:beef::1` as well as :ip:v6:`::1`.

There is also :ip:v6range:`2001:dada:b001::/64` and
:ip:v4range:`172.16.0.0/24`.

The extension should also handle malformed things like :ip:v4:`<IP>`,
:ip:v6:`<IP6>`, :ip:v4range:`<IPR>` and :ip:v6range:`<IPR6>` properly.
