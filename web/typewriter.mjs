import { keyboardLayout, keyOutput } from './keyboard-layout.mjs';
export function initTypewriter(){
  const board=document.getElementById('typewriter');if(!board)return;
  const buttons=[...board.querySelectorAll('[data-code]')];
  const keys=new Map(buttons.map(button=>[button.dataset.code,button]));
  const layout=new Map(keyboardLayout.map(key=>[key.code,key]));
  const soundButton=document.getElementById('typewriter-sound');
  const status=document.getElementById('typewriter-status');
  const readout=document.getElementById('keyboard-readout');
  const releases=new Map(),held=new Set(),latched=new Set();
  const state={caps:false,num:true,scroll:false};
  let audio,noise,muted=false;
  const AudioEngine=window.AudioContext||window.webkitAudioContext;
  function shiftOn(){return held.has('ShiftLeft')||held.has('ShiftRight')||latched.has('ShiftLeft')||latched.has('ShiftRight');}
  function sync(){
    board.dataset.caps=String(state.caps);board.dataset.num=String(state.num);board.dataset.shift=String(shiftOn());
    for(const [code,on] of [['CapsLock',state.caps],['NumLock',state.num],['ScrollLock',state.scroll]]){
      keys.get(code).setAttribute('aria-pressed',String(on));keys.get(code).setAttribute('aria-label',code+' '+(on?'on':'off'));
      const led=board.querySelector('[data-led="'+code+'"]');led.dataset.on=String(on);led.querySelector('.lock-state').textContent=on?'ON':'OFF';
    }
    for(const key of keyboardLayout){const button=keys.get(key.code);
      if(key.kind==='modifier')button.setAttribute('aria-pressed',String(held.has(key.code)||latched.has(key.code)));
      if(/^Key/.test(key.code)){button.querySelector('.key-primary').textContent=keyOutput(key,{caps:state.caps,shift:shiftOn()});button.querySelector('.key-secondary').textContent=state.caps!==shiftOn()?key.label.toLowerCase():key.label;}
      if(key.shift){button.querySelector('.key-primary').textContent=shiftOn()?key.shift:key.label;button.querySelector('.key-secondary').textContent=shiftOn()?key.label:key.shift;}
    }
  }
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
  function press(code,physical=false){
    const button=keys.get(code),key=layout.get(code);if(!button)return;
    if(key.kind==='lock'){
      const field={CapsLock:'caps',NumLock:'num',ScrollLock:'scroll'}[code];state[field]=!state[field];status.textContent=key.label+' '+(state[field]?'on.':'off.');
    }
    if(key.kind==='modifier'){
      if(physical)held.add(code);else if(latched.has(code))latched.delete(code);else latched.add(code);
    }
    sync();
    const value=keyOutput(key,{caps:state.caps,shift:shiftOn(),num:state.num});
    readout.textContent=key.kind==='lock'?key.label.toUpperCase()+' '+(button.getAttribute('aria-pressed')==='true'?'ON':'OFF'):code==='Space'?'SPACE':code.includes('Enter')?'RETURN':value;
    board.dataset.lastKey=code;board.dataset.lastOutput=value;
    clearTimeout(releases.get(button));button.classList.add('key-down');
    board.querySelector('[data-link-code="'+code+'"]')?.classList.add('link-active');
    strikeSound(code.includes('Enter'));
    if(!physical)releases.set(button,setTimeout(()=>release(code),150));
  }
  function release(code){const button=keys.get(code);if(!button)return;clearTimeout(releases.get(button));releases.delete(button);button.classList.remove('key-down');board.querySelector('[data-link-code="'+code+'"]')?.classList.remove('link-active');held.delete(code);sync();}
  function clearKeys(){for(const code of keys.keys())release(code);}
  for(const button of buttons)button.addEventListener('click',()=>press(button.dataset.code));
  soundButton.addEventListener('click',()=>{
    muted=!muted;soundButton.setAttribute('aria-pressed',String(muted));soundButton.setAttribute('aria-label',muted?'Enable keyboard sound':'Mute keyboard sound');status.textContent=muted?'Keyboard sound off.':'Keyboard sound on.';
    if(muted&&audio?.state==='running')audio.suspend().catch(()=>{});
  });
  board.addEventListener('keydown',event=>{
    if(event.isComposing)return;
    if(event.key==='Tab'){if(!event.repeat)press('Tab');return;}
    if((event.altKey||event.ctrlKey||event.metaKey)&&layout.get(event.code)?.kind!=='modifier')return;
    if((event.key==='Enter'||event.key===' ')&&document.activeElement!==board)return;
    const code=event.code||[...layout.values()].find(key=>key.label.toLowerCase()===event.key.toLowerCase())?.code;
    if(!keys.has(code))return;
    event.preventDefault();if(event.repeat)return;
    press(code,true);
    if(code.startsWith('Arrow')){
      const current=layout.get(document.activeElement.dataset.code);
      const targets=keyboardLayout.filter(key=>!current||key.code!==current.code).filter(key=>!current||(code==='ArrowLeft'?key.x<current.x:code==='ArrowRight'?key.x>current.x:code==='ArrowUp'?key.y<current.y:key.y>current.y));
      if(current)targets.sort((a,b)=>{const distance=k=>code==='ArrowLeft'||code==='ArrowRight'?Math.abs(k.x-current.x)+Math.abs(k.y-current.y)*8:Math.abs(k.y-current.y)+Math.abs(k.x-current.x)*8;return distance(a)-distance(b);});
      keys.get(targets[0]?.code)?.focus({preventScroll:true});
    }
  });
  board.addEventListener('keyup',event=>release(event.code));
  board.addEventListener('focusout',event=>{if(!board.contains(event.relatedTarget))clearKeys();});
  window.addEventListener('blur',clearKeys);
  document.addEventListener('visibilitychange',()=>{if(document.hidden){clearKeys();if(audio?.state==='running')audio.suspend().catch(()=>{});}});
  new IntersectionObserver(entries=>{if(!entries[0].isIntersecting)clearKeys();},{threshold:.1}).observe(board);
  sync();
}
