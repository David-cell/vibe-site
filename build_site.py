# -*- coding: utf-8 -*-
"""Vibe Coding Tools static site generator (editorial bento design)."""
import os, html, json as _json

OUT = os.path.dirname(os.path.abspath(__file__))

# ---- model pricing/comparison data: externalized to data/models.json ----
# Edit data/models.json (prices, context, use tags) and rebuild to update.
# When connected to Git + Netlify, a push auto-rebuilds and deploys the change.
def load_models():
    p = os.path.join(OUT, 'data', 'models.json')
    with open(p, 'r', encoding='utf-8') as f:
        return _json.load(f)['models']
MODELS = load_models()

def model_options():
    return ''.join('<option value="%s">%s</option>\n' % (m['id'], html.escape(m['label'])) for m in MODELS)

def model_cost_js():
    parts = ["'%s':[%s,%s]" % (m['id'], repr(float(m['in'])), repr(float(m['out']))) for m in MODELS]
    return '{' + ', '.join(parts) + '}'

def model_compare_rows():
    rows = ''
    for m in MODELS:
        use = ','.join(m.get('use', []))
        rows += ('<tr data-use="%s"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>\n'
                 % (use, html.escape(m['label']), m['context'],
                    '%.2f' % float(m['in']), '%.2f' % float(m['out']), html.escape(m['best'])))
    return rows

# ---- tool registry: (slug, num, name, blurb) ----
TOOLS = [
  ('prompt-generator',        '01', 'Vibe Coding Prompt Builder', 'Turn a vague idea into a structured, copy-ready AI prompt.'),
  ('ai-cost-calculator',      '02', 'AI Cost Calculator',      'Estimate API spend before you generate. Tokens in, dollars out.'),
  ('model-compare',           '03', 'LLM Model Compare',       'Filter models by use case, context window, and price.'),
  ('claude-md-generator',     '04', 'CLAUDE.md Generator',     'Generate project rule files AI agents actually follow.'),
  ('project-brief-generator', '05', 'Project Brief Generator', 'Turn a vague idea into a brief any AI agent can build.'),
  ('ai-pr-review',            '06', 'AI PR Review Checklist',  'Catch scope creep, gaps, and vibe debt before merge.'),
  ('ai-security-checklist',   '07', 'AI Code Security Checklist', 'The pitfalls most often baked into AI code.'),
]
TOOL_BY_SLUG = {t[0]: t for t in TOOLS}

# Contact email used across Privacy / About / Contact pages.
# NOTE: ensure this mailbox can actually receive mail (set up forwarding on david-cells.com),
# or swap it for a real address you control.
CONTACT_EMAIL = 'hello@david-cells.com'

# ---- icon library: Stitch logos for 8 tools, SVG fallbacks for 2 ----
def ico_svg(path_inner, viewbox='0 0 80 80'):
    return ('<svg class="tico" viewBox="%s" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
            '<rect x="6" y="6" width="68" height="68" rx="14" fill="none" stroke="#1E3A2C" stroke-width="4"/>'
            '%s</svg>') % (viewbox, path_inner)

def ico_png(slug):
    return '<svg class="tico tico-img" viewBox="0 0 320 320" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true"><image href="icons/%s.png" xlink:href="icons/%s.png" width="320" height="320" preserveAspectRatio="xMidYMid meet"/></svg>' % (slug, slug)

# All 10 tools use transparent PNG logos (Stitch-generated + custom)
ICONS = {
  'prompt-generator':       ico_svg('<text x="40" y="55" font-size="38" text-anchor="middle" fill="#1E3A2C" font-family="JetBrains Mono, monospace">&#9998;</text>'),
  'ai-cost-calculator':     ico_svg('<text x="40" y="55" font-size="42" text-anchor="middle" fill="#1E3A2C" font-family="JetBrains Mono, monospace">$</text>'),
  'model-compare':          ico_svg('<text x="40" y="55" font-size="40" text-anchor="middle" fill="#1E3A2C" font-family="JetBrains Mono, monospace">&#8801;</text>'),
  'claude-md-generator':    ico_svg('<text x="40" y="55" font-size="30" text-anchor="middle" fill="#1E3A2C" font-family="JetBrains Mono, monospace">MD</text>'),
  'project-brief-generator': ico_svg('<text x="40" y="55" font-size="34" text-anchor="middle" fill="#1E3A2C" font-family="JetBrains Mono, monospace">&#128221;</text>'),
  'ai-pr-review':           ico_svg('<text x="40" y="55" font-size="34" text-anchor="middle" fill="#1E3A2C" font-family="JetBrains Mono, monospace">&#10003;</text>'),
  'ai-security-checklist':  ico_svg('<text x="40" y="55" font-size="34" text-anchor="middle" fill="#1E3A2C" font-family="JetBrains Mono, monospace">&#128274;</text>'),
}

# ---- sidebar ----
def side(prefix='', active_slug=None, page_id=''):
    items = ''
    home_active = ' class="active"' if page_id == 'home' else ''
    items += (f'<a class="home" href="{prefix}index.html"{home_active}">'
              f'<span class="n">⌂</span><span>Home</span></a>')
    for slug, num, name, _ in TOOLS:
        cls = ' class="active"' if slug == active_slug else ''
        items += f'<a href="{prefix}{slug}.html"{cls}><span class="n">{num}</span><span>{html.escape(name)}</span></a>'
    brand = (f'<a class="brand" href="{prefix}index.html">Vibe Coding Tools'
             f'<small>Issue 01 · client-side</small></a>')
    blog_href = 'index.html' if page_id == 'blog' else f'{prefix}blog/index.html'
    about_href = f'{prefix}about.html'
    contact_href = f'{prefix}contact.html'
    privacy_href = f'{prefix}privacy.html'
    about_active = ' class="active"' if page_id == 'about' else ''
    contact_active = ' class="active"' if page_id == 'contact' else ''
    return f'''
<aside class="side">
  {brand}
  <form class="search" onsubmit="return false">
    <span class="ico">⌕</span>
    <input id="sideSearch" type="search" placeholder="filter tools…" oninput="filterSide(this.value)"/>
  </form>
  <div class="sec">Tools</div>
  <nav class="tools" id="sideNav">{items}</nav>
  <div class="bottom">
    <a href="{blog_href}">Blog</a>
    <a href="{about_href}"{about_active}>About</a>
    <a href="{contact_href}"{contact_active}>Contact</a>
    <a href="{privacy_href}">Privacy</a>
  </div>
  <div class="mark">Vol. 01 / 2026 · MK</div>
</aside>
'''

SCRIPT_FILTER = '''
<script>
function filterSide(q){
  q=(q||'').toLowerCase();
  document.querySelectorAll('#sideNav a').forEach(function(a){
    var t=a.textContent.toLowerCase();
    a.style.display=(q===''||t.indexOf(q)>=0)?'':'none';
  });
}
function act(name){
  var f = window[name];
  if (typeof f === 'function') { f(); }
}
</script>
'''

# ---- shared head + footer ----
HEAD = ('<!DOCTYPE html>\n<html lang="en">\n<head>\n'
'<meta charset="UTF-8" />\n<meta name="viewport" content="width=device-width, initial-scale=1.0" />\n'
'<title>__TITLE__</title>\n'
'<meta name="description" content="__META__" />\n'
'<link rel="canonical" href="__CANON__" />\n'
'<meta property="og:type" content="website" />\n'
'<meta property="og:site_name" content="Vibe Coding Tools" />\n'
'<meta property="og:title" content="__TITLE__" />\n'
'<meta property="og:description" content="__META__" />\n'
'<meta property="og:url" content="__CANON__" />\n'
'<meta name="twitter:card" content="summary_large_image" />\n'
'<meta name="twitter:title" content="__TITLE__" />\n'
'<meta name="twitter:description" content="__META__" />\n'
'<meta property="og:image" content="https://vibe.david-cells.com/og-image.png" />\n'
'<meta property="og:image:width" content="1200" />\n'
'<meta property="og:image:height" content="630" />\n'
'<meta name="twitter:image" content="https://vibe.david-cells.com/og-image.png" />\n'
'<link rel="preconnect" href="https://fonts.googleapis.com" />\n'
'<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />\n'
'<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,900&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet" />\n'
'<link rel="stylesheet" href="__CSS__" />\n'
'<script type="application/ld+json">__SCHEMA__</script>\n'
'<!-- Impact affiliate tracking -->\n'
'<script type="text/javascript">(function(i,m,p,a,c,t){c.ire_o=p;c[p]=c[p]||function(){(c[p].a=c[p].a||[]).push(arguments)};t=a.createElement(m);var z=a.getElementsByTagName(m)[0];t.async=1;t.src=i;z.parentNode.insertBefore(t,z)})("https://utt.impactcdn.com/P-A7561863-6222-4288-a584-35c6fbb4048e1.js","script","impactStat",document,window);impactStat("transformLinks");impactStat("trackImpression");</script>\n'
'<!-- Google AdSense -->\n'
'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4110184622096343" crossorigin="anonymous"></script>\n'
'</head>\n<body>\n<div class="shell">\n')

TAIL = ('</div>\n' + SCRIPT_FILTER + '</body>\n</html>')

def footer(prefix=''):
    return f'''
<footer class="site">
  <div>Vibe Coding Tools · 100% client-side</div>
  <div><a href="{prefix}index.html">Tools</a><a href="{prefix}blog/index.html">Blog</a><a href="{prefix}about.html">About</a><a href="{prefix}contact.html">Contact</a><a href="{prefix}privacy.html">Privacy</a></div>
  <div class="aff-disclose">Some links on this site are affiliate links. See our <a href="{prefix}privacy.html">Privacy</a> note.</div>
  <div class="colophon">
    <a class="home-link" href="https://blog.david-cells.com" target="_blank" rel="noopener noreferrer">
      <svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 11l9-8 9 8"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/></svg>
      <span class="hl-text">My homepage</span><span class="hl-domain">blog.david-cells.com</span><span class="hl-arrow">&#8599;</span>
    </a>
  </div>
</footer>
'''

SHIELD = ('<div class="shield"><b>Private</b> Everything runs in your browser. '
          'No uploads, no tracking, no signup.'
          '<span class="x">/ zero data collected</span></div>')

CAPTURE = ''

# ============================================================
# AFFILIATE / SPONSORED RECOMMENDATIONS
# Replace the placeholder referral IDs below with your real affiliate IDs.
# All links use rel="sponsored nofollow" + a visible "Sponsored" tag to stay
# FTC- and Google-compliant. WorldFirst receives the USD payouts.
# ============================================================
AFF_BY_POST = {
  'client-side-vs-server-side': [
    ('Vercel', 'https://vercel.com/?utm_source=devtoolbox&utm_campaign=affiliate',
     'Ship a client-side app like this one in minutes — global CDN, zero config, preview deploys on every PR.',
     'Free Hobby plan', 'Deploy for free'),
    ('Hostinger', 'https://www.hostinger.com?REFERRALCODE=YRADYW125Y5G',
     'Fast, reliable hosting with a free domain included — perfect for your first real project.',
     '20% off your first plan', 'Claim 20% off'),
  ],
  'debug-jwt-no-backend': [
    ('DigitalOcean', 'https://m.do.co/c/176fce64642a',
     'Spin up a VPS or managed database in under a minute. Predictable pricing from $4/mo, pay as you grow.',
     'Free $200 credit for new users', 'Claim $200 credit'),
  ],
  'best-ai-cost-calculators': [
    ('DigitalOcean', 'https://m.do.co/c/176fce64642a',
     'Self-host an API that formats and validates JSON at scale — built by developers, for developers.',
     'Free $200 credit for new users', 'Claim $200 credit'),
  ],
}

def aff_callout(items):
    rows = ''
    for label, url, blurb, perk, cta in items:
        rows += (f'<li class="aff-item">'
                 f'<div class="aff-item-top"><span class="aff-brand">{html.escape(label)}</span>'
                 f'<span class="aff-perk">&#9733; {html.escape(perk)}</span></div>'
                 f'<p class="aff-blurb">{html.escape(blurb)}</p>'
                 f'<a class="aff-btn" href="{url}" target="_blank" rel="sponsored nofollow noopener">'
                 f'{html.escape(cta)} <span class="aff-arrow">&#8594;</span></a>'
                 f'</li>')
    return (f'<div class="aff-box"><div class="aff-head">'
            f'<span class="aff-tag">Sponsored</span>'
            f'<span class="aff-title">Tools this article was built with</span></div>'
            f'<ul class="aff-list">{rows}</ul>'
            f'<p class="aff-note">Vibe Coding Tools may earn a commission when you sign up via these links — '
            f'at no extra cost to you. We only recommend tools we actually use.</p></div>')


# ---- schema ----
def webapp_schema(name, slug, features):
    return ('{"@context":"https://schema.org","@type":"WebApplication","name":"' + name.replace('"','\\"') +
        '","url":"https://vibe.david-cells.com/' + slug + '.html","applicationCategory":"DeveloperApplication",'
        '"operatingSystem":"Any","offers":{"@type":"Offer","price":"0","priceCurrency":"USD"},'
        '"featureList":"' + features.replace('"','\\"') + '","browserRequirements":"Requires JavaScript"}')

def page(title, meta, schema, body_main, active_slug=None, prefix='', page_id='', url='https://vibe.david-cells.com/'):
    h = (HEAD.replace('__TITLE__', title).replace('__META__', meta)
            .replace('__SCHEMA__', schema).replace('__CSS__', prefix + 'site.css')
            .replace('__CANON__', url))
    return h + side(prefix, active_slug, page_id) + main_shell(body_main) + TAIL

def main_shell(content):
    return '<main>' + content + '</main>'

# ============================================================
# INDEX (dashboard)
# ============================================================
# ============================================================
# SHARED NEO-BRUTALIST SHELL — used by EVERY page (incl. home)
# ============================================================
TW_CONFIG = r'''
tailwind.config = {
  darkMode: "class",
  theme: {
    extend: {
      "colors": {
        "on-secondary-fixed-variant":"#00530e","on-primary":"#393000","secondary-fixed":"#72ff70",
        "tertiary-fixed":"#5df7ff","inverse-on-surface":"#343024","on-error-container":"#ffdad6",
        "secondary":"#ecffe3","on-background":"#e9e2cf","on-tertiary-fixed":"#002021",
        "tertiary-container":"#1bf6ff","secondary-fixed-dim":"#00e639","surface-bright":"#3d392c",
        "primary-fixed-dim":"#e3c600","glass-tint":"rgba(255, 255, 255, 0.1)","secondary-container":"#13ff43",
        "on-tertiary-fixed-variant":"#004f52","background":"#161308","tertiary-fixed-dim":"#00dce4",
        "surface-container":"#222014","on-secondary":"#003907","surface-container-highest":"#383528",
        "on-primary-container":"#716200","surface-tint":"#e3c600","swiss-accent":"#E63946",
        "on-surface-variant":"#cfc6ab","on-primary-fixed":"#211b00","on-tertiary-container":"#006d71",
        "inverse-primary":"#6d5e00","error":"#ffb4ab","on-tertiary":"#003739","inverse-surface":"#e9e2cf",
        "surface-container-lowest":"#100e05","cyber-green":"#00FF41","outline":"#989177",
        "on-primary-fixed-variant":"#524600","surface":"#161308","primary-fixed":"#ffe24a",
        "retro-gray":"#C0C0C0","brutalist-yellow":"#FFDE00","surface-dim":"#161308","on-error":"#690005",
        "on-secondary-container":"#007117","primary-container":"#ffde00","tertiary":"#eeffff",
        "error-container":"#93000a","surface-variant":"#383528","primary":"#fffaf8",
        "surface-container-low":"#1e1c10","outline-variant":"#4c4732","surface-container-high":"#2d2a1d",
        "on-surface":"#e9e2cf","on-secondary-fixed":"#002203"
      },
      "borderRadius": {"DEFAULT":"0.125rem","lg":"0.25rem","xl":"0.5rem","full":"0.75rem"},
      "spacing": {"base":"4px","gap-md":"2rem","gap-lg":"4rem","gap-sm":"1rem","gap-xs":"0.5rem","sidebar-width":"280px","container-max":"1280px"},
      "fontFamily": {
        "display-lg":["Fraunces"],"display-lg-mobile":["Fraunces"],"body-md":["Inter"],
        "headline-md":["Fraunces"],"headline-sm":["Fraunces"],"label-caps":["JetBrains Mono"],
        "code-ui":["JetBrains Mono"],"body-lg":["Inter"]
      },
      "fontSize": {
        "display-lg":["48px",{"lineHeight":"1.1","letterSpacing":"-0.02em","fontWeight":"900"}],
        "display-lg-mobile":["32px",{"lineHeight":"1.1","fontWeight":"900"}],
        "body-md":["16px",{"lineHeight":"1.5","fontWeight":"400"}],
        "headline-md":["32px",{"lineHeight":"1.2","fontWeight":"600"}],
        "headline-sm":["24px",{"lineHeight":"1.3","fontWeight":"500"}],
        "label-caps":["12px",{"lineHeight":"1","letterSpacing":"0.05em","fontWeight":"600"}],
        "code-ui":["14px",{"lineHeight":"1.4","fontWeight":"400"}],
        "body-lg":["18px",{"lineHeight":"1.6","fontWeight":"400"}]
      },
      "boxShadow": {"brutal":"4px 4px 0px #000000","brutal-hover":"2px 2px 0px #000000"}
    }
  }
}'''

HEAD_BRU = ('''<!DOCTYPE html>
<html class="dark" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>__TITLE__</title>
<meta name="description" content="__META__"/>
<link rel="canonical" href="__CANON__"/>
<meta property="og:type" content="website"/>
<meta property="og:site_name" content="Vibe Coding Tools"/>
<meta property="og:title" content="__TITLE__"/>
<meta property="og:description" content="__META__"/>
<meta property="og:url" content="__CANON__"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="__TITLE__"/>
<meta name="twitter:description" content="__META__"/>
<meta property="og:image" content="https://vibe.david-cells.com/og-image.png"/>
<meta property="og:image:width" content="1200"/>
<meta property="og:image:height" content="630"/>
<meta name="twitter:image" content="https://vibe.david-cells.com/og-image.png"/>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<script id="tailwind-config">__TW_CONFIG__</script>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,900&family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet"/>
<link rel="stylesheet" href="__CSS__"/>
<script type="application/ld+json">__SCHEMA__</script>
<script type="text/javascript">(function(i,m,p,a,c,t){c.ire_o=p;c[p]=c[p]||function(){(c[p].a=c[p].a||[]).push(arguments)};t=a.createElement(m);var z=a.getElementsByTagName(m)[0];t.async=1;t.src=i;z.parentNode.insertBefore(t,z)})("https://utt.impactcdn.com/P-A7561863-6222-4288-a584-35c6fbb4048e1.js","script","impactStat",document,window);impactStat("transformLinks");impactStat("trackImpression");</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4110184622096343" crossorigin="anonymous"></script>
</head>''')

ICON = {
  'prompt-generator':'edit_note',
  'ai-cost-calculator':'calculate',
  'model-compare':'database',
  'claude-md-generator':'description',
  'project-brief-generator':'assignment',
  'ai-pr-review':'rate_review',
  'ai-security-checklist':'security',
}

def brutal_sidenav(active_slug=None, page_id='', prefix=''):
    nav = ''
    home_cls = 'bg-black text-[#FFDE00]' if page_id=='home' else 'hover:bg-black hover:text-[#FFDE00]'
    nav += ('<a class="flex items-center gap-sm %s p-3 brutal-border border-transparent transition-colors" href="%sindex.html">'
            '<span class="material-symbols-outlined">home</span>'
            '<span class="font-label-caps text-label-caps font-bold">Home</span></a>') % (home_cls, prefix)
    for slug, num, name, blurb in TOOLS:
        cls = 'bg-black text-[#FFDE00]' if slug==active_slug else 'hover:bg-black hover:text-[#FFDE00]'
        nav += ('<a class="flex items-center gap-sm text-black p-3 %s brutal-border border-transparent transition-colors" href="%s%s.html">'
                '<span class="material-symbols-outlined">%s</span>'
                '<span class="font-label-caps text-label-caps font-bold">%s</span></a>') % (cls, prefix, slug, ICON[slug], html.escape(name))
    def meta_cls(pid):
        return 'bg-black text-[#FFDE00]' if page_id==pid else 'hover:bg-black hover:text-[#FFDE00]'
    blog = ('<a class="flex items-center gap-sm text-black p-3 %s brutal-border border-transparent transition-colors" href="%sblog/index.html"><span class="material-symbols-outlined">article</span><span class="font-label-caps text-label-caps font-bold">Blog</span></a>') % (meta_cls('blog'), prefix)
    about = ('<a class="flex items-center gap-sm text-black p-3 %s brutal-border border-transparent transition-colors" href="%sabout.html"><span class="material-symbols-outlined">info</span><span class="font-label-caps text-label-caps font-bold">About</span></a>') % (meta_cls('about'), prefix)
    contact = ('<a class="flex items-center gap-sm text-black p-3 %s brutal-border border-transparent transition-colors" href="%scontact.html"><span class="material-symbols-outlined">mail</span><span class="font-label-caps text-label-caps font-bold">Contact</span></a>') % (meta_cls('contact'), prefix)
    privacy = ('<a class="flex items-center gap-sm text-black p-3 %s brutal-border border-transparent transition-colors" href="%sprivacy.html"><span class="material-symbols-outlined">security</span><span class="font-label-caps text-label-caps font-bold">Privacy</span></a>') % (meta_cls('privacy'), prefix)
    return ('''<nav class="hidden md:flex flex-col h-full w-[280px] bg-[#FFDE00] border-r-4 border-[#100e05] py-gap-sm px-gap-xs fixed left-0 top-0 z-50 text-black">
  <div class="mb-gap-md px-3 flex flex-col gap-2">
    <div class="flex items-center gap-3">
      <div class="w-12 h-12 bg-black flex items-center justify-center brutal-shadow">
        <span class="material-symbols-outlined text-[#FFDE00]" style="font-variation-settings: 'FILL' 1;">terminal</span>
      </div>
      <div>
        <h1 class="font-display-lg text-display-lg-mobile text-black uppercase">Vibe Coding</h1>
        <p class="font-label-caps text-label-caps text-black font-bold">Issue 01 · Client-Side</p>
      </div>
    </div>
    <div class="mt-4 bg-black text-[#FFDE00] font-label-caps text-label-caps uppercase p-2 inline-block border-2 border-black w-max">[PRIVATE ACCESS]</div>
  </div>
  <button class="mb-gap-sm mx-3 bg-white text-black font-label-caps text-label-caps uppercase p-3 brutal-border brutal-shadow brutal-hover transition-all flex items-center justify-center gap-2 font-bold">
    <span class="material-symbols-outlined">add</span> All Tools
  </button>
  <div class="flex-1 overflow-y-auto space-y-2 mt-4">
    __NAV__
  </div>
  <div class="mt-auto pt-gap-sm space-y-2">
    __META__
  </div>
</nav>''').replace('__NAV__', nav).replace('__META__', blog + about + contact + privacy)

def brutal_topbar(prefix=''):
    return ('''<header class="flex justify-between items-center h-16 px-gap-md bg-surface shrink-0 z-40 border-b-4 border-[#100e05]">
    <button class="md:hidden text-primary p-2 brutal-border bg-brutalist-yellow text-black brutal-shadow">
      <span class="material-symbols-outlined">menu</span>
    </button>
    <div class="flex items-center gap-gap-md">
      <span class="font-display-lg-mobile text-display-lg-mobile font-black text-on-surface tracking-tighter uppercase">Vibe Coding Tools</span>
      <div class="hidden md:flex gap-4">
        <a class="font-label-caps text-label-caps text-brutalist-yellow uppercase underline decoration-2 underline-offset-4" href="__P__blog/index.html">Blog</a>
        <a class="font-label-caps text-label-caps text-on-surface-variant hover:text-brutalist-yellow uppercase" href="__P__about.html">About</a>
      </div>
    </div>
    <div class="flex items-center gap-4">
      <a class="font-label-caps text-label-caps bg-brutalist-yellow text-black px-4 py-2 brutal-border brutal-shadow brutal-hover uppercase font-bold hidden sm:block" href="__P__contact.html">Feedback</a>
      <div class="flex gap-2">
        <button class="w-10 h-10 flex items-center justify-center bg-surface-container-highest brutal-border text-on-surface brutal-hover">
          <span class="material-symbols-outlined">dark_mode</span>
        </button>
        <button class="w-10 h-10 flex items-center justify-center bg-brutalist-yellow text-black brutal-border brutal-shadow brutal-hover">
          <span class="material-symbols-outlined">account_circle</span>
        </button>
      </div>
    </div>
  </header>''').replace('__P__', prefix)

def brutal_footer(prefix=''):
    return ('''<footer class="bg-surface-container-lowest border-t-4 border-[#100e05] py-gap-md px-gap-lg flex flex-col md:flex-row justify-between items-center gap-4 shrink-0">
    <span class="font-label-caps text-label-caps text-on-surface-variant uppercase font-bold">© 2026 Vibe Coding Tools. Zero data collected.</span>
    <div class="flex gap-4">
      <a class="font-label-caps text-label-caps text-on-surface-variant hover:text-brutalist-yellow uppercase transition-colors" href="__P__index.html">Tools</a>
      <a class="font-label-caps text-label-caps text-on-surface-variant hover:text-brutalist-yellow uppercase transition-colors" href="__P__blog/index.html">Blog</a>
      <a class="font-label-caps text-label-caps text-on-surface-variant hover:text-brutalist-yellow uppercase transition-colors" href="__P__about.html">About</a>
      <a class="font-label-caps text-label-caps text-on-surface-variant hover:text-brutalist-yellow uppercase transition-colors" href="__P__contact.html">Contact</a>
      <a class="font-label-caps text-label-caps text-on-surface-variant hover:text-brutalist-yellow uppercase transition-colors" href="__P__privacy.html">Privacy</a>
    </div>
  </footer>''').replace('__P__', prefix)

def page_brutalist(title, meta, schema, active_slug=None, page_id='', body='', url='https://vibe.david-cells.com/', prefix=''):
    head = (HEAD_BRU.replace('__TITLE__', title).replace('__META__', meta)
            .replace('__CANON__', url).replace('__SCHEMA__', schema)
            .replace('__CSS__', prefix + 'brutal.css').replace('__TW_CONFIG__', TW_CONFIG))
    chrome = ('<body class="bg-background text-on-surface font-body-md h-screen overflow-hidden flex selection:bg-brutalist-yellow selection:text-black">\n'
              + brutal_sidenav(active_slug, page_id, prefix)
              + '<div class="flex-1 flex flex-col md:ml-[280px] h-screen overflow-hidden bg-background">\n'
              + brutal_topbar(prefix)
              + '<main class="flex-1 overflow-y-auto p-gap-md lg:p-gap-lg"><div class="max-w-container-max mx-auto space-y-6">\n'
              + body
              + '\n</div></main>\n'
              + brutal_footer(prefix)
              + '</div>\n</body></html>')
    return head + chrome

def build_index():
    meta = 'Free, privacy-first vibe coding tools: a prompt builder, an AI cost calculator, an LLM model compare, a CLAUDE.md generator, a project brief generator, and AI code review + security checklists. 100% client-side.'
    schema = ('{"@context":"https://schema.org","@type":"WebSite","name":"Vibe Coding Tools","url":"https://vibe.david-cells.com/",'
              '"description":"Free, privacy-first online developer tools. Everything runs in your browser."}')

    # --- Neo-Brutalist homepage (self-contained: Tailwind CDN + template config + fonts) ---
    TW_CONFIG = r'''
tailwind.config = {
  darkMode: "class",
  theme: {
    extend: {
      "colors": {
        "on-secondary-fixed-variant":"#00530e","on-primary":"#393000","secondary-fixed":"#72ff70",
        "tertiary-fixed":"#5df7ff","inverse-on-surface":"#343024","on-error-container":"#ffdad6",
        "secondary":"#ecffe3","on-background":"#e9e2cf","on-tertiary-fixed":"#002021",
        "tertiary-container":"#1bf6ff","secondary-fixed-dim":"#00e639","surface-bright":"#3d392c",
        "primary-fixed-dim":"#e3c600","glass-tint":"rgba(255, 255, 255, 0.1)","secondary-container":"#13ff43",
        "on-tertiary-fixed-variant":"#004f52","background":"#161308","tertiary-fixed-dim":"#00dce4",
        "surface-container":"#222014","on-secondary":"#003907","surface-container-highest":"#383528",
        "on-primary-container":"#716200","surface-tint":"#e3c600","swiss-accent":"#E63946",
        "on-surface-variant":"#cfc6ab","on-primary-fixed":"#211b00","on-tertiary-container":"#006d71",
        "inverse-primary":"#6d5e00","error":"#ffb4ab","on-tertiary":"#003739","inverse-surface":"#e9e2cf",
        "surface-container-lowest":"#100e05","cyber-green":"#00FF41","outline":"#989177",
        "on-primary-fixed-variant":"#524600","surface":"#161308","primary-fixed":"#ffe24a",
        "retro-gray":"#C0C0C0","brutalist-yellow":"#FFDE00","surface-dim":"#161308","on-error":"#690005",
        "on-secondary-container":"#007117","primary-container":"#ffde00","tertiary":"#eeffff",
        "error-container":"#93000a","surface-variant":"#383528","primary":"#fffaf8",
        "surface-container-low":"#1e1c10","outline-variant":"#4c4732","surface-container-high":"#2d2a1d",
        "on-surface":"#e9e2cf","on-secondary-fixed":"#002203"
      },
      "borderRadius": {"DEFAULT":"0.125rem","lg":"0.25rem","xl":"0.5rem","full":"0.75rem"},
      "spacing": {"base":"4px","gap-md":"2rem","gap-lg":"4rem","gap-sm":"1rem","gap-xs":"0.5rem","sidebar-width":"280px","container-max":"1280px"},
      "fontFamily": {
        "display-lg":["Fraunces"],"display-lg-mobile":["Fraunces"],"body-md":["Inter"],
        "headline-md":["Fraunces"],"headline-sm":["Fraunces"],"label-caps":["JetBrains Mono"],
        "code-ui":["JetBrains Mono"],"body-lg":["Inter"]
      },
      "fontSize": {
        "display-lg":["48px",{"lineHeight":"1.1","letterSpacing":"-0.02em","fontWeight":"900"}],
        "display-lg-mobile":["32px",{"lineHeight":"1.1","fontWeight":"900"}],
        "body-md":["16px",{"lineHeight":"1.5","fontWeight":"400"}],
        "headline-md":["32px",{"lineHeight":"1.2","fontWeight":"600"}],
        "headline-sm":["24px",{"lineHeight":"1.3","fontWeight":"500"}],
        "label-caps":["12px",{"lineHeight":"1","letterSpacing":"0.05em","fontWeight":"600"}],
        "code-ui":["14px",{"lineHeight":"1.4","fontWeight":"400"}],
        "body-lg":["18px",{"lineHeight":"1.6","fontWeight":"400"}]
      },
      "boxShadow": {"brutal":"4px 4px 0px #000000","brutal-hover":"2px 2px 0px #000000"}
    }
  }
}'''

    head = ('''<!DOCTYPE html>
<html class="dark" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>Vibe Coding Tools — Privacy-first vibe coding utilities</title>
<meta name="description" content="__META__"/>
<link rel="canonical" href="https://vibe.david-cells.com/"/>
<meta property="og:type" content="website"/>
<meta property="og:site_name" content="Vibe Coding Tools"/>
<meta property="og:title" content="Vibe Coding Tools — Privacy-first vibe coding utilities"/>
<meta property="og:description" content="__META__"/>
<meta property="og:url" content="https://vibe.david-cells.com/"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="Vibe Coding Tools — Privacy-first vibe coding utilities"/>
<meta name="twitter:description" content="__META__"/>
<meta property="og:image" content="https://vibe.david-cells.com/og-image.png"/>
<meta property="og:image:width" content="1200"/>
<meta property="og:image:height" content="630"/>
<meta name="twitter:image" content="https://vibe.david-cells.com/og-image.png"/>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,900&family=Inter:wght@400&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet"/>
<script id="tailwind-config">__TW_CONFIG__</script>
<style>
.brutal-border{border:4px solid #100e05;}
.brutal-shadow{box-shadow:4px 4px 0px #100e05;}
.brutal-hover:hover{box-shadow:2px 2px 0px #100e05;transform:translate(2px,2px);}
</style>
<script type="application/ld+json">__SCHEMA__</script>
<script type="text/javascript">(function(i,m,p,a,c,t){c.ire_o=p;c[p]=c[p]||function(){(c[p].a=c[p].a||[]).push(arguments)};t=a.createElement(m);var z=a.getElementsByTagName(m)[0];t.async=1;t.src=i;z.parentNode.insertBefore(t,z)})("https://utt.impactcdn.com/P-A7561863-6222-4288-a584-35c6fbb4048e1.js","script","impactStat",document,window);impactStat("transformLinks");impactStat("trackImpression");</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4110184622096343" crossorigin="anonymous"></script>
</head>''')

    # tool -> Material Symbols icon + brutalist accent rotation
    ICON = {
      'prompt-generator':'edit_note',
      'ai-cost-calculator':'calculate',
      'model-compare':'database',
      'claude-md-generator':'description',
      'project-brief-generator':'assignment',
      'ai-pr-review':'rate_review',
      'ai-security-checklist':'security',
    }
    ACCENTS = [
      ('bg-brutalist-yellow text-black', 'text-black'),
      ('bg-surface-container text-on-surface', 'text-[#00FF41]'),
      ('bg-[#E63946] text-white', 'text-black'),
    ]

    side_nav = ''
    for slug, num, name, blurb in TOOLS:
        side_nav += ('<a class="flex items-center gap-sm text-black p-3 hover:bg-black hover:text-[#FFDE00] brutal-border border-transparent hover:border-black transition-colors" href="%s.html">'
                     '<span class="material-symbols-outlined">%s</span>'
                     '<span class="font-label-caps text-label-caps font-bold">%s</span></a>') % (slug, ICON[slug], html.escape(name))

    cards = ''
    for i, (slug, num, name, blurb) in enumerate(TOOLS):
        bg, ic = ACCENTS[i % 3]
        cards += ('<div class="border-4 border-black p-6 brutal-shadow flex flex-col justify-between %s">'
                  '<div>'
                  '<div class="flex justify-between items-start mb-4">'
                  '<span class="material-symbols-outlined text-4xl %s">%s</span>'
                  '<span class="font-label-caps text-label-caps opacity-70">%s</span>'
                  '</div>'
                  '<h3 class="font-headline-md text-headline-md uppercase mb-2">%s</h3>'
                  '<p class="font-body-md text-body-md opacity-90">%s</p>'
                  '</div>'
                  '<a href="%s.html" class="mt-6 font-label-caps text-label-caps border-b-2 border-current self-start uppercase hover:opacity-70 transition-opacity">Launch &rarr;</a>'
                  '</div>') % (bg, ic, ICON[slug], num, html.escape(name), html.escape(blurb), slug)

    body = ('''<body class="bg-background text-on-surface font-body-md h-screen overflow-hidden flex selection:bg-brutalist-yellow selection:text-black">
<!-- SideNavBar -->
<nav class="hidden md:flex flex-col h-full w-[280px] bg-[#FFDE00] border-r-4 border-[#100e05] py-gap-sm px-gap-xs fixed left-0 top-0 z-50 text-black">
  <div class="mb-gap-md px-3 flex flex-col gap-2">
    <div class="flex items-center gap-3">
      <div class="w-12 h-12 bg-black flex items-center justify-center brutal-shadow">
        <span class="material-symbols-outlined text-[#FFDE00]" style="font-variation-settings: 'FILL' 1;">terminal</span>
      </div>
      <div>
        <h1 class="font-display-lg text-display-lg-mobile text-black uppercase">Vibe Coding</h1>
        <p class="font-label-caps text-label-caps text-black font-bold">Issue 01 · Client-Side</p>
      </div>
    </div>
    <div class="mt-4 bg-black text-[#FFDE00] font-label-caps text-label-caps uppercase p-2 inline-block border-2 border-black w-max">[PRIVATE ACCESS]</div>
  </div>
  <button class="mb-gap-sm mx-3 bg-white text-black font-label-caps text-label-caps uppercase p-3 brutal-border brutal-shadow brutal-hover transition-all flex items-center justify-center gap-2 font-bold">
    <span class="material-symbols-outlined">add</span> All Tools
  </button>
  <div class="flex-1 overflow-y-auto space-y-2 mt-4">
    <a class="flex items-center gap-sm bg-black text-[#FFDE00] p-3 brutal-border" href="index.html">
      <span class="material-symbols-outlined">home</span>
      <span class="font-label-caps text-label-caps font-bold">Home</span>
    </a>
    __SIDENAV__
  </div>
  <div class="mt-auto pt-gap-sm space-y-2">
    <a class="flex items-center gap-sm text-black p-3 hover:bg-black hover:text-[#FFDE00] brutal-border border-transparent hover:border-black transition-colors" href="blog/index.html">
      <span class="material-symbols-outlined">article</span>
      <span class="font-label-caps text-label-caps font-bold">Blog</span>
    </a>
    <a class="flex items-center gap-sm text-black p-3 hover:bg-black hover:text-[#FFDE00] brutal-border border-transparent hover:border-black transition-colors" href="about.html">
      <span class="material-symbols-outlined">info</span>
      <span class="font-label-caps text-label-caps font-bold">About</span>
    </a>
    <a class="flex items-center gap-sm text-black p-3 hover:bg-black hover:text-[#FFDE00] brutal-border border-transparent hover:border-black transition-colors" href="contact.html">
      <span class="material-symbols-outlined">mail</span>
      <span class="font-label-caps text-label-caps font-bold">Contact</span>
    </a>
    <a class="flex items-center gap-sm text-black p-3 hover:bg-black hover:text-[#FFDE00] brutal-border border-transparent hover:border-black transition-colors" href="privacy.html">
      <span class="material-symbols-outlined">security</span>
      <span class="font-label-caps text-label-caps font-bold">Privacy</span>
    </a>
  </div>
</nav>

<!-- Main Content Area -->
<div class="flex-1 flex flex-col md:ml-[280px] h-screen overflow-hidden bg-background">
  <header class="flex justify-between items-center h-16 px-gap-md bg-surface shrink-0 z-40 border-b-4 border-[#100e05]">
    <button class="md:hidden text-primary p-2 brutal-border bg-brutalist-yellow text-black brutal-shadow">
      <span class="material-symbols-outlined">menu</span>
    </button>
    <div class="flex items-center gap-gap-md">
      <span class="font-display-lg-mobile text-display-lg-mobile font-black text-on-surface tracking-tighter uppercase">Vibe Coding Tools</span>
      <div class="hidden md:flex gap-4">
        <a class="font-label-caps text-label-caps text-brutalist-yellow uppercase underline decoration-2 underline-offset-4" href="blog/index.html">Blog</a>
        <a class="font-label-caps text-label-caps text-on-surface-variant hover:text-brutalist-yellow uppercase" href="about.html">About</a>
      </div>
    </div>
    <div class="flex items-center gap-4">
      <a class="font-label-caps text-label-caps bg-brutalist-yellow text-black px-4 py-2 brutal-border brutal-shadow brutal-hover uppercase font-bold hidden sm:block" href="contact.html">Feedback</a>
      <div class="flex gap-2">
        <button class="w-10 h-10 flex items-center justify-center bg-surface-container-highest brutal-border text-on-surface brutal-hover">
          <span class="material-symbols-outlined">dark_mode</span>
        </button>
        <button class="w-10 h-10 flex items-center justify-center bg-brutalist-yellow text-black brutal-border brutal-shadow brutal-hover">
          <span class="material-symbols-outlined">account_circle</span>
        </button>
      </div>
    </div>
  </header>

  <main class="flex-1 overflow-y-auto p-gap-md lg:p-gap-lg">
    <div class="max-w-container-max mx-auto space-y-gap-lg">
      <!-- Hero -->
      <section class="grid grid-cols-1 lg:grid-cols-2 gap-gap-md items-center">
        <div class="space-y-6">
          <div class="inline-block bg-[#E63946] text-white font-label-caps text-label-caps uppercase px-3 py-1 brutal-border shadow-[4px_4px_0px_#100e05]">SYSTEM ALERT // PRIVACY-FIRST</div>
          <h2 class="font-display-lg text-display-lg text-on-surface uppercase tracking-tighter leading-none">
            Build <br/><span class="text-brutalist-yellow" style="-webkit-text-stroke: 1px #100e05;">Privately</span>
          </h2>
          <p class="font-body-lg text-body-lg text-on-surface-variant max-w-lg">
            Seven practical tools to plan, prompt, pick, brief, and review your AI stack. Everything runs in your browser — no uploads, no tracking, no signup.
          </p>
          <div class="flex gap-4 pt-4">
            <a href="ai-cost-calculator.html" class="bg-brutalist-yellow text-black font-label-caps text-label-caps uppercase px-6 py-4 brutal-border brutal-shadow brutal-hover font-bold text-lg">Start: Cost Calculator</a>
          </div>
        </div>
        <div class="relative aspect-video bg-surface-container-lowest brutal-border brutal-shadow overflow-hidden group flex items-center justify-center">
          <span class="material-symbols-outlined text-[#FFDE00] text-[120px]" style="font-variation-settings: 'FILL' 1;">terminal</span>
        </div>
      </section>

      <!-- Stats strip -->
      <section class="grid grid-cols-1 md:grid-cols-3 gap-gap-sm">
        <div class="bg-surface-container border-4 border-black p-6 brutal-shadow">
          <div class="font-display-lg text-display-lg-mobile leading-none tracking-tighter text-brutalist-yellow">7</div>
          <div class="font-label-caps text-label-caps text-on-surface-variant uppercase mt-2">Tools · 0 servers</div>
        </div>
        <div class="bg-surface-container border-4 border-black p-6 brutal-shadow">
          <div class="font-display-lg text-display-lg-mobile leading-none tracking-tighter text-[#00FF41]">0</div>
          <div class="font-label-caps text-label-caps text-on-surface-variant uppercase mt-2">Bytes uploaded by you</div>
        </div>
        <div class="bg-surface-container border-4 border-black p-6 brutal-shadow">
          <div class="font-display-lg text-display-lg-mobile leading-none tracking-tighter text-[#E63946]">$0</div>
          <div class="font-label-caps text-label-caps text-on-surface-variant uppercase mt-2">To use, forever</div>
        </div>
      </section>

      <!-- Tools grid -->
      <section>
        <h2 class="font-headline-md text-headline-md uppercase text-on-surface mb-6 border-b-4 border-black pb-2 inline-block">All Tools</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-gap-sm">
          __TOOLCARDS__
        </div>
      </section>

      <!-- Privacy callout (replaces terminal mock) -->
      <section class="bg-[#E63946] border-4 border-black brutal-shadow p-gap-md relative text-white">
        <div class="absolute -top-4 -right-4 bg-brutalist-yellow text-black font-label-caps text-label-caps uppercase px-4 py-2 border-4 border-black shadow-[4px_4px_0px_#100e05] font-black rotate-3">Zero Data Collected</div>
        <h3 class="font-headline-sm text-headline-sm uppercase text-white mb-4 border-b-4 border-black pb-2 inline-block">Everything runs in your browser</h3>
        <p class="font-body-lg text-body-lg text-white/90 max-w-2xl">No account, no server, no upload. Your prompts, code, and tokens are processed locally with JavaScript and never leave your device. If you are offline, the tools still work.</p>
      </section>
    </div>
  </main>

  <!-- Footer -->
  <footer class="bg-surface-container-lowest border-t-4 border-[#100e05] py-gap-md px-gap-lg flex flex-col md:flex-row justify-between items-center gap-4 shrink-0">
    <span class="font-label-caps text-label-caps text-on-surface-variant uppercase font-bold">© 2026 Vibe Coding Tools. Zero data collected.</span>
    <div class="flex gap-4">
      <a class="font-label-caps text-label-caps text-on-surface-variant hover:text-brutalist-yellow uppercase transition-colors" href="index.html">Tools</a>
      <a class="font-label-caps text-label-caps text-on-surface-variant hover:text-brutalist-yellow uppercase transition-colors" href="blog/index.html">Blog</a>
      <a class="font-label-caps text-label-caps text-on-surface-variant hover:text-brutalist-yellow uppercase transition-colors" href="about.html">About</a>
      <a class="font-label-caps text-label-caps text-on-surface-variant hover:text-brutalist-yellow uppercase transition-colors" href="contact.html">Contact</a>
      <a class="font-label-caps text-label-caps text-on-surface-variant hover:text-brutalist-yellow uppercase transition-colors" href="privacy.html">Privacy</a>
    </div>
  </footer>
</div>
</body></html>''')

    doc = head.replace('__META__', meta).replace('__SCHEMA__', schema).replace('__TW_CONFIG__', TW_CONFIG)
    doc += body.replace('__SIDENAV__', side_nav).replace('__TOOLCARDS__', cards)
    return doc

# ============================================================
# TOOL PAGES
# ============================================================
TOOL_CONTENT = {}

# FAQ appended to every tool page (adds crawler-visible content)
TOOL_CONTENT['ai-cost-calculator'] = {
  'title':'AI Cost Calculator — Estimate API Spend | Vibe Coding Tools',
  'meta':'Estimate the monthly cost of any AI model API before you generate. Enter tokens and volume, get dollars — fully client-side.',
  'features':'Estimate AI API cost by model, tokens, and monthly volume, fully client-side',
  'desc':'Pick a model, enter tokens per request and monthly volume, and see the bill before you build.',
  'extra':'''<p><a href="blog/cursor-vs-windsurf.html">Compare the best vibe coding tools →</a></p>
<p><a href="blog/reduce-ai-coding-cost.html">Cut your AI coding bill with prompt caching →</a></p>''',
  'body':'''
<label for="modelSel">Model</label>
<select id="modelSel">
  __MODEL_OPTIONS__
</select>
<label for="ctxTok">System / context tokens <em>per request</em> (sent every call)</label>
<input id="ctxTok" type="number" value="4000" min="0" />
<label for="inTok">New input tokens <em>per request</em> (this turn)</label>
<input id="inTok" type="number" value="2000" min="0" />
<label for="outTok">Output tokens / request</label>
<input id="outTok" type="number" value="800" min="0" />
<label for="reqMo">Requests / month</label>
<input id="reqMo" type="number" value="10000" min="0" />
<label class="chk" style="margin:10px 0 4px"><input type="checkbox" id="cacheChk" /> Use prompt caching (cached tokens billed at ~10%)</label>
<div class="row">
  <button class="act" onclick="calcCost()">Calculate cost</button>
  <button class="ghost noflex" onclick="resetCost()">Reset</button>
</div>
<div class="out" id="costOut">—</div>
<p class="hint">Context tokens (system prompt + conversation history + reused code) are resent on every call, so they dominate spend. Caching the stable prefix cuts that portion ~90%. Prices are indicative per-million-token rates (USD) and change often.</p>
<script>
var COST = __MODEL_COST__;
function calcCost(){
  var m=document.getElementById('modelSel').value;
  var ctx=parseFloat(document.getElementById('ctxTok').value)||0;
  var it=parseFloat(document.getElementById('inTok').value)||0;
  var ot=parseFloat(document.getElementById('outTok').value)||0;
  var n=parseFloat(document.getElementById('reqMo').value)||0;
  var cached=document.getElementById('cacheChk').checked;
  var p=COST[m];
  var ctxRate=cached?p[0]*0.1:p[0];
  var ctxCost=n*(ctx/1000000)*ctxRate;
  var inCost=n*(it/1000000)*p[0];
  var outCost=n*(ot/1000000)*p[1];
  var total=ctxCost+inCost+outCost;
  var ctxShare=total>0?(ctxCost/total*100):0;
  var o=document.getElementById('costOut');
  o.className='out ok';
  var html='Estimated monthly cost: <b>$'+total.toFixed(2)+'</b><br>';
  html+='Context: $'+ctxCost.toFixed(2)+' &middot; New input: $'+inCost.toFixed(2)+' &middot; Output: $'+outCost.toFixed(2)+'<br>';
  html+='Context is <b>'+ctxShare.toFixed(0)+'%</b> of your spend'+(cached?' (cached @10%)':'')+'<br>';
  if(cached){
    var noCache=n*(ctx/1000000)*p[0];
    html+='Caching saves <b>$'+(noCache-ctxCost).toFixed(2)+'/mo</b> on context';
  } else {
    html+='Turn on caching to cut context cost ~90%';
  }
  o.innerHTML=html;
}
function resetCost(){
  document.getElementById('ctxTok').value=4000;
  document.getElementById('inTok').value=2000;
  document.getElementById('outTok').value=800;
  document.getElementById('reqMo').value=10000;
  document.getElementById('cacheChk').checked=false;
  calcCost();
}
calcCost();
</script>'''
}

TOOL_CONTENT['claude-md-generator'] = {
  'title':'CLAUDE.md Generator — Project Rules AI Agents Follow | Vibe Coding Tools',
  'meta':'Generate a CLAUDE.md, AGENTS.md, .cursorrules, or GEMINI.md for your project in seconds. Pick stack, conventions, and guardrails; copy clean Markdown.',
  'features':'Generate AI-agent project rule files (CLAUDE.md, AGENTS.md, .cursorrules, GEMINI.md) from stack and conventions, fully client-side',
  'desc':'Describe your project once and get a ready-to-paste rule file that keeps Cursor, Claude Code, and friends on track.',
  'extra':'''<p><a href="blog/write-claude-md.html">How to write a great CLAUDE.md (2026 guide) &rarr;</a></p>''',
  'body':'''
<label for="projName">Project name</label>
<input id="projName" type="text" value="My App" />
<label for="projType">Project type</label>
<select id="projType">
  <option value="web-app">Web app / SaaS</option>
  <option value="api">API / backend service</option>
  <option value="library">Library / package</option>
  <option value="cli">CLI tool</option>
  <option value="mobile">Mobile app</option>
  <option value="game">Game</option>
</select>
<label for="stack">Tech stack (one per line)</label>
<textarea id="stack" rows="3">TypeScript
React
Node.js (Express)
PostgreSQL</textarea>
<label>Conventions (check all that apply)</label>
<div class="checks">
  <label class="chk"><input type="checkbox" id="cTs" checked /> Use TypeScript strict mode</label>
  <label class="chk"><input type="checkbox" id="cTests" checked /> Write tests for new logic</label>
  <label class="chk"><input type="checkbox" id="cNostyle" /> Keep styles in CSS files</label>
  <label class="chk"><input type="checkbox" id="cNoconsole" checked /> No console.log in production</label>
  <label class="chk"><input type="checkbox" id="cSmall" /> Small, focused commits</label>
  <label class="chk"><input type="checkbox" id="cExplain" /> Explain non-obvious decisions</label>
</div>
<label for="guard">Guardrails — things the AI must NOT do</label>
<textarea id="guard" rows="3">Don't add dependencies without asking.
Don't rewrite working code "to clean it up".
Don't skip type checks or tests.</textarea>
<label for="fileFmt">Output format</label>
<select id="fileFmt">
  <option value="claude">CLAUDE.md</option>
  <option value="agents">AGENTS.md</option>
  <option value="cursor">.cursorrules</option>
  <option value="gemini">GEMINI.md</option>
</select>
<div class="row">
  <button class="act" onclick="genClaudeMd()">Generate rule file</button>
  <button class="ghost noflex" onclick="copyClaudeMd()">Copy</button>
</div>
<textarea id="mdOut" class="mdout" readonly placeholder="Your generated rule file appears here..."></textarea>
<p class="hint">Everything is assembled in your browser. Nothing is uploaded. Copy the output into a file named after the format you picked.</p>
<script>
function genClaudeMd(){
  var name=document.getElementById('projName').value.trim()||'My Project';
  var type=document.getElementById('projType').value;
  var stack=document.getElementById('stack').value.split(String.fromCharCode(10)).map(function(s){return s.trim();}).filter(Boolean);
  var typeTxt={'web-app':'a web application / SaaS','api':'an API or backend service','library':'a library or package','cli':'a command-line tool','mobile':'a mobile app','game':'a game'}[type];
  var convs=[];
  if(document.getElementById('cTs').checked) convs.push('- Enforce TypeScript strict mode; avoid <code>any</code> unless justified.');
  if(document.getElementById('cTests').checked) convs.push('- Write unit tests for new business logic and run them before reporting done.');
  if(document.getElementById('cNostyle').checked) convs.push('- Keep styles in CSS files; avoid large inline style attributes.');
  if(document.getElementById('cNoconsole').checked) convs.push('- Never leave console.log/print statements in production code.');
  if(document.getElementById('cSmall').checked) convs.push('- Make small, focused commits with clear messages.');
  if(document.getElementById('cExplain').checked) convs.push('- Briefly explain non-obvious or risky decisions in comments.');
  var guard=document.getElementById('guard').value.split(String.fromCharCode(10)).map(function(s){return s.trim();}).filter(Boolean);
  var fmt=document.getElementById('fileFmt').value;
  var fmtName={'claude':'CLAUDE.md','agents':'AGENTS.md','cursor':'.cursorrules','gemini':'GEMINI.md'}[fmt];
  var L=[];
  L.push('# '+name);
  L.push('');
  L.push('You are assisting with '+typeTxt+'. Follow this file exactly.');
  L.push('');
  L.push('## Stack');
  for(var i=0;i<stack.length;i++){ L.push('- '+stack[i]); }
  L.push('');
  L.push('## Conventions');
  for(var i=0;i<convs.length;i++){ L.push(convs[i]); }
  L.push('');
  L.push('## Workflow');
  L.push('- Read the relevant files before editing; prefer targeted diffs over full rewrites.');
  L.push('- After changes, run the type check and tests, and fix what breaks.');
  L.push('- Ask before adding new dependencies or making structural changes.');
  L.push('');
  L.push('## Guardrails (do NOT do these)');
  for(var i=0;i<guard.length;i++){ L.push('- '+guard[i]); }
  L.push('');
  L.push('_Generated by Vibe Coding Tools ('+fmtName+'). Edit freely._');
  document.getElementById('mdOut').value=L.join(String.fromCharCode(10));
}
function copyClaudeMd(){
  var t=document.getElementById('mdOut');
  if(!t.value){ genClaudeMd(); }
  if(navigator.clipboard){ navigator.clipboard.writeText(t.value).catch(function(){}); }
  else { t.select(); try{ document.execCommand('copy'); }catch(e){} }
}
genClaudeMd();
</script>'''
}

TOOL_CONTENT['project-brief-generator'] = {
  'title':'Project Brief Generator — Explain Your Idea to AI | Vibe Coding Tools',
  'meta':'Turn a vague app idea into a clear, copy-ready project brief any AI coding agent can act on. Names scope, users, stack, and constraints.',
  'features':'Turn a vague idea into a structured project brief with scope, users, features, and constraints, fully client-side',
  'desc':'Describe what you want in plain words and get a tight brief you can paste into Cursor, Claude Code, or any agent.',
  'extra':'''<p><a href="prompt-generator.html">Then turn it into a structured prompt →</a></p>
<p><a href="claude-md-generator.html">Or generate a CLAUDE.md from it →</a></p>''',
  'body':'''
<label for="bfName">Project name</label>
<input id="bfName" type="text" value="Habit Tracker" />
<label for="bfWhat">What does it do? (one or two sentences)</label>
<textarea id="bfWhat" rows="3">A mobile-friendly web app where users log daily habits and see streaks.</textarea>
<label for="bfPlatform">Target platform</label>
<select id="bfPlatform">
  <option>Web app (desktop + mobile)</option><option>Mobile app</option><option>API / backend</option><option>CLI tool</option><option>Browser extension</option>
</select>
<label for="bfUsers">Target users</label>
<input id="bfUsers" type="text" value="People building a daily routine" />
<label>Must-have features</label>
<div class="checks" id="bfFeats">
  <label class="chk"><input type="checkbox" value="User accounts" checked /> User accounts</label>
  <label class="chk"><input type="checkbox" value="Persistence / database" checked /> Persistence / database</label>
  <label class="chk"><input type="checkbox" value="Email notifications" /> Email notifications</label>
  <label class="chk"><input type="checkbox" value="Dark mode" checked /> Dark mode</label>
  <label class="chk"><input type="checkbox" value="Export data" /> Export data</label>
  <label class="chk"><input type="checkbox" value="Payments" /> Payments</label>
</div>
<label for="bfStack">Tech constraints (free text)</label>
<input id="bfStack" type="text" value="React, Node, Postgres, deploy on Netlify" />
<label for="bfNo">Hard constraints / must NOT do</label>
<textarea id="bfNo" rows="2">Avoid custom servers where possible; keep it free-tier friendly.</textarea>
<div class="row">
  <button class="act" onclick="genBrief()">Generate brief</button>
  <button class="ghost noflex" onclick="copyBrief()">Copy</button>
</div>
<textarea class="mdout" id="bfOut" readonly rows="14"></textarea>
<script>
function genBrief(){
  var NL=String.fromCharCode(10);
  var name=document.getElementById('bfName').value.trim()||'My Project';
  var what=(document.getElementById('bfWhat').value.trim()||'Describe the product.');
  var plat=document.getElementById('bfPlatform').value;
  var users=document.getElementById('bfUsers').value.trim()||'End users';
  var feats=[].slice.call(document.querySelectorAll('#bfFeats input:checked')).map(function(c){return c.value;});
  var stack=document.getElementById('bfStack').value.trim()||'No specific stack';
  var no=document.getElementById('bfNo').value.trim();
  var L=[];
  L.push('# Project Brief: '+name);
  L.push('');
  L.push('## What it is');
  L.push(what);
  L.push('');
  L.push('## Platform');
  L.push(plat);
  L.push('');
  L.push('## Target users');
  L.push(users);
  L.push('');
  L.push('## Must-have features');
  if(feats.length){ feats.forEach(function(f){ L.push('- '+f); }); }
  else { L.push('- (none selected)'); }
  L.push('');
  L.push('## Tech constraints');
  L.push(stack);
  if(no){ L.push(''); L.push('## Hard constraints (do NOT)'); L.push(no); }
  L.push('');
  L.push('## Build approach');
  L.push('Scaffold the project, implement the must-have features first, and confirm the stack before adding anything extra. Keep changes small and reviewable.');
  document.getElementById('bfOut').value=L.join(NL);
}
function copyBrief(){
  var t=document.getElementById('bfOut');
  if(!t.value){ genBrief(); }
  if(navigator.clipboard){ navigator.clipboard.writeText(t.value).catch(function(){}); }
  else { t.select(); try{ document.execCommand('copy'); }catch(e){} }
}
genBrief();
</script>''',
}

TOOL_CONTENT['ai-pr-review'] = {
  'title':'AI PR Review Checklist — Catch Vibe Debt | Vibe Coding Tools',
  'meta':'A practical review checklist for AI-generated pull requests: catch scope creep, security gaps, missing tests, and silent breakage before you merge.',
  'features':'Generate a copy-ready review checklist for AI-generated pull requests covering scope, security, tests, and breakage, fully client-side',
  'desc':'Tick the areas your change touches and get a focused review checklist plus a prompt you can hand to a reviewer or a second AI agent.',
  'extra':'''<p><a href="ai-security-checklist.html">Open the AI code security checklist →</a></p>
<p><a href="blog/reduce-ai-coding-cost.html">Why reviewing AI code costs less than debugging it →</a></p>''',
  'body':'''
<p class="hint">AI pull requests tend to drift scope, skip tests, and silently break working code. Tick what your change touches, then review against the generated checklist.</p>
<div class="checks" id="prAreas">
  <label class="chk"><input type="checkbox" value="Scope stayed within the request" checked /> Scope stayed within the request</label>
  <label class="chk"><input type="checkbox" value="No secrets, injection, or auth gaps" checked /> No secrets, injection, or auth gaps</label>
  <label class="chk"><input type="checkbox" value="Tests added or updated" checked /> Tests added or updated</label>
  <label class="chk"><input type="checkbox" value="Errors handled, no silent failures" /> Errors handled, no silent failures</label>
  <label class="chk"><input type="checkbox" value="No unrelated features broken" checked /> No unrelated features broken</label>
  <label class="chk"><input type="checkbox" value="No new dependencies without reason" /> No new dependencies without reason</label>
  <label class="chk"><input type="checkbox" value="No obvious performance regressions" /> No obvious performance regressions</label>
  <label class="chk"><input type="checkbox" value="No hardcoded keys or config leaks" /> No hardcoded keys or config leaks</label>
</div>
<div class="row">
  <button class="act" onclick="genPr()">Generate checklist</button>
  <button class="ghost noflex" onclick="copyPr()">Copy</button>
</div>
<textarea class="mdout" id="prOut" readonly rows="16"></textarea>
<script>
function genPr(){
  var NL=String.fromCharCode(10);
  var areas=[].slice.call(document.querySelectorAll('#prAreas input:checked')).map(function(c){return c.value;});
  var L=[];
  L.push('# Review this AI-generated PR');
  L.push('');
  L.push('Before merging, verify each checked area:');
  L.push('');
  if(areas.length){ areas.forEach(function(a){ L.push('- [ ] '+a); }); }
  else { L.push('- [ ] (select at least one area)'); }
  L.push('');
  L.push('## Red flags to reject');
  L.push('- Functionality that was not requested (scope creep)');
  L.push('- New dependencies added "just in case"');
  L.push('- Tests skipped with a comment like "should be fine"');
  L.push('- Working features edited outside the stated scope');
  L.push('- Hardcoded credentials, tokens, or internal URLs');
  L.push('');
  L.push('## Reviewer prompt');
  L.push('Review the diff for the areas above. Report only real problems with the file and line. Do not suggest refactors beyond the change.');
  document.getElementById('prOut').value=L.join(NL);
}
function copyPr(){
  var t=document.getElementById('prOut');
  if(!t.value){ genPr(); }
  if(navigator.clipboard){ navigator.clipboard.writeText(t.value).catch(function(){}); }
  else { t.select(); try{ document.execCommand('copy'); }catch(e){} }
}
genPr();
</script>''',
}

TOOL_CONTENT['ai-security-checklist'] = {
  'title':'AI Code Security Checklist — Common Pitfalls | Vibe Coding Tools',
  'meta':'The security pitfalls most often baked into AI-generated code, grouped by risk. Generate a copy-ready checklist before you ship.',
  'features':'List the most common security pitfalls in AI-generated code, grouped by risk, as a copy-ready checklist, fully client-side',
  'desc':'AI code looks confident but often ships injection, hardcoded secrets, and missing auth checks. Pick your stack and get the checklist that matters.',
  'extra':'''<p><a href="ai-pr-review.html">Pair it with the AI PR review checklist →</a></p>
<p><a href="claude-md-generator.html">Bake security rules into a CLAUDE.md →</a></p>''',
  'body':'''
<label for="secStack">Primary language / framework</label>
<select id="secStack">
  <option>JavaScript / TypeScript (Node)</option><option>Python</option><option>PHP</option><option>Go</option><option>Ruby</option><option>Java / Kotlin</option><option>SQL-heavy</option><option>Any / general</option>
</select>
<p class="hint">AI-generated code repeatedly fails on the items below. Tick what you have verified before shipping.</p>
<div class="checks" id="secItems">
  <label class="chk"><input type="checkbox" value="No SQL/script injection (parameterized queries, escaped input)" /> No SQL/script injection (parameterized queries)</label>
  <label class="chk"><input type="checkbox" value="No hardcoded secrets, API keys, or tokens in source" /> No hardcoded secrets or API keys</label>
  <label class="chk"><input type="checkbox" value="Auth checks on every protected route/function" /> Authorization checked on every protected route</label>
  <label class="chk"><input type="checkbox" value="User input validated and size-limited" /> User input validated and size-limited</label>
  <label class="chk"><input type="checkbox" value="No eval() / unsafe deserialization of untrusted data" /> No eval() / unsafe deserialization</label>
  <label class="chk"><input type="checkbox" value="Dependencies pinned and from trusted sources" /> Dependencies pinned and vetted</label>
  <label class="chk"><input type="checkbox" value="Errors do not leak stack traces or internals to users" /> Errors do not leak internals to users</label>
  <label class="chk"><input type="checkbox" value="File uploads type-checked and stored outside web root" /> Uploads type-checked, stored safely</label>
  <label class="chk"><input type="checkbox" value="Rate limiting / abuse protection on public endpoints" /> Rate limiting on public endpoints</label>
  <label class="chk"><input type="checkbox" value="HTTPS enforced and secure cookies (HttpOnly, SameSite)" /> HTTPS + secure cookie flags</label>
</div>
<div class="row">
  <button class="act" onclick="genSec()">Generate checklist</button>
  <button class="ghost noflex" onclick="copySec()">Copy</button>
</div>
<textarea class="mdout" id="secOut" readonly rows="16"></textarea>
<script>
function genSec(){
  var NL=String.fromCharCode(10);
  var stack=document.getElementById('secStack').value;
  var items=[].slice.call(document.querySelectorAll('#secItems input:checked')).map(function(c){return c.value;});
  var L=[];
  L.push('# AI Code Security Checklist ('+stack+')');
  L.push('');
  L.push('Verify before shipping AI-generated code:');
  L.push('');
  if(items.length){ items.forEach(function(i){ L.push('- [x] '+i); }); }
  L.push('- [ ] All items above reviewed');
  L.push('');
  L.push('Generated by Vibe Coding Tools — a starting point, not a substitute for a real security audit.');
  document.getElementById('secOut').value=L.join(NL);
}
function copySec(){
  var t=document.getElementById('secOut');
  if(!t.value){ genSec(); }
  if(navigator.clipboard){ navigator.clipboard.writeText(t.value).catch(function(){}); }
  else { t.select(); try{ document.execCommand('copy'); }catch(e){} }
}
genSec();
</script>''',
}

TOOL_CONTENT['prompt-generator'] = {
  'title':'Vibe Coding Prompt Builder — Structure Any Idea | Vibe Coding Tools',
  'meta':'Turn a vague app idea into a structured, copy-ready AI coding prompt. Pick type, stack, and features; get a prompt that ships.',
  'features':'Build structured vibe coding prompts from project type, stack, and feature checklist, fully client-side',
  'desc':'Select your project type and features, and get a clean, copy-ready prompt for Cursor, Claude, or any coding agent.',
  'extra':'''<p><a href="blog/best-vibe-coding-tools.html">See the best vibe coding tools →</a></p>''',
  'body':'''
<label for="pType">Project type</label>
<select id="pType">
  <option>Web app</option><option>Mobile app</option><option>API / backend</option>
  <option>CLI tool</option><option>Browser extension</option><option>Automation script</option>
</select>
<label for="pLevel">Your level</label>
<select id="pLevel">
  <option>Beginner (little coding)</option><option>Intermediate</option><option>Pro</option>
</select>
<label for="pStack">Tech stack (free text)</label>
<input id="pStack" type="text" value="React + Node + Postgres" />
<label>Features</label>
<div class="checks">
  <label class="chk"><input type="checkbox" value="User authentication" checked /> User authentication</label>
  <label class="chk"><input type="checkbox" value="Payments" /> Payments</label>
  <label class="chk"><input type="checkbox" value="Database persistence" checked /> Database persistence</label>
  <label class="chk"><input type="checkbox" value="Real-time updates" /> Real-time updates</label>
  <label class="chk"><input type="checkbox" value="File uploads" /> File uploads</label>
  <label class="chk"><input type="checkbox" value="Admin panel" /> Admin panel</label>
  <label class="chk"><input type="checkbox" value="Dark mode" /> Dark mode</label>
  <label class="chk"><input type="checkbox" value="Unit tests" /> Unit tests</label>
</div>
<div class="row">
  <button class="act" onclick="genPrompt()">Generate prompt</button>
  <button class="ghost noflex" onclick="copyPrompt()">Copy</button>
</div>
<textarea id="promptOut" readonly placeholder="Your structured prompt appears here…"></textarea>
<script>
function genPrompt(){
  var type=document.getElementById('pType').value;
  var level=document.getElementById('pLevel').value;
  var stack=document.getElementById('pStack').value||'(no stack specified)';
  var feats=Array.from(document.querySelectorAll('.checks input:checked')).map(function(c){return c.value;});
  var p='You are an expert '+level+' software engineer helping me build a '+type+'.\\n\\n';
  p+='Stack: '+stack+'.\\n\\n';
  p+='Core features to implement:\\n';
  feats.forEach(function(f){ p+='- '+f+'\\n'; });
  p+='\\nRequirements:\\n';
  p+='- Write clean, well-commented code following '+stack+' best practices.\\n';
  p+='- Explain key decisions briefly as you go.\\n';
  p+='- Include a short README with run instructions.\\n\\n';
  p+='Start by scaffolding the project and listing the file structure before writing code.';
  document.getElementById('promptOut').value=p;
}
function copyPrompt(){
  var t=document.getElementById('promptOut');
  if(!t.value){genPrompt();}
  t.select();
  try{document.execCommand('copy');}catch(e){}
}
genPrompt();
</script>'''
}

TOOL_CONTENT['model-compare'] = {
  'title':'LLM Model Compare — Filter by Use Case & Price | Vibe Coding Tools',
  'meta':'Compare leading LLMs side by side: context window, input/output price, and best-fit use case. Filter to find the right model fast.',
  'features':'Compare LLM models by context window, price, and use case with a client-side filter',
  'desc':'Filter models by what you need — coding, long context, cheap volume, or reasoning — and see the trade-offs instantly.',
  'extra':'''<p><a href="blog/cursor-vs-windsurf.html">Compare the best vibe coding tools →</a></p>''',
  'body':'''
<label for="useFilter">Filter by need</label>
<select id="useFilter" onchange="filterModels()">
  <option value="all">All uses</option>
  <option value="coding">Coding</option>
  <option value="long">Long context</option>
  <option value="cheap">Cheap / high volume</option>
  <option value="reasoning">Reasoning</option>
  <option value="multimodal">Multimodal</option>
</select>
<div class="tablewrap">
<table class="cmp">
  <thead><tr><th>Model</th><th>Context</th><th>In $/1M</th><th>Out $/1M</th><th>Best for</th></tr></thead>
  <tbody id="cmpBody">
    __MODEL_ROWS__
  </tbody>
</table>
</div>
<p class="hint">Indicative pricing (USD per 1M tokens). Context windows and rates shift constantly — verify on the provider site.</p>
__MODEL_PAGES__
<script>
function filterModels(){
  var v=document.getElementById('useFilter').value;
  document.querySelectorAll('#cmpBody tr').forEach(function(tr){
    var u=tr.getAttribute('data-use')||'';
    tr.style.display=(v==='all'||u.indexOf(v)>=0)?'':'none';
  });
}
filterModels();
</script>'''
}

TOOL_FAQ = {
  'ai-cost-calculator': '''
<h2>Frequently asked questions</h2>
<dl class="faq">
  <dt>Are the prices accurate?</dt>
  <dd>They are indicative per-million-token rates captured at build time. Providers change pricing often and use tiered or cached pricing, so treat the result as a planning estimate and confirm on the official pricing page before committing a budget.</dd>
  <dt>Does this calculator upload my inputs?</dt>
  <dd>No. All math runs in your browser. No token counts, model choices, or volumes leave your device.</dd>
  <dt>Which models are included?</dt>
  <dd>The most common API models from OpenAI, Anthropic, Google, DeepSeek, and Meta (hosted). It is not exhaustive — add your own mental math for anything missing.</dd>
  <dt>How do I lower my bill?</dt>
  <dd>Use a smaller or mini model for cheap, high-volume tasks, cache long system prompts, and keep outputs short. The calculator shows exactly how much each lever saves.</dd>
</dl>''',

  'prompt-generator': '''
<h2>Frequently asked questions</h2>
<dl class="faq">
  <dt>What is a vibe coding prompt?</dt>
  <dd>A vibe coding prompt tells an AI coding agent what to build and how. A good one names the project type, stack, and must-have features so the agent scaffolds the right thing instead of guessing.</dd>
  <dt>Do I need to know how to code?</dt>
  <dd>No. That is the point. Pick "Beginner" as your level and the prompt asks the agent to explain decisions and include run instructions, so you can ship without writing syntax yourself.</dd>
  <dt>Which tools accept this prompt?</dt>
  <dd>Any coding agent — Cursor, Claude Code, Windsurf, Replit, Bolt, or v0. The output is plain text you paste into the chat.</dd>
  <dt>Is my idea sent anywhere?</dt>
  <dd>No. The prompt is assembled locally in your browser. Nothing is uploaded.</dd>
</dl>''',

  'model-compare': '''
<h2>Frequently asked questions</h2>
<dl class="faq">
  <dt>How do I pick the right model?</dt>
  <dd>Start from your constraint: huge context — Gemini 3.1 Pro or Grok 4.3 (2M); cheapest volume — DeepSeek V4 Flash or Gemini 3.5 Flash; best coding — Claude Sonnet 5 or GPT-5.5. Use the filter to narrow, then verify pricing on the provider site.</dd>
  <dt>Why do input and output prices differ?</dt>
  <dd>Generating tokens (output) costs more compute than reading them (input), so nearly every provider charges more per output token.</dd>
  <dt>Are these prices current?</dt>
  <dd>They are indicative snapshots. AI pricing moves fast and often includes cached-token discounts, so confirm before budgeting.</dd>
  <dt>Is the comparison data uploaded?</dt>
  <dd>No. Filtering happens entirely in your browser.</dd>
</dl>''',

  'claude-md-generator': '''
<h2>Frequently asked questions</h2>
<dl class="faq">
  <dt>What is a CLAUDE.md / AGENTS.md?</dt>
  <dd>It is a plain-text rule file in your repo root that tells AI coding agents (Claude Code, Cursor, Windsurf, Gemini CLI) your stack, conventions, and guardrails. Agents read it on every task so they stay consistent instead of guessing.</dd>
  <dt>Which format should I pick?</dt>
  <dd>CLAUDE.md for Claude Code, AGENTS.md for the open Agents standard, .cursorrules for older Cursor setups, GEMINI.md for Gemini CLI. They hold the same content &mdash; pick the tool you use, or keep all four in sync.</dd>
  <dt>Does this generator upload my project info?</dt>
  <dd>No. The file is assembled entirely in your browser from your inputs. Nothing is sent anywhere.</dd>
  <dt>Is the output good enough to ship?</dt>
  <dd>It is a strong starting point. Paste it in, then tweak the guardrails to match how you actually want the agent to behave.</dd>
</dl>''',

  'project-brief-generator': '''
<h2>Frequently asked questions</h2>
<dl class="faq">
  <dt>Why do I need a brief if I have a prompt builder?</dt>
  <dd>A prompt tells the agent what to build this turn. A brief captures the product: who it is for, what it must and must not do. You stay aligned across many turns instead of re-explaining the idea each time.</dd>
  <dt>Is my idea uploaded?</dt>
  <dd>No. The brief is assembled in your browser from your inputs. Nothing leaves your device.</dd>
  <dt>What do I do with the output?</dt>
  <dd>Paste it into a CLAUDE.md, a Cursor project rule, or the first message of a new chat. It works as both a spec and a guardrail.</dd>
</dl>''',

  'ai-pr-review': '''
<h2>Frequently asked questions</h2>
<dl class="faq">
  <dt>Why review AI pull requests differently?</dt>
  <dd>AI-authored PRs tend to carry more issues and security findings than human PRs, often from silent scope creep. A focused checklist catches what a casual glance misses.</dd>
  <dt>Does this scan my code?</dt>
  <dd>No. It is a checklist generator, not a scanner. You (or a second agent) do the reviewing; this tool tells you what to look for.</dd>
  <dt>Can I hand the output to another AI to review?</dt>
  <dd>Yes. The generated reviewer prompt is written so a second model checks the diff without inventing unrelated refactors.</dd>
</dl>''',

  'ai-security-checklist': '''
<h2>Frequently asked questions</h2>
<dl class="faq">
  <dt>Is this a real security scanner?</dt>
  <dd>No. It is an educational checklist of the pitfalls most often found in AI-generated code. For production, run a real SAST/DAST tool and a proper audit.</dd>
  <dt>Why is AI code especially risky?</dt>
  <dd>Models optimize for code that runs and looks right, not for security boundaries. They routinely emit injection-prone queries, hardcoded keys, and missing auth checks.</dd>
  <dt>Should I bake these into CLAUDE.md?</dt>
  <dd>Yes. Listing "never hardcode secrets, always parameterize queries" as a project rule prevents the mistake at generation time instead of catching it later.</dd>
</dl>''',
}

def build_tool(slug):
    c = TOOL_CONTENT[slug]
    num, name = TOOL_BY_SLUG[slug][1], TOOL_BY_SLUG[slug][2]
    # inject externalized model data (prices/comparison) into the relevant tools
    body_src = c['body']
    if slug == 'ai-cost-calculator':
        body_src = (body_src.replace('__MODEL_OPTIONS__', model_options())
                             .replace('__MODEL_COST__', model_cost_js()))
    elif slug == 'model-compare':
        body_src = body_src.replace('__MODEL_ROWS__', model_compare_rows())
        links = ' &middot; '.join('<a href="models/%s.html">%s</a>' % (mm['id'], html.escape(mm['label'])) for mm in MODELS)
        body_src = body_src.replace('__MODEL_PAGES__', '<p class="hint">Per-model price pages: ' + links + '</p>')
    schema = webapp_schema('Vibe Coding Tools — ' + name, slug, c['features'])
    hero = (f'<div class="t-tool-hero">'
            f'<div class="crumb">Tools / {num} · {html.escape(name)}</div>'
            f'<h1>{html.escape(name)}</h1>'
            f'<p class="sub">{html.escape(c["desc"])}</p>'
            f'</div>')
    back = '<a class="back" href="index.html">← All tools</a>'
    body = back + SHIELD + hero + body_src + c['extra'] + TOOL_FAQ.get(slug, '')
    return page_brutalist(c['title'], c['meta'], schema, active_slug=slug, body=body, url='https://vibe.david-cells.com/' + slug + '.html')

# ============================================================
# PER-MODEL PRICING PAGES (programmatic SEO — one page per model)
# ============================================================
def build_model_page(m):
    slug = m['id']
    label = m['label']
    pin = '%.2f' % float(m['in'])
    pout = '%.2f' % float(m['out'])
    prefix = '../'
    title = '%s API Pricing & Context Window (2026) | Vibe Coding Tools' % label
    meta = ('%s pricing in 2026: $%s per 1M input tokens, $%s per 1M output tokens, %s context window. '
            'Estimate your monthly bill and compare %s to other LLMs.'
            % (label, pin, pout, m['context'], label))
    # sample workload for an illustrative monthly cost (crawlable, quotable figure)
    SAMPLE = {'req': 50000, 'ctx': 8000, 'in': 1000, 'out': 500}
    ex = (SAMPLE['req'] * (SAMPLE['ctx'] / 1e6) * float(m['in'])
          + SAMPLE['req'] * (SAMPLE['in'] / 1e6) * float(m['in'])
          + SAMPLE['req'] * (SAMPLE['out'] / 1e6) * float(m['out']))
    schema = ('{"@context":"https://schema.org","@type":"Product","name":"%s API",'
              '"offers":{"@type":"Offer","priceCurrency":"USD","price":"%s","unitText":"per 1M input tokens"}}'
              % (label.replace('"', '\\"'), pin))
    hero = ('''<div class="t-tool-hero article-hero">
      <div class="crumb"><a href="../index.html">Vibe Coding Tools</a> / <a href="../model-compare.html">Model Compare</a> / %s</div>
      <h1>%s API Pricing &amp; Context Window</h1>
      <p class="sub">Indicative 2026 rates. Verify on the provider's pricing page before budgeting.</p>
    </div>''' % (html.escape(label), html.escape(label)))
    table = ('''<div class="tablewrap"><table class="cmp">
      <thead><tr><th>Metric</th><th>Value</th></tr></thead>
      <tbody>
        <tr><td>Input price</td><td>$%s / 1M tokens</td></tr>
        <tr><td>Output price</td><td>$%s / 1M tokens</td></tr>
        <tr><td>Context window</td><td>%s</td></tr>
        <tr><td>Best for</td><td>%s</td></tr>
      </tbody></table></div>''' % (pin, pout, m['context'], html.escape(m['best'])))
    example = ('''<h2>Example monthly cost</h2>
    <p>At a sample workload of <strong>%s requests/month</strong> with %s context tokens, %s new input tokens, and %s output tokens per request,
    %s costs roughly <strong>$%s/month</strong> (uncached). Turn on prompt caching and the context portion drops to about 10%%, often cutting the bill by half.
    Estimate your own numbers with the <a class="link" href="../ai-cost-calculator.html">AI Cost Calculator</a>.</p>'''
    % (format(SAMPLE['req'], ','), format(SAMPLE['ctx'], ','), format(SAMPLE['in'], ','), format(SAMPLE['out'], ','),
       html.escape(label), format(ex, ',.2f')))
    compare_block = ('''<h2>How %s compares</h2>
    <p>%s sits among the current frontier and open-weight models. To see every model side by side — context window, input/output price, and best-fit use case —
    open the <a class="link" href="../model-compare.html">LLM Model Compare</a> tool and filter by what you need (coding, long context, cheap volume, or reasoning).</p>'''
    % (html.escape(label), html.escape(label)))
    faq = ('''<h2>Frequently asked questions</h2>
    <dl class="faq">
      <dt>How much does %s cost per 1M tokens?</dt>
      <dd>Input tokens are $%s per 1M and output tokens are $%s per 1M (indicative 2026 rates). Output costs more because generating tokens uses more compute.</dd>
      <dt>What is the %s context window?</dt>
      <dd>%s. A larger context window lets you send more code, docs, or conversation history per request without chunking.</dd>
      <dt>Is this %s pricing current?</dt>
      <dd>Rates are a snapshot captured at build time. AI pricing moves often and many providers offer cached-token discounts, so confirm on the official pricing page before committing a budget.</dd>
      <dt>How do I estimate my own %s bill?</dt>
      <dd>Use the <a class="link" href="../ai-cost-calculator.html">AI Cost Calculator</a> — enter your tokens and volume and see the monthly cost instantly, with and without prompt caching.</dd>
    </dl>''' % (label, pin, pout, label, m['context'], label, label))
    body = hero + '<article class="article">' + table + example + compare_block + faq + '</article>'
    return page_brutalist(title, meta, schema, body=body, prefix=prefix, url='https://vibe.david-cells.com/models/' + slug + '.html')

# ============================================================
# BLOG
# ============================================================
BLOG = {  'cursor-vs-windsurf': {
    'title':'Cursor vs Windsurf vs Claude Code (2026): Which Vibe Coding Tool Wins?',
    'meta':'A hands-on comparison of the three most popular vibe coding tools — Cursor, Windsurf, and Claude Code. Pricing, strengths, and which to pick.',
    'tag':'Vibe Coding',
    'date':'August 7, 2026',
    'read':'9 min read',
    'excerpt':'Cursor, Windsurf, and Claude Code all promise to let you ship software by describing it. Here is how they actually compare.',
    'body':'''
<p>If you build software by talking to an AI instead of typing it, you are vibe coding. The three
tools everyone argues about are <strong>Cursor</strong>, <strong>Windsurf</strong>, and
<strong>Claude Code</strong>. This comparison cuts through the hype so you can pick the one that fits
how you work.</p>

<h2>The short version</h2>
<ul>
  <li><strong>Cursor</strong> &mdash; the most polished all-rounder; best if you want an IDE that just works.</li>
  <li><strong>Windsurf</strong> &mdash; fastest feel and aggressive autocomplete; great for shipping UI quickly.</li>
  <li><strong>Claude Code</strong> &mdash; terminal-native agent; best for large refactors and codebase-wide changes.</li>
</ul>

<h2>Comparison table</h2>
<div class="tablewrap"><table class="cmp">
  <thead><tr><th>Tool</th><th>Form</th><th>Best at</th><th>Starting price</th></tr></thead>
  <tbody>
    <tr><td>Cursor</td><td>VS Code fork</td><td>Daily editing, Tab completions</td><td>~$20/mo (free tier)</td></tr>
    <tr><td>Windsurf</td><td>VS Code fork</td><td>Fast UI builds, Cascade agent</td><td>~$15/mo (free tier)</td></tr>
    <tr><td>Claude Code</td><td>Terminal CLI</td><td>Repo-wide refactors, scripts</td><td>~$20/mo (Pro)</td></tr>
  </tbody>
</table></div>

<h2>Cursor</h2>
<p>Cursor is a fork of VS Code with AI woven in. Its <em>Tab</em> completion predicts multi-line edits,
and <em>Composer</em> edits across files. If you already live in VS Code, the switch is painless.
The downside is that heavy agents can feel slower than Windsurf's Cascade.</p>

<h2>Windsurf</h2>
<p>Windsurf leads on raw speed and "flow." Its Cascade agent keeps context across a session and is
uncannily good at scaffolding front-ends. Some developers find it less precise than Cursor for fiddly
backend logic, but for shipping a prototype it is hard to beat.</p>

<h2>Claude Code</h2>
<p>Claude Code runs in your terminal and operates on the whole repository. It shines at the jobs that
scare junior devs: renaming across 40 files, writing a migration, or understanding an unfamiliar codebase.
It expects you to be comfortable in a shell.</p>

<h2>Which should you pick?</h2>
<p>Beginners and product builders: start with <strong>Cursor</strong> or <strong>Windsurf</strong>.
If you mostly live in the terminal and touch large codebases, <strong>Claude Code</strong> pays for
itself quickly. Most serious vibe coders end up using two.</p>

<p>Want to estimate what a project will actually cost to build with these models? Try our
<a class="link" href="../ai-cost-calculator.html">AI Cost Calculator</a>.</p>

<h2>Tools we actually use</h2>
<div class="aff-box">
  <div class="aff-head"><span class="aff-tag">Sponsored</span><span>Tools this comparison was built with</span></div>
  <ul class="aff-list">
    <li><a class="aff-link" href="https://example.com/aff/cursor" target="_blank" rel="sponsored nofollow noopener">Cursor &rarr;</a><p class="aff-blurb">AI-first code editor with Tab completions and Composer for multi-file edits.</p></li>
    <li><a class="aff-link" href="https://example.com/aff/windsurf" target="_blank" rel="sponsored nofollow noopener">Windsurf &rarr;</a><p class="aff-blurb">Fast agentic editor with the Cascade agent for rapid UI builds.</p></li>
    <li><a class="aff-link" href="https://example.com/aff/claude-code" target="_blank" rel="sponsored nofollow noopener">Claude Code &rarr;</a><p class="aff-blurb">Terminal-native agent for repo-wide refactors and migrations.</p></li>
  </ul>
  <p class="aff-note">Vibe Coding Tools may earn a commission when you sign up via these links, at no extra cost to you. We only recommend tools we use.</p>
</div>
'''
  },

  'best-vibe-coding-tools': {
    'title':'Best Vibe Coding Tools in 2026 (Tested &amp; Ranked)',
    'meta':'The best vibe coding tools of 2026, ranked: Cursor, Windsurf, Claude Code, Replit, v0, Bolt, Cline, and Aider — with who each one is for.',
    'tag':'Vibe Coding',
    'date':'August 7, 2026',
    'read':'11 min read',
    'excerpt':'From full IDEs to terminal agents to browser builders — the vibe coding landscape ranked by who should actually use each.',
    'body':'''
<p>Vibe coding is building software by describing what you want and letting AI write it. The tool
market exploded in 2025 and 2026. Here are the ones worth your time, ranked by fit rather than hype.</p>

<h2>1. Cursor</h2>
<p>The default choice. A VS Code fork with excellent completions and multi-file edits. Best for people
who want an AI upgrade without leaving a familiar editor.</p>

<h2>2. Windsurf</h2>
<p>The speed king. Cascade keeps context across a session and is brilliant at scaffolding UIs. Best for
shipping front-ends and prototypes fast.</p>

<h2>3. Claude Code</h2>
<p>A terminal agent that operates on your whole repo. Best for refactors, migrations, and understanding
big codebases. Expect to live in a shell.</p>

<h2>4. Replit</h2>
<p>Browser-based and zero-install. Best for absolute beginners who want to go from idea to a hosted app
without touching local setup.</p>

<h2>5. v0 (Vercel)</h2>
<p>Generates React components and full pages from prompts. Best for designers and frontend devs who want
shippable UI fast.</p>

<h2>6. Bolt</h2>
<p>Browser builder that scaffolds and runs full-stack apps. Best for quick demos and MVPs you can show
someone the same afternoon.</p>

<h2>7. Cline</h2>
<p>An open-source VS Code agent you can point at any model. Best for developers who want control and
self-hosting.</p>

<h2>8. Aider</h2>
<p>A terminal pair-programmer built for git workflows. Best for engineers who want AI edits committed
cleanly with tests.</p>

<h2>How to choose</h2>
<p>If you are new, start with <strong>Replit</strong> or <strong>Bolt</strong>. If you want a real editor,
<strong>Cursor</strong> or <strong>Windsurf</strong>. If you live in the terminal,
<strong>Claude Code</strong>, <strong>Cline</strong>, or <strong>Aider</strong>.</p>

<p>Before you commit, estimate your running cost with our
<a class="link" href="../ai-cost-calculator.html">AI Cost Calculator</a>, and structure your first
request with the <a class="link" href="../prompt-generator.html">Vibe Coding Prompt Builder</a>.</p>

<h2>Our picks (with offers)</h2>
<div class="aff-box">
  <div class="aff-head"><span class="aff-tag">Sponsored</span><span>Tools we recommend</span></div>
  <ul class="aff-list">
    <li><a class="aff-link" href="https://example.com/aff/cursor" target="_blank" rel="sponsored nofollow noopener">Cursor &rarr;</a><p class="aff-blurb">The all-rounder AI code editor. Free tier + Pro.</p></li>
    <li><a class="aff-link" href="https://example.com/aff/windsurf" target="_blank" rel="sponsored nofollow noopener">Windsurf &rarr;</a><p class="aff-blurb">Fastest agentic editor. Free tier + Pro.</p></li>
    <li><a class="aff-link" href="https://example.com/aff/replit" target="_blank" rel="sponsored nofollow noopener">Replit &rarr;</a><p class="aff-blurb">Zero-install, browser IDE. Free + Core.</p></li>
    <li><a class="aff-link" href="https://example.com/aff/claude-code" target="_blank" rel="sponsored nofollow noopener">Claude Code &rarr;</a><p class="aff-blurb">Terminal agent for big changes. Pro plan.</p></li>
  </ul>
  <p class="aff-note">Affiliate links — commissions help keep Vibe Coding Tools free. We only recommend tools we use.</p>
</div>
'''
  },

  'write-claude-md': {
    'title':'How to Write a CLAUDE.md for Your Project (2026 Guide)',
    'meta':'A practical 2026 guide to writing a CLAUDE.md / AGENTS.md that keeps AI coding agents on track. Includes a free generator you can use in your browser.',
    'tag':'Vibe Coding',
    'date':'August 7, 2026',
    'read':'8 min read',
    'excerpt':'A good CLAUDE.md is the highest-leverage file in a vibe-coded repo. Here is how to write one that actually works.',
    'body':'''
<p>If you let an AI agent edit your codebase, the single highest-leverage file you can add is a
<strong>CLAUDE.md</strong> (or AGENTS.md, .cursorrules, GEMINI.md). It tells the agent your stack,
your conventions, and the lines it must not cross &mdash; so it stops guessing and starts shipping
the right thing. This guide shows you how to write one, and you can generate a starter in seconds with
our <a class="link" href="../claude-md-generator.html">CLAUDE.md Generator</a>.</p>

<h2>Why it matters</h2>
<p>Agents are stateless between tasks. Without a rule file they re-derive your conventions every time,
and they will happily "tidy up" working code or pull in a dependency you did not ask for. A CLAUDE.md
removes that ambiguity. Teams report it pays for itself within a week of daily use.</p>

<h2>The four sections every CLAUDE.md needs</h2>
<ul>
  <li><strong>Stack</strong> &mdash; list the languages, frameworks, and key libraries so the agent targets the right APIs.</li>
  <li><strong>Conventions</strong> &mdash; TypeScript strict mode, tests required, no console.log in prod, commit style.</li>
  <li><strong>Workflow</strong> &mdash; read before editing, prefer diffs over rewrites, run checks before reporting done.</li>
  <li><strong>Guardrails</strong> &mdash; the things it must NOT do (add deps, rewrite working code, skip tests).</li>
</ul>

<h2>A starter template</h2>
<p>You can hand-write this, or use the generator. A minimal version looks like:</p>
<div class="tablewrap"><pre class="code"># My App

## Stack
- TypeScript, React, Node.js, PostgreSQL

## Conventions
- TypeScript strict mode; no &lt;code&gt;any&lt;/code&gt;
- Write tests for new logic

## Guardrails
- Don't add dependencies without asking
- Don't rewrite working code "to clean it up"</pre></div>

<h2>Keep it in sync</h2>
<p>When your stack changes, update the file. Agents trust it more than they trust inference, so a stale
CLAUDE.md is worse than none. If you use multiple tools, keep CLAUDE.md, AGENTS.md, and .cursorrules
pointing at the same rules.</p>

<p>Want the polished version with copy-ready formatting? Open the
<a class="link" href="../claude-md-generator.html">CLAUDE.md Generator</a> and export it in seconds.</p>

<h2>Tools we recommend</h2>
<div class="aff-box">
  <div class="aff-head"><span class="aff-tag">Sponsored</span><span>Agents that read your CLAUDE.md</span></div>
  <ul class="aff-list">
    <li><a class="aff-link" href="https://example.com/aff/claude-code" target="_blank" rel="sponsored nofollow noopener">Claude Code &rarr;</a><p class="aff-blurb">Terminal agent that reads CLAUDE.md on every task. Pro plan.</p></li>
    <li><a class="aff-link" href="https://example.com/aff/cursor" target="_blank" rel="sponsored nofollow noopener">Cursor &rarr;</a><p class="aff-blurb">AI editor that respects project rules and .cursorrules. Free tier + Pro.</p></li>
  </ul>
  <p class="aff-note">Affiliate links &mdash; commissions help keep Vibe Coding Tools free.</p>
</div>
'''
  },

  'reduce-ai-coding-cost': {
    'title':'Cut Your AI Coding Bill in Half (2026): Prompt Caching & Model Routing',
    'meta':'Practical 2026 tactics to lower AI coding API spend: prompt caching, tiered model routing, and tight context budgets. Includes a free calculator.',
    'tag':'Vibe Coding',
    'date':'August 7, 2026',
    'read':'7 min read',
    'excerpt':'AI coding bills balloon because the same context is resent on every call. Here is how to cut that spend without writing less code.',
    'body':'''
<p>AI coding can cost real money &mdash; teams report monthly API bills from $1,600 to $5,000. Most of that
spend is not the code the model writes; it is the <strong>context you resend on every request</strong>:
your system prompt, conversation history, and reused files. The fixes are simple, and you can model them
with our <a class="link" href="../ai-cost-calculator.html">AI Cost Calculator</a>.</p>

<h2>1. Cache the stable prefix</h2>
<p>System prompts, project rules (your CLAUDE.md), and fixed reference files rarely change between calls.
Providers bill cached tokens at roughly <strong>10%</strong> of the normal input rate. Turn on prompt caching
and the bulk of your context cost collapses. In the calculator above, toggle "Use prompt caching" to see the
savings on your own numbers.</p>

<h2>2. Route by difficulty</h2>
<p>You do not need the most expensive model for every task. Use a flagship model (Claude Sonnet 5, GPT-5.5) for
hard architecture and debugging, and a cheap model (Claude Haiku 4.5, Gemini 3.5 Flash) for boilerplate and refactors.
Tiered routing commonly cuts spend <strong>40&ndash;60%</strong>. Compare options in our
<a class="link" href="../model-compare.html">LLM Model Compare</a> tool.</p>

<h2>3. Shrink the context you resend</h2>
<p>Context bloat is the silent budget killer: every extra kilobyte is re-billed on every call. Prefer
targeted diffs over full-file rewrites, start a fresh session for a new task, and drop stale history.
One team cut per-request tokens <strong>83%</strong> just by sending patches instead of whole files.</p>

<h2>4. Cap the loop</h2>
<p>If a task is not solved in 15&ndash;25 turns, more turns will not help &mdash; you are in a loop. Stop,
change approach, or split the task. Unbounded agent loops are where bills quietly explode.</p>

<h2>Estimate before you build</h2>
<p>Plug your tokens and volume into the <a class="link" href="../ai-cost-calculator.html">AI Cost Calculator</a>
to see exactly how much each lever saves before you commit a budget.</p>

<h2>Tools with offers</h2>
<div class="aff-box">
  <div class="aff-head"><span class="aff-tag">Sponsored</span><span>Cost-efficient AI coding</span></div>
  <ul class="aff-list">
    <li><a class="aff-link" href="https://example.com/aff/claude-code" target="_blank" rel="sponsored nofollow noopener">Claude Code &rarr;</a><p class="aff-blurb">Prompt caching built in. Pro plan.</p></li>
    <li><a class="aff-link" href="https://example.com/aff/deepseek" target="_blank" rel="sponsored nofollow noopener">DeepSeek &rarr;</a><p class="aff-blurb">Open-weight models at a fraction of frontier pricing. API access.</p></li>
  </ul>
  <p class="aff-note">Affiliate links &mdash; commissions help keep Vibe Coding Tools free.</p>
</div>
'''
  },

  'is-vibe-coding-bad': {
    'title':'Is Vibe Coding Bad? The Honest Answer (2026)',
    'meta':'Vibe coding gets blamed for buggy code and job loss. Here is what the data and working developers actually say about its risks, limits, and when it is the right tool.',
    'tag':'Vibe Coding',
    'date':'August 7, 2026',
    'read':'7 min read',
    'excerpt':'Vibe coding is not magic and it is not a jobs apocalypse. It is a tool with a clear risk profile. Here is the honest, non-hyped version.',
    'body':'''
<p>"Vibe coding" — describing software in plain language and letting an AI write it — went from a joke to a
daily workflow in about a year. Along the way it picked up two loud camps: people calling it a scam that
produces unmaintainable garbage, and people calling it the end of programming jobs. Both are wrong. The
honest answer is more useful than either extreme.</p>

<h2>What "vibe coding" actually means</h2>
<p>Vibe coding is using an AI coding assistant (Cursor, Windsurf, Claude Code, or a chat model) to generate
code from a description rather than typing it by hand. You steer, test, and refine; the model does the
typing. It is a spectrum, not a switch — most developers today mix AI-generated and hand-written code.</p>

<h2>The real risks (they are specific, not vague)</h2>
<p>The criticism is not baseless, but it is specific. The genuine failure modes are:</p>
<ul>
  <li><strong>Unreviewed code in production.</strong> AI can produce code that runs but is wrong, insecure, or unmaintainable. Shipping it without review is the actual danger.</li>
  <li><strong>Hallucinated dependencies and APIs.</strong> Models invent libraries and functions. Left unchecked, this breaks builds and introduces supply-chain risk.</li>
  <li><strong>No mental model.</strong> If you cannot explain how the code works, you cannot debug it at 2 a.m. Vibe coding without learning degrades your own skill.</li>
  <li><strong>Hidden cost at scale.</strong> Generated code often resends huge context on every call; bills and latency creep up. Our <a class="link" href="../ai-cost-calculator.html">AI Cost Calculator</a> shows how fast that adds up.</li>
</ul>

<h2>Is it taking programming jobs?</h2>
<p>Not in the way headlines claim. The data shows AI coding tools are <em>raising output per developer</em>,
not eliminating developers. Surveys of working engineers in 2026 put daily AI-tool usage above 90% among
US developers, and the dominant effect is "ship more" rather than "hire fewer." The people most at risk are
those who refuse to use the tools, not the tools themselves.</p>

<h2>When vibe coding is the right call</h2>
<ul>
  <li><strong>Prototypes and internal tools</strong> — speed matters more than perfect architecture.</li>
  <li><strong>Boilerplate and refactors</strong> — let the model do the tedious parts.</li>
  <li><strong>Learning a new stack</strong> — generate, then read, then understand.</li>
</ul>

<h2>When you should NOT vibe code</h2>
<ul>
  <li><strong>Security-critical or safety-critical code</strong> — review every line, or write it yourself.</li>
  <li><strong>Code you will never understand</strong> — if you cannot maintain it, do not ship it.</li>
  <li><strong>Production systems with no test coverage</strong> — generated code needs tests around it.</li>
</ul>

<h2>The balanced verdict</h2>
<p>Vibe coding is not bad; <em>unreviewed</em> vibe coding is bad. Treat the model like a very fast, very
confident junior engineer: great for drafts, useless without review. Pair it with a
<a class="link" href="../ai-pr-review.html">PR review checklist</a> and an
<a class="link" href="../ai-security-checklist.html">AI security checklist</a>, keep learning, and it
becomes one of the highest-leverage tools you have.</p>

<h2>Tools with offers</h2>
<div class="aff-box">
  <div class="aff-head"><span class="aff-tag">Sponsored</span><span>Code with confidence</span></div>
  <ul class="aff-list">
    <li><a class="aff-link" href="https://example.com/aff/claude-code" target="_blank" rel="sponsored nofollow noopener">Claude Code &rarr;</a><p class="aff-blurb">Agentic coding with built-in review. Pro plan.</p></li>
    <li><a class="aff-link" href="https://example.com/aff/cursor" target="_blank" rel="sponsored nofollow noopener">Cursor &rarr;</a><p class="aff-blurb">Popular AI-first editor for fast iteration.</p></li>
  </ul>
  <p class="aff-note">Affiliate links &mdash; commissions help keep Vibe Coding Tools free.</p>
</div>
'''
  },

  'how-to-vibe-code-a-website': {
    'title':'How to Vibe Code a Website (Step by Step, 2026)',
    'meta':'A beginner-friendly walkthrough for building a real website by describing it to an AI — no deep coding background required. Tools, prompts, and the workflow that actually works.',
    'tag':'Vibe Coding',
    'date':'August 7, 2026',
    'read':'8 min read',
    'excerpt':'You do not need to be a programmer to ship a website in 2026. Here is the exact workflow: pick a tool, write a good spec, generate, test, and publish.',
    'body':'''
<p>You can build and publish a real website in an afternoon without writing code by hand. "Vibe coding" a
website means describing what you want in plain language and letting an AI tool generate the HTML, CSS, and
JavaScript. This guide walks the exact workflow that works for beginners.</p>

<h2>Step 1 — Write a one-page spec first</h2>
<p>Do not open the tool and start typing "make me a site." Spend ten minutes on a spec: what is the site
for, who visits, what pages, what it must do. A clear brief is the single biggest predictor of a good
result. Use our <a class="link" href="../project-brief-generator.html">Project Brief Generator</a> to
turn a vague idea into a structured brief the AI can actually follow.</p>

<h2>Step 2 — Pick a tool</h2>
<p>For a first website, an AI-first editor (Cursor, Windsurf) or an agent (Claude Code) both work. If you
have no setup preference, start with a chat model and ask it to build a single static HTML file — the
simplest thing that can go live. Compare options in our
<a class="link" href="../blog/cursor-vs-windsurf.html">Cursor vs Windsurf vs Claude Code</a> guide.</p>

<h2>Step 3 — Generate from the spec</h2>
<p>Paste your brief and ask for a complete, self-contained page. Good prompt anatomy matters: goal,
audience, constraints, and "do not invent features." Our
<a class="link" href="../prompt-generator.html">Prompt Generator</a> builds that structure for you so the
model does not guess.</p>

<h2>Step 4 — Test it like a visitor</h2>
<p>Open the file in a browser. Click every button. Resize the window. Does it break on mobile? Most "it
does not work" complaints come from skipping this step. If something is wrong, describe the symptom in
plain language and ask the model to fix it.</p>

<h2>Step 5 — Keep the context tight</h2>
<p>Each revision resends your whole conversation. Long sessions get expensive and the model forgets
details. Start a fresh chat per change, and use our
<a class="link" href="../ai-cost-calculator.html">AI Cost Calculator</a> to see how context size drives
your bill.</p>

<h2>Step 6 — Publish</h2>
<p>For a static site, drag the folder into Netlify or Cloudflare Pages and you are live with a free URL.
Point a custom domain at it later. No server, no database, no maintenance.</p>

<h2>Step 7 — Review before you trust it</h2>
<p>Before sharing, run our <a class="link" href="../ai-security-checklist.html">AI Security Checklist</a> —
generated sites sometimes leak keys or call unknown scripts. A two-minute check prevents embarrassing
mistakes.</p>

<h2>The honest part</h2>
<p>Vibe coding a website gets you 80% of the way fast. The last 20% — accessibility, performance, edge
cases — is where knowing a little HTML pays off. Treat the AI as a co-pilot, not a captain, and you will
ship something real today and understand it tomorrow.</p>

<h2>Tools with offers</h2>
<div class="aff-box">
  <div class="aff-head"><span class="aff-tag">Sponsored</span><span>Ship your first site</span></div>
  <ul class="aff-list">
    <li><a class="aff-link" href="https://example.com/aff/netlify" target="_blank" rel="sponsored nofollow noopener">Netlify &rarr;</a><p class="aff-blurb">Drag-drop deploy for static sites. Free tier.</p></li>
    <li><a class="aff-link" href="https://example.com/aff/cloudflare-pages" target="_blank" rel="sponsored nofollow noopener">Cloudflare Pages &rarr;</a><p class="aff-blurb">Fast, free static hosting on the edge.</p></li>
  </ul>
  <p class="aff-note">Affiliate links &mdash; commissions help keep Vibe Coding Tools free.</p>
</div>
'''
  },

  'best-ai-app-builder': {
    'title':'Best AI App Builder (2026): Compared & Ranked',
    'meta':'The best AI app builders let you ship real software by describing it. We compare the top platforms on ease, control, pricing, and who each one is for.',
    'tag':'Vibe Coding',
    'date':'August 7, 2026',
    'read':'10 min read',
    'excerpt':'Bubble, FlutterFlow, Cursor, Claude Code, v0, Replit Agent, Lovable — which AI app builder actually ships your idea? A no-hype comparison.',
    'body':'''
<p>AI app builders promise the same thing: describe what you want, get working software. In 2026 the
category split into two camps — <strong>no-code platforms</strong> (visual builders with AI assist) and
<strong>code-generation agents</strong> (AI that writes real code you can own and edit). This comparison
covers the leaders in each, with the trade-offs that actually matter when you ship.</p>

<h2>Comparison table</h2>
<div class="tablewrap"><table class="cmp">
  <thead><tr><th>Builder</th><th>Type</th><th>Best for</th><th>Own the code?</th><th>Price from</th></tr></thead>
  <tbody>
    <tr><td>Bubble</td><td>No-code</td><td>Complex web apps, logic-heavy</td><td>Export-limited</td><td>$29/mo</td></tr>
    <tr><td>FlutterFlow</td><td>No-code</td><td>Mobile + cross-platform</td><td>Yes (Flutter)</td><td>$30/mo</td></tr>
    <tr><td>Lovable</td><td>Code-gen</td><td>Fast web app MVPs</td><td>Yes</td><td>$20/mo</td></tr>
    <tr><td>v0 (Vercel)</td><td>Code-gen</td><td>React/Next UI</td><td>Yes</td><td>$20/mo</td></tr>
    <tr><td>Replit Agent</td><td>Code-gen</td><td>Full-stack, in-browser</td><td>Yes</td><td>$15/mo</td></tr>
    <tr><td>Cursor</td><td>Code-gen</td><td>Developers, full control</td><td>Yes</td><td>$20/mo</td></tr>
    <tr><td>Claude Code</td><td>Code-gen</td><td>Agentic, terminal-native</td><td>Yes</td><td>$20/mo</td></tr>
  </tbody>
</table></div>

<h2>No-code vs code-gen: the real difference</h2>
<p>No-code platforms (Bubble, FlutterFlow) are fastest for non-technical users but lock you into their
runtime — leaving is hard. Code-generation agents (Cursor, Claude Code, Lovable) produce real, portable
code you can host anywhere, which matters the moment you need custom logic or a fair price at scale.</p>

<h2>How to choose</h2>
<ul>
  <li><strong>Non-technical, need it yesterday:</strong> Lovable or v0 for web, FlutterFlow for mobile.</li>
  <li><strong>Developer, want control and portability:</strong> Cursor or Claude Code.</li>
  <li><strong>Complex business logic, will stay put:</strong> Bubble.</li>
  <li><strong>Tight budget, learning:</strong> Replit Agent's free tier.</li>
</ul>

<h2>The cost nobody mentions</h2>
<p>Subscriptions are the visible cost. The hidden one is <strong>API tokens if your app calls an LLM</strong>.
A viral feature can turn a $20/mo plan into a four-figure bill overnight. Model the spend first with our
<a class="link" href="../ai-cost-calculator.html">AI Cost Calculator</a>, and compare model prices in our
<a class="link" href="../model-compare.html">LLM Model Compare</a> tool before you commit.</p>

<h2>Verdict</h2>
<p>There is no single "best." For a portable, ownable MVP built by someone willing to learn a little, a
code-gen agent wins. For pure speed with zero learning curve, Lovable or v0. Pick by who you are, not by
the loudest marketing.</p>

<h2>Tools with offers</h2>
<div class="aff-box">
  <div class="aff-head"><span class="aff-tag">Sponsored</span><span>Build & ship faster</span></div>
  <ul class="aff-list">
    <li><a class="aff-link" href="https://example.com/aff/lovable" target="_blank" rel="sponsored nofollow noopener">Lovable &rarr;</a><p class="aff-blurb">Describe an app, get a deployable MVP.</p></li>
    <li><a class="aff-link" href="https://example.com/aff/cursor" target="_blank" rel="sponsored nofollow noopener">Cursor &rarr;</a><p class="aff-blurb">AI-first editor for full control.</p></li>
    <li><a class="aff-link" href="https://example.com/aff/flutterflow" target="_blank" rel="sponsored nofollow noopener">FlutterFlow &rarr;</a><p class="aff-blurb">No-code mobile + cross-platform.</p></li>
  </ul>
  <p class="aff-note">Affiliate links &mdash; commissions help keep Vibe Coding Tools free.</p>
</div>
'''
  },
}

def build_blog_index():
    meta = 'Practical how-to guides for vibe coding and AI-assisted development: tool comparisons, cost-saving workflows, and step-by-step build walkthroughs.'
    schema = '{"@context":"https://schema.org","@type":"Blog","name":"Vibe Coding Tools Blog","description":"'+meta.replace('"','\\"')+'"}'
    hero = ('''<div class="t-tool-hero article-hero">
      <div class="crumb"><a href="../index.html">Vibe Coding Tools</a> / Blog</div>
      <h1>Blog</h1>
      <p class="sub">Clear, practical guides to the tools you use every day — written for developers and everyday users.</p>
    </div>''')
    posts = ''
    for slug, c in BLOG.items():
        posts += (f'''<a class="post-card" href="{slug}.html">
          <span class="tag">{html.escape(c['tag'])}</span>
          <h3>{html.escape(c['title'])}</h3>
          <p>{html.escape(c['excerpt'])}</p>
          <span class="read">{html.escape(c['read'])} · {html.escape(c['date'])}</span>
        </a>''')
    body = hero + '<div class="post-grid">' + posts + '</div>'
    return page_brutalist('Blog — Vibe Coding Tools', meta, schema, body=body, prefix='../', page_id='blog', url='https://vibe.david-cells.com/blog/')

def build_blog_post(slug):
    c = BLOG[slug]
    meta = c['meta']
    schema = ('{"@context":"https://schema.org","@type":"BlogPosting","headline":"'
              + c['title'].replace('"','\\"')
              + '","author":{"@type":"Organization","name":"Vibe Coding Tools"},'
              + '"datePublished":"2026-08-03","publisher":{"@type":"Organization","name":"Vibe Coding Tools"}}')
    hero = (f'''<div class="t-tool-hero article-hero">
      <div class="crumb"><a href="index.html">Blog</a> / {html.escape(c['tag'])}</div>
      <h1>{html.escape(c['title'])}</h1>
      <p class="sub">By Vibe Coding Tools · {html.escape(c['date'])} · {html.escape(c['read'])}</p>
    </div>''')
    aff = aff_callout(AFF_BY_POST[slug]) if slug in AFF_BY_POST else ''
    body = hero + '<article class="article">' + c['body'] + '</article>' + aff
    return page_brutalist(c['title'] + ' — Vibe Coding Tools', meta, schema, body=body, prefix='../', page_id='blog', url='https://vibe.david-cells.com/blog/' + slug + '.html')

# ============================================================
# PRIVACY POLICY
# ============================================================
PRIVACY_SECTIONS = [
  ('no-collect', '1. Data We Do Not Collect',
   '''<p>All of our tools (the AI cost calculator, the prompt builder, the model compare, and the CLAUDE.md
   generator) run <strong>entirely inside your web browser</strong>. The tokens, prompts, project details,
   and rule files you enter are <strong>never uploaded to our servers</strong>. We do not have a backend,
   database, or API that receives your input. We cannot see, log, or store your data.</p>'''),
  ('local-storage', '2. Local Storage',
   '''<p>We do not use local storage or cookies of our own to track you or persist your inputs.
   Any temporary data held by the browser during a tool's operation is discarded when you leave the page.</p>'''),
  ('ads', '3. Advertising and Third-Party Cookies',
   '''<p>To keep the tools free, this site may display advertisements served by third-party networks
   such as <strong>Google AdSense</strong>. These partners may use cookies and similar technologies
   to serve ads based on your prior visits to this or other websites. This is standard behavior for
   ad-supported sites and is governed by the third party's own privacy policies.</p>
   <ul>
     <li>You can review how Google uses advertising cookies here:
       <a class="link" href="https://policies.google.com/technologies/ads" target="_blank" rel="noopener">Google Ads Policy</a>.</li>
     <li>You can opt out of personalized advertising via
       <a class="link" href="https://www.google.com/settings/ads" target="_blank" rel="noopener">Google Ads Settings</a>
       or <a class="link" href="https://optout.aboutads.info/" target="_blank" rel="noopener">YourAdChoices</a>.</li>
   </ul>'''),
  ('children', '4. Children\'s Privacy',
   '''<p>This site is not directed to children under 13, and we do not knowingly collect personal information
   from children.</p>'''),
  ('changes', '5. Changes',
   '''<p>We may update this policy from time to time. Material changes will be reflected by the "last updated"
   date above.</p>'''),
  ('contact', '6. Contact',
   f'''<p>If you have questions about this policy or the site, contact us at
   <a class="link" href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>.</p>'''),
]

def build_privacy():
    meta = 'Privacy Policy for Vibe Coding Tools free online tools. We do not collect, store, or upload your data. All processing happens locally in your browser.'
    schema = '{"@context":"https://schema.org","@type":"WebPage","name":"Vibe Coding Tools Privacy Policy"}'
    hero = ('''<div class="t-tool-hero article-hero">
      <div class="crumb"><a href="index.html">Vibe Coding Tools</a> / Privacy</div>
      <h1>Privacy Policy</h1>
      <p class="sub">Last updated: August 3, 2026</p>
    </div>''')
    toc = '<nav class="toc"><div class="tt">On this page</div><ol>'
    for sid, title, _ in PRIVACY_SECTIONS:
        toc += f'<li><a href="#{sid}">{html.escape(title.split(" ",1)[1] if " " in title else title)}</a></li>'
    toc += '</ol></nav>'
    article = '<article class="article"><p>Vibe Coding Tools ("we", "us", "the site") provides free, browser-based developer and utility tools. '
    article += 'This policy explains what data we handle — and, importantly, what we do <strong>not</strong> handle.</p>'
    for sid, title, body in PRIVACY_SECTIONS:
        article += f'<h2 id="{sid}">{html.escape(title)}</h2>{body}'
    article += ('<div class="callout">Bottom line: the tools themselves collect nothing. The only tracking on this site '
                'comes from third-party ad networks, which you can opt out of at any time.</div>')
    article += '</article>'
    body = hero + toc + article
    return page_brutalist('Privacy Policy — Vibe Coding Tools', meta, schema, body=body, page_id='privacy', url='https://vibe.david-cells.com/privacy.html')

# ============================================================
def build_about():
    meta = 'Vibe Coding Tools is a free, privacy-first collection of browser-based developer tools, built and maintained by independent developer David Dai. No accounts, no servers, no uploads.'
    schema = '{"@context":"https://schema.org","@type":"AboutPage","name":"About Vibe Coding Tools"}'
    hero = ('''<div class="t-tool-hero article-hero">
      <div class="crumb"><a href="index.html">Vibe Coding Tools</a> / About</div>
      <h1>About Vibe Coding Tools</h1>
      <p class="sub">Free, private, browser-based tools — built by one developer who got tired of uploading data to random websites.</p>
    </div>''')
    article = ('''
<article class="article">
  <h2>What Vibe Coding Tools is</h2>
  <p>Vibe Coding Tools is a growing collection of small, focused utilities for developers building with AI:
  an AI Cost Calculator, an LLM Model Compare, a Prompt Generator, a CLAUDE.md Generator, a Project Brief
  Generator, an AI PR Review checklist, and an AI Security Checklist. Every tool solves one concrete
  problem and does it well — and runs entirely in your browser.</p>

  <h2>Who maintains it</h2>
  <p>Vibe Coding Tools is designed, built, and maintained by <strong>David Dai</strong>, an independent developer.
  There is no company behind it and no venture capital — just one person who ships useful tools and keeps
  them working. You can reach David directly at
  <a class="link" href="mailto:''' + CONTACT_EMAIL + '''">''' + CONTACT_EMAIL + '''</a>.</p>

  <h2>Why it exists: a privacy-first philosophy</h2>
  <p>Most online developer tools work by <em>uploading your data to a server</em>. Paste a JWT, a private
  config, or a screenshot, and it leaves your machine. That is a real risk: tokens leak, files contain
  secrets, and you rarely know where the data ends up.</p>
  <p>Vibe Coding Tools takes the opposite approach. <strong>Every tool runs entirely in your browser.</strong>
  Your inputs are processed locally with JavaScript and never uploaded. There are no accounts to create,
  no servers to send to, and nothing to leak. If you are offline, the tools still work.</p>
  <div class="callout">The tools themselves collect nothing. We do not store, transmit, or profile your
  data. The only third-party code on the site is the advertising network that keeps the project free —
  and you can opt out of personalized ads at any time.</div>

  <h2>How it is funded</h2>
  <p>Vibe Coding Tools is free to use forever. To cover hosting and development time, the site may show
  non-intrusive advertisements from networks such as Google AdSense. The tools themselves remain
  completely free and ad-free in their function.</p>

  <h2>The bigger idea</h2>
  <p>The web is full of tools that ask for too much. Vibe Coding Tools is an experiment in the opposite:
  powerful utilities that respect your data by simply never asking for it. If that resonates, the
  <a class="link" href="blog/index.html">Blog</a> explains how each tool works and why client-side
  processing is safer.</p>
</article>
''')
    body = hero + article
    return page_brutalist('About Vibe Coding Tools — Privacy-first developer tools', meta, schema, body=body, page_id='about', url='https://vibe.david-cells.com/about.html')

# ============================================================
def build_contact():
    meta = 'Get in touch with Vibe Coding Tools. Questions, feedback, or tool requests — email us directly. No forms, no middlemen.'
    schema = '{"@context":"https://schema.org","@type":"ContactPage","name":"Contact Vibe Coding Tools"}'
    hero = ('''<div class="t-tool-hero article-hero">
      <div class="crumb"><a href="index.html">Vibe Coding Tools</a> / Contact</div>
      <h1>Contact</h1>
      <p class="sub">Questions, feedback, bug reports, or a tool you wish existed? Reach out directly.</p>
    </div>''')
    article = ('''
<article class="article">
  <h2>Email</h2>
  <p>The fastest way to reach us is by email:</p>
  <p style="margin:18px 0"><a class="cta-mail" href="mailto:''' + CONTACT_EMAIL + '''">''' + CONTACT_EMAIL + '''</a></p>
  <p>We read every message and typically reply within a few days. Because this is a one-person project,
  please be patient if a reply takes a little longer during busy periods.</p>

  <h2>What to include</h2>
  <ul>
    <li><strong>Bug reports</strong> — tell us which tool, what you did, and what you expected vs. what happened.</li>
    <li><strong>Tool requests</strong> — if you need a utility we do not have yet, we want to hear about it.</li>
    <li><strong>Privacy questions</strong> — see the <a class="link" href="privacy.html">Privacy Policy</a> first; email us if anything is unclear.</li>
  </ul>

  <h2>A note on this site</h2>
  <p>Vibe Coding Tools is a static, client-side site. There is no contact form by design — submitting data through
  a server would contradict the privacy-first principle the project is built on. A direct email link keeps
  things simple and keeps your message in your hands.</p>
  <div class="callout">Prefer to browse first? The <a class="link" href="blog/index.html">Blog</a> covers how
  every tool works, and the <a class="link" href="about.html">About</a> page explains the project's philosophy.</div>
</article>
''')
    body = hero + article
    return page_brutalist('Contact Vibe Coding Tools — Get in touch', meta, schema, body=body, page_id='contact', url='https://vibe.david-cells.com/contact.html')

# ============================================================
def main():
    with open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(build_index())
    for slug, *_ in TOOLS:
        with open(os.path.join(OUT, slug + '.html'), 'w', encoding='utf-8') as f:
            f.write(build_tool(slug))
    # blog
    with open(os.path.join(OUT, 'blog', 'index.html'), 'w', encoding='utf-8') as f:
        f.write(build_blog_index())
    for slug in BLOG:
        with open(os.path.join(OUT, 'blog', slug + '.html'), 'w', encoding='utf-8') as f:
            f.write(build_blog_post(slug))
    # per-model pricing pages (programmatic SEO)
    os.makedirs(os.path.join(OUT, 'models'), exist_ok=True)
    for m in MODELS:
        with open(os.path.join(OUT, 'models', m['id'] + '.html'), 'w', encoding='utf-8') as f:
            f.write(build_model_page(m))
    # about + contact
    with open(os.path.join(OUT, 'about.html'), 'w', encoding='utf-8') as f:
        f.write(build_about())
    with open(os.path.join(OUT, 'contact.html'), 'w', encoding='utf-8') as f:
        f.write(build_contact())
    # sitemap.xml
    urls = ['https://vibe.david-cells.com/', 'https://vibe.david-cells.com/about.html',
            'https://vibe.david-cells.com/contact.html', 'https://vibe.david-cells.com/privacy.html']
    for slug, *_ in TOOLS:
        urls.append('https://vibe.david-cells.com/' + slug + '.html')
    urls.append('https://vibe.david-cells.com/blog/')
    for slug in BLOG:
        urls.append('https://vibe.david-cells.com/blog/' + slug + '.html')
    for m in MODELS:
        urls.append('https://vibe.david-cells.com/models/' + m['id'] + '.html')
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        sitemap += '  <url><loc>' + u + '</loc></url>\n'
    sitemap += '</urlset>\n'
    with open(os.path.join(OUT, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write(sitemap)
    # robots.txt
    robots = ('User-agent: *\nAllow: /\n\nSitemap: https://vibe.david-cells.com/sitemap.xml\n')
    with open(os.path.join(OUT, 'robots.txt'), 'w', encoding='utf-8') as f:
        f.write(robots)
    # privacy
    with open(os.path.join(OUT, 'privacy.html'), 'w', encoding='utf-8') as f:
        f.write(build_privacy())
    # ads.txt  — replace the placeholder pub ID with your real AdSense publisher ID
    # (ca-pub-XXXXXXXXXXXXXXXX) once approved. Format: google.com, pub-XXXX, DIRECT, f08c47fec0942fa0
    adsense_pub = 'pub-4110184622096343'  # real AdSense publisher ID
    ads_txt = ('google.com, %s, DIRECT, f08c47fec0942fa0\n' % adsense_pub)
    with open(os.path.join(OUT, 'ads.txt'), 'w', encoding='utf-8') as f:
        f.write(ads_txt)
    print('Generated index + %d tool pages + blog (index + %d posts) + privacy + about + contact' % (len(TOOLS), len(BLOG)))

if __name__ == '__main__':
    main()
