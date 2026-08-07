import os,zipfile
root='C:/Users/Administrator/WorkBuddy/2026-08-03-14-21-33/vibe-site'
out=os.path.join(root,'vibe-site-deploy.zip')
files=['site.css','og-image.png','ads.txt','robots.txt','data/models.json']
for f in os.listdir(root):
    if f.endswith('.html'): files.append(f)
    elif os.path.isdir(os.path.join(root,f)) and f not in ('__pycache__','data'):
        for g in os.listdir(os.path.join(root,f)):
            if g.endswith('.html'): files.append(f+'/'+g)
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
    for fp in files:
        p=os.path.join(root,fp)
        if os.path.exists(p): z.write(p,fp)
print('zip files:',len(files))
