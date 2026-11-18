import wave,struct,math,sys
w=wave.open(sys.argv[1]);sr=w.getframerate();ch=w.getnchannels()
raw=struct.unpack('<%dh'%(w.getnframes()*ch),w.readframes(w.getnframes()))
d=[sum(raw[i:i+ch])/ch for i in range(0,len(raw),ch)][::4]; sr//=4  # downsample (rough, notes < 5kHz fine)
N=8192;pc=[0.0]*12
def good(freq,seg):
    k=2*math.pi*freq/sr;c=2*math.cos(k);a=b=0
    for x in seg: a,b=x+c*a-b,a
    return a*a+b*b-c*a*b
for s in range(0,len(d)-N,N*3):
    seg=[d[s+i]*(0.5-0.5*math.cos(2*math.pi*i/N)) for i in range(N)]
    for midi in range(48,84):
        pc[midi%12]+=good(440*2**((midi-69)/12),seg)
t=sum(pc);names='C C# D D# E F F# G G# A A# B'.split()
print(' '.join(f'{n}:{p/t*100:.0f}' for n,p in zip(names,pc)))
print('in-key %',round(sum(pc[i] for i in [0,2,4,5,7,9,11])/t*100,1))
