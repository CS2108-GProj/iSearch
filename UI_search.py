# import the necessary packages
from color_histogram.colordescriptor import ColorDescriptor
from color_histogram.searcher import Searcher
import cv2
from Tkinter import *
import tkFileDialog
from PIL import Image, ImageTk

class UI_class:

    def __init__(self, master, search_path):

        # Features
        self.Color_Histogram = BooleanVar()

        # Initialize frame
        self.search_path = search_path
        self.master = master
        self.init_UI()

    def run(self):
        self.master.mainloop()

    # Initialize UI
    def init_UI(self):
        topframe = Frame(self.master)
        topframe.pack()

        # Search Buttons
        self.bbutton = Button(topframe, text=" Choose an image ", command=self.on_input_query)
        self.bbutton.grid(row=1, column=1)
        self.cbutton = Button(topframe, text=" Search ", command=self.on_search)
        self.cbutton.grid(row=1, column=2)

        # Features
        self.CH_check_box = Checkbutton(topframe, text="Color Histogram", variable=self.Color_Histogram, onvalue=True,
                                        offvalue=False, command=self.trigger_color_historgram)
        self.CH_check_box.grid(row=2, column=1)

        # Input Image Label
        self.input_image_label = Label(topframe)
        self.input_image_label.grid(row=3, column=1)

        # Output Image Label List
        self.output_img_frame = Frame(self.master)
        self.output_img_frame.pack()

        self.output_image_label_list = []
        COLUMNS = 5
        for index in range(10):
            r, c = divmod(index, COLUMNS)
            cur_label = Label(self.output_img_frame)
            cur_label.grid(row=r, column=c)
            self.output_image_label_list.append(cur_label)

        # Error Dialog Box
        self.error_box = Label(topframe)
        self.error_box.grid(row=4)

        # Logo
        self.logo = Label(topframe, text="iSearch")
        self.logo.grid(row=5)

    """
        UI events
    """
    # Input query
    def on_input_query(self):
        self.display_query_img_browser()
        self.display_query_img()


    # Call on_search
    def on_search(self):
        if self.Color_Histogram.get():
            self.process_ch()
            self.display_results_imgs()
        else:
            self.display_error("Please choose a feature")


    """
        UI update
    """
    # Display local query image browser
    def display_query_img_browser(self):
        from tkFileDialog import askopenfilename
        self.filename = tkFileDialog.askopenfile(title='Choose an Image File').name


    # Display input query image
    def display_query_img(self):
        image_file = Image.open(self.filename)

        resized = image_file.resize((100, 100), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(resized)

        self.input_image_label.config(image=img)
        self.input_image_label.image=img
        self.logo.config(text="Upload 1 image")


    # Show result images
    def display_results_imgs(self):
        self.output_img_frame = Frame(self.master)
        self.output_img_frame.pack()

        # perform the on_search
        searcher = Searcher("index.csv")
        results = searcher.search(self.queryfeatures)

        # show result pictures
        image_count = 0
        for (score, resultID) in results:
            # load the result image and display it

            im = Image.open( self.search_path + "/" + resultID)
            resized = im.resize((100, 100), Image.ANTIALIAS)
            tkimage = ImageTk.PhotoImage(resized)
            self.output_image_label_list[image_count].config(image=tkimage)
            self.output_image_label_list[image_count].image = tkimage
            image_count += 1


    # Display Error
    def display_error(self, message):
        self.error_box.config(text=message)

    """
        Feature Process functions
    """
    # Process with color histogram
    def process_ch(self):
        # process query image to feature vector
        # initialize the image descriptor
        cd = ColorDescriptor((8, 12, 3))

        # load the query image and describe it
        query = cv2.imread(self.filename)
        self.queryfeatures = cd.describe(query)


    # Prcess with visual concept
    def process_vc(self):
        # To be implemented
        return None

    # Test function on feature triggering
    def trigger_color_historgram(self):
        print ">>>>>>> CH feature is ", self.Color_Histogram.get()


if __name__ == "__main__":
    root = Tk()
    window = UI_class(root, 'dataset')
    window.run()
