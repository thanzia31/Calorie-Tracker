
import matplotlib.pyplot as plt
from io import StringIO
import numpy as np
import warnings
warnings.filterwarnings("ignore")
def graphfun(cal,cal_needed):
    
    ys = cal
    
    xs=np.arange(1,len(cal)+1)
    fig=plt.figure()

    plt.plot(10,cal_needed,marker='o',markerfacecolor='red',c='red',markersize=10)   
    plt.xlim(0,10.15)
    plt.axhline(y = cal_needed,xmin=0,xmax=9)
    plt.annotate('Target Calorie',(10,cal_needed),xytext=(10,1650),
                 ha='center')
    plt.xlabel('DAYS')
    plt.ylabel('CALORIES')
    plt.xticks([1,2,3,4,5,6,7,8,9,10])
    for pos in ['top','right']:
        plt.gca().spines[pos].set_visible(False)
    #plt.plot(xs,ys,'bo-',linewidth=2,color='cyan')
    plt.bar(xs, ys, color ='maroon',
        width = 0.8)
    #plt.show()
    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)

    data = imgdata.getvalue()
    return data

def single_point(cal,cal_needed):
    fig=plt.figure()
    y=[cal,cal_needed]
    x=[1,2]
    if cal == 0:
        return 'No Data Added For This Day'
    else:
        plt.plot(x,y,marker='o')
        #plt.vlines(x, 0, y, linestyle="dashed")
        plt.hlines(y, 0, x, linestyle="dashed",color='black')
        plt.ylim(100,2000)
        plt.xlim(0,3)
        plt.xticks([0,1,2,3])
        imgdata = StringIO()
        fig.savefig(imgdata, format='svg')
        imgdata.seek(0)

        data = imgdata.getvalue()
        return data