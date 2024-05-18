INP r1
INP r2
.loop
ADD r0 r1
SUB r2 1
BGT r2 0 loop
OUT r0
END
