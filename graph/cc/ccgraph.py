import matplotlib.pyplot as plt
import os
def genplt(filename):
    pwd = os.getcwd()

    logfilepath = os.path.join(pwd,filename)


    logfile=open(logfilepath,'r')

    lines=logfile.readlines()


    i=1
    while(i<len(lines)):
        print("i="+str(i))
        cca=(lines[i])[:-1]
        x=linetolist(lines[i+1])
        yupl=linetolist(lines[i+2])
        yrtt=linetolist(lines[i+3])
        


        datafile=open(cca+".dat",'w')
        scriptfile=open(cca+".plt",'w')
        datafile.write("BDP UPL RTT\n")
        for j in range(0,len(x)):
            datafile.write(x[j]+" ")
            datafile.write(yupl[j]+" ")
            datafile.write(yrtt[j]+"\n")
        datafile.close()

        CMD1="set term png\nset output '%s.png' "%cca
        CMD2='''
set key fixed right top vertical Right noreverse noenhanced autotitle nobox
set style data linespoints
set xlabel "Botten Neck Buffer BDP"
set ylabel "Delay time, ms"
        '''
        CMD3="set title '%s'"%cca
        CMD4="plot '%s.dat' using 2:xtic(1) title columnheader(2), for [i=3:3] '' using i title columnheader(i)"%cca

        scriptfile.write(CMD1+"\n")
        scriptfile.write(CMD2+"\n")
        scriptfile.write(CMD3+"\n")
        scriptfile.write(CMD4+"\n")
        scriptfile.close()

        i=i+4

def linetolist(line):
    list=line.split()
    return list


if __name__ == '__main__':
    l=['ccf1s']
    for i in l:
        genplt(i)