
import tableprint
import numpy as np

target_afr_table = []
engine_load_scale = [35, 75, 125, 175, 250, 325, 400, 450, 550, 700, 950, 1250]
engine_rpm_scale = [600, 1000, 1200, 1500, 1600, 2000, 2500, 3000, 3500, 3900, 4100, 4500, 4800, 5500, 6300, 7000]

target_afr_table.append([14.7, 14.7, 14.5, 14, 13.3, 12.5, 12.3, 12.3, 12, 12, 12, 12])
target_afr_table.append([14.7, 14.7, 14.5, 14, 13.3, 12.5, 12.3, 12.3, 12, 12, 12, 12])
target_afr_table.append([14.7, 14.7, 14.5, 14, 13.3, 12.5, 12.3, 12.3, 12, 12, 12, 12])
target_afr_table.append([14.7, 14.7, 14.5, 14, 13.3, 12.5, 12.3, 12.3, 12, 12, 12, 12])
target_afr_table.append([14.7, 14.7, 14.5, 14, 13.3, 12.5, 12.3, 12.3, 12, 12, 12, 12])
target_afr_table.append([14.7, 14.7, 14.5, 14, 13.3, 12.5, 12.3, 12.3, 12, 12, 12, 12])
target_afr_table.append([14.7, 14.6, 14.4, 14, 13.3, 12.5, 12.3, 12.3, 12, 12, 12, 12])
target_afr_table.append([14.7, 14.6, 14.3, 13.9, 13, 12.5, 12.3, 12.3, 12, 12, 12, 12])
target_afr_table.append([14.7, 14.6, 14.3, 13.9, 13, 12.5, 12.3, 12.3, 12, 12, 12, 12])
target_afr_table.append([14.7, 14.6, 14.3, 13.8, 13, 12.5, 12.3, 12.3, 12, 12, 12, 12])
target_afr_table.append([14.7, 14.5, 14.2, 13.7, 13, 12.5, 12.3, 12.3, 12, 12, 12, 12])
target_afr_table.append([14.5, 14.4, 14.2, 13.7, 12.7, 12.5, 12.3, 12.3, 12, 12, 12, 12])
target_afr_table.append([14.5, 14.4, 14.2, 13.7, 12.7, 12.5, 12.3, 12.3, 12, 12, 12, 12])
target_afr_table.append([14.5, 14.4, 14.2, 13.5, 12.7, 12.5, 12.3, 12.3, 12, 12, 12, 12])
target_afr_table.append([14.5, 14.4, 14.2, 13.5, 12.7, 12.5, 12.3, 12.3, 12, 12, 12, 12])
target_afr_table.append([14.5, 14.4, 14.2, 13.5, 12.7, 12.5, 12.3, 12.3, 12, 12, 12, 12])

print(len(target_afr_table))


afr_history_table_file = open("afr_history_table").readlines(); afr_history_table = []
current_fuel_map_file = open("current_fuel_map").readlines(); current_fuel_map = []

# Parse afr_history_table
for line in afr_history_table_file:
  line = line.strip("\n")
  tmp = []
  for x in line.split("\t"):
    if len(x) < 5:
      tmp.append(99.00)
      continue
    tmp.append(float(x))

  afr_history_table.append(tmp)

# Parse fuel map
for line in current_fuel_map_file:
  line = line.strip("\n")
  tmp = []
  for x in line.split("\t"):
    if len(x) < 5:
      tmp.append(99.00)
      continue
    tmp.append(float(x))

  current_fuel_map.append(tmp)

# Prepare headers
headers = ['RxL'] + [str(x) for x in engine_load_scale]
data = []

for i, target_afr in enumerate(current_fuel_map): data.append([str(engine_rpm_scale[i])] + [str(x) for x in target_afr])

# Print table
print("\r\nOld map")
tableprint.table(data , headers)

difference_new_table = []
# (afr - target) / target
for i in range(0, len(target_afr_table)):
  difference_new_table_tmp = []

  for ii in range(0, len(target_afr_table[i])):
    divide = False

    if (afr_history_table[i][ii] == 99.0):
      difference_new_table_tmp.append(current_fuel_map[i][ii])
      continue
    
    difference = float("%0.3f" % ((afr_history_table[i][ii] - target_afr_table[i][ii]) / afr_history_table[i][ii]))
    
    if (difference == 0.00):
      difference_new_table_tmp.append(current_fuel_map[i][ii])
      continue
    
    if (difference < 0.00): 
      difference = difference * -1
      divide = True

    difference = float("%.03f" % (difference + 1.00))
    
    new = 0.000

    if (divide == True):
      new = (float("%0.3f" % (current_fuel_map[i][ii] / difference)))

    if (divide == False):
      new = (float("%0.3f" % (difference * current_fuel_map[i][ii])))

    difference_new_table_tmp.append(new)
  difference_new_table.append(difference_new_table_tmp)

# Prepare headers
headers = ['RxL'] + [str(x) for x in engine_load_scale]
data = []

for i, target_afr in enumerate(difference_new_table): data.append([str(engine_rpm_scale[i])] + [str(x) for x in target_afr])

# Print table
print("\r\nNew map")
tableprint.table(data , headers)

outfile = open("new_fuel_map", "w+")

for ii, a in enumerate(difference_new_table):
  for i, b in enumerate(a):
    outfile.write(str(b))
    if (i + 1 != len(a)): 
      outfile.write("\t")
  if (ii + 1 != len(difference_new_table)):
    outfile.write("\n")

outfile.close()
