import tkinter as tk
import tkinter.messagebox
import customtkinter
import modules.create_filter as create_filter
import modules.save_key_ronin as save_key_ronin
import modules.main
import threading
import sys
import os


def resource_path(relative_path):
    """This function is for the path of additional files for tkinter"""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("dark-blue")



class App(customtkinter.CTk):

    WIDTH = 780
    HEIGHT = 520

    def __init__(self):
        super().__init__()

        self.title("Bloodmoon")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol(
            "WM_DELETE_WINDOW", self.on_closing
        )  # call .on_closing() when app gets closed
        self.iconbitmap("image\QUEST_logo_sword_RGB-1.ico")
        self.resizable(False,False)

        def save_file():
            """Saving Filter Using GUI"""
            print("File Saved!")
            filter_name = self.entry_1.get()

            check_name = create_filter.get_filter_by_name(filter_name)
            if len(check_name) >= 1:
                buy_price = self.entry_3.get()
                num_axie = self.entry_4.get()
                axie_filter = self.entry_5.get()
                create_filter.gui_update(filter_name, buy_price, axie_filter, num_axie)
                tkinter.messagebox.showinfo(
                    "Bloodmoon Sniper Bot", f"Filter {filter_name} is updated."
                )
                self.entry_1.delete(0, tk.END)
                self.entry_3.delete(0, tk.END)
                self.entry_4.delete(0, tk.END)
                self.entry_5.delete(0, tk.END)

            else:
                buy_price = self.entry_3.get()
                num_axie = self.entry_4.get()
                axie_filter = self.entry_5.get()
                self.entry_1.delete(0, tk.END)
                self.entry_3.delete(0, tk.END)
                self.entry_4.delete(0, tk.END)
                self.entry_5.delete(0, tk.END)
                tkinter.messagebox.showinfo(
                    "Bloodmoon Sniper Bot",
                    f"Filter {filter_name} is added!",
                )
                return (
                    create_filter.create_filter(
                        1, filter_name, buy_price, num_axie, axie_filter
                    ),
                    get_list(),
                )

        def edit_filter():
            """Editing filter on GUI"""
            listing_name = self.listbox.get(self.listbox.curselection())
            filter_data = create_filter.get_filter_by_name(listing_name)
            self.entry_1.delete(0, tk.END)
            self.entry_1.insert(0, filter_data[0][0])
            self.entry_3.delete(0, tk.END)
            self.entry_3.insert(0, filter_data[0][1])
            self.entry_4.delete(0, tk.END)
            self.entry_4.insert(0, filter_data[0][3])
            self.entry_5.delete(0, tk.END)
            self.entry_5.insert(0, filter_data[0][4])

        def delete_filter():
            """Delete Filter on GUI"""
            listing_name = self.listbox.get(self.listbox.curselection())
            create_filter.delete_filter(listing_name)
            print("Filter Deleted.")

            tkinter.messagebox.showinfo(
                "Bloodmoon Sniper Bot",
                f"Filter {listing_name} is successfully deleted!",
            )
            get_list()

        def add_key():

            key_add = tk.Tk()
            key_add.title("Bloodmoon")
            key_add.configure(background="#353358", height=App.HEIGHT, width=App.WIDTH)
            key_add.iconbitmap("image\QUEST_logo_sword_RGB-1.ico")

            def save_account():

                pvt_key = entry_1.get()
                ronin_add = entry_2.get()

                ronin_account = create_filter.get_ron_by_add(ronin_add)

                if len(ronin_account) < 1:
                    gas_price = entry_3.get()
                    save_key_ronin.add_key_address(1, pvt_key, ronin_add, gas_price)
                    entry_1.delete(0, tk.END)
                    entry_2.delete(0, tk.END)
                    entry_3.delete(0, tk.END)
                    tkinter.messagebox.showinfo(
                        "Bloodmoon Sniper Bot", f"Ronin account {ronin_add} is added!"
                    )
                    get_list()
                else:
                    print("Account already setup.")

            def edit_ron():
                """Editing Ronin Details on GUI"""
                ronin = listbox.get(listbox.curselection())
                ron_data = create_filter.get_ron_by_add(ronin)

                entry_1.delete(0, tk.END)
                entry_1.insert(0, "Not Editable")
                entry_2.delete(0, tk.END)
                entry_2.insert(0, ron_data[0][1])
                entry_3.delete(0, tk.END)
                entry_3.insert(0, ron_data[0][2])

            def cancel_edit():
                """Cancel Edit on GUI"""
                entry_1.delete(0, tk.END)
                entry_2.delete(0, tk.END)
                entry_3.delete(0, tk.END)

            def delete_ron():
                """Deleting ronin account"""
                ronin = listbox.get(listbox.curselection())
                create_filter.delete_ronin(ronin)
                tkinter.messagebox.showinfo(
                    "Bloodmoon Sniper Bot", f"Filter {ronin} is successfully deleted!"
                )
                get_list()

            def active_account():
                """Setting the active account"""
                active = listbox.get(listbox.curselection())
                save_key_ronin.set_active(active)

            # ============ create two frames ============

            # configure grid layout (2x1)
            key_add.grid_columnconfigure(1, weight=1)
            key_add.grid_rowconfigure(0, weight=1)

            frame_left = customtkinter.CTkFrame(
                master=key_add, width=100, corner_radius=0
            )
            frame_left.grid(row=0, column=0, sticky="nswe")

            frame_right = customtkinter.CTkFrame(master=key_add)
            frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

            # ============ frame_left ============

            # configure grid layout (1x11)
            frame_left.grid_rowconfigure(
                0, minsize=10
            )  # empty row with minsize as spacing
            # empty row with minsize as spacing
            frame_left.grid_rowconfigure(10, weight=1)
            frame_left.grid_rowconfigure(
                13, minsize=10
            )  # empty row with minsize as spacing

            label_1 = customtkinter.CTkLabel(
                master=frame_left,
                justify=tkinter.LEFT,
                text="Setup your account",
                text_font=("Poppins", 25, "bold"),
            )
            label_1.grid(row=1, column=0, pady=10, padx=20, sticky="ew", columnspan=2)

            entry_1 = customtkinter.CTkEntry(
                master=frame_left,
                placeholder_text="Enter your private key",
                width=200,
                text_color="#000000",
            )
            entry_1.grid(row=2, column=0, pady=10, padx=20, sticky="ew", columnspan=2)

            entry_2 = customtkinter.CTkEntry(
                master=frame_left,
                placeholder_text="Enter your Ronin Address",
                width=200,
                text_color="#000000",
            )
            entry_2.grid(row=3, column=0, pady=10, padx=20, sticky="ew", columnspan=2)

            entry_3 = customtkinter.CTkEntry(
                master=frame_left,
                placeholder_text="Gas Price(Leave blank for default value)",
                width=200,
                text_color="#000000",
            )
            entry_3.grid(row=4, column=0, pady=10, padx=20, sticky="ew", columnspan=2)

            button_1 = customtkinter.CTkButton(
                master=frame_left, command=save_account, text="Save"
            )
            button_1.grid(row=5, column=0, pady=10, padx=20)

            button_2 = customtkinter.CTkButton(
                master=frame_left, command=cancel_edit, text="Cancel"
            )
            button_2.grid(row=5, column=1, pady=10, padx=20)

            # ============ frame_right ============

            # configure grid layout (3x7)
            frame_right.rowconfigure((0, 1, 2, 3), weight=1)
            frame_right.rowconfigure(7, weight=10)
            frame_right.columnconfigure((0, 1), weight=1)
            frame_right.columnconfigure(2, weight=0)

            frame_info = customtkinter.CTkFrame(master=frame_right)
            frame_info.grid(
                row=0,
                column=0,
                columnspan=2,
                rowspan=4,
                pady=20,
                padx=20,
                sticky="nsew",
            )

            # ============ frame_info ============

            # configure grid layout (1x1)
            frame_info.rowconfigure(0, weight=0)
            frame_info.rowconfigure(1, weight=1)
            frame_info.rowconfigure(2, weight=1)
            frame_info.rowconfigure(3, weight=1)
            frame_info.columnconfigure(0, weight=1)

            label_info_1 = customtkinter.CTkLabel(
                master=frame_info,
                text="Ronin Accounts",
                height=35,
                corner_radius=6,  # <- custom corner radius
                fg_color=("white", "#e96b6d"),  # <- custom tuple-color
                justify=tkinter.LEFT,
            )
            label_info_1.grid(
                column=0, row=0, sticky="nwe", padx=15, pady=15, columnspan=2
            )

            listbox = tk.Listbox(master=frame_info)
            listbox.grid(column=0, row=1, sticky="nwe", padx=15, pady=15, columnspan=2)

            def get_list():
                """Get List of Ronin Accounts"""
                account_list = create_filter.ron_list()
                x = 0
                listbox.delete(0, customtkinter.END)
                for list in account_list:
                    listbox.insert(x + 1, list[1])
                    x += 1

            get_list()

            try:
                active_ron = save_key_ronin.get_active()
                label_info_2 = customtkinter.CTkLabel(
                    master=frame_info,
                    text=f"Active Account: {active_ron}",
                    height=35,
                    corner_radius=6,  # <- custom corner radius
                    fg_color=("white", "#e96b6d"),  # <- custom tuple-color
                    justify=tkinter.LEFT,
                )
                label_info_2.grid(
                    column=0, row=2, sticky="nwe", padx=15, pady=15, columnspan=2
                )

            except:
                print("No Data yet!")

            edit_ronin = customtkinter.CTkButton(
                master=frame_info, text="Edit", command=edit_ron
            )
            edit_ronin.grid(column=0, row=3, padx=15, pady=5, sticky="ew")

            delete_ronin = customtkinter.CTkButton(
                master=frame_info, text="Delete", command=delete_ron
            )
            delete_ronin.grid(column=1, row=3, padx=15, pady=5, sticky="ew")

            set_active = customtkinter.CTkButton(
                master=frame_info, text="Set as Active", command=active_account
            )
            set_active.grid(column=0, row=4, padx=15, pady=5, sticky="ew", columnspan=2)

        def cancel_edit():
            """Cancel editing"""
            self.entry_1.delete(0, tk.END)
            self.entry_3.delete(0, tk.END)
            self.entry_4.delete(0, tk.END)
            self.entry_5.delete(0, tk.END)


        def start_bot():
            """Start Bot in GUI""" 
            modules.main.init()

        def user_quit():
            raise SystemExit

        menu_bar = tkinter.Menu(self, background="#353358")
        self.configure(menu=menu_bar)

        file_menu = tkinter.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Ronin Accounts", command=add_key)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=user_quit)

        help_menu = tkinter.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(
            master=self, width=100, corner_radius=0
        )
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frame_left ============

        # configure grid layout (1x8)
        self.frame_left.grid_rowconfigure(
            0,
            minsize=10,
        )
        self.label_1 = customtkinter.CTkLabel(
            master=self.frame_left,
            text="QU3ST Axie Sniper",
            text_font=("Poppins Bold", 25, "bold"),
        )  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=10, columnspan=2)

        self.entry_1 = customtkinter.CTkEntry(
            master=self.frame_left,
            placeholder_text="Name your Axie Sniper..",
            text_color="#000000",
        )
        self.entry_1.grid(row=2, column=0, pady=10, padx=20, sticky="ew", columnspan=2)

        self.entry_3 = customtkinter.CTkEntry(
            master=self.frame_left,
            placeholder_text="Set the buy price (ETH)...",
            text_color="#000000",
        )
        self.entry_3.grid(row=4, column=0, pady=10, padx=20, sticky="ew", columnspan=2)

        self.entry_4 = customtkinter.CTkEntry(
            master=self.frame_left,
            placeholder_text="How many Axies should it buy before stopping..",
            text_color="#000000",
        )
        self.entry_4.grid(row=5, column=0, pady=10, padx=20, sticky="ew", columnspan=2)

        self.entry_5 = customtkinter.CTkEntry(
            master=self.frame_left,
            placeholder_text="Paste the market place filter link here...",
            text_color="#000000",
        )
        self.entry_5.grid(row=6, column=0, pady=10, padx=20, sticky="ew", columnspan=2)

        self.save_button = customtkinter.CTkButton(
            master=self.frame_left, text="Save", command=save_file
        )
        self.save_button.grid(
            row=7,
            column=0,
            pady=10,
            padx=20,
        )


        self.cancel_button = customtkinter.CTkButton(
            master=self.frame_left, text="Cancel", command=cancel_edit
        )
        self.cancel_button.grid(
            row=7,
            column=1,
            pady=10,
            padx=20,
        )


        # ============ frame_right ============

        # configure grid layout (3x7)f
        self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_right.rowconfigure(7, weight=10)
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=0)

        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(
            row=0, column=0, columnspan=2, rowspan=4, pady=20, padx=20, sticky="nsew"
        )

        # ============ frame_info ============

        # configure grid layout (1x1)
        self.frame_info.rowconfigure(0, weight=0)
        self.frame_info.rowconfigure(1, weight=1)
        self.frame_info.rowconfigure(2, weight=1)
        self.frame_info.rowconfigure(3, weight=1)
        self.frame_info.columnconfigure(0, weight=1)

        self.label_info_1 = customtkinter.CTkLabel(
            master=self.frame_info,
            text="Sniping List",
            height=35,
            text_font=("Cabin", -19, "bold"),
            corner_radius=6,  # <- custom corner radius
            fg_color=("white", "#e96b6d"),  # <- custom tuple-color
            justify=tkinter.LEFT,
        )
        self.label_info_1.grid(
            column=0, row=0, sticky="nwe", padx=15, pady=15, columnspan=2
        )

        self.listbox = tk.Listbox(master=self.frame_info)
        self.listbox.grid(column=0, row=1, sticky="nwe", padx=15, pady=15, columnspan=2)

        def get_list():
            snipe_list = create_filter.get_snipe_list()
            x = 0
            self.listbox.delete(0, customtkinter.END)
            for list in snipe_list:
                self.listbox.insert(x + 1, list[0])
                x += 1

        get_list()

        self.edit_filter = customtkinter.CTkButton(
            master=self.frame_info, text="Edit", command=edit_filter
        )
        self.edit_filter.grid(column=0, row=2, padx=15, pady=15, sticky="ew")

        self.delete_filter = customtkinter.CTkButton(
            master=self.frame_info, text="Delete", command=delete_filter
        )
        self.delete_filter.grid(column=1, row=2, padx=15, pady=15, sticky="ew")

       
        def start_thread():
            """Start threading to stop GUI freeze"""
            main_thread = threading.Thread(target=start_bot, args=(), daemon=True)
            main_thread.start()
            main_thread.join()

        self.run_button = customtkinter.CTkButton(
            master=self.frame_info,
            text="Run Bot",
            command=start_thread,
            bg="#d2ffd2",
        )
        self.run_button.grid(
            row=3, column=0, pady=15, padx=15, sticky="ew", columnspan=2
        )

    def change_appearance_mode(self, new_appearance_mode):
        """Change appearance of GUI"""
        customtkinter.set_appearance_mode(new_appearance_mode)

    def on_closing(self, event=0):
        """Stop running mainloop on close"""
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
