import {portalConfiguration} from './portal.mjs';
import {workdayQualified13} from './downloads.mjs';
// Native Brix composition matching the owner's preferred local documentation design.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const progress=JSON.parse(fs.readFileSync(new URL('../../docs/milestones/m11-progress.json',import.meta.url),'utf8'));
const developmentProgress=JSON.parse(fs.readFileSync(new URL('../../docs/milestones/m12-progress.json',import.meta.url),'utf8'));
let sequence=0;
const site='https://engaceros.brixcanvas.com';
const expanded=Number(progress.current_stage.split('.')[1])>=5;
const final=progress.qualified_download==='M11.6';
const ink='#152434',muted='#5a6976',teal='#087c71',dark='#101e2c',paper='#f7f9f9';
const b=(type,props)=>({id:`engine-home-${++sequence}`,type,props});
const text=(value,size=16,color=muted,more={})=>b('text',{text:value,size,color,padX:0,py:10,lineHeight:1.65,...more});
const heading=(value,size=26,color=ink,more={})=>b('heading',{text:value,size,color,level:2,weight:600,padX:0,py:12,fluid:true,...more});
const button=(label,href,more={})=>b('button',{label,href,bg:teal,color:'#ffffff',hoverBg:'#065f56',radius:'none',size:'sm',align:'left',padX:0,py:12,...more});
const layout=(columns,more={})=>b('layout',{columns:columns.map(children=>({children})),contentWidth:1280,padY:0,...more});
const card=(n,title,description,label,slug)=>[
 text(n,11,teal,{letterSpacing:'1.2px',weight:600}),heading(title,21,ink,{level:3}),text(description,14),
 button(label,`${site}/blog/${slug}`,{bg:'#ffffff',color:teal,hoverBg:'#edf5f2',size:'sm'}),
];
export function nativeDesign({development=developmentProgress}={}){
 sequence=0;
 const native=/^M12\.(?:[1-9]|1[0-8])$/.test(development.qualified_download);
 const label=native?development.qualified_download:progress.qualified_download;
 const number=native?Number(label.split('.')[1]):0;
 const delivery=development.stages.find(s=>s.id===label);
 const guide=native?`install-m12${number}`:progress.release_guide;
 const knownIssueBrix=native?(development.known_issues||[]).filter(issue=>issue.status==='open').map(issue=>b('alert',{variant:'info',title:'Retained test observation · '+issue.observed_in,text:issue.observation+' Read the matching release scope before testing.'})):[];
 const header=b('menubrix',{brand:'E_  ENGACER OS',brandHref:'/',items:[{label:'Documentation',href:'/blog/documentation'},{label:'Downloads',href:'/blog/downloads'},{label:'GitHub ↗',href:'https://github.com/enginsoysal/engacer-os'},{label:'Search',href:'/search'}],mode:'inline',width:'full',shape:'square',size:'l',bg:dark,textColor:'#d5e1e8',hoverColor:'#35ceba',blur:false,border:false,shadow:false});
 header.style={bg:{color:dark}};
 const status=layout([[text('● Independent kernel. Open source.',11,'#50616c',{py:6})],[text('INDEPENDENT · BUILT FROM SCRATCH',10,'#50616c',{align:'right',letterSpacing:'1px',py:6})]],{bg:{kind:'color',color:'#eaf0f0'},borderBottom:1,borderColor:'#dbe3e6'});
 const terminal=layout([[
   text('PROJECT SNAPSHOT / X86-64',10,'#90a6b8',{letterSpacing:'1.5px',py:10}),
   heading('ENGACER OS',18,'#e4edf1',{py:12}),
   text('Original kernel · BIOS + UEFI boot',13,'#35ceba'),
   text('Tested native delivery: '+label+' · Scoped VM tests',12,'#90a6b8'),
   text(development.current_stage+' · '+development.stages.find(s=>s.id===development.current_stage).title,13,'#35ceba'),
   text('M12.0–M12.18 · Ordered delivery with tests and publication',12,'#90a6b8'),
   b('code',{code:'Next → Review → Install → Restart\nIDE / SATA / supported SCSI / NVMe\nDevices · USB file copies · Safe removal'}),
 ]],{bg:{kind:'color',color:dark},border:1,borderColor:'#35ceba',radius:4,padY:18,minH:320,valign:'center'});
 const hero=layout([[
   text('THE ENGACER OS KNOWLEDGE BASE',11,teal,{letterSpacing:'1.6px',weight:600,py:12}),
   heading('The M12 desktop',52,ink,{level:1,py:0,letterSpacing:'-1.8px'}),
   heading('made familiar.',52,teal,{py:0,letterSpacing:'-1.8px'}),
   text(native?`${label} delivers ${delivery.title.toLowerCase()} in the real native desktop. Use its matching ISO, VMware package and stage guide. ${number===18?'The final named-VM regression is recorded with exact source and media evidence.':'Each remaining M12 stage follows in order with its own tests and publication.'}`:'M12.0 establishes the design: recognizable app icons, consistent Files navigation, clear controls and a coherent desktop. Nineteen stages follow in order. These concepts are not a new native build; M11.6 remains the current tested VMware download.',18,muted,{py:20}),
   layout([[button('See the M12 plan →',`${site}/blog/docs-milestones-m12`,{size:'sm'})],[button(`Download ${label} ↓`,`${site}/blog/downloads`,{variant:'outline',bg:ink,size:'sm'})]]),
 ],[terminal]],{padY:52,valign:'center'});
 hero.props.columns[0].width=55;hero.props.columns[1].width=45;
 hero.props.columns[0].children.at(-1).props.columns[0].width=60;
 hero.props.columns[0].children.at(-1).props.columns[1].width=40;
 const cards=layout([
   native?card('01 / CURRENT NATIVE STAGE',delivery.title,'Use the real native desktop with the behavior qualified for this stage. Its matching guide explains the controls, evidence and limits.','Read the stage guide ↗','docs-handbook-'+guide):card('01 / M12 DESIGN','One coherent desktop.','Recognizable icons, shared controls and a Files window that keeps Back, breadcrumbs and the sidebar visible, including USB empty states.','Explore the design contract ↗','docs-architecture-desktop-m12'),
   card('02 / TESTED DOWNLOAD','Install in VMware','The current qualified download is '+label+'. Use its prepared VMware ZIP and matching installation guide. Read the exact tested profiles and limits before choosing other hardware.','Open the setup guide ↗','docs-handbook-'+(guide||'install-m116')),
   card('03 / MAKE IT YOURS','Build your own distro.','Choose your accent, wallpaper, window style and default content with a validated distribution profile.','Open the distro guide ↗','docs-handbook-distributions'),
 ],{bg:{kind:'color',color:'#ffffff'},border:1,borderColor:'#dbe3e6',divided:true,ruleColor:'#dbe3e6',radius:4,padY:24});
 cards.props.columns.forEach(column=>{column.width=100/3;});
 const bottom=layout([[
   text('BUILT IN THE OPEN',11,teal,{letterSpacing:'1.5px'}),heading('Understand the decisions behind the OS.',19),
   text('Explore the kernel contracts, memory model, filesystem layout and compatibility roadmap. Every milestone links implementation claims to evidence.',14),
   button('Explore the architecture →',`${site}/blog/docs-architecture-overview`,{bg:paper,color:teal,hoverBg:'#edf5f2'}),
 ],[
   text('ONE SOURCE OF TRUTH',11,teal,{letterSpacing:'1.5px'}),heading('Documentation that follows the code.',19),
   text('Guides identify their canonical GitHub source commit. Official releases supply original download files and complete SHA256 checksums.',14),
   button('View the milestone plan →',`${site}/blog/docs-roadmap-milestones`,{bg:paper,color:teal,hoverBg:'#edf5f2'}),
 ]],{padY:32,borderBottom:1,borderColor:'#dbe3e6'});
 bottom.props.columns.forEach(column=>{column.width=50;});
 const main=layout([[
   hero,...knownIssueBrix,...(native?[heading('From the real '+label+' VM',27,ink,{py:18}),b('image',{url:`https://raw.githubusercontent.com/enginsoysal/engacer-os/main/evidence/M12/${number}/feature.png`,alt:`Native Engacer OS ${label} from its actual tested native guest, not a design concept. Read its matching stage qualification and capture provenance.`,naturalSize:true,radius:8})]:[heading('M12.0 original design concept',27,ink,{py:18}),b('image',{url:'https://raw.githubusercontent.com/enginsoysal/engacer-os/main/docs/architecture/figures/m12/overview.svg',alt:'Original M12.0 design concept, not a native VM capture. Distinct app icons and a proposed Start layout.',naturalSize:true,radius:8}),heading('From the real M11.6 VM — current tested download',27,ink,{py:18}),b('image',{url:'https://raw.githubusercontent.com/enginsoysal/engacer-os/main/evidence/M11/6/setup/vmware/first-start-guide.png',alt:'Native Engacer OS M11.6 in the tested VMware guest. This remains the qualified download while M12 development proceeds.',naturalSize:true,radius:8})]),heading('A good place to start',27,ink,{py:24}),cards,
   b('alert',{variant:'info',title:'Development progress and tested downloads',text:native?`${label} is a scoped native delivery. ${number===18?'The final M12 named virtual regression is recorded in its acceptance.':'Full final M12 qualification remains M12.18; later stages follow in order.'} Earlier M11 results do not qualify these new bytes. Read the matching release scope. Physical hardware, 3D and general Windows compatibility remain unqualified.`:'M12.0 is a design-only delivery. M12.1–M12.18 follow in order, each with scoped tests, guides and publication before the next begins. M11.6 remains the published native ISO and VMware package. Read its matching release scope. Qualification covers named virtual profiles; physical hardware, 3D and general Windows compatibility remain unqualified.'}),bottom,
 ]],{bg:{kind:'color',color:paper},padY:12});
 const footer=b('socialcircles',{copyright:'Engacer OS / MIT licensed · Documentation & releases on GitHub',bg:paper,circleBg:teal,items:[{label:'github',href:'https://github.com/enginsoysal/engacer-os'},{label:'website',href:`${site}/blog/documentation`}]});
 return [header,status,main,footer];
}
export function portalDesign({stage=0,searchReady=false,ownerIssues=JSON.parse(fs.readFileSync(new URL('../../docs/milestones/m13-progress.json',import.meta.url),'utf8')).owner_additions||[],stabilityQualification=JSON.parse(fs.readFileSync(new URL('../../docs/milestones/m13-progress.json',import.meta.url),'utf8')).stability_qualification}={}){
 if(!Number.isInteger(stage)||stage<0||stage>13)throw Error('Invalid qualified M13 stage');
 const current=stage?`M13.${stage}`:'M12.18';
 const stabilityWork=stage===12&&JSON.parse(fs.readFileSync(new URL('../../docs/milestones/m13-progress.json',import.meta.url),'utf8')).current_stage==='M13.13';
 const workdayQualified=stage===13&&workdayQualified13(stabilityQualification);
 const unstable=!workdayQualified&&stage>=7&&ownerIssues.some(issue=>issue.id==='long-uptime-freeze'&&issue.status!=='resolved');
 sequence=0;
 const header=b('menubrix',{brand:'E_  ENGACER OS',brandHref:'/',items:[{label:'Start here',href:'/blog/guide-start'},{label:'Install',href:'/blog/guide-install'},{label:'Use',href:'/blog/guide-use'},{label:'Customize',href:'/blog/guide-customize'},{label:'Downloads',href:'/blog/downloads'},{label:'Search',href:'/search'}],mode:'inline',width:'full',shape:'square',size:'l',bg:dark,textColor:'#d5e1e8',hoverColor:'#35ceba',blur:false,border:false,shadow:false});header.style={bg:{color:dark}};
 if(searchReady){header.props.documentationPortal=portalConfiguration();header.props.items=header.props.items.filter(item=>item.label!=='Search');header.props.bg=paper;header.props.textColor=ink;header.style.bg.color=paper;}
 const status=layout([[text('CURRENT DOWNLOAD · '+current,11,teal,{weight:600,py:6})],[text(workdayQualified?'EIGHT-HOUR VM WORKDAY QUALIFIED':unstable?(stage>=9?'STABILITY PENDING · TESTING ONLY':'KNOWN FREEZES · TESTING ONLY'):stage?`M13.${stage} · QUALIFIED STAGE DELIVERY`:'M13.0 · DESIGN & DOCUMENTATION PORTAL',11,muted,{align:'right',py:6})]],{bg:{kind:'color',color:'#eaf0f0'}});
 const hero=layout([[
 text('YOUR SPACE. YOUR SYSTEM.',11,teal,{weight:600,letterSpacing:'1.4px'}),heading('Start with what you want to do.',44,ink,{level:1,letterSpacing:'-1px'}),text('Install Engacer OS, find your way around the desktop, or make it yours. Current guides come first. Project history has its own place.',18),
 layout([[button('Download '+current+(unstable?' (testing only)':''),site+'/blog/downloads')],[button('Install Engacer OS →',site+'/blog/guide-install')],[button('Read the guide →',site+'/blog/documentation')]])
 ]],{padY:42});
 const choices=layout([
 card('01 / START HERE','A clear beginning','Understand the current release, what works and the first steps to take.','Get started →','guide-start'),
 card('02 / EVERYDAY USE','Feel at home','Find apps, switch windows, navigate folders and work with USB drives.','Use your desktop →','guide-use'),
 card('03 / YOUR CHOICES','Make it yours','Change supported preferences or build your own distribution.','Explore customization →','guide-customize')
 ],{bg:{kind:'color',color:'#ffffff'},border:1,borderColor:'#dbe3e6',divided:true,ruleColor:'#dbe3e6',radius:6,padY:22});choices.props.columns.forEach(c=>c.width=100/3);
 const reportedIssues=unstable?[b('alert',{variant:'info',title:stage>=9?'Stability qualification pending':'Known freezes: testing only',text:'Frequent freezes are reported on M13.8, following the earlier M13.7 report. Do not use this build for everyday work. Stability is not qualified. M13.9-M13.12 finish the product in order; M13.13 is the blocking eight-hour stability release gate. This download does not claim a fix.'})]:[];
 const main=layout([[
 hero,...reportedIssues,choices,heading(workdayQualified?'Next: hardware recognition.':stabilityWork?'Current work: stability qualification.':unstable?'Current work: desktop finishing.':'Next: a desktop that feels finished.',28,ink,{py:28}),text(workdayQualified?'M13.0-M13.13 is complete within its recorded scope. The frozen M13.13 candidate passed eight real hours in the named enabled-device VMware starter, including two uninterrupted idle hours, repeated desktop tasks and independent saved-data starts. Hardware recognition is the next priority. This is not universal hardware qualification or a diagnosis of the historical natural freezes.':stabilityWork?`${current} installation and desktop integration is complete within its recorded scope. M13.13 is now testing stability, including eight actual hours and two uninterrupted idle hours. This remains a testing download until that gate passes. Hardware expansion follows stability.`:unstable?`${current} is available for controlled testing only. M13.9-M13.12 are being completed in order. Stability work follows in M13.13. M13.13 must pass its eight-real-hour stability gate before hardware expansion. Historical task checks do not establish stability.`:stage?`M13.${stage} is the current scoped native delivery. Install its matching ISO or prepared VMware package, read its release guide and explore the documented changes. The M13.0–M13.13 program follows one published stage at a time; later hardware and Windows work remains separate.`:'M13.0 records the complete M13.0–M13.12 plan, original installation and desktop concepts, and the documentation/search design. It is design work, not a new native OS release. M12.18 remains the tested ISO and VMware download.',17),
 button('See the M13 plan and progress →',site+'/blog/docs-milestones-m13'),
 b('image',{url:stage?`https://raw.githubusercontent.com/enginsoysal/engacer-os/main/evidence/M13/${stage}/feature.png`:'https://raw.githubusercontent.com/enginsoysal/engacer-os/main/docs/architecture/figures/m13/desktop.svg',alt:stage?`Actual Engacer OS M13.${stage} native capture from the matching stage qualification.`:'Original M13.0 desktop and Files design concept. Proposed layout, not a native screenshot or implemented M13 behavior.',naturalSize:true,radius:8}),
 button('Explore all M13 concepts →',site+'/blog/docs-architecture-desktop-m13'),
 b('alert',{variant:'info',title:searchReady?'Find a guide without leaving this page':'Search redesign — design prototype',text:searchReady?'Use Search documentation or Ctrl+K. Current guides come first; include the archive when you want historical details. Articles keep task navigation alongside the text.':'Same-page search with keyboard navigation and archive filtering is specified and prototyped in M13.0. Production BrixCanvas still uses its existing Search page until the replacement is implemented and verified.'}),
 heading('Prefer to explore the project?',25),text('Current technical reference and the next plan are separate from earlier milestone and release records.',16),
 layout([[button('Project & development →',site+'/blog/guide-project',{bg:paper,color:teal})],[button('History & full reference →',site+'/blog/documentation-archive',{bg:paper,color:teal})]]),
 b('alert',{variant:'info',title:workdayQualified?'Named VMware workday qualified':unstable?'Stability is not qualified':'What is qualified today?',text:workdayQualified?'The exact enabled-device VMware starter passed the M13.13 workday gate. Historical natural-freeze causes remain unestablished; separately labelled injected recovery is not their reproduction. Physical hardware, vendor GPU 3D, general Windows compatibility and unlimited uptime are not qualified. Read the matching release and stability guide.':unstable?current+' is testing-only; stability qualification is scheduled for M13.13. Earlier M13.8 freeze observations remain documented. Historical named VM task checks do not establish a stable everyday system.':current+' is qualified for its named virtual-machine profiles. Physical hardware, GPU 3D and general Windows compatibility remain separate work. Read the matching release limits before testing.'})
 ]],{bg:{kind:'color',color:paper},padY:12});
 const footer=b('socialcircles',{copyright:'Engacer OS / MIT licensed · Current guides first, history separately archived.',bg:paper,circleBg:teal,items:[{label:'github',href:'https://github.com/enginsoysal/engacer-os'},{label:'website',href:site+'/blog/documentation'}]});
 return [header,status,main,footer];
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 const out=process.argv[2]||'build/brix/design';fs.mkdirSync(out,{recursive:true});
 const stageArg=process.argv.find(arg=>arg.startsWith('--stage='));
 portalDesign({stage:stageArg?Number(stageArg.split('=')[1]):0,searchReady:process.argv.includes('--search-ready')}).forEach((section,index)=>fs.writeFileSync(path.join(out,`${index+1}.json`),JSON.stringify({brixcanvas:1,section})));
 console.log('Prepared four native Brix clipboard payloads for the complete homepage.');
}
