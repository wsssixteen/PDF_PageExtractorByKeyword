'''
Copyright (c) 2023, wsssixteen
All rights reserved.

This source code is licensed under the BSD 3-Clause license found in the
LICENSE file in the root directory of this source tree.'''


import PyPDF2
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter.filedialog import askopenfilename
import os

# Function to search, filter & save PDF file
def search_and_save_pdf(input_file, output_file, keyword, progress_var):
    print(f"Received input file: {input_file}")
    print(f"Received output file: {output_file}")
    print(f"Received keyword file: {keyword}")
    # Open the input PDF file in read binary mode
    with open(input_file, 'rb') as input_pdf:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(input_pdf)

        # Check if PDF needs password to access
        if pdf_reader.is_encrypted:
            password = simpledialog.askstring("Password", "The file requires a password:", show='*')
            if password is None:
                return 3
            else: 
                result = pdf_reader.decrypt(password)
                # Check decrypt result
                if result == 0:
                    return 2
                else: 
                    # Show progress bar after confirmation & proceed
                    progress_bar.pack()

        # Create a PDF writer object
        pdf_writer = PyPDF2.PdfWriter()

        # Boolean to check if keyword exists in file
        convert_result = 0

        num_pages = len(pdf_reader.pages)

        # Iterate over the pages of the input PDF
        for page_num in range(num_pages): 
            # Get the current page
            page = pdf_reader.pages[page_num]
            # Extract the text from the current page
            text = page.extract_text()
            # Check if the keyword is in the text
            if keyword.lower() in text.lower():
                convert_result = 1
                # If the keyword is found, add the page to the output PDF
                pdf_writer.add_page(page)
            # Progress bar
            progress = (page_num + 1) / num_pages * 100
            progress_var.set(progress)
            root.update_idletasks()
        
        if convert_result == 1:
            # Open the output PDF file in write binary mode
            with open(output_file, 'wb') as output_pdf:
                print(f"Saving output file to: {output_file}")
                # Write the output PDF
                pdf_writer.write(output_pdf)

    return convert_result

# End of function to search, filter & save
# =========================================

def on_buttonSearch_click():
    # Get the text form the entry widget
    file_path = askopenfilename()

    entry.delete(0, tk.END)
    entry.insert(0, file_path)

def on_buttonConvert_click():
    if not entry2.get():
        message_label.config(text="Enter a keyword!")
        return

    # Append text to the file path
    file_path, ext = os.path.splitext(entry.get())
    file_path_filtered = file_path + "_Filtered" + ext
    file_path = file_path + ext

    # Check if the file already exists
    if os.path.exists(file_path_filtered):
        # If it does, change the naming scheme
        counter = 2
        while os.path.exists(file_path_filtered):
            file_path_filtered = f"{file_path}_Filtered_{counter}{ext}"
            counter += 1

    # Hide message label to make space for progress bar
    message_label.pack_forget()

    convert_result = search_and_save_pdf(file_path,file_path_filtered,entry2.get(),progress_var)
    print(f'convert_result returns: {convert_result}')

    # Hide progress bar & replace it back with message label
    progress_bar.pack_forget()
    message_label.pack()

    # Update the text property of the message label 
    if convert_result == 0:
        message_label.config(text="Keyword not found in file!")
    elif convert_result == 1:
        message_label.config(text="New file created successfully!")
    elif convert_result == 2:
        message_label.config(text="Password was not accepted!")
    elif convert_result == 3:
        message_label.config(text="User cancelled inserting password!")


# Create the main window
root = tk.Tk()
root.geometry("425x225")

root.title("PDF Extractor: Extract pages based on keyword")
root.iconbitmap(r'C:\Users\vice4\Desktop\NH_logo.ico')

frame = tk.Frame(root)
frame.pack(pady=10)

# Create a label widget
label = tk.Label(frame, text="Enter the file path below or use the button:")
label.pack(pady=0)

#Create an entry widget
entry = tk.Entry(frame, width=50)
entry.pack(pady=5)

#Create a button to choose file
chooseFilebutton = tk.Button(frame, text="Choose file", command=on_buttonSearch_click)
chooseFilebutton.pack()

# Create a label widget
label2 = tk.Label(root, text="Enter the keyword to filter below:")
label2.pack(pady=5)

entry2 = tk.Entry(root, width=50)
entry2.pack(padx=5)

#Create a button to convert file
convertButton = tk.Button(root, text="Convert File", command=on_buttonConvert_click)
convertButton.pack(pady=5)
# Bind <Return>(Keyboard Enter) to the button
convertButton.bind("<Return>", lambda event: convertButton.invoke())

feedbackFrame = tk.Frame(root)
feedbackFrame.pack()

# Create a label widget for the feedback message
message_label = tk.Label(feedbackFrame, text="")
message_label.pack()

# Create a progress bar
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(feedbackFrame, variable=progress_var, maximum=100)

frame3 = tk.Frame(root)
frame3.pack()

label3 = tk.Label(frame3, text="©92&97")
label3.pack(side=tk.RIGHT)


#run the main loop
root.mainloop()

# End of GUI