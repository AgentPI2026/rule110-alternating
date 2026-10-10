// Exhaustive: ordered triple of symmetric ECA rules (cell i uses r[i%3]), block code words c0,c1 (3-bit), ring of NB blocks.
// For tau in 1..6, test whether tau steps map encoded states to encoded states via a well-defined ECA f on block neighbourhoods.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define NB 5
#define NC (3*NB)
static int sym[64],ns=0;
int main(int argc,char**argv){
  int part=atoi(argv[1]),nparts=atoi(argv[2]);
  for(int r=0;r<256;r++){int ok=1;for(int a=0;a<8;a++){int l=(a>>2)&1,c=(a>>1)&1,rr=a&1;int b=(rr<<2)|(c<<1)|l;if(((r>>a)&1)!=((r>>b)&1))ok=0;}if(ok)sym[ns++]=r;}
  long found=0;
  for(int ia=part;ia<ns;ia+=nparts)for(int ib=0;ib<ns;ib++)for(int ic=0;ic<ns;ic++){
    int R[3]={sym[ia],sym[ib],sym[ic]};
    for(int c0=0;c0<8;c0++)for(int c1=0;c1<8;c1++){ if(c0==c1)continue;
      int alive=0x3F;int tab[7][8];for(int t=0;t<7;t++)for(int k=0;k<8;k++)tab[t][k]=-1;
      for(int cfg=0;cfg<(1<<NB)&&alive;cfg++){
        unsigned char x[NC],y[NC];
        for(int j=0;j<NB;j++){int c=((cfg>>j)&1)?c1:c0;for(int k=0;k<3;k++)x[3*j+k]=(c>>(2-k))&1;}
        for(int t=1;t<=6;t++){
          for(int i=0;i<NC;i++){int n=(x[(i+NC-1)%NC]<<2)|(x[i]<<1)|x[(i+1)%NC];y[i]=(R[i%3]>>n)&1;}
          memcpy(x,y,NC);
          if(!((alive>>(t-1))&1))continue;
          int dec[NB],ok=1;
          for(int j=0;j<NB&&ok;j++){int c=(x[3*j]<<2)|(x[3*j+1]<<1)|x[3*j+2];if(c==c0)dec[j]=0;else if(c==c1)dec[j]=1;else ok=0;}
          if(ok){for(int j=0;j<NB&&ok;j++){int nb=(((cfg>>((j+NB-1)%NB))&1)<<2)|(((cfg>>j)&1)<<1)|((cfg>>((j+1)%NB))&1);
              if(tab[t][nb]==-1)tab[t][nb]=dec[j];else if(tab[t][nb]!=dec[j])ok=0;}}
          if(!ok)alive&=~(1<<(t-1));
        }}
      for(int t=1;t<=6;t++)if((alive>>(t-1))&1){int eca=0,full=1;for(int k=0;k<8;k++){if(tab[t][k]<0)full=0;else eca|=tab[t][k]<<k;}
        if(full){printf("%d %d %d %d %d %d %d\n",eca,R[0],R[1],R[2],c0,c1,t);found++;}}
    }}
  fprintf(stderr,"part %d: %ld\n",part,found);
}
