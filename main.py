from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont
import glob, os, shutil

BACKGROUND_COLOR = "#B1DDC6"
file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])



def upload_image():
    

    if file_path:

        img = Image.open(file_path)
        tk_image= ImageTk.PhotoImage(img)
        canvas.create_image(250, 250, image=tk_image)
        canvas.image = tk_image
        canvas.file_path = file_path

        
def save_image(file_path, save_dir="Downloads"):
    
    os.makedirs(save_dir, exist_ok=True)
    saved_path = os.path.join(save_dir, os.path.basename(file_path))
    shutil.copy(file_path, saved_path)

    print(f"Image saved to {saved_path}")


    

def create_watermark():
    watermark_text = "©VictoriaMunteanu"
    img = Image.open(canvas.file_path).convert("RGBA")

    #create a transparent layer 

    txt_layer = Image.new("RGBA", img.size)
    draw = ImageDraw.Draw(txt_layer)

    # load a font 

    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()


    #set the position and text color 

    text_position = (img.width - 200, img.height- 100)
    text_color = (255, 255, 255, 128)
    draw.text(text_position, watermark_text, font=font, fill=text_color)


    watermarked = Image.alpha_composite(img.convert("RGBA"), txt_layer)
    watermarked = watermarked.convert("RGB")

    #update image on canvas 

    tk_watermark = ImageTk.PhotoImage(watermarked)
    canvas.create_image(250, 50, image=tk_watermark)
    canvas.image = tk_watermark







""".................................UI Setup ......................................"""

#ui setup 
window = Tk()
window.title("Watermark")
window.config(padx=100, pady=100, bg=BACKGROUND_COLOR)


canvas = Canvas(width=500, height=500, bg="white")
canvas.grid(column=0, row=0, columnspan=2)

""".................................Buttons ......................................"""

upload_button = Button(text="Upload Image", bg="blue",command=upload_image, fg="white")
upload_button.grid(column=0, row=1)

watermark_button = Button(text="Add Watermark", bg="pink",command=create_watermark,  fg="black")
watermark_button.grid(column=1, row=1)

save_button = Button(text="Save Image", bg="green",command=save_image, fg="white")
save_button.grid(column=0, row=2)




window.mainloop()


