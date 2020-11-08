import csv
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = "Adobe Heiti Std"
plt.rcParams['font.family'] = "sans-serif"

#Markforged samples (n = 4):
original_length = [0.00133533461, 0.00133533461, 0.001366388903, 0.00133533461]                                                    
original_area = [0.8809660627, 0.8879028034,0.8480022125,0.8809660627]
#Hand layup samples (n = 15):
# original_area = [1.05457989,0.9707070974,1.286089239,1.613168724]
# original_length = [0.002061640983,0.002124114952,0.001874219075,0.001686797168]                

for i in range(1,5):
    globals()['load_extension_%s' % i] = []
    filename = 'M_Flexure_' + str(i) + '.csv'
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

    globals()['strain_%s'%i] = np.multiply(globals()['extension_%s' %i], globals()['length_array_%s' %i][:,0])
    globals()['stress_%s'%i] = np.multiply(globals()['load_%s' %i], globals()['area_array_%s' %i][:,0])
    thelabel = 'Flexure specimen ' + str(i)
    plt.plot(globals()['strain_%s'%i], globals()['stress_%s'%i], label=thelabel)
    plt.legend()

plt.title("Markforged Flexure Stress-Strain")
plt.xlabel('Strain, mm/mm')
plt.ylabel('Stress, MPa')
plt.show()