import unittest
from observe20 import groups, sample


class GroupedFreshReads(unittest.TestCase):
    def test_groups_stay_bounded_and_preserve_every_field(self):
        rows=[('mouse_dirty',100,4),('head',104,4),('tail',108,4),
              ('mouse_head11',100000,4),('mouse_tail11',100004,4),('paints',100008,8)]
        plan=groups(rows)
        self.assertEqual(len(plan),2)
        self.assertTrue(all(end-start<=65536 for start,end,_ in plan))
        self.assertEqual(sorted(item for _,_,items in plan for item in items),sorted(rows))

    def test_every_sample_observes_changed_memory_without_state_cache(self):
        names=['mouse_dirty','mouse_head11','mouse_tail11','head','tail','paints']
        rows=[(name,i*8,8 if name=='paints' else 4) for i,name in enumerate(names)]
        memory=bytearray(48)
        class ReadOnly:
            calls=0
            @staticmethod
            def memory(g,start,size):
                ReadOnly.calls+=1
                return bytes(memory[start:start+size])
        plan=groups(rows)
        self.assertEqual(sample(ReadOnly,None,plan),(0,0,0,0,0,0))
        memory[40:48]=(19).to_bytes(8,'little')
        self.assertEqual(sample(ReadOnly,None,plan),(0,0,0,0,0,19))
        self.assertEqual(ReadOnly.calls,2)


if __name__=='__main__':unittest.main()
