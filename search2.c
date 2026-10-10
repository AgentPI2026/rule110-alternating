// Search: spatial period-3 assignment of three symmetric ECA rules; coarse-grain (cell 3k+off, every tau steps); score vs rule 110 / 124.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define L 96
static uint64_t s[2]={0x123456789abcdefULL,0xfedcba987654321ULL};
static uint64_t rnd(){uint64_t a=s[0],b=s[1];s[0]=b;a^=a<<23;s[1]=a^b^(a>>17)^(b>>26);return s[1]+b;}
static int sym[64],nsym=0;
int main(int argc,char**argv){
  int INITS=argc>1?atoi(argv[1]):3;
  for(int r=0;r<256;r++){int ok=1;for(int a=0;a<8;a++){int l=(a>>2)&1,c=(a>>1)&1,rr=a&1;int b=(rr<<2)|(c<<1)|l;if(((r>>a)&1)!=((r>>b)&1))ok=0;}if(ok)sym[nsym++]=r;}
  fprintf(stderr,"%d symmetric rules\n",nsym);
  static unsigned char init[8][L];for(int k=0;k<INITS;k++)for(int i=0;i<L;i++)init[k][i]=rnd()&1;
  int T=240,BURN=60;
  for(int a=0;a<nsym;a++)for(int b=a;b<nsym;b++)for(int c=b;c<nsym;c++){
    int perms[6][3]={{0,1,2},{0,2,1},{1,0,2},{1,2,0},{2,0,1},{2,1,0}};int R3[3]={sym[a],sym[b],sym[c]};
    for(int p=0;p<6;p++){ if((a==b&&p>0&&0))continue;
      int rr[3]={R3[perms[p][0]],R3[perms[p][1]],R3[perms[p][2]]};
      // simulate
      static unsigned char hist[8][241][L];
      for(int k=0;k<INITS;k++){unsigned char cur[L],nx[L];memcpy(cur,init[k],L);memcpy(hist[k][0],cur,L);
        for(int t=1;t<=T;t++){for(int i=0;i<L;i++){int n=(cur[(i+L-1)%L]<<2)|(cur[i]<<1)|cur[(i+1)%L];nx[i]=(rr[i%3]>>n)&1;}memcpy(cur,nx,L);memcpy(hist[k][t],cur,L);}}
      for(int tau=1;tau<=4;tau++)for(int off=0;off<3;off++){
        for(int tgt=0;tgt<2;tgt++){int R=tgt?124:110;long m=0,tot=0,chg=0,act=0;
          for(int k=0;k<INITS;k++)for(int t=BURN;t+tau<=T;t+=tau)for(int j=0;j<L/3;j++){
            int i0=3*((j+L/3-1)%(L/3))+off,i1=3*j+off,i2=3*((j+1)%(L/3))+off;
            int n=(hist[k][t][i0]<<2)|(hist[k][t][i1]<<1)|hist[k][t][i2];
            if(n!=0&&n!=7){m+=((R>>n)&1)==hist[k][t+tau][i1];act++;} chg+=hist[k][t+tau][i1]!=hist[k][t][i1];tot++;}
          double f=act?(double)m/act:0;if(f>0.97&&chg>0.2*tot&&act>0.3*tot)printf("%d %d %d perm%d tau%d off%d R%d %.4f\n",rr[0],rr[1],rr[2],p,tau,off,R,f);}}
    }}
}
