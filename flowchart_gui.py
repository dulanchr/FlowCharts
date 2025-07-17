import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from PIL import ImageTk, Image
from Converter import generate_flowchart_direct
import os
import sys
import tempfile

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class ModernFlowchartApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pseudocode to Flowchart Converter")
        self.root.geometry("1400x800")
        
        # Configure modern styling
        self.setup_styles()
        
        # Default settings
        self.font_size = 12
        self.font_path = resource_path("fonts/NotoSans-Regular.ttf")
        self.output_file = "flowchart.png"
        
        # Image viewing settings
        self.current_image = None
        self.original_image = None
        self.zoom_level = 1.0
        self.min_zoom = 0.1
        self.max_zoom = 5.0
        
        # Panning settings
        self.pan_start_x = 0
        self.pan_start_y = 0
        self.is_panning = False
        
        # Create UI elements
        self.create_widgets()
        
    def setup_styles(self):
        """Configure modern styling for the application"""
        # Configure root background
        self.root.configure(bg='#f8f9fa')
        
        # Configure ttk styles
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure custom styles
        style.configure('Title.TLabel', 
                       font=('Segoe UI', 16, 'bold'),
                       background='#f8f9fa',
                       foreground='#2c3e50')
        
        style.configure('Modern.TButton',
                       font=('Segoe UI', 10),
                       padding=(20, 10))
        
        style.configure('Primary.TButton',
                       font=('Segoe UI', 11, 'bold'),
                       padding=(25, 12))
        
        style.map('Primary.TButton',
                  background=[('active', '#3498db'),
                            ('pressed', '#2980b9')])
        
    def create_widgets(self):
        # Main container
        main_container = tk.Frame(self.root, bg='#f8f9fa')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_container, bg='#f8f9fa')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(header_frame, text="Pseudocode to Flowchart Converter", 
                               style='Title.TLabel')
        title_label.pack(side=tk.LEFT)
        
        # Control panel
        control_frame = tk.Frame(main_container, bg='#ffffff', relief=tk.RAISED, bd=1)
        control_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Inner control frame with padding
        inner_control = tk.Frame(control_frame, bg='#ffffff')
        inner_control.pack(fill=tk.X, padx=20, pady=15)
        
        # File operations section
        file_frame = tk.Frame(inner_control, bg='#ffffff')
        file_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        ttk.Button(file_frame, text="Load Example", 
                  command=self.load_example, style='Modern.TButton').pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(file_frame, text="Load File", 
                  command=self.load_from_file, style='Modern.TButton').pack(side=tk.LEFT, padx=(0, 10))
        
        # ttk.Button(file_frame, text="Save", 
        #           command=self.save_pseudocode, style='Modern.TButton').pack(side=tk.LEFT, padx=(0, 20))
        
        # Font size section
        font_frame = tk.Frame(inner_control, bg='#ffffff')
        font_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        tk.Label(font_frame, text="Font Size:", font=('Segoe UI', 10), 
                bg='#ffffff', fg='#2c3e50').pack(side=tk.LEFT, padx=(0, 5))
        
        self.font_size_var = tk.StringVar(value=str(self.font_size))
        font_spinbox = tk.Spinbox(font_frame, from_=8, to=24, textvariable=self.font_size_var, 
                                 width=4, font=('Segoe UI', 10))
        font_spinbox.pack(side=tk.LEFT, padx=(0, 20))
        
        # Generate button
        generate_btn = ttk.Button(inner_control, text="Generate Flowchart", 
                                 command=self.generate_flowchart, style='Primary.TButton')
        generate_btn.pack(side=tk.RIGHT)
        
        # Main content area with PanedWindow for resizable splitter
        content_frame = tk.Frame(main_container, bg='#f8f9fa')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create PanedWindow for resizable splitter
        self.paned_window = tk.PanedWindow(content_frame, orient=tk.HORIZONTAL, 
                                          sashrelief=tk.RAISED, sashwidth=5,
                                          bg='#e1e8ed', bd=0)
        self.paned_window.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Text input
        left_panel = tk.Frame(self.paned_window, bg='#ffffff', relief=tk.RAISED, bd=1)
        left_panel.pack(fill=tk.BOTH, expand=True)
        
        # Add to paned window
        self.paned_window.add(left_panel, minsize=300)
        
        # Text area header
        text_header = tk.Frame(left_panel, bg='#ecf0f1', height=40)
        text_header.pack(fill=tk.X)
        text_header.pack_propagate(False)
        
        tk.Label(text_header, text="Pseudocode Input", font=('Segoe UI', 12, 'bold'), 
                bg='#ecf0f1', fg='#2c3e50').pack(side=tk.LEFT, padx=15, pady=10)
        
        # Text input area with modern styling
        text_container = tk.Frame(left_panel, bg='#ffffff')
        text_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        self.text_area = scrolledtext.ScrolledText(text_container, 
                                                  wrap=tk.WORD, 
                                                  font=('Consolas', 11),
                                                  bg='#ffffff',
                                                  fg='#2c3e50',
                                                  relief=tk.FLAT,
                                                  bd=1,
                                                  selectbackground='#3498db',
                                                  selectforeground='#ffffff',
                                                  insertbackground='#2c3e50')
        self.text_area.pack(fill=tk.BOTH, expand=True)
        
        # Right panel - Image display
        right_panel = tk.Frame(self.paned_window, bg='#ffffff', relief=tk.RAISED, bd=1)
        right_panel.pack(fill=tk.BOTH, expand=True)
        
        # Add to paned window
        self.paned_window.add(right_panel, minsize=300)
        
        # Image header
        image_header = tk.Frame(right_panel, bg='#ecf0f1', height=40)
        image_header.pack(fill=tk.X)
        image_header.pack_propagate(False)
        
        tk.Label(image_header, text="Generated Flowchart", font=('Segoe UI', 12, 'bold'), 
                bg='#ecf0f1', fg='#2c3e50').pack(side=tk.LEFT, padx=15, pady=10)
        
        # Image controls
        image_controls = tk.Frame(image_header, bg='#ecf0f1')
        image_controls.pack(side=tk.RIGHT, padx=15, pady=5)
        
        # Zoom controls
        ttk.Button(image_controls, text="−", width=3, 
                  command=self.zoom_out).pack(side=tk.LEFT, padx=2)
        
        self.zoom_var = tk.StringVar(value="100%")
        zoom_label = tk.Label(image_controls, textvariable=self.zoom_var, 
                             font=('Segoe UI', 9), bg='#ecf0f1', fg='#2c3e50', width=6)
        zoom_label.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(image_controls, text="+", width=3, 
                  command=self.zoom_in).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(image_controls, text="Fit", width=4, 
                  command=self.fit_to_frame).pack(side=tk.LEFT, padx=(10, 2))
        
        ttk.Button(image_controls, text="1:1", width=4, 
                  command=self.actual_size).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(image_controls, text="Save Image", 
                  command=self.save_image).pack(side=tk.LEFT, padx=(10, 0))
        
        # Add keyboard shortcuts info
        shortcuts_btn = ttk.Button(image_controls, text="?", width=3, 
                                  command=self.show_shortcuts)
        shortcuts_btn.pack(side=tk.LEFT, padx=(5, 0))
        
        # Image display area with scrollbars
        self.image_frame = tk.Frame(right_panel, bg='#ffffff')
        self.image_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        image_container = tk.Frame(self.image_frame, bg='#ffffff')
        image_container.pack(fill=tk.BOTH, expand=True)
        
        # Create canvas with scrollbars
        self.canvas = tk.Canvas(image_container, bg='#f8f9fa', highlightthickness=0)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(image_container, orient=tk.VERTICAL, command=self.canvas.yview)
        h_scrollbar = ttk.Scrollbar(image_container, orient=tk.HORIZONTAL, command=self.canvas.xview)
        
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack scrollbars and canvas
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Placeholder for image
        self.image_label = tk.Label(self.canvas, 
                                   text="Flowchart will appear here\nafter generation",
                                   font=('Segoe UI', 14),
                                   bg='#f8f9fa',
                                   fg='#95a5a6',
                                   relief=tk.FLAT,
                                   bd=1)
        self.canvas.create_window(0, 0, window=self.image_label, anchor=tk.NW)
        
        # Bind mouse wheel for zooming (with Ctrl key)
        self.canvas.bind("<Control-MouseWheel>", self.on_ctrl_mousewheel)
        self.canvas.bind("<Control-Button-4>", self.on_ctrl_mousewheel)
        self.canvas.bind("<Control-Button-5>", self.on_ctrl_mousewheel)
        
        # Bind middle mouse button for panning
        self.canvas.bind("<Button-2>", self.start_pan)
        self.canvas.bind("<B2-Motion>", self.do_pan)
        self.canvas.bind("<ButtonRelease-2>", self.end_pan)
        
        # Bind regular mouse wheel for scrolling
        self.canvas.bind("<MouseWheel>", self.on_scroll)
        self.canvas.bind("<Button-4>", self.on_scroll)
        self.canvas.bind("<Button-5>", self.on_scroll)
        
        # Make canvas focusable for keyboard events
        self.canvas.bind("<Button-1>", lambda e: self.canvas.focus_set())
        
        # Bind keyboard shortcuts
        self.root.bind("<Control-equal>", lambda e: self.zoom_in())
        self.root.bind("<Control-plus>", lambda e: self.zoom_in())
        self.root.bind("<Control-minus>", lambda e: self.zoom_out())
        self.root.bind("<Control-0>", lambda e: self.fit_to_frame())
        self.root.bind("<Control-1>", lambda e: self.actual_size())
        
        # Status bar
        status_frame = tk.Frame(main_container, bg='#34495e', height=30)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        status_frame.pack_propagate(False)
        
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = tk.Label(status_frame, textvariable=self.status_var, 
                                  bg='#34495e', fg='#ecf0f1', 
                                  font=('Segoe UI', 9),
                                  anchor=tk.W)
        self.status_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=5)
        
        # Load initial example
        self.load_example()
        
        # Set initial paned window position (60% left, 40% right)
        self.root.after(100, lambda: self.paned_window.sash_place(0, int(self.root.winfo_width() * 0.6), 0))
        
    def load_example(self):
        example_code = """INPUT age
IF age >= 18 THEN
    IF age < 35 THEN
        OUTPUT "Associate"
    ELSE 
        IF age <= 55 THEN
            OUTPUT "Management"
        ELSE 
            OUTPUT "Too old"  
        ENDIF
    ENDIF
ELSE
    OUTPUT "Too young"
ENDIF"""
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, example_code)
        self.status_var.set("Example pseudocode loaded")
        
    def load_from_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Pseudocode File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(tk.END, content)
                    self.status_var.set(f"Loaded: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not load file:\n{str(e)}")
    
    def save_pseudocode(self):
        file_path = filedialog.asksaveasfilename(
            title="Save Pseudocode",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(self.text_area.get(1.0, tk.END))
                    self.status_var.set(f"Saved: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file:\n{str(e)}")
    
    def generate_flowchart(self):
        # Get pseudocode from text area
        pseudocode = self.text_area.get(1.0, tk.END).strip()
        
        if not pseudocode:
            messagebox.showwarning("Warning", "Please enter some pseudocode first.")
            return
        
        # Update status
        self.status_var.set("Generating flowchart...")
        self.root.update()
        
        # Create a temporary file
        temp_file = os.path.join(tempfile.gettempdir(), "temp_pseudocode.txt")
        try:
            with open(temp_file, 'w', encoding='utf-8') as file:
                file.write(pseudocode)
            
            # Get font size
            try:
                self.font_size = int(self.font_size_var.get())
            except ValueError:
                messagebox.showerror("Error", "Font size must be a number")
                return
                
            # Generate flowchart
            output_file = os.path.join(tempfile.gettempdir(), "temp_flowchart.png")
            generate_flowchart_direct(self.font_size, temp_file, output_file, self.font_path)
            
            # Display the image
            self.display_image(output_file)
            
            self.status_var.set("Flowchart generated successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not generate flowchart:\n{str(e)}")
            self.status_var.set("Error generating flowchart")
        finally:
            # Clean up temporary files
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def display_image(self, image_path):
        try:
            # Store the original image
            self.original_image = Image.open(image_path)
            self.current_image = self.original_image.copy()
            
            # Reset zoom level
            self.zoom_level = 1.0
            
            # Fit to frame initially
            self.fit_to_frame()
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not display image:\n{str(e)}")
            self.status_var.set("Error displaying image")
    
    def update_image_display(self):
        """Update the image display with current zoom level"""
        if self.original_image is None:
            return
            
        try:
            # Calculate new size based on zoom level
            original_width, original_height = self.original_image.size
            new_width = int(original_width * self.zoom_level)
            new_height = int(original_height * self.zoom_level)
            
            # Resize image
            resized_image = self.original_image.resize((new_width, new_height), Image.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(resized_image)
            
            # Update the label
            self.image_label.config(image=photo, text="", bg='#ffffff')
            self.image_label.image = photo  # Keep a reference
            
            # Update canvas scroll region
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            
            # Update zoom percentage display
            self.zoom_var.set(f"{int(self.zoom_level * 100)}%")
            
        except Exception as e:
            print(f"Error updating image display: {e}")
    
    def zoom_in(self):
        """Zoom in by 25%"""
        if self.original_image and self.zoom_level < self.max_zoom:
            self.zoom_level = min(self.zoom_level * 1.25, self.max_zoom)
            self.update_image_display()
    
    def zoom_out(self):
        """Zoom out by 25%"""
        if self.original_image and self.zoom_level > self.min_zoom:
            self.zoom_level = max(self.zoom_level * 0.8, self.min_zoom)
            self.update_image_display()
    
    def fit_to_frame(self):
        """Fit image to frame while maintaining aspect ratio"""
        if self.original_image is None:
            return
            
        # Update canvas to get current size
        self.canvas.update()
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width > 1 and canvas_height > 1:
            # Calculate scale factor
            img_width, img_height = self.original_image.size
            scale_w = canvas_width / img_width
            scale_h = canvas_height / img_height
            self.zoom_level = min(scale_w, scale_h) * 0.9  # 90% of frame size for padding
            
            # Ensure zoom level is within bounds
            self.zoom_level = max(self.min_zoom, min(self.zoom_level, self.max_zoom))
            
            self.update_image_display()
    
    def actual_size(self):
        """Show image at actual size (100%)"""
        if self.original_image:
            self.zoom_level = 1.0
            self.update_image_display()
    
    def on_ctrl_mousewheel(self, event):
        """Handle Ctrl+mouse wheel zooming"""
        if self.original_image is None:
            return
            
        # Determine zoom direction
        if event.delta > 0 or event.num == 4:  # Zoom in
            if self.zoom_level < self.max_zoom:
                self.zoom_level = min(self.zoom_level * 1.1, self.max_zoom)
                self.update_image_display()
        else:  # Zoom out
            if self.zoom_level > self.min_zoom:
                self.zoom_level = max(self.zoom_level * 0.9, self.min_zoom)
                self.update_image_display()
    
    def on_scroll(self, event):
        """Handle regular mouse wheel scrolling"""
        # Determine scroll direction and amount
        if event.delta > 0 or event.num == 4:
            delta = -1
        else:
            delta = 1
            
        # Scroll vertically by default, horizontally with Shift
        if event.state & 0x1:  # Shift key pressed
            self.canvas.xview_scroll(delta, "units")
        else:
            self.canvas.yview_scroll(delta, "units")
    
    def start_pan(self, event):
        """Start panning with middle mouse button"""
        self.canvas.config(cursor="fleur")
        self.pan_start_x = event.x
        self.pan_start_y = event.y
        self.is_panning = True
    
    def do_pan(self, event):
        """Perform panning with middle mouse button"""
        if self.is_panning:
            # Calculate movement
            dx = event.x - self.pan_start_x
            dy = event.y - self.pan_start_y
            
            # Get current scroll position
            x_view = self.canvas.canvasx(0)
            y_view = self.canvas.canvasy(0)
            
            # Update canvas view
            self.canvas.xview_moveto((x_view - dx) / self.canvas.winfo_width())
            self.canvas.yview_moveto((y_view - dy) / self.canvas.winfo_height())
            
            # Update pan start position
            self.pan_start_x = event.x
            self.pan_start_y = event.y
    
    def end_pan(self, event):
        """End panning with middle mouse button"""
        self.canvas.config(cursor="")
        self.is_panning = False
    
    def save_image(self):
        """Save the current flowchart image"""
        if self.original_image is None:
            messagebox.showwarning("Warning", "No flowchart to save. Please generate a flowchart first.")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Save Flowchart Image",
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg"),
                ("PDF files", "*.pdf"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                # Save the original image (not the zoomed version)
                self.original_image.save(file_path)
                self.status_var.set(f"Image saved: {os.path.basename(file_path)}")
                messagebox.showinfo("Success", f"Flowchart saved successfully to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save image:\n{str(e)}")
                self.status_var.set("Error saving image")
    
    def show_shortcuts(self):
        """Show keyboard shortcuts and mouse controls"""
        shortcuts_text = """Keyboard Shortcuts & Mouse Controls:

ZOOM CONTROLS:
• Ctrl + Mouse Wheel: Zoom in/out
• Ctrl + Plus (+): Zoom in
• Ctrl + Minus (-): Zoom out
• Ctrl + 0: Fit to frame
• Ctrl + 1: Actual size (100%)

NAVIGATION:
• Middle Mouse Button + Drag: Pan around image
• Mouse Wheel: Scroll vertically
• Shift + Mouse Wheel: Scroll horizontally

PANEL CONTROLS:
• Drag the divider between panels to resize
• Minimum panel size: 300px each

TIP: Click on the image area first to ensure it receives keyboard focus."""
        
        messagebox.showinfo("Keyboard Shortcuts & Controls", shortcuts_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernFlowchartApp(root)
    root.mainloop()