// A stage becomes a download only when its required public assets exist.
export function releaseLabel(release,stable,stageTag){
 if(release.tag_name==='m120-v0.12.0-design')return 'Design only — no ISO';
 if(release.prerelease)return /^m12/.test(release.tag_name)?'Development preview':'Historical preview';
 return stable?'Earlier release':release.tag_name===stageTag?'Latest stage delivery':'Latest stable';
}
export function stageRelease11(releases){
 for(const number of [6,5,4]){
  const tag=`m11${number}-v0.11.${number}`,image=`EngacerOS-M11${number===6?'FINAL':`STAGE${number}`}`;
  const release=releases.find(r=>r.tag_name===tag&&!r.draft&&!r.prerelease);
  if(!release)continue;
  const names=new Set(release.assets.map(a=>a.name));
  if(!names.has(image+'.iso')||!names.has(image+'-VMware.zip')||!names.has(`m11${number===6?'final':`stage${number}`}-build-manifest.json`))continue;
  return {id:`M11${number}`,label:`M11.${number}`,tag,image,guide:`install-m11${number}`};
 }
 return null;
}
export function stageRelease12(releases){
 for(let number=18;number>=1;number--){
  const tag=`m12${number}-v0.12.${number}`,image=`EngacerOS-M12STAGE${number}`;
  const release=releases.find(r=>r.tag_name===tag&&!r.draft&&!r.prerelease);
  if(!release)continue;
  const names=new Set(release.assets.map(a=>a.name));
  if(!names.has(image+'.iso')||!names.has(image+'-VMware.zip')||!names.has(`m12stage${number}-build-manifest.json`))continue;
  return {id:`M12${number}`,label:`M12.${number}`,tag,image,guide:`install-m12${number}`};
 }
 return null;
}

export function stageRelease13(releases){
 for(let number=13;number>=1;number--){
  const tag=`m13${number}-v0.13.${number}`,image=`EngacerOS-M13STAGE${number}`;
  const release=releases.find(r=>r.tag_name===tag&&!r.draft&&!r.prerelease);
  if(!release)continue;
  const names=new Set(release.assets.map(a=>a.name));
  if(!names.has(image+'.iso')||!names.has(image+'-VMware.zip')||!names.has(`m13stage${number}-build-manifest.json`))continue;
  return {id:`M13${number}`,label:`M13.${number}`,tag,image,guide:`install-m13${number}`};
 }
 return null;
}
