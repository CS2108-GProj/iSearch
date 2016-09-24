# import the necessary packages
from Tkinter import *
import tkFileDialog
from PIL import Image, ImageTk
#import integrate_search
from integrate_search import search as iSearch

class UI_class:

    def __init__(self, master):

        # Features
        self.Color_Histogram = BooleanVar()
        self.Visual_Keyword = BooleanVar()
        self.Visual_Concept = BooleanVar()

        # Initialize frame
        #self.search_path = search_path
        self.master = master
        self.init_UI()

    def run(self):
        self.master.mainloop()

    # Initialize UI
    def init_UI(self):
        topframe = Frame(self.master)
        topframe.pack()

        # Search Buttons
        self.browse_button = Button(topframe, text=" Choose an image ", command=self.on_input_query)
        self.search_button = Button(topframe, text=" Search ", command=self.on_search)

        # Features
        self.CH_check_box = Checkbutton(topframe, text="Color Histogram", variable=self.Color_Histogram, onvalue=True,
                                        offvalue=False)
        self.VW_check_box = Checkbutton(topframe, text="Visual Keyword", variable=self.Visual_Keyword, onvalue=True,
                                        offvalue=False)
        self.VC_check_box = Checkbutton(topframe, text="Visual Concept + Deep Learning", variable=self.Visual_Concept, onvalue=True,
                                        offvalue=False)

        # Input Image Label
        self.input_image_label = Label(topframe)

        # Error Dialog Box
        self.error_box = Label(topframe)

        # Logo
        self.logo = Label(topframe, text="iSearch")

        # Output Image Label List
        self.output_img_frame = Frame(self.master)
        self.output_img_frame.pack(side=RIGHT)

        self.output_image_label_list = []
        COLUMNS = 5
        for index in range(10):
            r, c = divmod(index, COLUMNS)
            cur_label = Label(self.output_img_frame)
            cur_label.grid(row=r, column=c)
            self.output_image_label_list.append(cur_label)

        # Position UI Elements
        self.browse_button.grid(row=1, column=1)
        self.search_button.grid(row=2, column=1)

        self.CH_check_box.grid(row=3, column=1)
        self.VW_check_box.grid(row=3, column=2)
        self.VC_check_box.grid(row=3, column=3)

        self.input_image_label.grid(row=4, column=1)
        self.error_box.grid(row=5, column=1)
        self.logo.grid(row=6, column=1)


    """
        UI events
    """
    # Input query
    def on_input_query(self):
        self.display_query_img_browser()
        self.display_query_img()


    # Call on_search
    def on_search(self):
        if self.Color_Histogram.get() or self.Visual_Keyword.get() or self.Visual_Concept.get():
            result = iSearch(query=self.filename, CH=self.Color_Histogram.get(), VW=self.Visual_Keyword.get(), VC=self.Visual_Concept.get(), threshold=1500, result_limit=10)
            print(result)
            self.display_results_imgs(result)
        else:
            self.display_error("Please choose a feature")

            # Test function on feature triggering


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
    def display_results_imgs(self, results):
        image_count = 0
        for item_score in results:
            # load the result image and display it

            im = Image.open(item_score['image_name'])
            resized = im.resize((100, 100), Image.ANTIALIAS)
            tkimage = ImageTk.PhotoImage(resized)
            self.output_image_label_list[image_count].config(image=tkimage)
            self.output_image_label_list[image_count].image = tkimage
            image_count += 1


    # Display Error
    def display_error(self, message):
        self.error_box.config(text=message)


    """
        Feature Process & Search functions
    """
    # # Process with color histogram
    # def process_ch(self):
    #     # process query image to feature vector
    #     # initialize the image descriptor
    #     cd = ColorDescriptor((8, 12, 3))
    #
    #     # load the query image and describe it
    #     query = cv2.imread(self.filename)
    #     return cd.describe(query)
    #
    #
    # # Search with CH
    # def search_ch(self, query):
    #     # perform the on_search
    #     searcher = CH_Searcher("index.csv")
    #     return searcher.search(query)
    #
    #
    # # Prcess with visual concept
    # def process_vc(self):
    #     # To be implemented
    #     return None


if __name__ == "__main__":
    root = Tk()
    window = UI_class(root)
    window.run()
