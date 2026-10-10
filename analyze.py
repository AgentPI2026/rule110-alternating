import numpy as np,collections,sys
def tab(r):return np.array([(r>>i)&1 for i in range(8)],np.uint8)
def mirror(r): # swap left/right
    o=0
    for a in range(8):
        l,c,rr=(a>>2)&1,(a>>1)&1,a&1;b=(rr<<2)|(c<<1)|l
        o|=((r>>a)&1)<<b
    return o
def comp(r): # conjugate by complement
    o=0
    for a in range(8):
        b=7-a;o|=(1-((r>>b)&1))<<a
    return o
def canon(r):return min(r,mirror(r),comp(r),mirror(comp(r)))
rep={}
for line in open('all.txt'):
    e,a,b,c,c0,c1,t=map(int,line.split())
    k=(e,t)
    if k not in rep or (a,b,c,c0,c1)<rep[k][:5]: rep[k]=(a,b,c,c0,c1)
print("distinct (eca,tau):",len(rep))
rng=np.random.default_rng(1)
def verify(e,t,a,b,c,c0,c1,NB=11,K=200):
    L=3*NB;R=np.stack([tab(a),tab(b),tab(c)]);ri=np.arange(L)%3
    bits=rng.integers(0,2,(K,NB)).astype(np.uint8)
    code={0:[(c0>>2)&1,(c0>>1)&1,c0&1],1:[(c1>>2)&1,(c1>>1)&1,c1&1]}
    x=np.array([[code[v][k] for v in row for k in range(3)] for row in bits],np.uint8)
    for _ in range(t):
        n=(np.roll(x,1,1)<<2)|(x<<1)|np.roll(x,-1,1);x=R[ri[None,:],n]
    blk=x.reshape(K,NB,3);w0=(blk==np.array(code[0])).all(-1);w1=(blk==np.array(code[1])).all(-1)
    if not (w0|w1).all():return False
    dec=w1.astype(np.uint8);nb=(np.roll(bits,1,1)<<2)|(bits<<1)|np.roll(bits,-1,1)
    return bool((tab(e)[nb]==dec).all())
good={}
for (e,t),cfg in sorted(rep.items()):
    # try every config for this (e,t) until one verifies on the larger ring
    pass
# verification over ALL configs for (e,t) is heavy; sample up to 50 configs per key
by=collections.defaultdict(list)
for line in open('all.txt'):
    e,a,b,c,c0,c1,t=map(int,line.split());L=by[(e,t)]
    if len(L)<400: L.append((a,b,c,c0,c1))
ver={}
for (e,t),L in sorted(by.items()):
    ok=[x for x in L if verify(e,t,*x)]
    ver[(e,t)]=(len(ok),len(L),ok[:1])
emu=collections.defaultdict(list)
for (e,t),(n,m,ex) in ver.items():
    if n>0: emu[e].append((t,ex[0]))
print("ECAs emulated (verified on 11-block ring):",len(emu))
chiral=[e for e in emu if e!=mirror(e)]
classes=collections.defaultdict(list)
for e in emu:classes[canon(e)].append(e)
print("equivalence classes emulated:",len(classes),"of 88")
allc=sorted({canon(r) for r in range(256)})
print("classes NOT emulated:",[c for c in allc if c not in classes])
print("chiral classes emulated:",sorted(c for c in classes if c!=mirror(c) or any(x!=mirror(x) for x in classes[c])))
import json;json.dump({str(e):[(t,list(x)) for t,x in v] for e,v in emu.items()},open('emulated.json','w'))
for e in (110,124,30,106,54,45,41):print(e,"->",sorted(set(t for t,_ in emu.get(e,[]))) or "no")
