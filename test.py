import csv
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = "Adobe Heiti Std"
plt.rcParams['font.family'] = "sans-serif"

original_length = [25.4] * 14                                                                          #mm
original_area = [12.7*4.3, 12.8*4.4, 12.7*4.3, 12.7*4.4, 12.7*4.4, 12.8*4.3, 12.7*4.3,12.7*4.3, 12.8*4.4, 12.7*4.3, 12.7*4.4, 12.7*4.4, 12.8*4.3, 12.7*4.3]                #mm^2

for i in range(1,15):
    globals()['load_extension_%s' % i] = []
    filename = 'T_Tension_' + str(i) + '.csv'
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

    globals()['strain_%s'%i] = np.divide(globals()['extension_%s' %i], globals()['length_array_%s' %i][:,0])
    globals()['stress_%s'%i] = np.divide(globals()['load_%s' %i], globals()['area_array_%s' %i][:,0])
    thelabel = 'Tensile specimen ' + str(i)
    plt.plot(globals()['strain_%s'%i], globals()['stress_%s'%i], label=thelabel)
    plt.legend()

plt.title("Hand Layup Tensile Stress-Strain")
plt.xlabel('Strain, mm/mm')
plt.ylabel('Stress, MPa')
plt.show()