import csv
import matplotlib.pyplot as plt
import numpy as np
#===================================
sample_set = 'm'
#===================================
plt.rcParams['font.sans-serif'] = "Adobe Heiti Std"
plt.rcParams['font.family'] = "sans-serif"

if (sample_set == 'm'):
    original_length_array = [0.00133533461, 0.00133533461, 0.001366388903, 0.00133533461]                                                    
    original_area_array = [0.8809660627, 0.8879028034,0.8480022125,0.8809660627]
    plt.title("Markforged Flexure Stress-Strain")
    filestem = 'M_Flexure_'
else:
    original_length_array = [0.002061640983,0.002124114952,0.001874219075,0.001686797168] 
    original_area_array = [1.05457989,0.9707070974,1.286089239,1.613168724]       
    plt.title("Hand Layup Flexure Stress-Strain")
    filestem = 'T_Flexure_'
        
for i in range(1,5):
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

    globals()['strain_%s'%i] = np.multiply(globals()['extension_%s' %i], globals()['length_array_%s' %i])
    globals()['stress_%s'%i] = np.multiply(globals()['load_%s' %i], globals()['area_array_%s' %i])
    thelabel = 'Flexure specimen ' + str(i)
    plt.plot(globals()['strain_%s'%i], globals()['stress_%s'%i], label=thelabel)
    plt.legend()

plt.xlabel('Strain, mm/mm')
plt.ylabel('Stress, MPa')
plt.show()