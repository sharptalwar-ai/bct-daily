"""Builds ../index.html from template.html + ../data/*.json. Run: python3 src/build.py"""
import json,os
H=os.path.dirname(os.path.abspath(__file__)); R=os.path.dirname(H)
page=open(os.path.join(H,'template.html')).read()
body,script=page.split('<script>'); script=script.split('</script>')[0]
data={f[:-5]:json.load(open(os.path.join(R,'data',f))) for f in sorted(os.listdir(os.path.join(R,'data'))) if f.endswith('.json')}
d3=open(os.path.join(H,'d3.min.js')).read()
shim='''const __files=%s;
const dash=(()=>{const calcs={},draws=[],memo={};
 const api={data(id){if(__files[id])return{status:'ok',data:__files[id]};if(calcs[id]){if(!(id in memo)){const c=calcs[id];memo[id]=c.fn(...c.inputs.map(i=>api.data(i).data));}return{status:'ok',data:memo[id]};}return{status:'missing',data:[]};},
  calc(id,o){calcs[id]=o},draw(name,fn){draws.push([name,fn]);},
  run(){for(const[name,fn]of draws)document.querySelectorAll('[data-draw="'+name+'"]').forEach(el=>{try{fn(el)}catch(e){console.error(name,e)}});}};
 return api;})();''' % json.dumps(data,ensure_ascii=False)
out=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow">
<title>Blumont Capital Tower — Daily Management Report</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet"></head><body>
{body}
<script>{d3}</script>
<script>{shim}
{script}
dash.run();let __t,__w=innerWidth;addEventListener('resize',()=>{{if(innerWidth===__w)return;__w=innerWidth;clearTimeout(__t);__t=setTimeout(dash.run,150)}});
</script></body></html>'''
open(os.path.join(R,'index.html'),'w').write(out); print('built',len(out))
