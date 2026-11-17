"""Bounded sparse clones of owned native test fixtures; never host disks."""
import hashlib,os
from pathlib import Path

def clone(ui,source,suite):
 base=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6'
 source=Path(source).resolve();assert source.is_relative_to(base.resolve()) and source.is_file()
 work=ui.q.new_work(suite);target=ui.q.sparse_disk(work/'owned.img',source.stat().st_size)
 zero=bytes(1024**2);digest=hashlib.sha256()
 with source.open('rb') as src,target.open('r+b') as dst:
  while data:=src.read(len(zero)):
   digest.update(data)
   if data!=zero[:len(data)]:dst.write(data)
   else:dst.seek(len(data),1)
 check=hashlib.sha256()
 with target.open('rb') as stream:
  while data:=stream.read(len(zero)):check.update(data)
 assert digest.digest()==check.digest() and target.stat().st_size==source.stat().st_size
 return work,target,dict(source_sha256=digest.hexdigest(),clone_sha256=check.hexdigest(),logical_bytes=target.stat().st_size,allocated_bytes=ui.module('access_workspace16',ui.ROOT/'tests/m6/workspace.py').allocated(target))
