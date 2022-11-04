import tkinter
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):

    WIDTH = 780
    HEIGHT = 520

    def __init__(self):
        super().__init__()

        self.title("Bloodmon")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        def save_file():
            print("File Saved!")

        def add_key():
            print("Key added")
            key_add = tkinter.Tk()
            key_add.title("Bloodmoon")
            
            def button_callback():
                print("Button click")
                key_add.destroy()

            frame_1 = customtkinter.CTkFrame(master=key_add)
            frame_1.pack(fill="both", expand=True)

            label_1 = customtkinter.CTkLabel(master=frame_1, justify=tkinter.LEFT,text="Enter your private key and Ronin Address",text_font=("Roboto Medium", -16))
            label_1.pack(pady=12, padx=10)


            entry_1 = customtkinter.CTkEntry(master=frame_1, placeholder_text="Enter your private key",width=200)
            entry_1.pack(pady=12, padx=10)

            entry_2 = customtkinter.CTkEntry(master=frame_1, placeholder_text="Enter your Ronin Address",width=200)
            entry_2.pack(pady=12, padx=10)

            button_1 = customtkinter.CTkButton(master=frame_1, command=button_callback,text="Save")
            button_1.pack(pady=12, padx=10)


        menu_bar = tkinter.Menu(self)
        self.config(menu=menu_bar)

        file_menu = tkinter.Menu(menu_bar,tearoff=0)
        menu_bar.add_cascade(label="File",menu=file_menu)
        file_menu.add_command(label="Save",command=save_file)
        file_menu.add_command(label="Add Key & Address",command=add_key)
        file_menu.add_separator()
        file_menu.add_command(label="Exit",command=quit)

        help_menu = tkinter.Menu(menu_bar,tearoff=0)
        menu_bar.add_cascade(label="Help",menu=help_menu)
        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frame_left ============

        # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
        # self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(7, weight=1)
        self.frame_left.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Bloodmoon Axie Sniper Bot",
                                              text_font=("Roboto Medium", -16))  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        self.entry_1 = customtkinter.CTkEntry(master=self.frame_left,
                                                placeholder_text="Name Axie Sniper")
        self.entry_1.grid(row=2, column=0, pady=10, padx=20)

        self.entry_2 = customtkinter.CTkEntry(master=self.frame_left,
                                                placeholder_text="Gas Price")
        self.entry_2.grid(row=3, column=0, pady=10, padx=20)

        self.entry_3 = customtkinter.CTkEntry(master=self.frame_left,
                                                placeholder_text="Buy Price")
        self.entry_3.grid(row=4, column=0, pady=10, padx=20)

        self.entry_4 = customtkinter.CTkEntry(master=self.frame_left,
                                                placeholder_text="Number of Axie to buy")
        self.entry_4.grid(row=5, column=0, pady=10, padx=20)

        self.entry_5 = customtkinter.CTkEntry(master=self.frame_left,
                                                placeholder_text="Filter Link")
        self.entry_5.grid(row=6, column=0, pady=10, padx=20)

        self.label_mode = customtkinter.CTkLabel(master=self.frame_left, text="Appearance Mode:")
        self.label_mode.grid(row=9, column=0, pady=0, padx=20, sticky="w")

        self.optionmenu_1 = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                        values=["Light", "Dark", "System"],
                                                        command=self.change_appearance_mode)
        self.optionmenu_1.grid(row=10, column=0, pady=10, padx=20, sticky="w")

        # ============ frame_right ============

        # configure grid layout (3x7)
        self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_right.rowconfigure(7, weight=10)
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=0)

        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=0, column=0, columnspan=2, rowspan=4, pady=20, padx=20, sticky="nsew")

        # ============ frame_info ============

        # configure grid layout (1x1)
        self.frame_info.rowconfigure(0, weight=1)
        self.frame_info.columnconfigure(0, weight=1)

        self.label_info_1 = customtkinter.CTkLabel(master=self.frame_info,
                                                   text="Sniping List",
                                                   height=100,
                                                   corner_radius=6,  # <- custom corner radius
                                                   fg_color=("white", "gray38"),  # <- custom tuple-color
                                                   justify=tkinter.LEFT)
        self.label_info_1.grid(column=0, row=0, sticky="nwe", padx=15, pady=15)

        self.optionmenu_1.set("Dark")


    def button_event(self):
        print("Button pressed")

    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def on_closing(self, event=0):
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()