import numpy as np,sys,time
from exact import make,decode,r110,encode
def run(N,K,Tmax,seed,mode):
    rng=np.random.default_rng(seed);step=make(N)
    x=rng.integers(0,2,(K,3*N)).astype(np.uint8) if mode=="raw" else encode(rng.integers(0,2,(K,N)).astype(np.uint8))
    locked=np.full(K,-1);prev=None
    for t in range(1,Tmax+1):
        x=step(x)
        if t%3==0 or True:
            d,ok=decode(x);full=ok.all(-1)
            if full.any():
                # check consistency over 3 steps for fully-valid runs
                y=x.copy()
                for _ in range(3):y=step(y)
                d2,ok2=decode(y);cons=ok2.all(-1)&(d2==r110(np.where(d==2,0,d))).all(-1)
                newly=full&cons&(locked<0);locked[newly]=t
        if (locked>=0).all():break
    return locked
if __name__=="__main__":
    N=int(sys.argv[1]);K=int(sys.argv[2]);Tmax=int(sys.argv[3]);mode=sys.argv[4]
    t0=time.time();L=run(N,K,Tmax,1,mode);ok=L>=0
    print(f"N={N} blocks ({3*N} cells) mode={mode} K={K} Tmax={Tmax}: locked {ok.sum()}/{K}, median lock time {np.median(L[ok]) if ok.any() else None}, {time.time()-t0:.0f}s")
