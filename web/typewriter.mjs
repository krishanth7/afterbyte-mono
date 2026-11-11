export function initTypewriter(){
  const board=document.getElementById('typewriter');
  if(!board)return;
  const buttons=[...board.querySelectorAll('button')];
  const soundButton=document.getElementById('typewriter-sound');
  const status=document.getElementById('typewriter-status');
  const keys=new Map([...board.querySelectorAll('[data-type-key]')].map(button=>[button.dataset.typeKey,button]));
  const releases=new Map();
  let audio,noise,muted=false;
  const AudioEngine=window.AudioContext||window.webkitAudioContext;
  const observer=new IntersectionObserver(entries=>{if(!entries[0].isIntersecting)clearKeys();},{threshold:.15});
  observer.observe(board);
  async function strikeSound(carriage=false){
    if(muted||!AudioEngine)return;
    try{
      if(!audio){
        audio=new AudioEngine();
        noise=audio.createBuffer(1,Math.ceil(audio.sampleRate*.11),audio.sampleRate);
        const samples=noise.getChannelData(0);for(let i=0;i<samples.length;i++)samples[i]=Math.random()*2-1;
      }
      if(audio.state==='suspended')await audio.resume();
      if(audio.state!=='running'||muted)return;
      board.dataset.audioState=audio.state;
      const time=audio.currentTime;
      const master=audio.createGain();master.gain.value=.22;master.connect(audio.destination);
      const impact=audio.createBufferSource();impact.buffer=noise;
      const filter=audio.createBiquadFilter();filter.type='bandpass';filter.frequency.value=carriage?1200:1900+Math.random()*400;filter.Q.value=.65;
      const envelope=audio.createGain();envelope.gain.setValueAtTime(.9,time);envelope.gain.exponentialRampToValueAtTime(.001,time+.075);
      impact.connect(filter).connect(envelope).connect(master);impact.start(time);impact.stop(time+.1);
      const metal=audio.createOscillator();metal.type='triangle';metal.frequency.setValueAtTime(carriage?1800:520+Math.random()*90,time);metal.frequency.exponentialRampToValueAtTime(carriage?1600:180,time+.055);
      const ring=audio.createGain();ring.gain.setValueAtTime(carriage?.17:.12,time);ring.gain.exponentialRampToValueAtTime(.001,time+(carriage?.22:.09));
      metal.connect(ring).connect(master);metal.start(time);metal.stop(time+(carriage?.24:.11));
      metal.onended=()=>{impact.disconnect();filter.disconnect();envelope.disconnect();metal.disconnect();ring.disconnect();master.disconnect();};
    }catch{/* Visual key feedback remains available if browser audio is unavailable. */}
  }
  function press(button,held=false){
    if(!button)return;
    clearTimeout(releases.get(button));button.classList.add('key-down');board.dataset.lastKey=button.dataset.typeKey;
    strikeSound(button.dataset.typeKey==='Enter');
    if(!held)releases.set(button,setTimeout(()=>{button.classList.remove('key-down');releases.delete(button);},150));
  }
  function clearKeys(){for(const timer of releases.values())clearTimeout(timer);releases.clear();buttons.forEach(button=>button.classList.remove('key-down'));}
  for(const button of buttons){
    button.addEventListener('click',()=>{
      if(button===soundButton){
        muted=!muted;soundButton.setAttribute('aria-pressed',String(muted));soundButton.setAttribute('aria-label',muted?'Enable keyboard sound':'Mute keyboard sound');status.textContent=muted?'Keyboard sound off.':'Keyboard sound on.';
        if(muted&&audio?.state==='running')audio.suspend().catch(()=>{});
      }else press(button);
    });
  }
  board.addEventListener('keydown',event=>{
    if(event.altKey||event.ctrlKey||event.metaKey||event.isComposing)return;
    if(['ArrowLeft','ArrowRight','ArrowUp','ArrowDown','Home','End'].includes(event.key)){
      event.preventDefault();const index=buttons.indexOf(document.activeElement);let next;
      if(event.key==='Home')next=0;else if(event.key==='End')next=buttons.length-1;
      else if(event.key==='ArrowUp'||event.key==='ArrowDown')next=Math.max(0,Math.min(buttons.length-1,index+(event.key==='ArrowUp'?-11:11)));
      else next=(Math.max(index,0)+(event.key==='ArrowRight'?1:-1)+buttons.length)%buttons.length;
      buttons[next].focus({preventScroll:true});return;
    }
    if(event.key==='Enter'&&document.activeElement!==board)return;
    if(event.key===' '&&document.activeElement!==board)return;
    const key=event.key.length===1?event.key.toUpperCase():event.key;
    if(keys.has(key)){event.preventDefault();if(!event.repeat)press(keys.get(key),true);}
  });
  board.addEventListener('keyup',event=>{const key=event.key.length===1?event.key.toUpperCase():event.key;keys.get(key)?.classList.remove('key-down');});
  board.addEventListener('focusout',event=>{if(!board.contains(event.relatedTarget))clearKeys();});
  window.addEventListener('blur',clearKeys);
  document.addEventListener('visibilitychange',()=>{if(document.hidden){clearKeys();if(audio?.state==='running')audio.suspend().catch(()=>{});}});
  // Physical input is scoped to this focused component; the rest of the page keeps its normal shortcuts.
}
