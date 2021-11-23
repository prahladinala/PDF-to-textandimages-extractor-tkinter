from tkinter import *
import PyPDF2
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile
from functions import display_logo, display_textbox, extract_images, display_icon, display_images, resize_image

page_contents = []
all_images = []
img_idx = [0]
displayed_img = []

def left_arrow(all_images, current_img, what_text):
    # Restrict the number of clicks to number of images availabe
    if img_idx[-1] >= 1:
        new_idx = img_idx[-1] - 1
        img_idx.pop()
        img_idx.append(new_idx)
        if displayed_img:
            displayed_img[-1].grid_forget()
            displayed_img.pop()
        new_img = all_images[img_idx[-1]]
        current_img = display_images(new_img)
        displayed_img.append(current_img)
        what_text.set("image " + str(img_idx[-1] + 1) + " out of " + str(len(all_images)))

    elif img_idx == -1:
        print("index out of range")
        if displayed_img:
            displayed_img[-1].grid_forget()
            displayed_img.pop()

def right_arrow(all_images, current_img, what_text):
    # Restrict the number of clicks to number of images availabe
    if img_idx[-1] < len(all_images) -1:
        new_idx = img_idx[-1] +1
        img_idx.pop()
        img_idx.append(new_idx)
        if displayed_img:
            displayed_img[-1].grid_forget()
            displayed_img.pop()
        new_img = all_images[img_idx[-1]]
        current_img = display_images(new_img)
        displayed_img.append(current_img)
        what_text.set("image " + str(img_idx[-1] + 1) + " out of " + str(len(all_images)))

    elif img_idx == -1:
        print("index out of range")
        if displayed_img:
            displayed_img[-1].grid_forget()
            displayed_img.pop()


def copy_text(content):
    # making clipboard clear
    root.clipboard_clear()

    # adding content to clipboard
    root.clipboard_append(content[-1])
    # -1 to select last file we selected

def save_all(images):
    # counter to differentiate image names > represents each of the images
    counter = 1
    for i in images:
        # CONVERT CMYK Images to RGB
        if i.mode != "RGB":
            i = i.convert("RGB")
        i.save("img" + str(counter) + ".png", format="png")
        counter += 1

def save_image(i):
    # CONVERT CMYK Images to RGB
    if i.mode != "RGB":
        i = i.convert("RGB")
    i.save("img.png", format="png")

# START WITH root
root = Tk()
root.geometry('+%d+%d'%(350,10)) #place GUI at x=350, y=10

# HEADER AREA - LOGO AND BROWSE BUTTON
header = Frame(root, width=800, height=175, bg="white")
header.grid(columnspan=3, rowspan=2, row=0)

# MAIN CONTENT AREA - TEXT AND IMAGE EXTRACTION
main_content = Frame(root, width=800, height=250, bg="#20bebe")
main_content.grid(columnspan=3, rowspan=2, row=4)

# OPEN FILE FUNCTION
def open_file():
    # CLEAR LIST 
    for i in img_idx:
        img_idx.pop()
    img_idx.append(0)

    # changing button text
    browse_text.set("Loading...")
    file = askopenfile(parent=root, mode='rb', filetypes=[("Pdf file", "*.pdf")])
    if file:
        read_pdf = PyPDF2.PdfFileReader(file)
        page = read_pdf.getPage(0)
        page_content = page.extractText()
        #page_content = page_content.encode('cp1252')
        page_content = page_content.replace('\u2122', "'")

        # GETTING ALL PAGE CONTENTS > TEXT
        page_contents.append(page_content)

        if displayed_img:
            displayed_img[-1].grid_forget()
            displayed_img.pop()
        
        for i in range(0, len(all_images)):
            all_images.pop()

        # GET IMAGES
        images = extract_images(page)

        for i in images:
            all_images.append(i)

        img = images[img_idx[-1]]
        
        current_image = display_images(img)
        displayed_img.append(current_image)

        #show text box on row 4 col 0
        display_textbox(page_content, 4, 0, root)

        #reset the button text back to Browse
        browse_text.set("Browse")

        # DISPLAY SECTIONS ONLY IS SOME FILE IS SELECTED
        # IMAGE PAGINATION SECTION
        img_menu = Frame(root, width=800, height=60)
        img_menu.grid(columnspan=3, rowspan=1, row=2)

        # TEXT WIDGET > pagination text
        # variable pagination text
        what_text = StringVar()
        what_img = Label(root, textvariable=what_text, font=("shanti", 10))
        what_text.set("image " + str(img_idx[-1] + 1) + " out of " + str(len(all_images)))
        what_img.grid(row=2, column=1)

        # IMAGE BUTTON
        # placing images as icons for buttons
        display_icon('arrow_l.png', 2, 0, E, lambda:left_arrow(all_images, current_image, what_text))
        display_icon('arrow_r.png', 2, 2, W, lambda:right_arrow(all_images, current_image, what_text))

        # SAVE IMAGE SECTION
        save_img = Frame(root, width=800, height=60, bg="#c8c8c8")
        save_img.grid(columnspan=3, rowspan=1, row=3)

        # BUTTONS WIDGET > for save image section
        copyText_btn = Button(root, text="copy text", command=lambda:copy_text(page_contents), font=('shanti', 10), height=1, width=15)
        saveAll_btn = Button(root, text="save all images", command=lambda:save_all(all_images), font=('shanti', 10), height=1, width=15)
        save_btn = Button(root, text="save image", command=lambda:save_image(all_images[img_idx[-1]]), font=('shanti', 10), height=1, width=15)

        # placing buttons on grid
        copyText_btn.grid(row=3, column=0)
        saveAll_btn.grid(row=3, column=1)
        save_btn.grid(row=3, column=2)

display_logo('logo.png', 0, 0)

# INSTRUCTIONS
instructions = Label(root, text="Select a PDF file", font=("Raleway", 10), bg="white")
# placing instructions on grid
instructions.grid(column=2, row=0, sticky=SE, padx=75, pady=5)

# BROWSER BUTTON
# variable for button text
browse_text = StringVar()
# Button
browse_btn = Button(root, textvariable=browse_text, command=lambda:open_file(), font=("Raleway",12), bg="#20bebe", fg="white", height=1, width=15)
# set browser text
browse_text.set("Browse")
# placing button to grid
browse_btn.grid(column=2, row=1, sticky=NE, padx=50)

root.mainloop()
# END WITH mainloop()

# ABOVE AND BELOW CODE WILL NOT APPEAR IN WINDOW