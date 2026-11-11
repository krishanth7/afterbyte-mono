export async function initRepositoryStars(){
  const count=document.getElementById('github-star-count');
  const link=document.querySelector('.github-stars');
  if(!count||!link)return;
  function show(value){
    if(!Number.isSafeInteger(value)||value<0)return;
    count.textContent=new Intl.NumberFormat('en',{notation:'compact',maximumFractionDigits:1}).format(value);
    count.hidden=false;
    link.setAttribute('aria-label','Star Afterbyte Mono on GitHub · '+value.toLocaleString('en')+(value===1?' star':' stars'));
    link.title=value.toLocaleString('en')+(value===1?' GitHub star':' GitHub stars');
  }
  const key='afterbyte-repository-stars';
  try{const cached=JSON.parse(localStorage.getItem(key));if(cached&&Date.now()-cached.at<3600000){show(cached.count);return;}}catch{/* Storage is optional. */}
  const controller=new AbortController();
  const timer=setTimeout(()=>controller.abort(),5000);
  try{
    const response=await fetch('https://api.github.com/repos/krishanth7/afterbyte-mono',{signal:controller.signal,credentials:'omit',referrerPolicy:'no-referrer',headers:{Accept:'application/vnd.github+json'}});
    if(!response.ok)return;
    const data=await response.json();
    if(!Number.isSafeInteger(data.stargazers_count)||data.stargazers_count<0)return;
    show(data.stargazers_count);
    try{localStorage.setItem(key,JSON.stringify({count:data.stargazers_count,at:Date.now()}));}catch{/* The repository link remains usable. */}
  }catch{/* Network failures leave the GitHub link usable without a count. */}finally{clearTimeout(timer);}
}
