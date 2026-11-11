export function initializeEffects({motionStopped, sample, onTextChange}) {
  const $ = id => document.getElementById(id);
  document.querySelectorAll('[data-key]').forEach(button => button.addEventListener('click', () => {
    if (sample.value.length < sample.maxLength) sample.value += button.dataset.key;
    onTextChange();
    $('keyboard-status').textContent = (button.dataset.key === ' ' ? 'Space' : button.dataset.key) + ' added to the type tester.';
  }));
  $('key-delete').addEventListener('click', () => {
    sample.value = [...sample.value].slice(0, -1).join('');
    onTextChange();
    $('keyboard-status').textContent = 'Last character removed from the tester.';
  });

  const starsCanvas = $('starfield'), starsContext = starsCanvas.getContext('2d');
  starsCanvas.width = starsCanvas.height = 500;
  const stars = Array.from({length: 90}, () => ({x:Math.random()*500-250,y:Math.random()*500-250,z:Math.random()*500}));
  let starVisible = false, speed = .84;
  const observer = new IntersectionObserver(entries => { starVisible = entries[0].isIntersecting; });
  observer.observe(starsCanvas);
  $('frequency').addEventListener('input', () => { speed = Number($('frequency').value) / 100; });
  function paintStars(dt, moving) {
    if (!starsContext) return;
    const context = starsContext;
    context.fillStyle = '#222'; context.fillRect(0,0,500,500);
    context.strokeStyle = '#ffa133'; context.fillStyle = '#ffa133';
    for (const star of stars) {
      const oldZ = star.z;
      if (moving) star.z -= dt * .06 * speed;
      if (star.z < 1) { star.z = 500; star.x = Math.random()*500-250; star.y = Math.random()*500-250; }
      const x = 250 + star.x*250/star.z, y = 250 + star.y*250/star.z;
      const size = Math.min(3, 1.5*(1-star.z/500)+.3);
      context.globalAlpha = Math.max(.2,1-star.z/600);
      context.fillRect(x,y,size,size);
      if (moving && oldZ>star.z) {context.beginPath();context.moveTo(250+star.x*250/oldZ,250+star.y*250/oldZ);context.lineTo(x,y);context.stroke();}
    }
    context.globalAlpha = 1;
    context.beginPath();context.moveTo(235,250);context.lineTo(265,250);context.moveTo(250,235);context.lineTo(250,265);context.stroke();
  }
  paintStars(0,false);

  // Self-contained arcade specimen. Input is captured only while its canvas is focused.
  const canvas = $('breakout'), context = canvas.getContext('2d');
  let state = 'ready', score = 0, lives = 3, paddle = 390, direction = 0;
  let ball, bricks;
  const paddleWidth=120, paddleY=386, radius=7;
  function resetBall(){ball={x:450,y:350,vx:200,vy:-230};}
  function reset(){state='ready';score=0;lives=3;paddle=390;direction=0;resetBall();bricks=Array.from({length:40},(_,i)=>({x:24+(i%10)*86,y:35+Math.floor(i/10)*33,alive:true}));updateGame('Ready. Arrow keys or drag to move.');drawGame();}
  function updateGame(message){$('game-score').textContent='SCORE '+String(score).padStart(3,'0')+' / LIVES '+lives;$('game-status').textContent=message;$('game-start').textContent=state==='ready'?'Start game':state==='paused'?'Resume game':state==='running'?'Game running':'Play again';$('game-start').disabled=state==='running';$('game-pause').disabled=state!=='running';}
  function drawGame(){if(!context)return;context.fillStyle='#141414';context.fillRect(0,0,900,420);context.strokeStyle='#444';context.strokeRect(12,12,876,396);bricks.forEach((brick,i)=>{if(brick.alive){context.fillStyle=['#8a8a6f','#bccabb','#c0c0c0','#ffa133'][Math.floor(i/10)];context.fillRect(brick.x,brick.y,78,22);}});context.fillStyle='#eee';context.fillRect(paddle,paddleY,paddleWidth,9);context.fillStyle='#ffa133';context.beginPath();context.arc(ball.x,ball.y,radius,0,Math.PI*2);context.fill();}
  function stepGame(dt){
    paddle=Math.min(900-paddleWidth-16,Math.max(16,paddle+direction*480*dt));
    ball.x+=ball.vx*dt;ball.y+=ball.vy*dt;
    if((ball.x<19&&ball.vx<0)||(ball.x>881&&ball.vx>0))ball.vx*=-1;
    if(ball.y<19&&ball.vy<0)ball.vy*=-1;
    if(ball.vy>0&&ball.y+radius>=paddleY&&ball.y-radius<=paddleY+9&&ball.x>=paddle-radius&&ball.x<=paddle+paddleWidth+radius){ball.y=paddleY-radius;ball.vy=-Math.abs(ball.vy);ball.vx=((ball.x-paddle)/paddleWidth-.5)*420;}
    for(const brick of bricks){if(brick.alive&&ball.x+radius>brick.x&&ball.x-radius<brick.x+78&&ball.y+radius>brick.y&&ball.y-radius<brick.y+22){brick.alive=false;ball.vy*=-1;score+=10;updateGame('Keep going.');break;}}
    if(ball.y>430){lives--;if(!lives){state='over';updateGame('Game over. Play again to retry.');}else{resetBall();updateGame('Ball reset. '+lives+' lives remain.');}}
    if(bricks.every(brick=>!brick.alive)){state='won';updateGame('All blocks cleared. Well played.');}
    drawGame();
  }
  $('game-start').addEventListener('click',()=>{if(state==='over'||state==='won')reset();state='running';updateGame('Playing. Arrow keys or drag to move.');canvas.focus({preventScroll:true});});
  $('game-pause').addEventListener('click',()=>{state='paused';direction=0;updateGame('Paused. Choose Resume game to continue.');});
  $('game-reset').addEventListener('click',reset);
  canvas.addEventListener('keydown',event=>{if(event.key==='ArrowLeft'||event.key==='ArrowRight'){event.preventDefault();direction=event.key==='ArrowLeft'?-1:1;}});
  canvas.addEventListener('keyup',event=>{if(event.key==='ArrowLeft'||event.key==='ArrowRight'){event.preventDefault();direction=0;}});
  canvas.addEventListener('blur',()=>{direction=0;if(state==='running'){state='paused';updateGame('Paused when the game lost focus.');}});
  function movePaddle(event){const box=canvas.getBoundingClientRect();paddle=Math.max(16,Math.min(764,(event.clientX-box.left)/box.width*900-paddleWidth/2));drawGame();}
  canvas.addEventListener('pointerdown',event=>{canvas.focus({preventScroll:true});canvas.setPointerCapture(event.pointerId);movePaddle(event);});
  canvas.addEventListener('pointermove',event=>{if(event.buttons||event.pointerType==='mouse')movePaddle(event);});
  document.addEventListener('visibilitychange',()=>{if(document.hidden&&state==='running'){state='paused';direction=0;updateGame('Paused while the page was hidden.');}});
  reset();
  let previous=performance.now();
  function frame(now){const dt=Math.min((now-previous)/1000,.025);previous=now;if(!document.hidden){if(starVisible&&!motionStopped())paintStars(dt*1000,true);if(state==='running')stepGame(dt);}requestAnimationFrame(frame);}
  requestAnimationFrame(frame);
}
