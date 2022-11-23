import tkinter as tk
import tkinter.messagebox
import pymongo
from pymongo import MongoClient
import customtkinter
import os
import sys
from PIL import Image, ImageTk
from buy_axie import App
from utils import db


verify_prod = db.records("SELECT * FROM verify")
db.commit()


if len(verify_prod)>0:
    main_app = App()
    main_app.mainloop()
else:
    print("Need Product Key!")
    customtkinter.set_appearance_mode(
        "Dark"
    )  # Modes: "System" (standard), "Dark", "Light"
    customtkinter.set_default_color_theme(
        "blue"
    )  # Themes: "blue" (standard), "green", "dark-blue"

    def resource_path(relative_path):
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

    class Product_key(customtkinter.CTk):

        WIDTH = 700
        HEIGHT = 300

        def __init__(self):
            super().__init__()

            self.title("Bloodmon")
            self.geometry(f"{Product_key.WIDTH}x{Product_key.HEIGHT}")
            self.protocol("WM_DELETE_WINDOW", self.on_closing)

            def check_key():
                """Check if the product key is in DB"""

                cluster = pymongo.MongoClient(
                 "mongodb+srv://ghost13:1234@cluster0.ehzq3fb.mongodb.net/?retryWrites=true&w=majority")
                mgdb = cluster["bloodmoon"]
                collection = mgdb["product_keys"]
                
                user_name= self.input_user.get()
                prod_key = self.input_product_key.get()

                db_data = collection.find({'prod_key': f"{prod_key}"})

                parsed_data=[]
                for x in db_data:
                    print(x)
                    parsed_data.append(x)
                
                if len(parsed_data) > 0 : 
                    if parsed_data[0]["status"] == "not_used":
                        
                        collection.update_one({'prod_key': f"{prod_key}"},{"$set":{'status':f"used by {user_name}"}})
                        db.execute("INSERT INTO verify(user_name,prod_stat) VALUES(?,?)",user_name,prod_key)
                        db.commit()
                        tkinter.messagebox.showinfo("Bloodmoon Sniper Bot",f"Successfully registered!")
                        main_app = App()
                        self.destroy()
                        main_app.mainloop()
                    else:
                        tkinter.messagebox.showinfo("Bloodmoon Sniper Bot","Key is already used!")
                else:
                        tkinter.messagebox.showinfo("Bloodmoon Sniper Bot","You entered an invalid key!")



            # ============ create two frames ============

            # configure grid layout (2x1)
            self.grid_columnconfigure(1, weight=1)
            self.grid_rowconfigure(0, weight=1)

            self.frame_left = customtkinter.CTkFrame(
                master=self, width=300, corner_radius=255
            )
            self.frame_left.grid(row=0, column=0, sticky="nswe")

            self.frame_right = customtkinter.CTkFrame(master=self)
            self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

            self.bg_image = Image.open(resource_path("q3logo.png"))
            self.resized_image = self.bg_image.resize((self.frame_left._current_width, 300))

            self.quest_img = ImageTk.PhotoImage(self.resized_image)
            # Show image using label
            self.label1 = customtkinter.CTkLabel(self.frame_left, image=self.quest_img)
            self.label1.place(x=0, y=0, relheight=1, relwidth=1)
            # ============ frame_right ============

            # configure grid layout (3x7)
            self.frame_right.rowconfigure((1, 2, 3), weight=0)
            self.frame_right.rowconfigure((0, 4), weight=10)
            self.frame_right.columnconfigure((0, 2), weight=0)
            self.frame_right.columnconfigure(1, weight=1)

            self.input_user = customtkinter.CTkEntry(
                master=self.frame_right, placeholder_text="Enter User Name"
            )
            self.input_user.grid(row=1, column=1, sticky="we", padx=30, pady=10)

            self.input_product_key = customtkinter.CTkEntry(
                master=self.frame_right, placeholder_text="Enter Product Key"
            )
            self.input_product_key.grid(row=2, column=1, sticky="we", padx=30, pady=10)

            self.confirm = customtkinter.CTkButton(
                master=self.frame_right, text="Confirm", command=check_key
            )
            self.confirm.grid(row=3, column=1, padx=10, pady=10)

        def change_appearance_mode(self, new_appearance_mode):
            customtkinter.set_appearance_mode(new_appearance_mode)

        def on_closing(self, event=0):
            self.destroy()

    if __name__ == "__main__":
        pd_key = Product_key()
        pd_key.mainloop()
