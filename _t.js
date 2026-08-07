const fs=require('fs');const html=fs.readFileSync('ai-cost-calculator.html','utf8');
const s=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m=>m[1]).find(x=>x.includes('var COST'));
const st={};const el=id=>st[id]||(st[id]={value:'0',checked:false,innerHTML:''});global.document={getElementById:el};
el('modelSel').value='gpt-5-5';el('ctxTok').value='4000';el('inTok').value='2000';el('outTok').value='800';el('reqMo').value='10000';el('cacheChk').checked=false;
eval(s);console.log('GPT-5.5 no-cache:',el('costOut').innerHTML.replace(/<[^>]+>/g,' '));
el('cacheChk').checked=true;calcCost();console.log('GPT-5.5 cached :',el('costOut').innerHTML.replace(/<[^>]+>/g,' '));
