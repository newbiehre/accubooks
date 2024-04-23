import tkinter as tk
from tkinter import messagebox, filedialog

from src.backend.statement_parser import StatementParser


class AccuBooksApp(tk.Tk):
    _instance = None
    _is_initialized = False

    ROOT_TITLE = "AccuBooks"
    ROOT_GEOMETRY = "700x600"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AccuBooksApp, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.file_list = None
        self.selected_files = None
        self.import_button = None

        if not self._is_initialized:
            tk.Tk.__init__(self, screenName=self.ROOT_TITLE, baseName=self.ROOT_TITLE)
            self.geometry(self.ROOT_GEOMETRY)
            self.title(self.ROOT_TITLE)
            self.show_content()
            self.mainloop()

    def show_content(self):
        frame = tk.Frame(self)
        frame.pack(padx=20, expand=True, fill=tk.BOTH)

        # First section
        first_section_frame = tk.Frame(frame)
        first_section_frame.pack(pady=10, expand=False, fill=tk.BOTH)

        # Browse files button
        self.selected_files = tk.StringVar()
        browse_button = tk.Button(first_section_frame, text="Browse Files", command=self.browse_files)
        browse_button.pack(side=tk.LEFT)

        # Deleted selected files button
        delete_button = tk.Button(first_section_frame, text="Delete Selected File(s)",
                                  command=self.delete_actively_selected_files)
        delete_button.pack(side=tk.RIGHT)

        # Create a Listbox to display selected files
        self.file_list = tk.Listbox(frame, selectmode="extended", height=25)
        self.file_list.pack(fill=tk.BOTH, expand=True)

        # First section
        last_section_frame = tk.Frame(frame)
        last_section_frame.pack(pady=10, expand=False, fill=tk.BOTH)

        # Import files button
        self.import_button = tk.Button(last_section_frame, text="Import", command=self.import_selected_files)
        self.import_button.pack(fill=tk.BOTH, expand=True)

        # Open csv button
        import_button = tk.Button(last_section_frame, text="Open Output Directory",
                                  command=StatementParser.open_exported_dir)
        import_button.pack(fill=tk.BOTH, expand=True)

    def browse_files(self):
        filetypes = [('PDF files', '*.pdf')]
        files = filedialog.askopenfilenames(parent=self, title="Only PDF file(s) can be selected", filetypes=filetypes)

        if files:
            for file in files:
                if file not in self.file_list.get(first=0, last=tk.END):
                    self.file_list.insert(tk.END, file)

        print(self.file_list.get(first=0, last=tk.END))

    def delete_actively_selected_files(self):
        currently_selected: tuple = self.file_list.curselection()
        if currently_selected:
            first, last = (None, None)
            try:
                first, last = currently_selected[0], currently_selected[-1]
            except IndexError:
                pass
            self.file_list.delete(first=first, last=last)

    def import_selected_files(self):
        selected_files = list(self.file_list.get(first=0, last=tk.END))

        if selected_files:
            size = self.file_list.size()
            try:
                self.import_button.config(state="disabled")
                for file_path in selected_files:
                    parsed_statement = StatementParser(file_path)
                    parsed_statement.parse_statement()
                    parsed_statement.export_csv_file()
                messagebox.showinfo(title=self.ROOT_TITLE, message=f"Imported {size} file{"s" if size > 1 else ""}!")
            except Exception as e:
                print(e)
                messagebox.showerror(title=self.ROOT_TITLE, message=f"Error: {e}")
            finally:
                self.import_button.config(state="normal")
        else:
            messagebox.showwarning(title=self.ROOT_TITLE, message="No files selected!")

        self.file_list.delete(0, tk.END)  # Empty file_list
