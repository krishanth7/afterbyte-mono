export function initScenes(){
  const $=id=>document.getElementById(id);
  const names={interface:'AFTERBYTE / INTERFACE STUDY',code:'AFTERBYTE / CODE STUDY',editorial:'AFTERBYTE / EDITORIAL STUDY'};
  const tabs=[...document.querySelectorAll('[data-preview]')];
  document.querySelector('.preview-switch').setAttribute('role','tablist');
  function showScene(button){
    const scene=button.dataset.preview;
    tabs.forEach(tab=>{const selected=tab===button;tab.setAttribute('aria-selected',String(selected));tab.tabIndex=selected?0:-1;});
    Object.keys(names).forEach(name=>$('preview-'+name).hidden=name!==scene);
    $('preview-title').textContent=names[scene];
  }
  tabs.forEach((button,index)=>{
    button.id='scene-tab-'+button.dataset.preview;button.role='tab';button.removeAttribute('aria-pressed');
    button.setAttribute('aria-controls','preview-'+button.dataset.preview);
    const panel=$('preview-'+button.dataset.preview);panel.role='tabpanel';panel.setAttribute('aria-labelledby',button.id);
    button.addEventListener('click',()=>showScene(button));
    button.addEventListener('keydown',event=>{
      if(!['ArrowLeft','ArrowRight','Home','End'].includes(event.key))return;
      event.preventDefault();
      const next=event.key==='Home'?0:event.key==='End'?tabs.length-1:(index+(event.key==='ArrowRight'?1:-1)+tabs.length)%tabs.length;
      showScene(tabs[next]);tabs[next].focus({preventScroll:true});
    });
  });
  showScene(tabs[0]);
  const headings={overview:'Everything in order.',activity:'A little activity.',reports:'The bigger picture.',settings:'Make yourself at home.'};
  const views=[...document.querySelectorAll('[data-interface-view]')];
  function showView(button){
    const selected=button.dataset.interfaceView;
    views.forEach(item=>item.setAttribute('aria-pressed',String(item===button)));
    Object.keys(headings).forEach(name=>$('interface-'+name).hidden=name!==selected);
    $('interface-heading').textContent=selected==='overview'?$('workspace-name').value||headings.overview:headings[selected];
  }
  views.forEach(button=>button.addEventListener('click',()=>showView(button)));
  $('workspace-name').addEventListener('input',()=>{if(views[0].getAttribute('aria-pressed')==='true')$('interface-heading').textContent=$('workspace-name').value||headings.overview;});
  $('show-chart').addEventListener('change',()=>{$('project-chart').toggleAttribute('hidden',!$('show-chart').checked);});
  $('compact-demo').addEventListener('change',()=>{$('interface-overview').classList.toggle('compact-rows',$('compact-demo').checked);});
  $('download-report').addEventListener('click',()=>{
    const blob=new Blob(['Project,Status,Count\nDesign system,Complete,8\nCharacter library,Ready,2499\n'],{type:'text/csv;charset=utf-8'});
    const url=URL.createObjectURL(blob),link=document.createElement('a');
    link.href=url;link.download='afterbyte-sample-report.csv';link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
    $('report-status').textContent='Sample report downloaded. Demo data only.';
  });
  async function copy(text,status,message){try{await navigator.clipboard.writeText(text);$(status).textContent=message;}catch{$(status).textContent='Clipboard unavailable. Select and copy the editable text manually.';}}
  const originalCode=$('editable-code').value;
  $('editable-code').addEventListener('input',()=>{$('code-demo-status').textContent=$('editable-code').value.length+' characters / editable specimen. Code is not executed.';});
  $('reset-code').addEventListener('click',()=>{$('editable-code').value=originalCode;$('code-demo-status').textContent='Code specimen reset. Code is not executed.';});
  $('copy-code').addEventListener('click',()=>copy($('editable-code').value,'code-demo-status','Code text copied.'));
  const headline=$('editorial-headline'),body=$('editorial-body'),originalHeadline=headline.value,originalBody=body.value;
  const headlines=['A little type.\nA lot of possibility.','Good ideas\nstart with a letter.','Make something\nunmistakably yours.'];let headlineIndex=0;
  $('shuffle-headline').addEventListener('click',()=>{headline.value=headlines[headlineIndex++%headlines.length];$('editorial-status').textContent='Headline changed. Edit it to make it your own.';});
  for(const input of[headline,body])input.addEventListener('input',()=>{$('editorial-status').textContent='Editorial text updated locally.';});
  $('reset-editorial').addEventListener('click',()=>{headline.value=originalHeadline;body.value=originalBody;$('editorial-status').textContent='Editorial specimen reset.';});
  $('copy-editorial').addEventListener('click',()=>copy(headline.value+'\n\n'+body.value,'editorial-status','Editorial text copied.'));
}
