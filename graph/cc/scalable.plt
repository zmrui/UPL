set term png
set output 'scalable.png' 

set key fixed right top vertical Right noreverse noenhanced autotitle nobox
set style data linespoints
set xlabel "Botten Neck Buffer BDP"
set ylabel "Delay time, ms"
        
set title 'scalable'
plot 'scalable.dat' using 2:xtic(1) title columnheader(2), for [i=3:3] '' using i title columnheader(i)
