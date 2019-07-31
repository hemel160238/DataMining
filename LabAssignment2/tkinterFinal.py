import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from os import listdir
from os.path import isfile, join
from PIL import Image, ImageTk
import numpy as np
import xlsxwriter
import time
import re
import math
import pandas

root = tk.Tk()
folder_dir = ''
feature_file = ''
query_image = ''
blank_img = r'blank_image/blank.png'


def fivenumber_and_variance(image_path):
    img = Image.open(image_path).convert('L')
    array = np.array(img)

    min = np.amin(array)
    first_quartile = np.percentile(array, 25)
    median = np.percentile(array, 50)
    third_quartile = np.percentile(array, 75)
    max = np.amax(array)

    variance = np.var(array)

    return [min, first_quartile, median, third_quartile, max, variance]

def MeanMedianAndMidrangeCalculator(image_path):
    img = Image.open(image_path).convert('L')
    arry = np.array(img)
    mean = np.mean(arry)
    median = np.median(arry)

    midrange = (np.amax(arry) - np.amin(arry))/2

    standard_dev = np.std(arry)
    return [mean, median, midrange]

def WriteXL(dataList):

    currentTime = time.strftime("%Y%m%d_%H%M%S")
    filename = 'output/'+currentTime + '_TrainETH80data2952.xlsx'

    xbook = xlsxwriter.Workbook(filename)
    xsheet = xbook.add_worksheet('data')

    xsheet.write_row(0, 0, ['image_name', 'min', 'first_quartile', 'median', 'third_quartile', 'maximum', 'variance'])

    for i in range (1,(len(dataList))):
        xsheet.write_row(i, 0, dataList[i-1])

    xsheet.write_row(i+1, 0, dataList[i])

    xbook.close()

    return

def savefeature():

    global folder_dir
    dataList = []

    if(len(folder_dir) == 0):
        messagebox.showwarning("Warning", "No folder Selected")
        return

    mypath = '../datasets/TrainETH80data2952/'

    mypath = folder_dir+'/'

    imagefiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    print(imagefiles)

    for imagePath in imagefiles:
        full_path = mypath + imagePath

        imageName = re.sub('[^a-zA-Z.]', '', imagePath).split('.')[0]
        #mean_median_and_midrange = MeanMedianAndMidrangeCalculator(full_path)
        five_and_var = fivenumber_and_variance(full_path)
        dataList.append([full_path, five_and_var[0], five_and_var[1], five_and_var[2], five_and_var[3], five_and_var[4], five_and_var[5]])

    WriteXL(dataList)

    messagebox.showinfo("Success", "Output xl is saved in output folder")

def selectfolder():
    global folder_dir
    print(folder_dir)
    root.directory = filedialog.askdirectory()
    folder_dir = root.directory
    print(folder_dir)

    if(len(folder_dir) > 0):
        #selected_training_folder['text'] = "Selected Folder : "+folder_dir
        selected_training_folder['text'] = "Folder Selected"
        selected_training_folder['bg'] = "green"

def selectFeatureFile():
    global feature_file
    print(feature_file)
    root.directory = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
    feature_file = root.directory
    print(feature_file)

    if(len(feature_file)>0):
        #selected_feature_file['text'] = "Selected Feature File is  : " + feature_file
        selected_feature_file['text'] = "Feature File Selected"
        selected_feature_file['bg'] = "green"

def selectQueryImage():
    global query_image
    print(query_image)
    root.directory = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg")])
    query_image = root.directory
    print(query_image)

    if(len(query_image)>0):
        img = ImageTk.PhotoImage(Image.open(query_image).resize((120, 120), Image.ANTIALIAS))


        query_image_box.configure(image = img)
        query_image_box.image = img


        selected_query_image['text'] = "Query Image Selected"
        #selected_query_image['text'] = "Selected query Image  is  : " + query_image
        selected_query_image['bg'] = "green"


def calculateCityBlockDist(point1, point2):
    return (abs(point1[0] - point2[0]) + abs(point1[1] - point2[1]) + abs(point1[2] - point2[2]) + abs(point1[3] - point2[3]) + abs(point1[4] - point2[4]) + abs(point1[5] - point2[5]))
def calculateEuDistance(first_image, second_image):
    return math.sqrt((first_image[0] - second_image[0])**2 + (first_image[1] - second_image[1])**2 + (first_image[2] - second_image[2])**2)

def update_dict(unit_image, image_array, diction):

    image_name = unit_image[0]
    eu_distance =  calculateEuDistance([unit_image[1], unit_image[2], unit_image[3]], image_array)

    if eu_distance < 1:
        print(unit_image)
        print(image_array)

    if (not image_name in diction):
        diction[image_name] = [eu_distance, 1]

    else:
        existing_list = diction[image_name]
        total_dist = existing_list[0] + eu_distance
        new_count = existing_list[1] + 1

        diction[image_name] = [total_dist, new_count]
    return diction


def calculateDistance(numpy_array, image_array):

    diction = {}
    for unit_image in numpy_array:
        diction = update_dict(unit_image, image_array, diction)

    for key, value in diction.items():
        avg_value = value[0]/value[1]
        diction[key] = [avg_value]

    return (min(diction, key = diction.get))


def showMachingImages(imageList):
    all_images = []

    for image in imageList:
        im = Image.open(image[0])
        resized = im.resize((120, 120), Image.ANTIALIAS)
        tkimage = ImageTk.PhotoImage(resized)
        all_images.append(tkimage)

    output_image1.configure(image=all_images[0])
    output_image1.image = all_images[0]

    output_image2.configure(image=all_images[1])
    output_image2.image = all_images[1]

    output_image3.configure(image=all_images[2])
    output_image3.image = all_images[2]

    output_image4.configure(image=all_images[3])
    output_image4.image = all_images[3]

    output_image5.configure(image=all_images[4])
    output_image5.image = all_images[4]

    output_image6.configure(image=all_images[5])
    output_image6.image = all_images[5]

    output_image7.configure(image=all_images[6])
    output_image7.image = all_images[6]

    output_image8.configure(image=all_images[7])
    output_image8.image = all_images[7]

    output_image9.configure(image=all_images[8])
    output_image9.image = all_images[8]

    output_image10.configure(image=all_images[9])
    output_image10.image = all_images[9]

    pass

def recognise():

    all_distance_list = []
    global feature_file
    global query_image

    if(len(query_image) == 0 or len(feature_file) == 0):
        messagebox.showwarning("Warning", "Select Image and Feature File")
        return

    df = pandas.read_excel(feature_file, sheet_name='data')
    npArray = df.to_numpy()
    image_path = query_image

    test_image = fivenumber_and_variance(query_image)

    for unit_image in npArray:
        durotto = calculateCityBlockDist(unit_image[1:], test_image)

        all_distance_list.append([unit_image[0], durotto])
        print(durotto)

    print(all_distance_list)
    sorted_distance = sorted(all_distance_list, key= lambda x: x[1])
    print(sorted_distance[:10])
    showMachingImages(sorted_distance[:10])



im = Image.open(blank_img)
resized = im.resize((120, 120), Image.ANTIALIAS)
tkimage = ImageTk.PhotoImage(resized)


tk.Label(root, text="Test Image").grid(row=0, column = 0)
query_image_box = tk.Label(root, image = tkimage)
query_image_box.grid(row = 0, column = 1)


tk.Label(root, text="Similar Images").grid(row=1, column = 0)

output_image1 = tk.Label(root, image = tkimage)
output_image1.grid(row = 1, column = 1)
output_image2 = tk.Label(root, image = tkimage)
output_image2.grid(row = 1, column = 2)
output_image3 = tk.Label(root, image = tkimage)
output_image3.grid(row = 1, column = 3)
output_image4 = tk.Label(root, image = tkimage)
output_image4.grid(row = 1, column = 4)
output_image5 = tk.Label(root, image = tkimage)
output_image5.grid(row = 1, column = 5)

output_image6 = tk.Label(root, image = tkimage)
output_image6.grid(row = 2, column = 1)
output_image7 = tk.Label(root, image = tkimage)
output_image7.grid(row = 2, column = 2)
output_image8 = tk.Label(root, image = tkimage)
output_image8.grid(row = 2, column = 3)
output_image9 = tk.Label(root, image = tkimage)
output_image9.grid(row = 2, column = 4)
output_image10 = tk.Label(root, image = tkimage)
output_image10.grid(row = 2, column = 5)


selected_training_folder = tk.Label(root, text = "No Folder Selected", bg = "red", fg = "white")
selected_training_folder.grid(row = 5, column = 1)

selected_feature_file = tk.Label(root, text = "No Feature File Selected", bg = "red", fg = "white")
selected_feature_file.grid(row = 6, column = 1)

selected_query_image = tk.Label(root, text = "No Query Image Selected", bg = "red", fg = "white")
selected_query_image.grid(row = 7, column = 1)

button_LoadTrainingImage = tk.Button(text = 'Load Training Image', command = selectfolder)
button_LoadTrainingImage.grid(row = 4, column = 1)

button_SaveFeature = tk.Button(text = 'Extract Feature and Save', command = savefeature)
button_SaveFeature.grid(row = 4, column = 2)

button_LoadFeatureFile = tk.Button(text = 'Load Feature File', command = selectFeatureFile)
button_LoadFeatureFile.grid(row = 4, column = 3)

button_LoadQueryImage = tk.Button(text = 'Load Query Image', command = selectQueryImage)
button_LoadQueryImage.grid(row = 4, column = 4)

button_RecogniseImage = tk.Button(text = 'Recognise', command = recognise)
button_RecogniseImage.grid(row = 4, column = 5)

tk.mainloop()