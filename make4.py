from midiutil import MIDIFile
import sys
S=[0,2,4,5,7,9,11]
scale=[n for n in range(36,100) if n%12 in S]
def step(n,k): return scale[scale.index(n)+k]
m=MIDIFile(3);m.addTempo(0,0,92)
m.addProgramChange(1,1,0,40)   # strings pad
m.addProgramChange(2,2,0,32)   # acoustic bass
m.addProgramChange(0,0,0,11)   # vibraphone lead
A=[(57,60,64),(53,57,60),(48,52,55),(55,59,62)]
B=[(53,57,60),(55,59,62),(57,60,64),(52,55,59)]
bass={'A':[45,41,36,43],'B':[41,43,45,40]}
# melodies: 4 bars each, (offset, scale-step from root, length)
mA=[[(0,0,1),(1,1,.5),(1.5,2,.5),(2,1,1),(3,0,1)],
    [(0,0,1.5),(1.5,-1,.5),(2,0,1),(3,2,1)],
    [(0,2,1),(1,1,1),(2,0,1),(3,1,1)],
    [(0,1,2),(2,0,.5),(2.5,-1,.5),(3,0,1)]]
mB=[[(0,0,.5),(.5,2,.5),(1,4,1),(2,3,1),(3,2,1)],
    [(0,4,1.5),(1.5,3,.5),(2,2,1),(3,1,1)],
    [(0,2,.5),(.5,3,.5),(1,4,1),(2,5,1),(3,4,1)],
    [(0,3,2),(2,2,1),(3,1,1)]]
rootsA=[72,69,67,71]; rootsB=[72,74,76,71]
t=0;used=set()
for s in 'AABA':
    ch=A if s=='A' else B; mel=mA if s=='A' else mB; roots=rootsA if s=='A' else rootsB
    for b in range(4):
        for n in ch[b]: m.addNote(1,1,n,t+b*4,4,45);used.add(n%12)
        bn=bass[s][b]
        m.addNote(2,2,bn,t+b*4,1.5,80);m.addNote(2,2,bn+7 if bn+7 in scale else bn,t+b*4+2,1.5,70)
        for off,k,ln in mel[b]:
            n=step(roots[b],k);used.add(n%12)
            m.addNote(0,0,n,t+b*4+off,ln*0.95,85 if off==0 else 75)
    t+=16
for n in [57,60,64,69]: m.addNote(0,0,n,t,4,80)
m.addNote(2,2,45,t,4,80)
print("out of key:",[u for u in used if u not in S])
m.writeFile(open('l4.mid','wb'))
