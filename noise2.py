import numpy as np
from exact import make,decode,encode
N=256;K=16;T=1200;BURN=300
rng=np.random.default_rng(4);step=make(N)
def valid(x): return decode(x)[1]
print("eps  wall-density(per block)  walls/sqrt(eps)  clean-check")
for eps in [0,1e-5,3e-5,1e-4,3e-4,1e-3,3e-3]:
    x=encode(rng.integers(0,2,(K,N)).astype(np.uint8));dens=[]
    for t in range(1,T+1):
        x=step(x)
        if eps>0: x=x^(rng.random(x.shape)<eps).astype(np.uint8)
        if t>=BURN and t%3==0:
            v=[valid(x)];y=x
            for _ in range(2): y=step(y);v.append(valid(y))   # noiseless lookahead just to label phase
            v=np.stack(v)                       # 3,K,N
            uniq=v.sum(0)==1;ph=np.where(uniq,v.argmax(0),-1)
            a=ph;b=np.roll(ph,-1,-1);m=(a>=0)&(b>=0)
            dens.append(((a!=b)&m).sum()/max(m.sum(),1))
    d=float(np.mean(dens));print(f"{eps:.0e} {d:.5f} {d/np.sqrt(eps) if eps>0 else 0:.2f}")
