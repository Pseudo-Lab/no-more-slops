(() => {
  const viewer=document.getElementById('image-viewer'),stage=document.getElementById('viewer-stage'),image=document.getElementById('viewer-image'),title=document.getElementById('viewer-title'),error=document.getElementById('viewer-error'),reviewStatus=document.getElementById('viewer-review-status');
  const buttons=Object.fromEntries([...viewer.querySelectorAll('[data-action]')].map(b=>[b.dataset.action,b]));
  let cards=[],index=0,mode='result',scale=1,x=0,y=0,opener=null,drag=null,epoch=0,oldOverflow='';
  const size=()=>({w:stage.clientWidth,h:stage.clientHeight});
  const fitScale=()=>Math.min(1,(size().w-24)/image.naturalWidth,(size().h-24)/image.naturalHeight);
  function paint(){
    if(!image.naturalWidth)return;
    const s=size(),w=image.naturalWidth*scale,h=image.naturalHeight*scale;
    x=w<=s.w?(s.w-w)/2:Math.max(s.w-w-60,Math.min(60,x));
    y=h<=s.h?(s.h-h)/2:Math.max(s.h-h-60,Math.min(60,y));
    image.style.width=image.naturalWidth+'px';image.style.height=image.naturalHeight+'px';
    image.style.transform=`translate(${x}px,${y}px) scale(${scale})`;
    document.getElementById('viewer-zoom').textContent=Math.round(scale*100)+'%';
  }
  function fit(){scale=fitScale();const s=size();x=(s.w-image.naturalWidth*scale)/2;y=(s.h-image.naturalHeight*scale)/2;paint();}
  function zoom(next,point){
    if(!image.naturalWidth||stage.getAttribute('aria-busy')==='true')return;
    const s=size(),p=point||{x:s.w/2,y:s.h/2};
    next=Math.max(Math.max(.01,fitScale()*.35),Math.min(6,next));
    x=p.x-(p.x-x)*next/scale;y=p.y-(p.y-y)*next/scale;scale=next;paint();
  }
  function load(reset){
    const card=cards[index],token=++epoch;
    if(mode==='result'&&!card.dataset.result)mode='original';
    if(mode==='baseline'&&!card.dataset.baseline)mode=card.dataset.result?'result':'original';
    if(mode==='review'&&!card.dataset.review)mode=card.dataset.result?'result':'original';
    title.textContent=card.querySelector('img').alt;
    document.getElementById('viewer-position').textContent=(index+1)+' / '+cards.length;
    buttons.previous.disabled=index===0;buttons.next.disabled=index===cards.length-1;
    buttons.result.disabled=!card.dataset.result;
    buttons.baseline.hidden=!card.dataset.baseline;
    buttons.baseline.setAttribute('aria-pressed',String(mode==='baseline'));
    buttons.review.hidden=!card.dataset.review;
    buttons.review.setAttribute('aria-pressed',String(mode==='review'));
    buttons.result.textContent=card.dataset.baseline?'개선 후':'추출 결과';
    buttons.original.setAttribute('aria-pressed',String(mode==='original'));buttons.result.setAttribute('aria-pressed',String(mode==='result'));
    const reviewCounts=[];
    if(/^\d+$/.test(card.dataset.reviewCount||''))reviewCounts.push('검토 필요 후보 '+Number(card.dataset.reviewCount).toLocaleString()+'개');
    if(/^\d+$/.test(card.dataset.unresolvedPorts||''))reviewCounts.push('접점 표시 '+Number(card.dataset.unresolvedPorts).toLocaleString()+'개');
    // Keep the summary's height stable while switching modes so the same
    // source coordinates remain at the same zoom and pan position.
    reviewStatus.hidden=!card.dataset.review;
    reviewStatus.textContent=reviewCounts.length?reviewCounts.join(', '):'검토가 필요한 경로';
    error.hidden=true;stage.setAttribute('aria-busy','true');
    image.onload=()=>{if(token!==epoch||!viewer.open)return;stage.setAttribute('aria-busy','false');reset?fit():paint();};
    image.onerror=()=>{if(token!==epoch||!viewer.open)return;stage.setAttribute('aria-busy','false');image.style.opacity='0';error.hidden=false;};
    const modeNames={baseline:'개선 전',result:'추출 결과',original:'원본',review:'검토 필요'};
    image.style.opacity='';image.alt=title.textContent+' '+modeNames[mode];image.src=card.dataset[mode];
  }
  function open(card){
    cards=[...document.querySelectorAll('article:not([hidden]) .preview')];index=cards.indexOf(card);if(index<0)return;
    opener=card;mode=card.dataset.result?'result':'original';oldOverflow=document.body.style.overflow;document.body.style.overflow='hidden';viewer.showModal();load(true);
  }
  function close(){++epoch;drag=null;stage.classList.remove('dragging');viewer.close();image.removeAttribute('src');document.body.style.overflow=oldOverflow;opener?.focus({preventScroll:true});}
  function navigate(step){const next=index+step;if(next<0||next>=cards.length)return;index=next;load(true);}
  document.querySelectorAll('.preview').forEach(card=>card.addEventListener('click',()=>open(card)));
  buttons.close.addEventListener('click',close);buttons.previous.addEventListener('click',()=>navigate(-1));buttons.next.addEventListener('click',()=>navigate(1));
  buttons['zoom-in'].addEventListener('click',()=>zoom(scale*1.4));buttons['zoom-out'].addEventListener('click',()=>zoom(scale/1.4));buttons.fit.addEventListener('click',fit);buttons.actual.addEventListener('click',()=>zoom(1));
  buttons.original.addEventListener('click',()=>{mode='original';load(false);});buttons.result.addEventListener('click',()=>{mode='result';load(false);});
  buttons.baseline.addEventListener('click',()=>{mode='baseline';load(false);});
  buttons.review.addEventListener('click',()=>{mode='review';load(false);});
  viewer.addEventListener('cancel',event=>{event.preventDefault();close();});
  viewer.addEventListener('click',event=>{const r=viewer.getBoundingClientRect();if(event.target===viewer&&(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom))close();});
  viewer.addEventListener('keydown',event=>{
    if(event.key==='ArrowLeft'){event.preventDefault();navigate(-1);}if(event.key==='ArrowRight'){event.preventDefault();navigate(1);}
    if(event.key==='+'||event.key==='='){event.preventDefault();zoom(scale*1.4);}if(event.key==='-'){event.preventDefault();zoom(scale/1.4);}if(event.key==='0'){event.preventDefault();zoom(1);}
  });
  stage.addEventListener('wheel',event=>{event.preventDefault();const r=stage.getBoundingClientRect();zoom(scale*Math.exp(-event.deltaY*.0015),{x:event.clientX-r.left,y:event.clientY-r.top});},{passive:false});
  stage.addEventListener('pointerdown',event=>{if(event.button!==0||stage.getAttribute('aria-busy')==='true')return;drag={id:event.pointerId,cx:event.clientX,cy:event.clientY,x,y};stage.setPointerCapture(event.pointerId);stage.classList.add('dragging');event.preventDefault();});
  stage.addEventListener('pointermove',event=>{if(!drag||event.pointerId!==drag.id)return;x=drag.x+event.clientX-drag.cx;y=drag.y+event.clientY-drag.cy;paint();});
  const stop=()=>{drag=null;stage.classList.remove('dragging');};stage.addEventListener('pointerup',stop);stage.addEventListener('pointercancel',stop);stage.addEventListener('lostpointercapture',stop);
  stage.addEventListener('dblclick',()=>{Math.abs(scale-fitScale())<.01?zoom(1):fit();});window.addEventListener('resize',()=>{if(viewer.open&&image.naturalWidth)fit();});
})();
