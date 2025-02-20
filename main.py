from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk, ImageDraw, ImageFont, UnidentifiedImageError 
import glob, os, shutil

BACKGROUND_COLOR = "#B1DDC6"
HEIGHT = 1080
WIDTH = 1920


def upload_image():
 
    try:
        file_path = askopenfilename()
        img= Image.open(file_path)
        img_width, img_height = img.size 

        if img_height > HEIGHT or img_width > WIDTH:
            while img_height > HEIGHT or img_width > WIDTH:
                img_height *= .99
                img_width *= .99

            img.resize(int(img_height), int(img_width))
            messagebox.showinfo(title="Warning!", 
                message="The uploaded image is larger than the canvas, it will be resized.")
        


        tk_image= ImageTk.PhotoImage(img)
        canvas.image = tk_image
        canvas.create_image(250, 250, image=tk_image, anchor="center")
        canvas.file_path = file_path

    except UnidentifiedImageError:
        messagebox.showinfo(title="Upload Error", 
            message="Image could not be read.")
    

def create_watermark():
    if not hasattr(canvas, "file_path"):
        messagebox.showerror("Error", "No image uploaded!")
        return

    watermark_text = "©VictoriaMunteanu"

    # Open image and ensure it's in RGBA mode
    img = Image.open(canvas.file_path).convert("RGBA")

    # Create a transparent layer
    txt_layer = Image.new("RGBA", img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)

    # Dynamically adjust font size based on image width
    font_size = max(40, img.width // 20)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    # Get text bounding box (accurate for newer Pillow versions)
    bbox = draw.textbbox((0, 0), watermark_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Calculate center position
    text_x = (img.width - text_width) // 2
    text_y = (img.height - text_height) // 2
    text_position = (text_x, text_y)

    # Set watermark text color (fully visible white)
    text_color = (255, 255, 255, 255)

    # Draw text on transparent layer
    draw.text(text_position, watermark_text, font=font, fill=text_color)

    # Merge layers
    watermarked = Image.alpha_composite(img, txt_layer).convert("RGB")

    # Convert to Tkinter-compatible image
    tk_watermark = ImageTk.PhotoImage(watermarked)

    # Update canvas
    canvas.create_image(canvas.winfo_width() // 2, canvas.winfo_height() // 2, image=tk_watermark, anchor="center")
    canvas.image = tk_watermark  # Prevent garbage collection



def save_image(save_dir="Downloads"):
    if not hasattr(canvas, "image"):
        messagebox.showerror("Error", "No image to save!")
        return

    os.makedirs(save_dir, exist_ok=True)
    saved_path = os.path.join(save_dir, "watermarked_image.jpg")

    # Save the watermarked image
    img = Image.open(canvas.file_path).convert("RGBA")

     # Convert RGBA to RGB (removes transparency)
    img = img.convert("RGB")


    # Save the image directly instead of copying
    img.save(saved_path, "JPEG")

    messagebox.showinfo("Success", f"Image saved to {saved_path}")
    print(f"Image saved to {saved_path}")


""".................................UI Setup ......................................"""

#ui setup 
window = Tk()
window.title("Watermark")
window.config(padx=100, pady=100, bg=BACKGROUND_COLOR)
# window.geometry(WIDTH, HEIGHT)


canvas = Canvas(window, width=500, height=500, bg="white")
canvas.grid(column=0, row=0, columnspan=2)

""".................................Buttons ......................................"""

upload_button = Button(text="Upload Image", bg="blue",command= lambda:upload_image(), fg="white")
upload_button.grid(column=0, row=1)

watermark_button = Button(text="Add Watermark", bg="pink",command=create_watermark,  fg="black")
watermark_button.grid(column=1, row=1)

save_button = Button(text="Save Image", bg="green",command=save_image, fg="white")
save_button.grid(column=0, row=2)




window.mainloop()


