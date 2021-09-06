set term png
set output 'f11c.png' 

set key fixed right top vertical Right noreverse noenhanced autotitle nobox
set style data linespoints
set xlabel "Botten Neck Buffer BDP"
set ylabel "Delay time, ms"
    
set title 'c2s=1 bytes, s2c=1000000 bytes, d1=1ms, d2=50ms, bw1=100Mbps, bw2=10Mbps'
plot 'f11c.dat' using 2:xtic(1) title columnheader(2), for [i=3:5] '' using i title columnheader(i)
