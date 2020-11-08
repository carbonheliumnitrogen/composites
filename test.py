import csv
import matplotlib.pyplot as plt
import numpy as np
#===================================
sample_set = 'm'
#===================================

plt.rcParams['font.sans-serif'] = "Adobe Heiti Std"
plt.rcParams['font.family'] = "sans-serif"

if (sample_set == 'm'):
    original_length_array = [88.9] * 7                                                                          #mm
    original_area_array = [12.7*4.3, 12.8*4.4, 12.7*4.3, 12.7*4.4, 12.7*4.4, 12.8*4.3, 12.7*4.3]
    n = 8  
    plt.title("Markforged Tensile Stress-Strain")
    filestem = 'M_Tension_'
              #mm^2
else:
    original_length_array = [88.9] * 14 # [25.3, 25.4, 25.3, 25.4, 25.4, 25.4, 25.4, 25.4, 25.3, 25.3, 25.3, 25.3, 25.4, 25.3]                                                                          #mm
    original_area_array = [12.9*3.3, 12.8*2.8, 12.6*3.2, 12.8*3.2, 12.7*2.7,12.7*2.9, 12.6*3.1,12.5*2.8,12.8*2.6,12.7*2.7,12.6*3.4,12.7*2.8,12.7*3.2,12.8*2.9]       
    n = 15   
    plt.title("Hand Layup Tensile Stress-Strain")
    filestem = 'T_Tension_'
      #mm^2

for i in range(1,n):
    original_length = original_length_array[i-1]
    original_area = original_area_array[i-1]
    globals()['load_extension_%s' % i] = []
    filename = filestem + str(i) + '.csv'
    with open(filename) as file:
        reader = csv.reader(file, delimiter = ',')
        for j in range(7):
            next(reader)
        for row in reader:
            globals()['load_extension_%s' % i].append(row)

    globals()['load_extension_array%s' %i] = np.array(globals()['load_extension_%s' % i])
    globals()['load_extension_array%s' %i] = globals()['load_extension_array%s' %i].astype('float')

    globals()['extension_%s' %i] = globals()['load_extension_array%s' %i][:,1]
    globals()['load_%s' %i] = globals()['load_extension_array%s' %i][:,2]

    globals()['length_array_%s' %i] = np.array([original_length] * len(globals()['extension_%s' %i]))
    globals()['area_array_%s' %i] = np.array([original_area] * len(globals()['load_%s' %i]))

    globals()['strain_%s'%i] = np.divide(globals()['extension_%s' %i], globals()['length_array_%s' %i])
    globals()['stress_%s'%i] = np.divide(globals()['load_%s' %i], globals()['area_array_%s' %i])
    thelabel = 'Tensile specimen ' + str(i)
    plt.plot(globals()['strain_%s'%i], globals()['stress_%s'%i], label=thelabel)
    plt.legend()

plt.xlabel('Strain, mm/mm')
plt.ylabel('Stress, MPa')
plt.show()