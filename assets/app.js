(function(){
var d=document,root=d.documentElement;
d.getElementById('themeBtn').onclick=function(){
  var cur=root.dataset.theme||(matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light');
  var n=cur==='dark'?'light':'dark';root.dataset.theme=n;try{localStorage.setItem('theme',n)}catch(e){}
};
var side=d.getElementById('side');
d.getElementById('menuBtn').onclick=function(){side.classList.toggle('open')};
d.addEventListener('click',function(e){if(side.classList.contains('open')&&!side.contains(e.target)&&!e.target.closest('#menuBtn'))side.classList.remove('open')});
d.querySelectorAll('.tabs').forEach(function(t){
  var btns=t.querySelectorAll(':scope>.tab-bar>.tab-btn'),ps=t.querySelectorAll(':scope>.tab-panel');
  btns.forEach(function(b,i){b.onclick=function(){btns.forEach(function(x,j){x.classList.toggle('on',i===j);ps[j].classList.toggle('on',i===j)})}});
});
var q=d.getElementById('q'),res=d.getElementById('results'),idx=window.SEARCH_INDEX||[];
function esc(s){return s.replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
q.addEventListener('input',function(){
  var v=q.value.trim().toLowerCase();if(!v){res.classList.remove('on');return}
  var words=v.split(/\s+/),out=[];
  idx.forEach(function(p){
    var hay=(p.t+' '+p.d+' '+p.x).toLowerCase(),s=0;
    for(var i=0;i<words.length;i++){if(hay.indexOf(words[i])<0){s=-1;break}
      s+=(p.t.toLowerCase().indexOf(words[i])>=0?10:0)+(p.d.toLowerCase().indexOf(words[i])>=0?3:1)}
    if(s>0)out.push([s,p]);
  });
  out.sort(function(a,b){return b[0]-a[0]});
  res.innerHTML=out.length?out.slice(0,8).map(function(r){var p=r[1];
    return '<a href="'+window.BASE+p.u+'"><b>'+esc(p.t)+'</b><small>'+esc(p.g)+' · '+esc(p.d.slice(0,90))+'</small></a>'}).join(''):'<a><b>'+(window.NO_RES||'No results')+'</b></a>';
  res.classList.add('on');
});
d.addEventListener('click',function(e){if(!e.target.closest('.search'))res.classList.remove('on')});
d.addEventListener('keydown',function(e){if(e.key==='/'&&d.activeElement!==q){e.preventDefault();q.focus()}});
})();
