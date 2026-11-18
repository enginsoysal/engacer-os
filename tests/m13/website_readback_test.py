"""Fresh readback retains failures and bounds independent GET concurrency."""
import threading,unittest
import website_readback as subject
class FreshReads(unittest.TestCase):
 def test_four_parallel_reads_remain_complete_and_stable(self):
  barrier=threading.Barrier(4);lock=threading.Lock();active=0;peak=0
  def fetch(url):
   nonlocal active,peak
   with lock:active+=1;peak=max(peak,active)
   barrier.wait(timeout=3)
   with lock:active-=1
   return dict(url=url,status=200)
  rows=subject.fresh_reads(['d','c','b','a'],fetch=fetch);self.assertEqual([r[0] for r in rows],list('abcd'));self.assertEqual(peak,4);self.assertTrue(all(len(r[2])==1 for r in rows))
 def test_transient_and_permanent_failures_are_all_retained(self):
  calls={};pauses=[]
  def fetch(url):
   calls[url]=calls.get(url,0)+1
   return dict(url=url,status=(200 if calls[url]==3 else 502) if url=='transient' else 404,error=None if calls[url]==3 and url=='transient' else 'observed refusal')
  rows=subject.fresh_reads(['transient','permanent'],fetch=fetch,pause=pauses.append);self.assertEqual(calls,dict(permanent=3,transient=3));self.assertEqual(sorted(pauses),[2,2,4,4]);self.assertEqual([a['status'] for a in rows[1][2]],[502,502,200]);self.assertEqual([a['status'] for a in rows[0][2]],[404,404,404]);self.assertEqual(rows[0][1]['status'],404)
 def test_soft_404_is_retried_even_with_http_200(self):
  calls=[]
  def fetch(url):
   calls.append(url);return dict(url=url,status=200,soft_404=len(calls)<3)
  rows=subject.fresh_reads(['guide'],fetch=fetch,pause=lambda _:None);self.assertEqual(len(calls),3);self.assertFalse(rows[0][1]['soft_404']);self.assertEqual(len(rows[0][2]),3)
if __name__=='__main__':unittest.main()
