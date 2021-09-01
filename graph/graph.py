import matplotlib.pyplot as plt
import os
def drawpic(filename):
    pwd = os.getcwd()
    filepath = os.path.join(pwd,filename)
    file=open(filepath,'r')
    lines=file.readlines()
    descriptiontext=lines[0]
    cca1text=lines[1]
    x1=linetolist(lines[2])
    y11_upl_list=linetolist(lines[3])
    y12_rtt_list=linetolist(lines[4])
    cca2text=lines[5]
    x2=linetolist(lines[6])
    y21_upl_list=linetolist(lines[7])
    y22_rtt_list=linetolist(lines[8])
    plt.plot(x1,y11_upl_list,'s-',color='r',label=cca1text+"UPL delay")
    plt.plot(x1,y12_rtt_list,'o-',color='r',label=cca1text+"RTT delay")
    plt.plot(x2,y21_upl_list,'s-',color='g',label=cca2text+"UPL delay")
    plt.plot(x2,y22_rtt_list,'o-',color='g',label=cca2text+"RTT delay")
    plt.savefig(os.path.join(pwd,filename))
    plt.show()


def linetolist(line):
    list=line.split()
    return list


if __name__ == '__main__':
    l=['f1','f2','f3','f4']
    for i in l:
        drawpic(i)