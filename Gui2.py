#Gestione GUI
import tkinter as tk
from tkinter import filedialog,PhotoImage,Canvas,INSERT
from PIL import Image, ImageTk
import os
import sys
import locale
import logging
try:
    import tkinter as tk # Python 3.x
    import tkinter.scrolledtext as ScrolledText
except ImportError:
    import Tkinter as tk # Python 2.x
    import ScrolledText

dir_path = os.path.dirname(os.path.realpath(__file__))

def choose_directory():
    directory_path = filedialog.askdirectory()
    if directory_path:
        entry_var.set(directory_path)

def save_info():
    global datasetG2
    global SogliaCropG2
    global CHaddG2
    global FinalClosingG2
    global ProtrusG2
    global EdgesG2
    datasetG2 = dataset_entry.get()
    SogliaCropG2 = int(sogliaCrop_entry.get()) #Soglia per il crop del volume iniziale
    CHaddG2 = int(CHadd_entry.get())
    FinalClosingG2 = int(FinalClosing_entry.get())
    ProtrusG2=int(Protrus_entry.get())#Con ampiezza inferiore (3 o 4) peggiora
    EdgesG2=int(Edges_entry.get()) #(4 forse e' troppo)

    
    root.destroy()


def Gui(dataset, SogliaCrop, CHadd, FinalClosing, Protrus, Edges):
	
	global root
	root = tk.Tk()
	root.configure(bg="#FFFFFF")
	root.title("MEDIA – METODICHE DIAGNOSTICHE AD ALTA EFFICIENZA PER IL PAZIENTE OSTEO-ARTICOLARE")

	# Constructing the first frame, frame1
	frame1 = tk.LabelFrame(root, bg="#FFFFFF",
	                    fg="#FFFFFF", bd=0,pady=5)
	frame1.grid(row=0, column=0)
	frame2 = tk.LabelFrame(root, bg="#DDFF99",
	                    fg="#DDFF99",bd=0)
	frame2.grid(row=1, column=0)
	frame3 = tk.LabelFrame(root, bg="#FFFFFF",
	                    fg="#FFFFFF",bd=0)
	frame3.grid(row=2, column=0)


	

	
	if sys.platform == "linux" or sys.platform == "linux2":
	    # linux
	    media_img = Image.open("media.png")
	elif sys.platform == "win32":
	    # Windows...
	    media_img = Image.open(dir_path + "\\media.png")
	    
	
	media_img = media_img.resize((int(media_img.size[0]/2), int(media_img.size[1]/2)), Image.LANCZOS)
	media_imgI = media_img.resize((int(media_img.size[0]/3), int(media_img.size[1]/3)), Image.LANCZOS)
	media_img = ImageTk.PhotoImage(media_img)
	media_imgI = ImageTk.PhotoImage(media_imgI)
	root.wm_iconphoto(True, media_imgI)
	media_imgL = tk.Label(frame1, image=media_img, bg="#FFFFFF",border=0,highlightthickness=0,borderwidth=0)
	media_imgL.grid(row=0,column=0)

	global entry_var
	entry_var = tk.StringVar(frame2,value=dataset)

	global dataset_entry
	dataset_entry = tk.Entry(frame2, textvariable=entry_var)
	dataset_entry.grid(row=1, column=2,sticky = "sw", padx=5)
	buttonData = tk.Button(frame2, text="DICOM Directory", command=choose_directory, bg="#B0E600",anchor="e",justify="right")
	buttonData.grid(row=1, column=1,sticky = "sw", padx=5)

	global sogliaCrop_entry
	sogliaCrop_l = tk.Label(frame2, text="Intensity Threshold:",fg = "#5A5A5A", bg="#DDFF99",anchor="e",justify="right")
	sogliaCrop_l.grid(row=2, column=1,sticky = "sw", padx=5)
	sogliaCrop_entry = tk.Entry(frame2)
	sogliaCrop_entry.insert(600, str(SogliaCrop))
	sogliaCrop_entry.grid(row=2, column=2,sticky = "sw", padx=5)

	global CHadd_entry
	CHadd_l = tk.Label(frame2, text="Convex Hull Dilation:",fg = "#5A5A5A", bg="#DDFF99",anchor="e",justify="right")
	CHadd_l.grid(row=3, column=1, sticky = "sw", padx=5)
	CHadd_entry = tk.Entry(frame2)
	CHadd_entry.insert(6, str(CHadd))
	CHadd_entry.grid(row=3, column=2,sticky = "sw", padx=5)
	CHadd_l = tk.Label(frame2, text="",font=("Arial", 4),bg="#DDFF99")
	CHadd_l.grid(row=4, column=1)

	global FinalClosing_entry
	FinalClosing_l = tk.Label(frame2, text="Final Closing:", fg = "#5A5A5A", bg="#DDFF99",anchor="e",justify="right")
	FinalClosing_l.grid(row=1, column=3,sticky = "sw",padx=5)
	slider_var1 = tk.IntVar()
	slider_var1.set(FinalClosing)
	FinalClosing_entry = tk.Scale(frame2,fg = "#5A5A5A",bg="#DDFF99" ,from_=1, to=20, resolution=1,
	                    border=0,highlightthickness=0,borderwidth=0, 
	                    variable=slider_var1, orient=tk.HORIZONTAL)
	FinalClosing_entry.grid(row=1, column=4,sticky = "w",padx=5)

	global Protrus_entry
	Protrus_l = tk.Label(frame2, text="Protrusion Removal:",fg = "#5A5A5A", bg="#DDFF99",anchor="e",justify="right")
	Protrus_l.grid(row=2, column=3,sticky = "sw",padx=5)
	slider_var1 = tk.IntVar()
	slider_var1.set(Protrus)
	Protrus_entry =tk.Scale(frame2,fg = "#5A5A5A",bg="#DDFF99" ,from_=1, to=10, resolution=1,
	                    border=0,highlightthickness=0,borderwidth=0, 
	                    variable=slider_var1, orient=tk.HORIZONTAL)

	Protrus_entry.grid(row=2, column=4,sticky = "w",padx=5)

	global Edges_entry
	Edges_l = tk.Label(frame2, text="Final Dilation:", fg = "#5A5A5A", bg="#DDFF99",anchor="e",justify="right")
	Edges_l.grid(row=3, column=3,sticky = "sw",padx=5)
	slider_var = tk.IntVar()
	slider_var.set(Edges)
	Edges_entry =tk.Scale(frame2,fg = "#5A5A5A", bg="#DDFF99" ,from_=1, to=10, resolution=1,
	                    border=0,highlightthickness=0,borderwidth=0, 
	                    variable=slider_var, orient=tk.HORIZONTAL)
	Edges_entry.grid(row=3, column=4,sticky = "w",padx=5)


	submit_button = tk.Button(frame3, text="Ok", bg = "#B0E600", command=save_info)
	submit_button.grid(row=0, column=2, padx=15, pady=15)

	exit_button = tk.Button(frame3, text="Exit", bg = "#FB9764", command=exit)
	exit_button.grid(row=0, column=0, padx=15, pady=15)

	root.bind("<Return>", (lambda event: save_info()))
	root.resizable(False, False)
	root.mainloop()

	return datasetG2, SogliaCropG2, CHaddG2, FinalClosingG2, ProtrusG2, EdgesG2

def save_info2():
    global ris
    ris=True

    esecuzione = os.popen("taskkill /IM SlicerApp-real.exe /F")
    risultato = esecuzione.read()

    rootR.destroy()

def pr(name,data1):
	#global name, data1
	#STL save...
	global ris
	ris = False

	data1.save(dir_path + "\\Print\\"+name)
	rootR.destroy()

def GuiFin(name,data1):
	global rootR
	rootR = tk.Tk()
	rootR.configure(bg="#FFFFFF")
	rootR.title("MEDIA")

	# Constructing the first frame, frame1
	frame1 = tk.LabelFrame(rootR, bg="#FFFFFF",
	                    fg="#FFFFFF", bd=0,pady=5)
	frame1.grid(row=0, column=0)
	frame2 = tk.LabelFrame(rootR, bg="#FFFFFF",
	                    fg="#FFFFFF",bd=0)
	frame2.grid(row=1, column=0)
	frame3 = tk.LabelFrame(rootR, bg="#FFFFFF",
	                    fg="#FFFFFF",bd=0)
	frame3.grid(row=2, column=0)

	if sys.platform == "linux" or sys.platform == "linux2":
	    # linux
	    media_img = Image.open("media.png")
	elif sys.platform == "win32":
	    # Windows...
	    media_img = Image.open(dir_path + "\\media.png")

	media_img = media_img.resize((int(media_img.size[0]/6), int(media_img.size[1]/6)), Image.LANCZOS)
	media_imgI = media_img.resize((int(media_img.size[0]/3), int(media_img.size[1]/3)), Image.LANCZOS)
	media_img = ImageTk.PhotoImage(media_img)
	media_imgI = ImageTk.PhotoImage(media_imgI)
	rootR.wm_iconphoto(True, media_imgI)
	media_imgL = tk.Label(frame1, image=media_img, bg="#FFFFFF",border=0,highlightthickness=0,borderwidth=0)
	media_imgL.grid(row=0,column=0)


	global ris_entry,ris
	ris_l = tk.Label(frame2, text="Would you like to continue with another segmentation?",fg = "#000000", bg="#FFFFFF")
	ris_l.grid(row=3, column=1, padx=5, pady=5)

	submit_button = tk.Button(frame3, text="Continue", bg="#B0E600", command=save_info2)
	submit_button.grid(row=0, column=3, padx=15, pady=15)
	exit_button = tk.Button(frame3, text="Exit", bg = "#FB9764", command=exit)
	exit_button.grid(row=0, column=2, padx=15, pady=15)
	print_button = tk.Button(frame3, text="Print STL", bg = "#FB5000", command= lambda: pr(name,data1))
	print_button.grid(row=0, column=4, padx=15, pady=15)

	rootR.bind("<Return>", (lambda event: save_info2()))
	rootR.resizable(False, False)
	rootR.mainloop()

	return ris

def error():
    rootE.destroy()

def GuiError():
	global rootE
	rootE = tk.Tk()
	rootE.configure(bg="#FFFFFF")
	rootE.title("ERROR")

	# Constructing the first frame, frame1
	frame1 = tk.LabelFrame(rootE, bg="#FFFFFF",
	                    fg="#FFFFFF", bd=0,pady=5)
	frame1.grid(row=0, column=0)
	frame2 = tk.LabelFrame(rootE, bg="#FFFFFF",
	                    fg="#FFFFFF",bd=0)
	frame2.grid(row=1, column=0)
	frame3 = tk.LabelFrame(rootE, bg="#FFFFFF",
	                    fg="#FFFFFF",bd=0)
	frame3.grid(row=2, column=0)

	if sys.platform == "linux" or sys.platform == "linux2":
	    # linux
	    media_img = Image.open("error..png")
	elif sys.platform == "win32":
	    # Windows...
	    media_img = Image.open(dir_path + "\\error.png")
		
	media_img = media_img.resize((int(media_img.size[0]/6), int(media_img.size[1]/6)), Image.LANCZOS)
	media_imgI = media_img.resize((int(media_img.size[0]/3), int(media_img.size[1]/3)), Image.LANCZOS)
	media_img = ImageTk.PhotoImage(media_img)
	media_imgI = ImageTk.PhotoImage(media_imgI)
	rootE.wm_iconphoto(True, media_imgI)
	media_imgL = tk.Label(frame1, image=media_img, bg="#FFFFFF",border=0,highlightthickness=0,borderwidth=0)
	media_imgL.grid(row=0,column=0)

	ris_l = tk.Label(frame2, text="File names information is empty. Cannot read series.\nPlease try again with a DICOM directory.",fg = "#000000", bg="#FFFFFF")
	ris_l.grid(row=3, column=1, padx=5, pady=5)

	exit_button = tk.Button(frame3, text="Exit", bg = "#FB9764",command=error)
	exit_button.grid(row=0, column=2, padx=15, pady=15)

	rootE.bind("<Return>", (lambda event: error()))
	rootE.resizable(False, False)
	rootE.mainloop()



# class WidgetLogger(logging.Handler):
#     def __init__(self, widget):
#         logging.Handler.__init__(self)
#         self.widget = widget

#     def emit(self, record):
#         # Append message (record) to the widget
#         self.widget.insert(INSERT, record + '\n')

# class myGUI(tk.Frame):

#     # This class defines the graphical user interface 
    
#     def __init__(self, parent, *args, **kwargs):
#         tk.Frame.__init__(self, parent, *args, **kwargs)
#         self.root = parent
#         self.build_gui()
        
#     def build_gui(self):                    
#         # Build GUI
#         self.root.title('TEST')
#         self.root.option_add('*tearOff', 'FALSE')
#         self.grid(column=0, row=0, sticky='ew')
#         self.grid_columnconfigure(0, weight=1, uniform='a')
#         self.grid_columnconfigure(1, weight=1, uniform='a')
#         self.grid_columnconfigure(2, weight=1, uniform='a')
#         self.grid_columnconfigure(3, weight=1, uniform='a')
        
#         # Add text widget to display logging info
#         st = ScrolledText.ScrolledText(self, state='disabled')
#         st.configure(font='TkFixedFont')
#         st.grid(column=0, row=1, sticky='w', columnspan=4)

#         # Create textLogger
#         text_handler = WidgetLogger(st)
        
#         # Logging configuration
#         logging.basicConfig(filename='test.log',
#             level=logging.INFO, 
#             format='%(asctime)s - %(levelname)s - %(message)s')        
        
#         # Add the handler to logger
#         logger = logging.getLogger()        
#         logger.addHandler(text_handler)
              
# def worker(msg):
#     # Skeleton worker function, runs in separate thread (see below)   
#     while True:
#         # Report time / date at 2-second intervals
#         #time.sleep(2)
#         #timeStr = time.asctime()
#         #msg = 'Current time: ' + timeStr
#         #print(msg)
#         logging.info(msg)
        
# def log_info():
    
#     rootL = tk.Tk()
#     myGUI(rootL)
#     rootL.mainloop()