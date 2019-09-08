import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

"""
implements cost function on various thresholds of data

@param the_data: 2-D np array of data [value,label]

@return best_threshold: the best threshold based on the cost function
@return threshold_list: list of thresholds used (for graphing later)
@return cost_list: list of costs associated with each threshold (for graphing later)
"""
def classifier(the_data):
    min_val = np.amin(the_data[:,0])
    max_val = np.amax(the_data[:,0])
    best_cost = math.inf
    best_threshold = -1
    threshold_list = np.arange(min_val,max_val,0.5)
    cost_list = []
    fp_rate = []
    tp_rate = []
    for threshold in threshold_list:
        FP = 0
        FN = 0
        TN = 0
        TP = 0
        for index in range(len(the_data)):
            if the_data[index,0] <= threshold:
                if the_data[index,1] == 0:
                    TN += 1
                else:
                    FN += 1
            else:
                if the_data[index,1] == 1:
                    TP += 1
                else:
                    FP += 1

        cost = FN + 2*FP 
        #cost = 2*FN + FP
        
        cost_list.append(cost)
        fp_rate.append((FP)/(FP+TN))
        tp_rate.append((TP)/(TP+FN))

        if cost <= best_cost:
            best_threshold = threshold
            best_cost = cost
            best_fp = FP
            best_fn = FN
            
    #print(f'best fp: {best_fp} and best fn: {best_fn}')        
    return best_threshold, threshold_list, cost_list,fp_rate,tp_rate

"""
Rounds data to nearest 0.5 MPH

@param data: np array of data to round
"""
def bin_data(data):
    new_data = np.copy(data)
    for index in range(len(data)):
        cur = new_data[index,0]
        if cur % 1 > 0.5:
            if (cur % 1) - .75 > 0:
                cur = math.ceil(cur)
            else:
                cur = math.floor(cur) + 0.5
        else:
            if (cur % 1) - .25 > 0:
                cur = math.floor(cur) + 0.5
            else:
                cur = math.floor(cur)
        new_data[index,0] = cur
        
    return new_data


"""
Graphs the cost vs threshold plot
@param thresholds: list of thresholds used for classifying data
@param costs: the cost associated with each threshold
"""
def graph_cost_threshold(thresholds, costs):
    plt.plot(thresholds,costs)
    plt.xlabel('Speed Threshold (MPH)')
    plt.ylabel('Cost (# of Incorrectly Predicted Cars)')
    plt.title('Cost Vs Speed Threshold')
    plt.show()
    
"""
graphs the roc curve

@param x: False Alarm rate 
@param y: True Positive rate
"""
def graph_ROC(x,y):
    #x-axis is False Alarm, aka FP Rate.
    #y-axis is TP 
    plt.plot(x,y)
    plt.xlabel('False Positive Rate (False Alarm Rate)')
    plt.ylabel('True Positive Rate (Correct Hit Rate)')
    plt.title('ROC Curve By Threshold')
    plt.show()


"""
Sorts np array of data while preserving associated columns of data

@param data: 2-D np array of data [value,label]
"""
def sort_data(data):
    sorted_indices = np.lexsort((data[:,0],data[:,1]))
    s = np.empty((len(sorted_indices),2))
    for i in range(len(sorted_indices)):
        s[i,0] = data[sorted_indices[i],0]
        s[i,1] = data[sorted_indices[i],1]
    return s

def main():
    data_np = np.array(pd.read_csv('actual_data.csv'))
    binned_data = bin_data(data_np)
    sorted_data = sort_data(binned_data)
    
    #print(classifier(sorted_data)[0])
    best_thresh, thresh_list, cost_list,fp_rate,tp_rate = classifier(sorted_data)
    
    graph_cost_threshold(thresh_list,cost_list)
    graph_ROC(fp_rate,tp_rate)

if __name__ == '__main__':
    main()