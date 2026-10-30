from PIL import Image, ImageDraw, ImageFont
import os
BASE=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT=os.path.join(BASE,"docs/assets"); os.makedirs(OUT,exist_ok=True)
NAVY=(11,18,32); TEAL=(45,212,191); WHITE=(255,255,255); LIGHT=(245,247,250); GOLD=(251,191,36)
def font(sz,bold=False):
    try: return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",sz)
    except: return ImageFont.load_default()
def loop_mark(d,cx,cy,s,color,wd=8):
    d.ellipse([cx-s,cy-s,cx+s,cy+s],outline=color,width=wd)
    d.arc([cx-s,cy-s,cx+s,cy+s],start=20,end=300,fill=color,width=wd)
    d.polygon([(cx+s*0.78,cy-s*0.32),(cx+s*0.32,cy-s*0.32),(cx+s*0.78,cy+s*0.12)],fill=color)
    # center dot, exactly centered
    d.ellipse([cx-10,cy-10,cx+10,cy+10],fill=color)
def icon(path,size):
    im=Image.new("RGB",(size,size),NAVY); d=ImageDraw.Draw(im)
    # centered disc, centered loop, centered label — no offset
    d.ellipse([size//2-size*0.40,size//2-size*0.40,size//2+size*0.40,size//2+size*0.40],fill=(20,40,70))
    loop_mark(d,size//2,size//2,size*0.22,TEAL,wd=max(6,size//80))
    d.text((size//2,size*0.84),"EVOLVELOOP",font=font(size//13,True),fill=WHITE,anchor="mm"); im.save(path)
def hero():
    im=Image.new("RGB",(1600,520),NAVY); d=ImageDraw.Draw(im)
    for i in range(520): 
        pass
    d.rectangle([0,460,1600,520],fill=TEAL); loop_mark(d,140,230,85,TEAL,wd=10)
    d.text((280,150),"EVOLVELOOP",font=font(110,True),fill=WHITE)
    d.text((280,275),"The Self-Immune Agent Framework",font=font(48,True),fill=TEAL)
    d.text((280,350),"Fail. Antibody. Immune memory. Train. Evolve. Record.",font=font(32),fill=(200,210,230))
    d.text((40,478),"v0.4  •  50% upgraded  •  Scanner + Real learning + Report",font=font(26,True),fill=NAVY); im.save(f"{OUT}/hero.png")
def flow(path,title,boxes,sub):
    W,H=1600,520; im=Image.new("RGB",(W,H),LIGHT); d=ImageDraw.Draw(im); d.text((50,35),title,font=font(40,True),fill=NAVY); d.text((50,85),sub,font=font(24),fill=(80,90,110))
    n=len(boxes); bw=190; gap=(W-100-(bw*n))//(n-1) if n>1 else 0; y=200
    for i,b in enumerate(boxes):
        x=50+i*(bw+gap); d.rounded_rectangle([x,y,x+bw,330],radius=20,fill=NAVY); 
        # wrap long labels
        words=b.split(); lines=[]; cur=""
        for w_ in words:
            if len(cur)+len(w_)<12: cur=(cur+" "+w_).strip()
            else: lines.append(cur); cur=w_
        if cur: lines.append(cur)
        for j,ln in enumerate(lines): d.text((x+bw//2,255+j*26),ln,font=font(22,True),fill=WHITE,anchor="mm")
        if i<n-1: d.polygon([(x+bw+6,265),(x+bw+gap-6,248),(x+bw+gap-6,282)],fill=TEAL)
    d.rectangle([50,380,W-50,460],fill=GOLD); d.text((W//2,420),"PROMOTION GATE  •  no signature + probe + status = functional only, never formal",font=font(24,True),fill=NAVY,anchor="mm"); im.save(path)
icon(f"{OUT}/icon.png",1024); icon(f"{OUT}/favicon.png",64); hero()
flow(f"{OUT}/workflow.png","HOW THE LOOP CLOSES — v0.4",["OBSERVE","FAIL","ANTIBODY","PROMOTE","SCAN","TRAIN","EVOLVE","REPORT"],"Scanner blocks recurrences BEFORE execution. Gen 1 creates rules, gen 2+ blocks both failures, report proves it.")
flow(f"{OUT}/architecture.png","ARCHITECTURE — v0.4",["PIPELINE","ANTIBODY","IMMUNE","SCANNER","LEARNER","VERSIONER","ENGRAM","REPORT"],"Real learner + report are new in v0.4. Mock SB3 adapter remains a stub, labelled honestly.")
print("assets v3 done")
