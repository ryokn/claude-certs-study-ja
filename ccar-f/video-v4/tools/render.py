#!/usr/bin/env python3
"""Approved series renderer: diagram types, panel headers, L/R focus (no dimming)."""
from pathlib import Path
import json,sys,subprocess,wave,re,math,argparse,os
from PIL import Image,ImageDraw

KIT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KIT_ROOT))
from tools import common as p  # noqa: E402

ROOT = None  # set in main()
BUILD = None
L=(66,170,965,765); RB=(1000,170,1858,765)
TYPE_NAME={'flow':'流れ図','table':'比較表','ba':'前後比較','struct':'構造図','branch':'分岐図','grid':'整理図'}
INK='#1b2233'

def parse(path):
 text=re.sub(r'<!--.*?-->','',open(path,encoding='utf-8').read(),flags=re.S)
 slides=[];cur=None;incode=False
 for raw in text.splitlines():
  line=raw.rstrip()
  if line.startswith('```'): incode=not incode; continue
  if incode: cur['code'].append(line); continue
  if line.startswith('## SLIDE:'):
   cur=dict(title=line[9:].strip(),code=[],lines=[],nodes=[],rows=[],cards=[]);slides.append(cur);continue
  if cur is None or not line.strip(): continue
  m=re.match(r'@(\w+)\s*:\s*(.*)$',line)
  if m:
   k,v=m.group(1),m.group(2).strip().replace('\\n','\n')
   parts=[x.strip() for x in v.split(' | ')]
   if k=='diagram': cur['dtype'],cur['dlabel']=parts
   elif k=='node': cur['nodes'].append([x.strip() for x in v.split(' || ')])
   elif k=='row': cur['rows'].append(parts)
   elif k=='card': cur['cards'].append(parts)
   elif k in ('cols','items','branches','before','after'): cur[k]=parts
   else: cur[k]=v
   continue
  m=re.match(r'^\[([LR])(?::(\d+))?\]\s*(\S+?)[:：]\s*(.+)$',line)
  assert m,('line without [L]/[R] marker',line)
  spk=p.ALIASES.get(m.group(3),m.group(3));assert spk in p.SPEAKERS,spk
  cur['lines'].append((m.group(1),spk,m.group(4).strip(),None if m.group(2) is None else int(m.group(2))))
 for s in slides: assert s.get('dtype') in TYPE_NAME,(s['title'],s.get('dtype'))
 chap=[int(re.match(r'第(\d)章',s['title']).group(1)) for s in slides]
 for i,s in enumerate(slides):
  s['chapter']=chap[i];s['total']=chap.count(chap[i]);s['current']=chap[:i+1].count(chap[i])
 return slides

HIRA=re.compile(r'[ぁ-ゖ]')
CLOSE='、。！？」』）)ーぁぃぅぇぉっゃゅょ…'
def sub_wrap(text,maxw=1320):
 f=p.font(48,True)
 if f.getlength(text)<=maxw: return [text]
 toks=re.findall(r"[A-Za-z0-9_.\-/<>{}[\]\"'=~:%$]+|.",text)
 best=None
 for i in range(1,len(toks)):
  a=''.join(toks[:i]);b=''.join(toks[i:])
  if f.getlength(a)>maxw or f.getlength(b)>maxw: continue
  prev,nxt=toks[i-1],toks[i]
  if nxt[0] in CLOSE: continue
  if prev in '、。！？': pr=3 if f.getlength(a)>=420 else 2
  elif HIRA.match(prev[-1]) and not HIRA.match(nxt[0]): pr=2
  elif prev in '」）' or nxt in '「（': pr=2
  elif HIRA.match(prev[-1]) and HIRA.match(nxt[0]): pr=0
  else: pr=1
  key=(pr,f.getlength(a))
  if best is None or key>best[0]: best=(key,[a,b])
 assert best,('subtitle >2 lines',text)
 return best[1]

def smart_wrap(text,f,maxw):
 toks=re.findall(r"[A-Za-z0-9_.\-/<>{}[\]\"'=~:%$]+|.",text);out=[]
 while toks:
  if f.getlength(''.join(toks))<=maxw: out.append(''.join(toks));break
  cands=[]
  for i in range(1,len(toks)):
   a=''.join(toks[:i])
   if f.getlength(a)>maxw: break
   prev,nxt=toks[i-1],toks[i]
   if nxt[0] in CLOSE: continue
   if prev in '、。！？・': pr=3
   elif HIRA.match(prev[-1]) and not HIRA.match(nxt[0]): pr=2
   elif prev in '」）' or nxt in '「（' or prev==' ': pr=2
   elif HIRA.match(prev[-1]) and HIRA.match(nxt[0]): pr=0
   else: pr=1
   cands.append((pr,f.getlength(a),i))
  if not cands: out.append(toks[0]);toks=toks[1:];continue
  good=[c for c in cands if c[0]>=2 and c[1]>=0.4*maxw]
  i=max(good or [c for c in cands if c[0]>=1] or cands,key=lambda c:(c[1]) )[2]
  out.append(''.join(toks[:i]).rstrip());toks=toks[i:]
  while toks and toks[0]==' ': toks=toks[1:]
 return out

def check_subs(slides):
 for s in slides:
  for side,spk,line,rv in s['lines']:
   w=sub_wrap(p.disp(line))
   if len(w)==2: print('WRAP',w[0],'／',w[1])

def prepare(slides):
 timeline=[];pcm=bytearray();t=0
 for si,s in enumerate(slides):
  for li,(side,speaker,line,rv) in enumerate(s['lines']):
   wp=p.tts(p.voicevox_url(),p.yomi(line),speaker,str(BUILD/'wav'))
   dur,sr,ch,sw=p.wav_info(wp)
   with wave.open(wp) as w: pcm.extend(w.readframes(w.getnframes()))
   gap=.16+(.35 if li==len(s['lines'])-1 else 0)
   pcm.extend(b'\0'*int(gap*sr)*ch*sw)
   timeline.append(dict(slide=si+1,side=side,reveal=rv,speaker=speaker,text=p.disp(line),start=t,dur=dur+gap))
   t+=dur+gap
  print('slide',si+1,'elapsed',round(t,2),flush=True)
 with wave.open(str(BUILD/'voice.wav'),'wb') as w:
  w.setnchannels(ch);w.setsampwidth(sw);w.setframerate(sr);w.writeframes(pcm)
 (BUILD/'timeline.json').write_text(json.dumps(timeline,ensure_ascii=False,indent=2))
 print('Duration:',t,flush=True)
 return timeline,t

def center(d,box,text,size=36,fill=INK,bold=True):
 f=p.font(size,bold);lines=[]
 for line in text.split('\n'): lines.extend(smart_wrap(line,f,box[2]-box[0]-36))
 assert len(lines)*size*1.3<box[3]-box[1],('overflow',text,lines,box)
 assert all(f.getlength(l)<=box[2]-box[0]-16 for l in lines),('too wide',text,box)
 yy=(box[1]+box[3]-len(lines)*size*1.3)/2-5
 for line in lines:
  d.text(((box[0]+box[2]-f.getlength(line))/2,yy),line,font=f,fill=fill);yy+=size*1.3

def arrow(d,x0,y0,x1,y1,col='#555555'):
 d.line((x0,y0,x1,y1),fill=col,width=4)
 a=math.atan2(y1-y0,x1-x0);L_=16
 pts=[(x1,y1)]+[(x1-L_*math.cos(a)+s*9*math.sin(a),y1-L_*math.sin(a)-s*9*math.cos(a)) for s in (1,-1)]
 d.polygon(pts,fill=col)

def header(d,box,tag,tagcol,label,dark):
 x0,y0,x1,y1=box;f=p.font(30,True);tw=f.getlength(tag)
 d.rounded_rectangle((x0+18,y0+16,x0+18+tw+32,y0+64),10,fill=tagcol)
 d.text((x0+34,y0+20),tag,font=f,fill='white')
 lx=x0+18+tw+50;assert lx+p.font(32,True).getlength(label)<=x1-150,('header label too long',label)
 d.text((lx,y0+20),label,font=p.font(32,True),fill='#e6e9f5' if dark else '#2b2f36')
 d.line((x0+18,y0+80,x1-18,y0+80),fill='#3a3f58' if dark else '#d5d9de',width=2)

# ---- diagram types (content area x 1030..1828, y 275..745) ----
X0,X1,Y0,Y1=1030,1828,275,745
ROWCOL=['#89b4fa','#fde68a','#a6e3a1']
def boxcol(text,ri):
 if text.startswith('いいえ'): return '#f38ba8'
 if text.startswith('はい'): return '#a6e3a1'
 return ROWCOL[ri%3]

def d_flow(d,s):
 nodes=s['nodes'];n=len(nodes);note=s.get('note')
 y1=Y1-(95 if note else 0);ag=70 if n<=3 else 42
 bh=min(130,(y1-Y0-(n-1)*ag)/n);tot=n*bh+(n-1)*ag;y=Y0+(y1-Y0-tot)/2
 rects=[]
 for ri,row in enumerate(nodes):
  k=len(row);gap=28
  if k==1: xs=[(X0+50,X1-50)]
  else:
   w=(X1-X0-(k-1)*gap)/k;xs=[(X0+i*(w+gap),X0+i*(w+gap)+w) for i in range(k)]
  rr=[]
  for (a,b),txt in zip(xs,row):
   r=(a,y,b,y+bh);d.rounded_rectangle(r,12,fill=boxcol(txt,ri));center(d,r,txt,36 if k<3 else 34);rr.append(r)
  rects.append(rr);y+=bh+ag
 for up,dn in zip(rects,rects[1:]):
  for a in up:
   for b in dn:
    ax=(a[0]+a[2])/2;bx=(b[0]+b[2])/2
    if len(up)>1 and len(dn)>1 and up.index(a)!=dn.index(b): continue
    arrow(d,ax,a[3]+4,bx,b[1]-6)
 if note:
  r=(X0,Y1-75,X1,Y1);d.rounded_rectangle(r,12,fill='#fff4d6',outline='#d97706',width=3);center(d,r,note,32,'#7c2d12')

def d_table(d,s):
 note=s.get('note');nv=len(s['cols']);sz=int(s.get('size',34))
 lw={1:240,2:220,3:150}[nv];cols=[X0,X0+lw]+[X0+lw+(X1-X0-lw)*(i+1)/nv for i in range(nv)]
 y=Y0+10;top=y;nr=len(s['rows'])
 avail=Y1-(100 if note else 0)-y-70;rh=min(120,avail/nr)
 d.rounded_rectangle((X0,y,X1,y+70),8,fill='#2f6f4f')
 for i,h in enumerate(s['cols']):center(d,(cols[i+1],y,cols[i+2],y+70),h,sz,'white')
 y+=70;vc=['#1e3a8a','#9d174d','#14532d']
 for r,row in enumerate(s['rows']):
  d.rectangle((X0,y,X1,y+rh),fill='#f3f6f4' if r%2==0 else 'white')
  center(d,(cols[0],y,cols[1],y+rh),row[0],min(sz,32),'#2f6f4f')
  for c in range(nv):center(d,(cols[c+1],y,cols[c+2],y+rh),row[c+1],sz,vc[c] if nv>1 else INK)
  y+=rh
 d.rectangle((X0,top,X1,y),outline='#c9d3cc',width=2)
 for c in cols[1:-1]:d.line((c,top,c,y),fill='#c9d3cc',width=2)
 if note:
  r=(X0,Y1-80,X1,Y1);d.rounded_rectangle(r,12,fill='#fff4d6',outline='#d97706',width=3);center(d,r,note,32,'#7c2d12')

def d_ba(d,s):
 note=s.get('note');y=Y0+(5 if note else 25);bh=200
 for i,((tag,txt),col) in enumerate(zip([s['before'],s['after']],['#64748b','#d97706'])):
  x=1040+i*410;box=(x,y,x+370,y+bh)
  d.rounded_rectangle(box,14,fill='#f3f6f4',outline=col,width=4)
  d.rounded_rectangle((x,y,x+370,y+60),14,fill=col);d.rectangle((x,y+30,x+370,y+60),fill=col)
  center(d,(x,y,x+370,y+60),tag,34,'white');center(d,(x,y+64,x+370,y+bh-4),txt,36)
 arrow(d,1429,y+bh+12,1429,y+bh+52)
 arrow(d,1410,y+bh/2,1446,y+bh/2,'#888888')
 r=(1040,y+bh+65,1820,y+bh+160);d.rounded_rectangle(r,14,fill='#a6e3a1');center(d,r,s['result'],36)
 if note:
  r=(1040,y+bh+180,1820,y+bh+260);assert r[3]<=Y1
  d.rounded_rectangle(r,12,fill='#eef2ff',outline='#6366f1',width=3);center(d,r,note,32,'#3730a3')

def d_struct(d,s):
 cx=(X0+X1)/2
 r=(cx-260,Y0,cx+260,Y0+72);d.rounded_rectangle(r,12,fill='#89b4fa');center(d,r,s['from'],34)
 arrow(d,cx,Y0+78,cx,Y0+118)
 card=(X0+20,Y0+124,X1-20,Y0+330);d.rounded_rectangle(card,14,fill='#fff7e0',outline='#d97706',width=3)
 center(d,(card[0],card[1]+4,card[2],card[1]+56),'構造化サマリー（項目を決める）',30,'#92400e')
 items=s['items'];rows=[items[:3],items[3:]];yy=card[1]+64
 for row in rows:
  w=220;g=18;tw=len(row)*w+(len(row)-1)*g;x=cx-tw/2
  for it in row:
   c=(x,yy,x+w,yy+62);d.rounded_rectangle(c,30,fill='white',outline='#d97706',width=2);center(d,c,it,32);x+=w+g
  yy+=72
 arrow(d,cx,card[3]+6,cx,card[3]+46)
 r=(cx-360,card[3]+52,cx+360,Y1);d.rounded_rectangle(r,12,fill='#a6e3a1')
 center(d,(r[0],r[1]+4,r[2],r[1]+50),s['to'],34)
 center(d,(r[0],r[1]+46,r[2],r[3]),'（'+s['note']+'）',28,'#14532d',False)

def d_branch(d,s):
 cx=(X0+X1)/2
 r=(cx-230,Y0+5,cx+230,Y0+85);d.rounded_rectangle(r,12,fill='#89b4fa');center(d,r,s['root'],36)
 bs=[]
 for i,(txt,col) in enumerate(zip(s['branches'],['#fde68a','#f9a8d4'])):
  x=1045+i*420;b=(x,Y0+165,x+360,Y0+265);d.rounded_rectangle(b,12,fill=col);center(d,b,txt,36);bs.append(b)
  arrow(d,cx+(-60 if i==0 else 60),Y0+89,(b[0]+b[2])/2,b[1]-6)
 sh=(X0+10,Y0+335,X1-10,Y1-5)
 for b in bs:
  xm=(b[0]+b[2])/2
  for yy in range(int(b[3])+6,int(sh[1])-4,16): d.line((xm,yy,xm,yy+8),fill='#888888',width=4)
 d.rounded_rectangle(sh,14,fill='#f1f5f9',outline='#d97706',width=4);center(d,sh,s['shared'],34,'#7c2d12')

def d_grid(d,s,reveal=None):
 cols=['#2f6f4f','#1e3a8a','#9d174d','#92400e','#5b21b6']
 cards=s['cards'];n=len(cards)
 for i,(title,sub) in enumerate(cards):
  show=reveal is None or i<reveal
  if n==4:
   x=1040+(i%2)*400;y=Y0+5+(i//2)*240;c=(x,y,x+380,y+220)
   d.rounded_rectangle(c,14,fill='#f8fafc',outline=cols[i],width=4)
   d.rounded_rectangle((x,y,x+380,y+76),14,fill=cols[i]);d.rectangle((x,y+40,x+380,y+76),fill=cols[i])
   center(d,(x,y,x+380,y+76),title,36,'white');center(d,(x,y+80,x+380,y+216),sub if show else '？',32,INK)
  else:
   g=14;h=(Y1-Y0-(n-1)*g)/n;y=Y0+i*(h+g);c=(X0,y,X1,y+h);tw=230 if n<=3 else 150
   d.rounded_rectangle(c,14,fill='#f8fafc',outline=cols[i],width=4)
   d.rounded_rectangle((X0,y,X0+tw,y+h),14,fill=cols[i]);d.rectangle((X0+tw-20,y,X0+tw,y+h),fill=cols[i])
   center(d,(X0,y,X0+tw,y+h),title,36 if n<=3 else 34,'white')
   center(d,(X0+tw,y,X1,y+h),sub if show else '？',34 if n<=3 else 34,INK if show else '#9ca3af')

DRAW=dict(flow=d_flow,table=d_table,ba=d_ba,struct=d_struct,branch=d_branch,grid=d_grid)

def body(s,reveal=None):
 im=Image.new('RGB',(1920,1080),'#1b2233');d=ImageDraw.Draw(im)
 d.rounded_rectangle((30,30,1890,790),18,fill='#fbfbf8')
 d.rounded_rectangle((30,30,1890,130),18,fill='#2f6f4f');d.rectangle((30,80,1890,130),fill='#2f6f4f')
 assert p.font(54,True).getlength(s['title'])<1560,s['title']
 d.text((66,47),s['title'],font=p.font(54,True),fill='white')
 pt=f"{s['current']} / {s['total']}";px=min(1710,1866-int(p.font(40,True).getlength(pt))-52)
 assert p.font(54,True).getlength(s['title'])<px-66-30,s['title']
 d.rounded_rectangle((px,50,1866,112),30,fill='#1f4d36')
 center(d,(px,50,1866,112),pt,40,'white')
 d.rounded_rectangle(L,14,fill='#1e1e2e');header(d,L,'具体例','#7c5cff',s['code_label'],True)
 y=L[1]+100;lh=54
 for line in s['code']:
  assert p.font(38,mono=True).getlength(line)<=843,(s['title'],line)
  assert y+50<=L[3]-8,(s['title'],'code height')
  d.text((94,y),line,font=p.font(38,mono=True),fill=p.code_color(line));y+=lh
 d.rounded_rectangle(RB,14,fill='white',outline='#c9d3cc',width=3)
 header(d,RB,TYPE_NAME[s['dtype']],'#2f8f5f',s['dlabel'],False)
 (d_grid(d,s,reveal) if s['dtype']=='grid' else DRAW[s['dtype']](d,s))
 return im

def focus(im,side):
 a=im.copy();d=ImageDraw.Draw(a);act=RB if side=='R' else L
 d.rounded_rectangle((act[0]-8,act[1]-8,act[2]+8,act[3]+8),18,outline='#ffb000',width=8)
 f=p.font(28,True);t='いまココ';tw=f.getlength(t)
 d.rounded_rectangle((act[2]-tw-40,act[1]-24,act[2]+8,act[1]+22),12,fill='#ffb000');d.text((act[2]-tw-18,act[1]-22),t,font=f,fill='#1b2233')
 return a

def frame(base,speaker,text):
 im=base.copy();d=ImageDraw.Draw(im)
 for kind,cx in [('めたん',135),('ずんだもん',1785)]:
  head,_=p.load_head(kind,dim=kind!=speaker)
  im.paste(head,(int(cx-head.width/2),int(1080-66-head.height)),head)
 d=ImageDraw.Draw(im)
 for kind,cx in [('めたん',135),('ずんだもん',1785)]:
  name=p.SPEAKERS[kind]['name'];f=p.font(28,True);tw=f.getlength(name)
  col=p.SPEAKERS[kind]['tag'] if kind==speaker else '#787882'
  d.rounded_rectangle((cx-tw/2-14,1020,cx+tw/2+14,1066),10,fill=col)
  d.text((cx-tw/2,1019),name,font=f,fill='white')
 d.rounded_rectangle((270,808,1650,1064),16,fill='black',outline=p.SPEAKERS[speaker]['color'],width=4)
 lines=sub_wrap(text)
 yy=830
 for line in lines:d.text((300,yy),line,font=p.font(48,True),fill='white');yy+=70
 return im

def render(slides,timeline,t):
 cache={}
 def base(si,rv):
  k=(si,rv)
  if k not in cache: cache[k]=body(slides[si],rv)
  return cache[k]
 for i,s_ in enumerate(slides):base(i,None).save(BUILD/'slides'/f'{i+1:02}.png')
 concat=[]
 for n,e in enumerate(timeline):
  fn=BUILD/'frames'/f'{n+1:04}.png';frame(focus(base(e['slide']-1,e['reveal']),e['side']),e['speaker'],e['text']).save(fn)
  concat.append(f"file '{fn}'\nduration {e['dur']:.6f}\n")
 end=Image.new('RGB',(1920,1080),'#1b2233');de=ImageDraw.Draw(end)
 center(de,(0,330,1920,430),'ご視聴ありがとうございました',64,'white')
 center(de,(0,500,1920,560),'VOICEVOX:ずんだもん / VOICEVOX:四国めたん',40,'#cfe8d8')
 center(de,(0,580,1920,640),'BGM：昼下がり気分（KK / OpenTracks）',36,'#aabbcc')
 ef=BUILD/'frames'/'end.png';end.save(ef)
 concat.append(f"file '{ef}'\nduration 4\n")
 (BUILD/'frames.txt').write_text(''.join(concat))
 total=t+4
 subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','warning','-f','concat','-safe','0','-i',str(BUILD/'frames.txt'),'-i',str(BUILD/'voice.wav'),'-af','apad','-vf','fps=30,format=yuv420p,tpad=stop_mode=clone:stop_duration=4','-c:v','libx264','-threads','4','-preset','fast','-tune','stillimage','-crf','20','-c:a','aac','-b:a','192k','-ar','48000','-t',f'{total:.3f}','-movflags','+faststart',str(ROOT/OUT_VOICE)],check=True)

OUT_VOICE = 'voice-only.mp4'

def setup(ep_dir: Path):
 global ROOT, BUILD
 ROOT = ep_dir.resolve()
 BUILD = ROOT / 'build'
 for name in ('wav', 'frames', 'slides'):
  (BUILD / name).mkdir(parents=True, exist_ok=True)

def run(ep_dir: Path, *, slides_only=False, tts_only=False, max_slides=None, out_voice=None):
 global OUT_VOICE
 setup(ep_dir)
 OUT_VOICE = out_voice or 'voice-only.mp4'
 script = ROOT / 'script.md'
 assert script.exists(), f'missing {script}'
 slides = parse(str(script))
 if max_slides:
  slides = slides[:max_slides]
  # recompute chapter counters for subset
  chap = [s['chapter'] for s in slides]
  for i, s in enumerate(slides):
   s['total'] = chap.count(chap[i]); s['current'] = chap[:i+1].count(chap[i])
 check_subs(slides)
 if slides_only:
  for i, s in enumerate(slides):
   body(s).save(BUILD / 'slides' / f'{i+1:02}.png')
  print('slides-only:', BUILD / 'slides')
  return None, 0
 tl, t = prepare(slides)
 if not tts_only:
  render(slides, tl, t)
 return tl, t

if __name__ == '__main__':
 ap = argparse.ArgumentParser()
 ap.add_argument('episode_dir', nargs='?', default='.')
 ap.add_argument('--slides-only', action='store_true')
 ap.add_argument('--tts-only', action='store_true')
 ap.add_argument('--max-slides', type=int, default=None)
 ap.add_argument('--out-voice', default='voice-only.mp4')
 a = ap.parse_args()
 run(Path(a.episode_dir), slides_only=a.slides_only, tts_only=a.tts_only,
     max_slides=a.max_slides, out_voice=a.out_voice)
