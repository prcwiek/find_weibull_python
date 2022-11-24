#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Simple program for finding the Weibull distribution parameters
# k shape factor and c scale factor.
# The file with the example wind measurement data set comes
# from the measurement mast US Virgin Islands St. Thomas Bovoni and
# was downloaded from the site 
# https://midcdmz.nrel.gov/apps/sitehome.pl?site=USVILONA.
# 
# Roberts, O.; Andreas, A.; (1997). United States Virgin Islands:
# St. Thomas & St. Croix (Data); NREL Report No. DA-5500-64451.
# http://dx.doi.org/10.7799/1183464 
# https://midcdmz.nrel.gov/
#
# https://midcdmz.nrel.gov/

import argparse
import math
import matplotlib.pyplot as plt
from numpy import arange
import os
import pandas as pd
import sys

def k_estimator(x, kin):
    
    n = x.shape[0]
    
    res = (float((ws**3).sum()) / n) / ((float(x.sum())/n)**3)
    res = res * (math.gamma(1+1/kin)**3) - math.gamma(1+3/kin)
    
    return(res)

def bisection(x, ikmin, ikmax, eps, iter):
    
    # initial values
    kmin = ikmin
    kmax = ikmax
    fkmin = k_estimator(x, kmin)
    fkmax = k_estimator(x, kmax)
    
    if (fkmin * fkmax > 0):
        print("Error: Both estimated k values are greater than zero!")
        k = 0
        sys.exit()
    
    for i in range(1, iter):
        k = (kmin + kmax) / 2
        fk = k_estimator(x, k)
        fkk = (fkmax - fkmin) / (kmax - kmin)

        if abs(fk/fkk) - eps > 0:
            if (fk*fkmin < 0):
                kmax = k
                fkmax = fk
            else:
                if fk * fkmin == 0: 
                    return(k)
                kmin = k
                fkmin = fk
        else:
            return(k)

    k = 0
    return(k)

# function weibull return a probability for given parameters:
# c scale factor
# k shape factor
# ws wind speed
def weibull(c, k, ws):
    return((k/c)*((ws/c)**(k-1)) * math.exp(-(ws/c)**k))

# get command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('input_file', help="text or csv file with wind speed data",
                    nargs='?', default='WS125.txt')
parser.add_argument('-p', help="if True, plots will be generated and saved",
                    action='count', default=0)

args = parser.parse_args()

# input file name
if os.path.isfile(args.input_file):
    input_file = args.input_file
    print("Using file: " + input_file)
else:
    if os.path.isfile("WS125.txt"):
        print("Using default file: WS125.txt")
        input_file = "WS125.txt"
    elif os.path.isfile("data_example/WS125.txt"):
        print("Using default file: data_example/WS125.txt")
        input_file = "data_example/WS125.txt"
    else:
        print("Default file not found! Please enter path of file with data!")
        sys.exit()
print()

# check if -p parameter exists
if args.p > 0:
    make_plot = True
else:
    make_plot = False

# check if a default file exist 
if not os.path.isfile(input_file):
    if not os.path.isfile("/data_example/" + input_file):
        sys.exit()
    
# read a file    
ws = pd.read_csv(input_file)

# range for searching k and c
kmin = 1.0
kmax = 8.0

#accuracy
eps = 0.000001

# number of iterations
niter = 50

# mean wind speed
ws_mean = float(ws.iloc[:,0].mean())

# median wind speed
ws_median = float(ws.iloc[:,].median())

# shape factor
k = bisection(ws, kmin, kmax, eps, niter)

# scale factor
c = ws_mean * (0.586 + 0.433/k)**(-1/k)

print("Found Weibull distribution parameters:")
print()
print(f"shape factor k: {k:.2f}")
print(f"scale factor c: {c:.2f}")
print()
print(f"Mean wind speed: {ws_mean:.2f} m/s")
print(f"Median wind speed: {ws_median:.2f} m/s")

# generate and save plot
if make_plot:
    ddist = pd.DataFrame(data=arange(0,25,0.1), columns=['wind_speed'])
    ddist['probability'] = ddist['wind_speed'].apply(lambda x: weibull(c, k, x))
    fig, ax = plt.subplots()
    
    ax.hist(ws.iloc[0:], bins=30, density=True, rwidth=1, align='left',
            color='#FFA500', edgecolor='grey')
    
    ax.plot(ddist.wind_speed, ddist.probability, color='#A52A2A',
            label='Weibull distribution\nc={:.2f}\nk={:.2f}'.format(c,k) )
    
    ax.set_title("Probability histogram and Weibull distribution")
    ax.set_xlabel("Wind speed (m/s)")
    ax.set_ylabel("Probability (%)")
    ax.legend()
    
    plt.xlim(0, 25)
    plt.xticks(range(0,25,5))
    plt.savefig("distribution.png", dpi=200)
    plt.close(fig)
    print()
    print("File distribution.png saved!")
    
