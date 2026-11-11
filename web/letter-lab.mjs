export function initLetterLab({sample, onTextChange}) {
  const board=document.querySelector('.letter-board');
  const status=document.getElementById('letter-status');
  const buttons=[...board.querySelectorAll('[data-letter]')];
  const states=buttons.map(button=>({button,x:0,y:0,angle:0,dragged:false,pointer:null}));
  const clamp=(value,min,max)=>Math.max(min,Math.min(max,value));
  function position(state,x,y){
    const tile=state.button;
    const margin=22;
    state.x=clamp(x,margin-tile.offsetLeft,board.clientWidth-tile.offsetLeft-tile.offsetWidth-margin);
    state.y=clamp(y,margin-tile.offsetTop,board.clientHeight-tile.offsetTop-tile.offsetHeight-margin);
    tile.style.setProperty('--drag-x',state.x+'px');
    tile.style.setProperty('--drag-y',state.y+'px');
  }
  for(const state of states){
    const button=state.button;
    button.addEventListener('pointerdown',event=>{
      if(event.button!==0)return;
      state.pointer={id:event.pointerId,startX:event.clientX,startY:event.clientY,originX:state.x,originY:state.y};
      state.dragged=false;
      button.setPointerCapture(event.pointerId);
      button.classList.add('dragging');
    });
    button.addEventListener('pointermove',event=>{
      if(!state.pointer||state.pointer.id!==event.pointerId)return;
      const dx=event.clientX-state.pointer.startX,dy=event.clientY-state.pointer.startY;
      if(Math.hypot(dx,dy)>5)state.dragged=true;
      if(state.dragged)position(state,state.pointer.originX+dx,state.pointer.originY+dy);
    });
    function release(event){
      if(!state.pointer||state.pointer.id!==event.pointerId)return;
      state.pointer=null;
      button.classList.remove('dragging');
      if(button.hasPointerCapture(event.pointerId))button.releasePointerCapture(event.pointerId);
      if(state.dragged)status.textContent='Letter '+button.dataset.letter+' moved. Use arrow keys to adjust its position.';
    }
    button.addEventListener('pointerup',release);
    button.addEventListener('pointercancel',release);
    button.addEventListener('lostpointercapture',()=>{state.pointer=null;button.classList.remove('dragging');});
    button.addEventListener('keydown',event=>{
      const moves={ArrowLeft:[-8,0],ArrowRight:[8,0],ArrowUp:[0,-8],ArrowDown:[0,8]};
      if(!moves[event.key])return;
      event.preventDefault();
      const [dx,dy]=moves[event.key];
      position(state,state.x+dx,state.y+dy);
      status.textContent='Letter '+button.dataset.letter+' moved.';
    });
    button.addEventListener('click',event=>{
      if(event.detail>0&&state.dragged){state.dragged=false;return;}
      const character=button.dataset.letter;
      if(sample.value.length+character.length>sample.maxLength){status.textContent='The tester is full. Remove some text to try another letter.';return;}
      sample.value+=character;
      onTextChange();
      status.textContent=character+' added to the type playground below.';
    });
  }
  let composition=0;
  const slots=[{x:.09,y:.17},{x:.49,y:.11},{x:.33,y:.51}];
  document.getElementById('shuffle-letters').addEventListener('click',()=>{
    composition=(composition+1)%3;
    states.forEach((state,index)=>{
      const slot=slots[(index+composition)%3];
      position(state,board.clientWidth*slot.x-state.button.offsetLeft,board.clientHeight*slot.y-state.button.offsetTop);
      state.angle=[-12,9,-5][(index+composition)%3];
      state.button.style.setProperty('--rotation',state.angle+'deg');
    });
    status.textContent='Composition shuffled. Drag a letter or click to try it.';
  });
  if('ResizeObserver'in window)new ResizeObserver(()=>states.forEach(state=>position(state,state.x,state.y))).observe(board);
}
