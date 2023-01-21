from statistics import stdev, variance, median, mean
import math, os
def graph_plot(f,y,y50_,y3, x, x50):    
    try:
        f.write("被害量の標準偏差:"+str(stdev(y))+"\n")#被害量を表すyの分散を表示
        f.write("被害量の分散:"+str(variance(y))+"\n")#分散
        f.write("被害量の平均:"+str(mean(y))+"\n")
        #母分散既知の95%信頼区間を求める
        y_bottom = mean(y)-1.96*math.sqrt((variance(y)/len(y)))
        y_up = mean(y) + 1.96*math.sqrt((variance(y)/len(y)))
        li = [y_bottom, y_up]
        f.write("95%信頼区間は:"+str(li)+"でした。\n")
        #print(y)

        plt.plot(x,y) 
        
        root1 = "".join([os.getcwd(),"\py_graph","\折れ線グラフ"])
        pict_name = root1
        plt.savefig(pict_name)#戦闘の被害を折れ線グラフで表示し、それを保存する！横軸が戦闘回数で縦軸が被害量
        plt.clf()
        root2 = "".join([os.getcwd(),"\py_graph","\棒グラフ"])
        if y50_ !=[]:
            pict_name = root2
            plt.bar(x50,y50_)
            plt.savefig(pict_name)#戦闘の被害を棒グラフで表示し、それを保存する。
        #plt.show()
        plt.clf()
        """以下では上と同じことをファイルに書き込むのではなくprintする。"""
        #print("被害量の標準偏差:"+str(stdev(y))+"\n")#被害量を表すyの分散を表示
        #print("被害量の分散:"+str(variance(y))+"\n")#分散
        print("被害量の平均:"+str(mean(y)))
        #母分散既知の95%信頼区間を求める
        print("95%信頼区間は:"+str(li)+"でした。\n")
    except:
        f.write("戦闘回数1回の場合被害の統計は計算できません。")
        print("被害量は"+str(y)+"でした")

def statistics_for_monte(f, y):
    """上記の関数からグラフを削除したもの。ver0.95ではこちらを使用する"""
    try:
        f.write("被害量の標準偏差:"+str(stdev(y))+"\n")#被害量を表すyの分散を表示
        f.write("被害量の分散:"+str(variance(y))+"\n")#分散
        f.write("被害量の平均:"+str(mean(y))+"\n")
        #母分散既知の95%信頼区間を求める
        y_bottom = mean(y)-1.96*math.sqrt((variance(y)/len(y)))
        y_up = mean(y) + 1.96*math.sqrt((variance(y)/len(y)))
        li = [y_bottom, y_up]
        f.write("95%信頼区間は:"+str(li)+"でした。\n")
        
        """以下では上と同じことをファイルに書き込むのではなくprintする。"""
        #print("被害量の標準偏差:"+str(stdev(y)))#被害量を表すyの分散を表示
        #print("被害量の分散:"+str(variance(y)))#分散
        print("被害量の平均:"+str(mean(y)))
        print("95%信頼区間は:"+str(li)+"でした。\n")
    except:
        f.write("戦闘回数1回の場合被害の統計は計算できません。")
        print("被害量は"+str(y)+"でした")