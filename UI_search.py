# import the necessary packages
from color_histogram.colordescriptor import ColorDescriptor
from color_histogram.searcher import Searcher
import cv2
from Tkinter import *
import tkFileDialog
from PIL import Image, ImageTk

class UI_class:

    def __init__(self, master, search_path):

        # Intialize Features
        self.Color_Histogram = BooleanVar()

        # Initialize frame
        self.search_path = search_path
        self.master = master
        topframe = Frame(self.master)
        topframe.pack()

        # Search Buttons
        topspace = Label(topframe).grid(row=0, columnspan=2)
        self.bbutton = Button(topframe, text=" Choose an image ", command=self.input_query)
        self.bbutton.grid(row=1, column=1)
        self.cbutton = Button(topframe, text=" Search ", command=self.search)
        self.cbutton.grid(row=1, column=2)

        # Features
        self.CH_check_box = Checkbutton(topframe, text="Color Histogram", variable=self.Color_Histogram, onvalue=True, offvalue=False, command=self.trigger_color_historgram)
        self.CH_check_box.grid(row = 2, column = 1)
        downspace = Label(topframe).grid(row=3, columnspan=4)

        self.master.mainloop()


    # Input query
    def input_query(self):
        self.browse_query_img()
        self.display_query_img()


    # Call search
    def search(self):
        self.process_query_img()
        self.show_results_imgs()


    # Browse local query image
    def browse_query_img(self):
        from tkFileDialog import askopenfilename
        self.filename = tkFileDialog.askopenfile(title='Choose an Image File').name


    # Display input query image
    def display_query_img(self):
        image_file = Image.open(self.filename)

        resized = image_file.resize((100, 100), Image.ANTIALIAS)
        im = ImageTk.PhotoImage(resized)
        image_label = Label(self.master, image=im)
        image_label.pack()

        self.master.mainloop()


    # Process query image, extract image data according to selected features
    def process_query_img(self):
        if (self.CH_check_box):
            self.process_ch()
        else:
            self.generate_error("Please choose one feature")


    def show_results_imgs(self):
        self.result_img_frame = Frame(self.master)
        self.result_img_frame.pack()

        # perform the search
        searcher = Searcher("index.csv")
        results = searcher.search(self.queryfeatures)

        # show result pictures
        COLUMNS = 5
        image_count = 0
        for (score, resultID) in results:
            # load the result image and display it
            image_count += 1
            r, c = divmod(image_count - 1, COLUMNS)
            im = Image.open( self.search_path + "/" + resultID)
            resized = im.resize((100, 100), Image.ANTIALIAS)
            tkimage = ImageTk.PhotoImage(resized)
            myvar = Label(self.result_img_frame, image=tkimage)
            myvar.image = tkimage
            myvar.grid(row=r, column=c)

        self.master.mainloop()


    # Display error
    def generate_error(self, message):
        w = Label(self.master, text=message)
        w.pack()

        self.master.mainloop()


    # Process with color histogram
    def process_ch(self):
        # process query image to feature vector
        # initialize the image descriptor
        cd = ColorDescriptor((8, 12, 3))

        # load the query image and describe it
        query = cv2.imread(self.filename)
        self.queryfeatures = cd.describe(query)

    # Test function on feature triggering
    def trigger_color_historgram(self):
        print ">>>>>>> CH feature is ", self.Color_Histogram.get()


root = Tk()
window = UI_class(root,'dataset')
