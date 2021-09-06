import matplotlib.pyplot as plt
import os
def genplt(filename):
    pwd = os.getcwd()

    datafilename=filename+".dat"
    scriptfilename=filename+".plt"

    logfilepath = os.path.join(pwd,filename)
    datafilepath = os.path.join(pwd,datafilename)
    scriptfilepath = os.path.join(pwd,scriptfilename)

    logfile=open(logfilepath,'r')
    datafile=open(datafilepath,'w')
    scriptfile=open(scriptfilepath,'w')

    lines=logfile.readlines()
    descriptiontext=lines[0]
    cca1text=lines[1]
    x1=linetolist(lines[2])
    y11_upl_list=linetolist(lines[3])
    y12_rtt_list=linetolist(lines[4])
    cca2text=lines[5]
    x2=linetolist(lines[6])
    y21_upl_list=linetolist(lines[7])
    y22_rtt_list=linetolist(lines[8])

    datafile.write("BDP UPLwithBBR RTTwithBBR UPLwithCUBIC RTTwithCUBIC\n")

    for i in range(0,len(x1)):
        datafile.write(x1[i]+" ")
        datafile.write(y11_upl_list[i]+" ")
        datafile.write(y12_rtt_list[i]+" ")
        datafile.write(y21_upl_list[i]+" ")
        datafile.write(y22_rtt_list[i]+"\n")
    datafile.close()

    CMD1="#set output '%s.png' "%filename
    CMD2='''
set key fixed right top vertical Right noreverse noenhanced autotitle nobox
set style data linespoints
set xlabel "Botten Neck Buffer BDP"
set ylabel "Delay time, ms"
    '''
    CMD3="set title '%s'"%descriptiontext[:-1]
    CMD4="plot '%s.dat' using 2:xtic(1) title columnheader(2), for [i=3:5] '' using i title columnheader(i)"%filename

    scriptfile.write(CMD1+"\n")
    scriptfile.write(CMD2+"\n")
    scriptfile.write(CMD3+"\n")
    scriptfile.write(CMD4+"\n")
    scriptfile.close()



def linetolist(line):
    list=line.split()
    return list


if __name__ == '__main__':
    l=['f5s2','f5s']
    for i in l:
        genplt(i)