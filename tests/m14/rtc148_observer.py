"""Owned QEMU RTC fault injection through documented monitor I/O, no guest-memory patching."""
import re

def monitor(g,text):
 result=g.qmp('human-monitor-command',{'command-line':text});assert isinstance(result,str) and 'unknown command' not in result.lower(),result;return result

def read_b(g):
 monitor(g,'o /b 0x70 0x8b');text=monitor(g,'i /b 0x71');match=re.search(r'0x([0-9a-fA-F]+)\s*$',text);assert match,text;return int(match.group(1),16)

def write_b(g,value):
 monitor(g,'o /b 0x70 0x8b');monitor(g,'o /b 0x71 '+hex(value))

def begin(g,ui):
 anchor=int.from_bytes(ui.memory(g,ui.symbol('utc_filetime148',installed=True)[0],8),'little');assert anchor>0,'UTC must be genuinely initialized before injecting the RTC fault'
 saved=None;g.qmp('stop')
 try:
  saved=read_b(g);assert not saved&0x80,saved;write_b(g,saved|0x80);assert read_b(g)&0x80
 except BaseException:
  if saved is not None:write_b(g,saved)
  raise
 finally:monitor(g,'o /b 0x70 0');g.qmp('cont')
 return dict(scope=__doc__,saved_status_b=saved,injected_status_b=saved|0x80,initialized_anchor_filetime=anchor)

def end(g,fault):
 g.qmp('stop')
 try:
  observed=read_b(g);assert observed&0x80,observed
 finally:
  try:
   write_b(g,fault['saved_status_b']);restored=read_b(g);assert restored==fault['saved_status_b'],restored
  finally:monitor(g,'o /b 0x70 0');g.qmp('cont')
 return dict(fault,observed_frozen_status_b=observed,restored_status_b=restored)
