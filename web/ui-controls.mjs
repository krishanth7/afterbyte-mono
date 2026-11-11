export function initGroupPicker(){
  const select=document.getElementById('group');
  const picker=document.getElementById('group-picker');
  const trigger=document.getElementById('group-trigger');
  const list=document.getElementById('group-options');
  const value=document.getElementById('group-value');
  const options=[...select.options];
  let active=0,typeBuffer='',typeTimer;
  function highlight(index){
    active=(index+options.length)%options.length;
    [...list.children].forEach((item,i)=>item.classList.toggle('active-option',i===active));
    trigger.setAttribute('aria-activedescendant','group-option-'+options[active].value);
    list.children[active]?.scrollIntoView({block:'nearest'});
  }
  function close(){list.hidden=true;trigger.setAttribute('aria-expanded','false');trigger.removeAttribute('aria-activedescendant');}
  function sync(){
    active=select.selectedIndex;
    value.textContent=options[active].textContent;
    trigger.setAttribute('aria-valuetext',value.textContent);
    [...list.children].forEach((item,i)=>item.setAttribute('aria-selected',String(i===active)));
  }
  function open(){list.hidden=false;trigger.setAttribute('aria-expanded','true');highlight(select.selectedIndex);}
  function choose(index){select.value=options[index].value;select.dispatchEvent(new Event('change',{bubbles:true}));close();trigger.focus({preventScroll:true});}
  options.forEach((option,index)=>{
    const item=document.createElement('li');
    item.id='group-option-'+option.value;
    item.role='option';
    item.textContent=option.textContent;
    item.addEventListener('click',()=>choose(index));
    list.append(item);
  });
  trigger.addEventListener('click',()=>list.hidden?open():close());
  trigger.addEventListener('keydown',event=>{
    if(event.key==='Tab'){close();return;}
    if(event.key==='Escape'){event.preventDefault();close();return;}
    if(['ArrowDown','ArrowUp','Home','End','Enter',' '].includes(event.key)){
      event.preventDefault();
      if(list.hidden){open();return;}
      if(event.key==='Enter'||event.key===' '){choose(active);return;}
      highlight(event.key==='Home'?0:event.key==='End'?options.length-1:active+(event.key==='ArrowDown'?1:-1));
    }else if(event.key.length===1&&!event.ctrlKey&&!event.metaKey){
      event.preventDefault();
      typeBuffer+=event.key.toLowerCase();clearTimeout(typeTimer);typeTimer=setTimeout(()=>{typeBuffer='';},700);
      if(list.hidden)open();
      const index=options.findIndex(option=>option.textContent.toLowerCase().startsWith(typeBuffer));
      if(index>=0)highlight(index);
    }
  });
  select.addEventListener('change',sync);
  document.addEventListener('pointerdown',event=>{if(!picker.contains(event.target))close();});
  document.addEventListener('focusin',event=>{if(!picker.contains(event.target))close();});
  document.getElementById('group-label').setAttribute('for','group-trigger');
  trigger.setAttribute('aria-labelledby','group-label');
  sync();select.hidden=true;picker.hidden=false;
}
