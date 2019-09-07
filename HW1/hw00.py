"""
Justin Lad
CSCI 720: BDA
HW00
1/23/2018
"""

import math
import numpy as np
import matplotlib.pyplot as plt

"""
Basic function to calculate time to travel 20 miles

@param speed: positive valued speed in MPH

@return time: amount of time in minutes to travel 20 miles
"""
def get_time(speed):
    #time is distance / speed, leaving unit of hour. Then multiply by 60 to get minutes
    return 60 * 20 / speed


"""
Produces speed vs time graph (Part A)
"""
def graph_mph():
    x = np.arange(1,81,1)
    y = np.zeros(len(x))
    #can i do this as a lambda?
    for i in range(len(x)):
        y[i] = get_time(x[i])
    plt.scatter(x,y)
    plt.xlabel('Speed (MPH)')
    plt.ylabel('Time to Travel 20 miles (minutes)')
    plt.title('Relationship Between Travel Time and Speed')
    plt.show()
    plt.close()


"""
Produces speed vs saved time graph (Part B)
"""
def saved_time():
    x = np.arange(5,85,5)
    y = np.zeros(len(x))
    for i in range(len(x)):
        if i < len(x) - 1:
            print(x[i])
            cur = get_time(x[i])
            y[i] = cur - get_time(x[i+1])

    #need to ignore last data point, as it was only used to calculate diff in speed from 80 and 75 mph
    plt.scatter(x[:-1],y[:-1])
    plt.xlabel('Actual Driving Speed (MPH)')
    plt.ylabel('Time Saved (minutes)')
    plt.title('Time Saved if Traveling 5MPH Faster Than Current Speed')
    plt.show()
    plt.close()


"""
Produces teeth on back cog vs gear ratio graph (Part C)
"""
def gear_ratios():
    front = [73,51,31]
    back = [19,23,33,41,53,63,71]

    data = [[]]
    data = np.zeros([len(front),len(back)])
    labels = ['Gear A','Gear B', 'Gear C']
    for f in range(len(front)):
        for b in range(len(back)):
            data[f][b] = front[f] / back[b]

    for i in range(len(front)):
        plt.scatter(back, data[i], label=labels[i])
        plt.plot(back,data[i])

    plt.legend()
    plt.xlabel('Number of Teeth on Back Cog')
    plt.ylabel('Gear Ratio')
    plt.title('Relationship Between Gear Ratio and Teeth on Back Cog')
    plt.show()
    plt.close()


def main():
    graph_mph()
    saved_time()
    gear_ratios()


if __name__ == '__main__':
    main()
