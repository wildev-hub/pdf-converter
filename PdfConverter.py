import os
import datetime
from pdf2image import convert_from_path
from PIL import Image
from tkinter import Tk, filedialog, simpledialog, messagebox

def main():
    # === HIDE ROOT WINDOW ===
    root = Tk()
    root.withdraw()

    # === STEP 1: SELECT PDF FILE ===
    pdf_path = filedialog.askopenfilename(
        title="Select a PDF file",
        filetypes=[("PDF Files", "*.pdf")]
    )
    if not pdf_path:
        messagebox.showinfo("Cancelled", "No file selected.")
        return

    # === STEP 2: ASK COMPRESSION QUALITY ===
    quality = simpledialog.askinteger(
        "JPEG Quality",
        "Enter compression quality (1 = smallest, 100 = best quality):",
        minvalue=1,
        maxvalue=100,
        initialvalue=70
    )
    if not quality:
        messagebox.showinfo("Cancelled", "No quality selected.")
        return

    # === STEP 3: CREATE UNIQUE OUTPUT FOLDER ===
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    base_folder = os.path.dirname(pdf_path)
    folder_name = f"output_images_{timestamp}"
    output_folder = os.path.join(base_folder, folder_name)
    os.makedirs(output_folder, exist_ok=True)

    # === CONVERT PDF TO JPEG ===
    print(f"Converting '{pdf_path}' to JPEG images...")
    images = convert_from_path(pdf_path)

    for i, img in enumerate(images):
        jpg_path = os.path.join(output_folder, f"page_{i+1}.jpg")
        img.save(jpg_path, "JPEG")
        print(f"Saved: {jpg_path}")

    # === COMPRESS EACH JPEG ===
    print("\nCompressing images...")
    for file in os.listdir(output_folder):
        if file.endswith(".jpg") and not file.endswith("_compressed.jpg"):
            img_path = os.path.join(output_folder, file)
            img = Image.open(img_path)
            compressed_path = os.path.join(output_folder, file.replace(".jpg", "_compressed.jpg"))
            img.save(compressed_path, "JPEG", optimize=True, quality=quality)
            print(f"Compressed: {compressed_path}")

    # === DONE ===
    messagebox.showinfo("Done!", f"✅ Conversion complete!\nImages saved to:\n{output_folder}")
    print(f"\nAll images saved safely to: {output_folder}")

if __name__ == "__main__":
    main()
