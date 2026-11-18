"""Same three-sample functional barrier with bounded fresh grouped guest reads.

No guest writes, mutable-state cache, timing pass or stability qualification.
Only immutable symbol addresses are grouped; every sample reads actual memory.
"""
import time


def groups(records, maximum=65536):
    result=[]
    for name,address,size in sorted(records, key=lambda item:item[1]):
        assert 0 < size <= maximum
        if not result or address+size-result[-1][0] > maximum:
            result.append([address,address+size,[]])
        result[-1][1]=max(result[-1][1],address+size)
        result[-1][2].append((name,address,size))
    return result


def sample(ui,g,plan):
    values={}
    for start,end,items in plan:
        raw=ui.memory(g,start,end-start)
        assert len(raw)==end-start
        for name,address,size in items:
            values[name]=int.from_bytes(raw[address-start:address-start+size],'little')
    return tuple(values[name] for name in ('mouse_dirty','mouse_head11','mouse_tail11','head','tail','paints'))


def bind(ui,base=None):
    base=base or ui.Pointer
    class Pointer(base):
        def drain(self):
            super().drain()
            if 'M7_DESKTOP_READY' not in self.guest.log():return
            records=[]
            for name in ('mouse_dirty','mouse_head11','mouse_tail11','head','tail','paints'):
                width=8 if name=='paints' else 4
                address,size=ui.symbol(name,width,True)
                assert size==width
                records.append((name,address,width))
            plan=groups(records)
            g=self.guest;cpus=len(g.qmp('query-cpus-fast'))
            previous=None;stable=0;deadline=time.monotonic()+30
            while True:
                current=sample(ui,g,plan)
                halted=g.qmp('human-monitor-command',{'command-line':'info registers -a'}).count('HLT=1')==cpus
                empty=not current[0] and current[1]==current[2] and current[3]==current[4]
                stable=stable+1 if empty and halted and current==previous else 0
                if stable>=3:return
                previous=current
                if time.monotonic()>deadline:raise TimeoutError('Owned native desktop did not reach three consecutive fresh stable/empty/halted observations')
                time.sleep(.05)
    ui.Pointer=Pointer
    return dict(method='Three consecutive fresh stable input/paint samples and all CPUs halted',
                maximum_group_bytes=65536,mutable_guest_state_cached=False,guest_memory_written=False)
