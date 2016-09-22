import csv
import os
from glob import glob

result = [y for x in os.walk('./indexes') for y in glob(os.path.join(x[0], '*.csv'))]

# write a single index.csv file using indexes generated.
with open('index.csv', 'w') as csvoutput:
    writer = csv.writer(csvoutput)
    for file in result:
        base = os.path.basename(file)
        fileName = os.path.splitext(base)[0]
        with open(file, 'r') as csvinput:
            reader = csv.reader(csvinput)
            row = next(reader)
            row.append(fileName)
            writer.writerow(row)