"""Read-only readiness barrier for owned M13.6 desktop input observations.

A hover paint is not proof that a later click/keyboard edge has completed. Observe
three consecutive idle/empty-queue/stable-paint samples without modifying state.
Host settling is deliberately not input latency or FPS evidence.
"""
import time

def bind(ui):
 base=ui.Pointer
 class Pointer(base):
  def drain(self):
   super().drain()
   if 'M7_DESKTOP_READY' not in self.guest.log():return
   previous=None;stable=0;deadline=time.monotonic()+30
   while True:
    super().drain()
    g=self.guest
    sample=(ui.integer(g,'mouse_dirty',True),ui.integer(g,'mouse_head11',True),ui.integer(g,'mouse_tail11',True),ui.integer(g,'head',True),ui.integer(g,'tail',True),int.from_bytes(ui.memory(g,ui.symbol('paints',8,True)[0],8),'little'))
    halted=g.qmp('human-monitor-command',{'command-line':'info registers -a'}).count('HLT=1')==len(g.qmp('query-cpus-fast'))
    empty=not sample[0] and sample[1]==sample[2] and sample[3]==sample[4]
    stable=stable+1 if empty and halted and sample==previous else 0
    if stable>=3:return
    previous=sample
    if time.monotonic()>deadline:raise TimeoutError('Owned native desktop did not reach consecutive stable observations')
    time.sleep(.05)
 ui.Pointer=Pointer
