from tkinter import *
from PIL import ImageTk, Image
import os


def scan_for_images():
    ''' Function that checks and finds all 
    image files in a current directory. Then
    it stores all image filenames in a list.'''

    filenames = os.listdir()
    images = []

    for filename in filenames:
        try:
            image = Image.open(filename)
        except:
            pass
        else:
            images.append(filename)
            image.close()

    return images

def check_and_resize(image):
    """
    resizes image to fit app window if it overflows frame

    app window space for image:
     
        width(800)
        ----------
        |        | height(560)
        |        |
        ----------

    **Case 1 image (image fits window space):

        original_width <= 800
            -----
            |   | original_height <= 560
            -----
        image is directly returned by function, 
        bacause it fits image space in app window

    **Case 2 only image width overflows image space in window

        original_width > 800
        ------------------
        |                | original_height <= 560
        |                | 
        ------------------

    **Case 3 only image height overflows image space in window

        original_width <= 800
        -------
        |     |
        |     |
        |     | original_height > 560
        |     |
        -------

    **Case 4 both height and width overflows image space in window

        original_width > 800
        ------------------
        |                |
        |                |  original_height > 560
        |                |
        |                |
        ------------------

    In each case, x and y is resized with ratio to not mess an image
    """

    # image size
    original_width, original_height = image.size
    # app window size
    width, height = 800, 560

    #**Case 1: if image fits window
    if original_width <= 800 and original_height <= 560:
        # directly return original image
        return image

    #**Case 2: only x overflows
    if original_width > 800 and original_height <= 560:
        new_width = width
        new_height = int(original_height * float(width) / float(original_width))

    #**Case 3: only y overflows
    if original_width <= 800 and original_height > 560:
        new_height = height
        new_width = int(original_width * float(height) / float(original_height))

    #**Case 4: both x and y overflows
    if original_width > 800 and original_height > 560:
        # step 1 resize x
        step1_width = width
        step1_height = int(original_height * float(width) / float(original_width))

        # resizing x in step 1
        resized_step1 = image.resize((step1_width, step1_height), Image.ANTIALIAS)

        # if y still overflows y of window after resizing x, function resizes y too
        if step1_height > 560:
            # step 2 resize y if it still overflows window
            new_height = height
            new_width = int(step1_width * float(height) / float(step1_height))

            # resize step 2
            resized_final = resized_step1.resize((new_width, new_height), Image.ANTIALIAS)

            # return resized image
            return resized_final
        
        return resized_step1

    # resize and return resized image if Case 2 or 3 is satisfied
    resized = image.resize((new_width, new_height), Image.ANTIALIAS)
    return resized


def get_first_image():
    global current_image
    
    image_file = check_and_resize(Image.open(image_filenames[0]))
    current_image = ImageTk.PhotoImage(image_file)
    

def check_buttons():
    """ Check buttons if it's possible to move forward or back"""
    global button_back
    global button_forward

    if current_index == 0:
        button_back["state"] = DISABLED
    else:
        button_back["state"] = NORMAL

    if current_index == image_filenames.index(image_filenames[-1]):
        button_forward["state"] = DISABLED
    else:
        button_forward["state"] = NORMAL


def view_another_image(direction):
    global image_widget
    global image_file
    global current_index
    global current_image

    if direction == "forward":
        current_index += 1
    else:
        current_index -= 1

    image_widget.place_forget()

    processed_image_file = check_and_resize(Image.open(image_filenames[current_index]))
    final_result = ImageTk.PhotoImage(processed_image_file)
    current_image = final_result
    
    image_widget = Label(root, image=current_image)

    image_widget.place(y=0, width=800, height=560)

    check_buttons()


# Get all image filenames
image_filenames = scan_for_images()
current_index = 0
current_image = None

# create root window
root = Tk()
root.geometry("800x600")
root.title("Image Viewer")
root.resizable(False, False)

#---define widgets
# forward and back buttons
button_forward = Button(root, text=">>", command=lambda : view_another_image("forward"))
button_back = Button(root, text="<<", command=lambda : view_another_image("back"), state=DISABLED)

# image (label)
if image_filenames:
    # if image(s) found image is displayed and buttons are checked  
    get_first_image()
    check_buttons()
    image_widget = Label(root, image=current_image)
else:
    # else, buttons are disabled and "Images not found" message is displayed
    # display message
    image_widget = Label(root, text="Images not found")
    
    # disable buttons (back is already disabled)
    button_forward["state"] = DISABLED

#---place widgets
button_forward.place(x=400, y=560, width=50, height=40)
button_back.place(x=350, y=560, width=50, height=40)
image_widget.place(y=0, width=800, height=560)

root.mainloop()