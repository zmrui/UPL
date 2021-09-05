#set output 'f3c.png' 

set key fixed right top vertical Right noreverse noenhanced autotitle nobox
set style data linespoints
set xlabel "Botten Neck Buffer BDP"
set ylabel "Delay time, ms"
    
set title 'c2s=1 bytes, s2c=1000 bytes, d1=1ms, d2=100ms, bw1=200Mbps, bw2=100Mbps, bf1 = 1 * BDP'
plot 'f3c.dat' using 2:xtic(1) title columnheader(2), for [i=3:5] '' using i title columnheader(i)