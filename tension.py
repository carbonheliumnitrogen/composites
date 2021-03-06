import csv
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal
from scipy import optimize
import pwlf
import warnings
#Indicate sample ID and group here (Tension)
#===========================================
file_id = 6
file_group = 'm'
#===========================================

#Measured specimen dimensions. Import file
original_length = 88.9
markforged = [54.61, 56.32, 54.61, 55.88, 55.88, 55.04, 55.88]
layup = [42.57, 35.84, 40.32, 40.96, 34.29, 36.83, 39.06, 35.00, 33.28, 34.29, 42.84, 35.56, 40.64, 37.12]
if (file_group == 't'):
    filename = 'T_Tension_' + str(file_id) +'.csv'
    original_area = layup[file_id-1]
else:
    filename = 'M_Tension_' + str(file_id) +'.csv'
    original_area = markforged[file_id-1]
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

strain = np.divide(extension,length_array)
stress = np.divide(load,area_array)

#=====================================================
#Calculate material properties 
#=====================================================
ultimate_tensile_stress = (max(stress))
elongation_at_break = strain[np.where(stress == ultimate_tensile_stress)]
elongation_at_break = elongation_at_break[0]

#To fit the data to a piecewise linear model, we use the PWLF package
myPWLF = pwlf.PiecewiseLinFit(strain[:800],stress[:800])
res = myPWLF.fit(2)
xHat = np.linspace(0, elongation_at_break, 1000)
yHat = myPWLF.predict(xHat)
m1 = np.max(myPWLF.slopes)
m2 = np.min(myPWLF.slopes)

#=====================================================
#Configure graph and plot
#=====================================================
plt.title(filename)
plt.xlabel('Strain, mm/mm')
plt.ylabel('Stress, MPa')

#Plot the data
plt.plot(strain, stress, label='Raw data')
plt.plot(xHat,yHat,label='Piecewise linear fit')

#Vertical bars for failure spots
plt.axvline(x=myPWLF.fit_breaks[1], ymin=0, ymax=100, ls='--')
plt.text(myPWLF.fit_breaks[1]+0.001,2,'First ply failure',rotation=90)
plt.axvline(x=elongation_at_break, ymin=0, ymax=100, ls='--')
plt.text(elongation_at_break+0.001,2,'Ultimate failure',rotation=90)

#Display info and legend
p = plt.annotate(' Ultimate tensile strength ' + str(ultimate_tensile_stress)[0:7] + ' MPa \n First elastic modulus ' + str(m1)[0:8] + ' MPa \n Second elastic modulus ' + str(m2)[0:7] + ' MPa \n First ply failure strain ' + str(myPWLF.fit_breaks[1])[0:5] + '\n Ultimate failure strain ' + str(elongation_at_break)[0:5], xy=(0.01, 0.7), xycoords='axes fraction')
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
print('First ply failure strain....   ' + str(myPWLF.fit_breaks[1]))
print('Ultimate failure strain.....   ' + str(elongation_at_break))
print('==========================================================')