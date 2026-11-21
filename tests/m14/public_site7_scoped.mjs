// Verify available public content/layouts while preserving reported platform limits.
import {createHash} from 'node:crypto';
import {createRequire} from 'node:module';
import path from 'node:path';
import {parseArgs} from 'node:util';
import {fileURLToPath} from 'node:url';
import fs from 'node:fs/promises';
const require=createRequire(process.env.ENGACER_PLAYWRIGHT_ROOT?path.resolve(process.env.ENGACER_PLAYWRIGHT_ROOT,'package.json'):import.meta.url);
const {chromium,expect}=require('@playwright/test');
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
const {values}=parseArgs({options:{source:{type:'string'},save:{type:'string'},payload:{type:'string'},output:{type:'string'}}});
const ref=values.source;if(!/^[0-9a-f]{40}$/.test(ref||''))throw Error('Exact documentation commit required');
const saved=JSON.parse(await fs.readFile(values.save,'utf8'));if(saved.source_commit!==ref||!saved.home.startsWith('Saved')||!saved.recovery.startsWith('Saved'))throw Error('Matching actual native Save evidence required');
const payload=JSON.parse(await fs.readFile(values.payload,'utf8'));if(payload.source_commit!==ref)throw Error('Publication source differs');
const guide=payload.page.blog.posts.find(p=>p.slug==='docs-handbook-install-m147');const guideRef=guide.meta.find(m=>m.key==='engine_source_commit').value;
const accepted=JSON.parse(await fs.readFile(root+'/evidence/M14/7/acceptance-results.json','utf8'));
const out=path.resolve(root,values.output||'build/m14-native/stage7/public-browser-scoped');if(!out.startsWith(path.resolve(root,'build/m14-native')+path.sep))throw Error('Owned M14 scratch required');await fs.mkdir(out,{recursive:true});
const browser=await chromium.launch({headless:true});const reports=[];let complete=false;
try{for(const width of [1280,390]){
 const page=await browser.newPage({viewport:{width,height:900},deviceScaleFactor:1});const errors=[];page.on('pageerror',e=>errors.push(String(e)));
 const home=await page.goto('https://engaceros.brixcanvas.com');if(home.status()!==200)throw Error('Home unavailable');await expect(page.locator('body')).toContainText('M14.7');await expect(page.locator('body')).toContainText('Engacer OS');
 await expect.poll(()=>page.locator('img').evaluateAll(rows=>rows.length>0&&rows.every(x=>x.complete&&x.naturalWidth>0))).toBe(true);
 const layout=await page.evaluate(()=>({viewport:innerWidth,document:document.documentElement.scrollWidth,images:[...document.images].map(x=>({src:x.currentSrc,loaded:x.complete&&x.naturalWidth>0}))}));if(layout.document>width)throw Error('Home horizontal overflow');
 const platform={search_opener_count:await page.getByRole('button',{name:'Search documentation',exact:true}).count(),mobile_menu_opener_count:await page.getByRole('button',{name:'Open menu',exact:true}).count()};let mobileMenuVerified=false;
 if(width<768&&platform.mobile_menu_opener_count===1){await page.getByRole('button',{name:'Open menu',exact:true}).click();await expect(page.getByRole('link',{name:'Install',exact:true})).toBeVisible();await page.getByRole('button',{name:'Close menu',exact:true}).click();mobileMenuVerified=true;}
 await page.screenshot({path:out+'/'+width+'-home.png',fullPage:true});
 for(const slug of ['documentation','guide-install','guide-use','guide-customize','documentation-archive']){const response=await page.goto('https://engaceros.brixcanvas.com/blog/'+slug);if(response.status()!==200)throw Error('Task route unavailable '+slug);await expect(page.locator('body')).toContainText('Engacer OS');}
 await page.goto('https://engaceros.brixcanvas.com/blog/docs-handbook-install-m147');await expect(page.getByRole('link',{name:'docs/handbook/install-m147.md',exact:true})).toHaveAttribute('href','https://github.com/enginsoysal/engacer-os/blob/'+guideRef+'/docs/handbook/install-m147.md');await expect(page.locator('body')).toContainText('Follow setup');await expect(page.locator('body')).toContainText('M14.7');await page.screenshot({path:out+'/'+width+'-current-guide.png',fullPage:true});
 await page.goto('https://engaceros.brixcanvas.com/blog/docs-handbook-files-m137');platform.task_sidebar_count=await page.getByRole('navigation',{name:'Documentation sections'}).count();platform.expected_task_next_count=await page.locator('a[href="/blog/docs-handbook-transfers-m137"]').filter({hasText:'Next article'}).count();
 await page.goto('https://engaceros.brixcanvas.com/blog/downloads');for(const name of ['EngacerOS-M14STAGE7.iso','EngacerOS-M14STAGE7-VMware.zip'])await expect(page.locator('a[href="https://github.com/enginsoysal/engacer-os/releases/download/m147-v0.14.7/'+name+'"]').first()).toBeVisible();await expect(page.locator('body')).toContainText(accepted.iso_sha256);await page.screenshot({path:out+'/'+width+'-downloads.png',fullPage:true});
 const missing=await page.goto('https://engaceros.brixcanvas.com/m14-missing-page-check');if(missing.status()!==404)throw Error('Recovery must retain HTTP404');await expect(page.locator('body')).toContainText('Engacer OS');if(errors.length)throw Error('Page runtime errors: '+errors.join('; '));
 reports.push({width,passed:true,layout,platform,mobile_menu_verified:mobileMenuVerified,page_errors:errors,checks:['current native homepage','loaded actual images','task routes and archive','exact guide source','matching ISO/VMware links and ISO checksum','404 recovery','no runtime errors']});await page.close();
}complete=true;}finally{await browser.close();const result={passed:complete&&reports.length===2,stage:'M14.7',build_id:accepted.build_id,source_commit:ref,observer_sha256:createHash('sha256').update(await fs.readFile(fileURLToPath(import.meta.url))).digest('hex'),owner_scope:'owner-publication-scope.json',full_public_site_qualified:false,native_editor_save:saved.home,recovery_editor_save:saved.recovery,production_search:false,task_sidebar:false,ordered_task_navigation:false,mobile_menu:reports.find(r=>r.width===390)?.mobile_menu_verified||false,current_guide:complete,matching_download:complete,desktop:reports.find(r=>r.width===1280)?.layout,mobile:reports.find(r=>r.width===390)?.layout,reports,limits:['Reported advanced search/sidebar/ordered article navigation are not qualified by this scoped observer. Their original strict failure remains preserved. No platform feature is relabelled as passed.']};await fs.writeFile(out+'/results.json',JSON.stringify(result,null,2)+'\n');}
console.log('PASS scoped public content/layout checks; advanced platform controls remain unqualified');
