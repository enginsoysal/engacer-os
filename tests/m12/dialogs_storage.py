"""Independent persisted payload and optional-record checks after native dialogs."""
import json,os,struct,zipfile,zlib
from pathlib import Path
import dialogs_native as d
ui=d.ui;ROOT=d.ROOT

def main():
    native=json.loads((ROOT/'build/m12/stage8/dialogs-native/results.json').read_text());meta=json.loads(ui.manifest_path12().read_text());assert native['passed'] and native['build_id']==meta['build_id']
    disk=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m12-stage8-dialogs'/native['owned_fixture']/'owned.img'
    read=lambda name:ui.s.s.document(disk,'/Users/Owner/'+name)
    guide=(ROOT/'distros/packages/m12-desktop-guide/content.txt').read_bytes();text=b'Original native text'
    assert read('Documents/First.txt')==text+b' saved before open'
    assert read('Downloads/Saved.txt')==read('Documents/Existing.txt')==text+b' edited'
    assert read('Documents/Projects/Nested.txt')==guide
    assert read('Documents/Welcome.txt')==guide
    extracted=[]
    with zipfile.ZipFile(ROOT/'distros/packages/apps-guide/ArchiveSample.zip') as archive:
        for item in archive.infolist():
            if item.is_dir():continue
            assert ui.s.s.document(disk,native['extracted_folder']+'/'+item.filename)==archive.read(item);extracted.append(item.filename)
    assert extracted
    record=read('AppData/file-dialogs12.bin');assert len(record)==792
    magic,version,reserved=struct.unpack_from('<QII',record);crc,padding=struct.unpack_from('<II',record,784)
    assert magic==0x31524b4350494c46 and version==1 and reserved==padding==0 and zlib.crc32(record[:784])==crc
    locations=[record[16+i*256:16+(i+1)*256].split(b'\0')[0].decode() for i in range(3)]
    assert locations==['/Users/Owner/Downloads','/Users/Owner/Documents','/Users/Owner/Documents'],locations
    result=dict(passed=True,build_id=meta['build_id'],owned_fixture=native['owned_fixture'],extracted_members=extracted,remembered_locations=locations,checks=['Independent GPT and metadata/data CRC checks confirm exact original, Save as, explicit replacement, Save before Open and discarded-dirty document bytes','Every extracted member matches Python ZIP decoding of the original included archive','The 792-byte per-user record has a valid version, reserved fields, CRC and separate successful Open/Save/folder locations'])
    out=ROOT/'build/m12/stage8/dialogs-storage';out.mkdir(parents=True,exist_ok=True);(out/'results.json').write_bytes((json.dumps(result,indent=2)+'\n').encode());print(json.dumps(result,indent=2))
if __name__=='__main__':main()
