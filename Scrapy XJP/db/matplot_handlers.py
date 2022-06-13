import matplotlib.pyplot as plt
import numpy as np
from decimal import Decimal
import math

def plot_draw(x,y,name,title):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    x_axis = np.arange(1,len(x)+1)

    ax.set_xlim(1,len(x)+0.5)
    ax.set_ylim(190000,2100000)

    ax.set_xticks(np.linspace(1.1,len(x)+0.1,len(x)))
    # ax.set_yticks(np.linspace(min(y),max(y),10))
    ax.set_yticks(np.linspace(200000, 2000000, 10))

    ax.set_xticklabels(x,rotation='10')
    ax.set_yticklabels(['20W','40W','60W','80W','100W','120W','140W','160W','180W','200W'])

    ax.plot(x_axis, y, 'r-.x', label=name)
    common_decoration(ax,title)
    plt.show()

def bar_draw(x,y,name,title):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    x_axis = np.arange(1,len(x)*2+1,2)

    ax.set_xlim(0.1,len(x)*2+0.5)
    yMin,yMax = round(min(y)/10000)*9000,round(max(y)/10000)*11000
    ax.set_ylim(yMin, yMax)

    ax.set_xticks(np.linspace(1,len(x)*1.9,len(x)))
    ax.set_yticks(np.linspace(yMin, yMax, 10))
    ax.set_xticklabels(x,rotation='10')
    # ax.set_yticklabels(['20W','40W','60W','80W','100W','120W','140W','160W','180W','200W'])

    common_decoration(ax, title)
    ax.bar(x_axis,y,color=["mistyrose","lightcoral","indianred","firebrick","brown","darkred","maroon",'lightcoral'],bottom=0,
           edgecolor='gold',label=name,linewidth=2,width=1.5,alpha=1)
    ax.legend(loc=1, shadow=True, labelspacing=2, handlelength=3, fontsize=12)

    plt.show()

# decorate spine, title, tick_params
def common_decoration(ax,title):
    ax.tick_params(direction='inout',length=6,color='r')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_linewidth(3)

    ax.set_title(title,fontsize=14,backgroundcolor='y',fontweight='bold',color='black',verticalalignment='center')


def main():
    x = ['toronto', 'ottawa', 'hamilton', 'vancouver', 'calgary', 'edmonton', 'halifax', 'st-johns']
    y = [Decimal('1866033.296703'), Decimal('856633.709302'), Decimal('1066032.736264'), Decimal('1988586.862069'), Decimal('824496.467391'), Decimal('551388.293478'), Decimal('628141.561798'), Decimal('367381.927711')]
    name = 'AVERAGE PRICE'
    title = 'Each citys average housing price'
    # bar_draw(x, y,name,title)

if __name__ == '__main__':
    main()