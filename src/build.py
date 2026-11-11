import json,os,re
H=os.path.dirname(os.path.abspath(__file__)); R=os.path.dirname(H)
page=open(os.path.join(H,'template.html')).read().replace('<meta name="dash-one-writer">\n','')
body,script=page.split('<script>'); script=script.split('</script>')[0]
data={f[:-5]:json.load(open(os.path.join(R,'data',f))) for f in sorted(os.listdir(os.path.join(R,'data')))}
d3=open(os.path.join(H,'d3.min.js')).read()
tokens='''
:root{--color-fg:#1c1b19;--color-fg-muted:#6b675f;--color-bg:#faf8f4;--color-panel:#ffffff;--color-border-line:#e4dfd5;--color-ok:#2f7d57;--color-warn:#b06a12;--color-bad:#b3392f;
--font-anthropic-sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;--font-anthropic-serif:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif;
--cds-font-size-caption:12.5px;--cds-font-size-body:14.5px;--cds-font-size-heading:17px;--cds-font-size-title:24px;--cds-font-weight-medium:600;
--cds-gap-xs:4px;--cds-gap-sm:8px;--cds-gap-md:14px;--cds-gap-lg:24px;--cds-gap-xl:40px;--cds-pad-md:14px;--cds-pad-lg:20px;--cds-radius:12px;
--cds-chart-grid:#ece7dd;--cds-chart-axis:#cfc8ba;--cds-chart-reference:#a9a294;--cds-text-secondary:#6b675f;--cds-surface-popover:#ffffff;--cds-border:#e4dfd5;--cds-shadow-popover:0 6px 24px rgba(0,0,0,.12)}
@media (prefers-color-scheme:dark){:root{--color-fg:#f1eee8;--color-fg-muted:#a8a295;--color-bg:#171614;--color-panel:#201f1c;--color-border-line:#34322d;--color-ok:#5fbf8f;--color-warn:#e0a24a;--color-bad:#ea7a6f;--cds-chart-grid:#2b2925;--cds-chart-axis:#45423b;--cds-chart-reference:#6f6a5f;--cds-text-secondary:#a8a295;--cds-surface-popover:#262420;--cds-border:#3a3832;--cds-shadow-popover:0 6px 24px rgba(0,0,0,.5)}}
html{background:var(--color-bg)}body{margin:0;padding:clamp(18px,4vw,48px);font-size:var(--cds-font-size-body);background:var(--color-bg);color:var(--color-fg);-webkit-text-size-adjust:100%}
'''
shim='''
const __files=%s;
const dash=(()=>{const calcs={},draws=[],memo={};
 const api={colors:[matchMedia('(prefers-color-scheme:dark)').matches?'#d9a15a':'#9a5b1e',matchMedia('(prefers-color-scheme:dark)').matches?'#8fa3b5':'#5d7285'],
  data(id){if(__files[id])return{status:'ok',data:__files[id]};if(calcs[id]){if(!(id in memo)){const c=calcs[id];memo[id]=c.fn(...c.inputs.map(i=>api.data(i).data));}return{status:'ok',data:memo[id]};}return{status:'missing',data:[]};},
  calc(id,o){calcs[id]=o},draw(name,fn){if(fn)draws.push([name,fn]);},onData(fn){fn()},
  run(){for(const[name,fn]of draws)document.querySelectorAll('[data-draw="'+name+'"]').forEach(el=>{try{fn(el)}catch(e){console.error(name,e)}});}};
 return api;})();
''' % json.dumps(data,ensure_ascii=False)
out=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow">
<title>Blumont Capital Tower — Daily Management Report</title><style>{tokens}</style></head><body>
{body}
<script>{d3}</script>
<script>{shim}
{script}
dash.run();let __t;addEventListener('resize',()=>{{clearTimeout(__t);__t=setTimeout(dash.run,150)}});
</script></body></html>'''
open(os.path.join(R,'index.html'),'w').write(out); print(len(out))
