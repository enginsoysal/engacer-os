"""Bound immutable symbol lookups and disable client QMP Nagle delays.

This changes only the host observer. It never caches guest state, writes guest
memory, changes native scheduling or turns host readiness times into native FPS.
"""
from functools import lru_cache
import hashlib
import socket


def bind(ui):
    base = ui.symbol
    fingerprints = {k: hashlib.sha256(v.encode('utf-8')).hexdigest()
                    for k, v in ui.MAPS74.items()}

    @lru_cache(maxsize=512)
    def symbol(name, size=None, installed=False):
        return base(name, size, installed)

    # Imported primitives retain their original module globals.
    base.__globals__['symbol'] = symbol
    ui.symbol = symbol
    original = ui.q.connect

    def connect(port, process):
        value = original(port, process)
        value.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        return value

    ui.q.connect = connect
    return dict(immutable_map_sha256=fingerprints, maximum_symbol_cache_entries=512,
                mutable_guest_state_cached=False, qmp_client_tcp_nodelay=True)
