import csv
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal
from scipy import optimize
from scipy import stats
import pwlf
import warnings
#Indicate sample ID and group here (Flexure)
#===========================================
file_id = 2
file_group = 't'
#===========================================

if (file_group == 'm'):
    filename = 'M_Flexure_' + str(file_id) +'.csv'
    m_length = [0.00133533461, 0.00133533461, 0.001366388903, 0.00133533461]                                                    
    m_area = [0.8809660627, 0.8879028034,0.8480022125,0.8809660627]
    fpfarray = [3802,3884,4057,3718]
    ultarray = [5344,6698,6115,6119]
    original_area = m_area[file_id-1]
    original_length = m_length[file_id-1]
    fpf = fpfarray[file_id-1]
    ult = ultarray[file_id-1]
else:
    filename = 'T_Flexure_' + str(file_id) +'.csv'
    t_length = [0.002061640983,0.002124114952,0.001874219075,0.001686797168] 
    t_area = [1.05457989,0.9707070974,1.286089239,1.613168724]
    fpfarray = [734,777,702,1927]
    ultarray = [0] * 4
    original_area = t_area[file_id-1]
    original_length = t_length[file_id-1]
    fpf = fpfarray[file_id-1]
    ult = ultarray[file_id-1]

plt.rcParams['font.sans-serif'] = "Lato"
plt.rcParams['font.family'] = "sans-serif"
plt.rcParams['font.size'] = 15

#Get the data from the CSV file, organize it, and compute
#stress and strain using specimen dimensions
load_extension = []
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

#Smooth data (uses zero-phase filtering). Also, calculate first/second
#derivatives, for help finding peaks if necessary.
b,a = scipy.signal.butter(3,0.05, analog=False)
smoothed_stress = scipy.signal.filtfilt(b,a,stress)

slopes = 0.001*np.diff(smoothed_stress)/np.diff(strain)
smoothed_slopes = -1*scipy.signal.filtfilt(b,a,slopes)

second = 0.00005*np.diff(smoothed_slopes)/np.diff(strain[:len(slopes)])
second = scipy.signal.filtfilt(b,a,second)
#=====================================================
#Calculate material properties 
#=====================================================
ultimate_tensile_stress = (max(stress))

#For the hand layup samples the laminate failure occurs at ultimate tensile stress,
#for the Markforged samples they don't necessarily. So we use the find_peaks function to 
#detect where failure occurs.
if (file_group == 't'):
    ult = np.where(stress == ultimate_tensile_stress)[0][0]
first_ply_failure = strain[fpf]
elongation_at_break = strain[ult]

minima, _ = scipy.signal.find_peaks(stress, prominence=2)
#print(minima)
#plt.plot(strain[minima], stress[minima], "xr")

#Fit lines to regions I and II. Get slopes and prepare to graph
m1,b1, a,b,c = stats.linregress(strain[0:fpf], smoothed_stress[0:fpf])
m2,b2, a,b,c = stats.linregress(strain[fpf:ult], smoothed_stress[fpf:ult])
xHat1 = np.linspace(strain[0], strain[fpf], 1000)
yHat1 = np.multiply(m1, xHat1) + b1
xHat2 = np.linspace(strain[fpf], strain[ult], 1000)
yHat2 = np.multiply(m2, xHat2) + b2

#=====================================================
#Configure graph and plot
#=====================================================
plt.title(filename)
plt.xlabel('Strain, mm/mm')
plt.ylabel('Stress, MPa')

#Plot the data
plt.plot(strain, stress, label='Raw data',zorder=0)
plt.plot(xHat1, yHat1, label='Region I - Linear fit', zorder=10, lw = 3)
plt.plot(xHat2, yHat2, label='Region II - Linear fit', zorder = 10, lw = 3)

#Vertical bars for failure spots
plt.axvline(x=first_ply_failure, ymin=0, ymax=100, ls='--')
plt.text(first_ply_failure+0.0001,2,'First ply failure',rotation=90)
plt.axvline(x=elongation_at_break, ymin=0, ymax=100, ls='--')
plt.text(elongation_at_break+0.0001,2,'Laminate failure',rotation=90)

#Display info and legend
p = plt.annotate(' Ultimate tensile strength ' + str(ultimate_tensile_stress)[0:7] + ' MPa \n First elastic modulus ' + str(m1)[0:8] + ' MPa \n Second elastic modulus ' + str(m2)[0:7] + ' MPa \n First ply failure strain ' + str(first_ply_failure)[0:6] + '\n Laminate failure strain ' + str(elongation_at_break)[0:6], xy=(0.01, 0.65), xycoords='axes fraction', zorder=100)
p.set_bbox(dict(facecolor='white', alpha=1))
plt.legend(loc='upper left')

plt.show()

#Print stuff to console window
print('==========================================================')
print('Parsing file ' + filename)
print()
print('Ultimate tensile strength...   ' + str(ultimate_tensile_stress) + ' MPa')
print('First elastic modulus.......   ' + str(m1) + ' MPa')
print('Second elastic modulus......   ' + str(m2) + ' MPa')
print('First ply failure strain....   ' + str(first_ply_failure))
print('Laminate failure strain.....   ' + str(elongation_at_break))
print('==========================================================')