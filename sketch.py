#Playground for testing things

import csv
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal
from scipy import optimize
from scipy import stats
import pwlf
import warnings

file_id = 4
file_group = 'm'

if (file_group == 'm'):
    filename = 'M_Flexure_' + str(file_id) +'.csv'
    m_length = [0.00133533461, 0.00133533461, 0.001366388903, 0.00133533461]                                                    
    m_area = [0.8809660627, 0.8879028034,0.8480022125,0.8809660627]
    fpf = [3802,3098,4057,3718]
    ult = [5344,6741,6115,6119]
    original_area = m_area[file_id-1]
    original_length = m_length[file_id-1]
else:
    filename = 'T_Flexure_' + str(file_id) +'.csv'
    t_length = [0.002061640983,0.002124114952,0.001874219075,0.001686797168] 
    t_area = [1.05457989,0.9707070974,1.286089239,1.613168724]
    original_area = t_area[file_id-1]
    original_length = t_length[file_id-1]

plt.rcParams['font.sans-serif'] = "Lato"
plt.rcParams['font.family'] = "sans-serif"
plt.rcParams['font.size'] = 15

load_extension = []
#This is a "list of lists": [[t1, stress1, strain1], [t2, stress2, strain2], ... ]
with open(filename) as file:
    reader = csv.reader(file, delimiter = ',')
    for i in range(7):
        next(reader)
    for row in reader:
        load_extension.append(row)

load_extension_array = np.array(load_extension)
load_extension_array = load_extension_array.astype('float')

extension = load_extension_array[:,1]
load = load_extension_array[:,2]

length_array = np.array([original_length] * len(extension))
area_array = np.array([original_area] * len(load))

strain = np.multiply(extension,length_array)
stress = np.multiply(load,area_array)

#Smooth data
b,a = scipy.signal.butter(3,0.05, analog=False)
smoothed_stress = scipy.signal.filtfilt(b,a,stress)

slopes = 0.001*np.diff(smoothed_stress)/np.diff(strain)
smoothed_slopes = -1*scipy.signal.filtfilt(b,a,slopes)

second = 0.00005*np.diff(smoothed_slopes)/np.diff(strain[:len(slopes)])
second = scipy.signal.filtfilt(b,a,second)
#=====================================================
#Calculate material properties 
ultimate_tensile_stress = (max(stress))
elongation_at_break = strain[np.where(stress == ultimate_tensile_stress)][0]


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

#x_crit = np.where(strain == find_nearest(strain,myPWLF.fit_breaks[1]))[0][0]
ult = np.where(strain == find_nearest(strain,elongation_at_break))[0][0]

minima, _ = scipy.signal.find_peaks(stress, prominence=3)
print(minima)
#plt.plot(strain[100:10000],second[100:10000])
plt.plot(strain[minima], stress[minima], "xr")
#print(x_crit)
print(len(strain))#beta = myPWLF.beta()
#print(beta)

#sorted_slopes = np.sort(myPWLF.slopes)
#print(sorted_slopes)
#m1 = sorted_slopes[-1]

#plt.plot(strain[x_crit:ult],smoothed_stress[x_crit:ult],label='second half')
# PWLF2 = pwlf.PiecewiseLinFit(strain[x_crit:ult],smoothed_stress[x_crit:ult])
# res = PWLF2.fit(2)
# xHat2 = np.linspace(myPWLF.fit_breaks[1], elongation_at_break, 1000)
# yHat2 = PWLF2.predict(xHat2)
#xHat1 = np.linspace(strain[0], myPWLF.fit_breaks[1], 1000)
#yHat1 = np.multiply(m1,xHat1)# + myPWLF.beta

#slope,intercept,r_value, p_value, std_err = stats.linregress(strain[x_crit:ult],smoothed_stress[x_crit:ult])
#xHat2 = np.linspace(myPWLF.fit_breaks[1], elongation_at_break, 1000)
#yHat2 = np.multiply(slope,xHat2) + intercept
m1 = 0
m2 = 0#slope
print('==========================================================')
print('Parsing file ' + filename)
print()
print('Ultimate tensile strength...   ' + str(ultimate_tensile_stress) + ' MPa')
print('First elastic modulus.......   ' + str(m1) + ' MPa')
print('Second elastic modulus......   ' + str(m2) + ' MPa')
#print('First ply failure strain....   ' + str(myPWLF.fit_breaks[1]))
print('Ultimate failure strain.....   ' + str(elongation_at_break))
print('==========================================================')



#=====================================================
#Configure graph and plot
plt.title(filename)
plt.xlabel('Strain, mm/mm')
plt.ylabel('Stress, MPa')
#print(str(len(xHat)) + ' and ' + str(len(xHat1)))
plt.plot(strain, smoothed_stress, label='Raw data')
#plt.plot(strain[100:3500], second[100:3500],label='Second deriv')
plt.plot(strain[:3500], smoothed_slopes[:3500], label='First derivative')
#plt.plot(xHat1, yHat1, label='First half')
#plt.plot(xHat2, yHat2, label='Second half')

#plt.axvline(x=myPWLF.fit_breaks[1], ymin=0, ymax=100, ls='--')
#plt.text(myPWLF.fit_breaks[1]+0.001,2,'First ply failure',rotation=90)
plt.axvline(x=elongation_at_break, ymin=0, ymax=100, ls='--')
plt.text(elongation_at_break+0.001,2,'Ultimate failure',rotation=90)
#p = plt.annotate(' Ultimate tensile strength ' + str(ultimate_tensile_stress)[0:7] + ' MPa \n First elastic modulus ' + str(m1)[0:8] + ' MPa \n Second elastic modulus ' + str(m2)[0:7] + ' MPa \n First ply failure strain ' + str(myPWLF.fit_breaks[1])[0:5] + '\n Ultimate failure strain ' + str(elongation_at_break)[0:5], xy=(0.01, 0.7), xycoords='axes fraction')
#p.set_bbox(dict(facecolor='white', alpha=1))
#plt.axvline(x=strain[x_crit], ls='dashdot')
print(len(strain))

plt.legend(loc='upper left')
plt.show()

