import numpy as np
tab=lambda r:np.array([(r>>i)&1 for i in range(8)],np.uint8)
def make(N,rules=(36,37,5)):
    tabs=np.stack([tab(r) for r in rules]);ri=np.arange(3*N)%3
    def step(x):
        n=(np.roll(x,1,-1)<<2)|(x<<1)|np.roll(x,-1,-1);return tabs[ri,n]
    return step
def encode(b):  # logical 0 -> [1,0,0], 1 -> [0,0,0]
    blk=np.where(b[...,None]==0,np.array([1,0,0]),np.array([0,0,0])).astype(np.uint8);return blk.reshape(*b.shape[:-1],-1)
def decode(x):
    blk=x.reshape(*x.shape[:-1],-1,3)
    ok0=(blk==[1,0,0]).all(-1);ok1=(blk==[0,0,0]).all(-1)
    return np.where(ok0,0,np.where(ok1,1,2)),ok0|ok1   # 2 = invalid
def r110(b):
    n=(np.roll(b,1,-1)<<2)|(b<<1)|np.roll(b,-1,-1);return tab(110)[n]
if __name__=="__main__":
    N=64;rng=np.random.default_rng(0);step=make(N)
    for trial in range(3):
        b=rng.integers(0,2,N).astype(np.uint8);x=encode(b);good=True
        for k in range(40):
            for _ in range(3):x=step(x)
            b=r110(b)
            d,ok=decode(x)
            if not ok.all() or not (d==b).all():good=False;print("trial",trial,"mismatch at macro step",k,"valid frac",ok.mean());break
        print("trial",trial,"exact for 40 macro steps:",good)
