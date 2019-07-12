from os import listdir
from os.path import isfile, join
from PIL import Image
import numpy as np
import xlsxwriter
import time

def MeanAndStandardDevCalculator(image_path):
    img = Image.open(image_path).convert('L')
    arry = np.array(img)
    mean = np.mean(arry)
    standard_dev = np.std(arry)
    return [mean, standard_dev]

def WriteXL(dataList):

    currentTime = time.strftime("%Y%m%d_%H%M%S")
    filename = '../output/'+currentTime + '_TrainETH80data328.xlsx'

    xbook = xlsxwriter.Workbook(filename)
    xsheet = xbook.add_worksheet('data')

    xsheet.write_row(0, 0, ['image_name', 'mean', 'standard_deviation'])

    for i in range (1,(len(dataList))):
        xsheet.write_row(i, 0, dataList[i-1])

    xsheet.write_row(i+1, 0, dataList[i])

    xbook.close()

    return



dataList = []
mypath = '../datasets/TestETH80data328/'
imagefiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
print(imagefiles)

for imagePath in imagefiles:
    full_path = mypath+imagePath
    mean_and_deviation = MeanAndStandardDevCalculator(full_path)
    dataList.append([imagePath, mean_and_deviation[0], mean_and_deviation[1]])



WriteXL(dataList)




