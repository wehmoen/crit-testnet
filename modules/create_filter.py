from . import db
import os


def add_name(input_mode):
    """Adding listing name"""
    filter_name = input(
        "Please name your filter. Leave blank to go back to main menu.\n"
    )
    if filter_name == "":
        return main_menu()
    return filter_name


def add_purchase_price(input_mode):
    """Adding purchase price"""
    purchase_price = input("Please enter the purchase price.\n")
    return purchase_price


def add_num_asset(input_mode):
    """Adding a number of assets to buy"""
    num_assets = input("Please enter the number of assets to buy with this filter.\n")
    try:
        num_assets = int(num_assets)
        return num_assets
    except:
        print("Num assets is invalid. Please only enter a number.")
        return add_num_asset()


def transform_filterdata(input_data):

    new_filter = {}
    for value in input_data:
        temp_data = value.split("=")
        filter_type = temp_data[0]
        try:
            filter_value = int(temp_data[1])
        except:
            filter_value = temp_data[1]
        if filter_type == "region":
            new_filter["region"] = "japan"
            continue
        if filter_type in ["auctionTypes", "stage", "page", "partTypes"]:
            continue
        if filter_type == "excludeParts":
            filter_type = "parts"
            if filter_value in new_filter["parts"]:
                new_filter["parts"][new_filter["parts"].index(filter_value)] = (
                    "!" + filter_value
                )
                continue
        if filter_type in ["mystic", "japan", "xmas", "shiny", "summer"]:
            filter_type = "num" + filter_type.capitalize()
        if filter_type == "class":
            filter_type = "classes"
        if filter_type in ["part", "bodyShape"]:
            filter_type = filter_type + "s"
        if filter_type == "title":
            filter_value = filter_value.replace("-", " ")
        if filter_type == "type":
            filter_type = "landType"
        if not filter_type in new_filter:
            new_filter[filter_type] = []
        new_filter[filter_type].append(filter_value)

    return new_filter


def transform_link_data(asset_type, url):

    if asset_type == "":
        asset_type = (
            url[: url.find("?")]
            .replace("https://app.axieinfinity.com/marketplace/", "")
            .replace("/", "")
        )

    elif not asset_type == url[: url.find("?")].replace(
        "https://app.axieinfinity.com/marketplace/", ""
    ).replace("/", ""):
        new_asset_type = (
            url[: url.find("?")]
            .replace("https://app.axieinfinity.com/marketplace/", "")
            .replace("/", "")
        )
        print(
            "Cannot change filter type. Previous type was "
            + asset_type
            + " new filter type is "
            + new_asset_type
            + "."
        )
        return add_new_filter()
    try:
        input_data = url[url.find("?") + 1 :].split("&")
        new_filter = transform_filterdata(input_data)

        for value in new_filter:
            if len(new_filter[value]) == 0:
                new_filter[value] = None

        return new_filter

    except:
        print("Something went wrong with the filter. Did you enter the URL correctly?")
        print(
            "e.g.: https://app.axieinfinity.com/marketplace/axies/?class=Beast&mystic=1&auctionTypes=Sale"
        )
        print("Would search for a 1 part mystic beast")
        return add_new_filter()


def add_new_filter(input_mode=0, asset_type="", gui_filter=""):
    """Adding new sniper filter to DB"""
    if input_mode == 0:
        """Save on general input"""
        url = input("Please paste marketplace url of your filter.\n")
        return transform_link_data(asset_type, url)
    else:
        """Save on GUI"""
        return transform_link_data(asset_type, gui_filter)


def create_filter(
    input_mode=0,
    gui_ftname="",
    gui_buy_price=int(0),
    gui_num_axie=int(0),
    gui_filter="",
):

    """Main create new filter function"""
    if input_mode == 0:
        filter_name = add_name(input_mode)
        purchase_price = add_purchase_price(input_mode)
        num_assets = add_num_asset(input_mode)
        new_filter = add_new_filter(input_mode)

        if filter_name == "":
            return add_name(input_mode)
        if purchase_price == 0:
            return add_purchase_price(input_mode)
        if num_assets == 0:
            return add_num_asset(input_mode)
        if new_filter is None:
            return add_new_filter(input_mode)
        else:
            print("Added filter successfully!")
            print("**************************")
            print(f"Name:{filter_name}")
            print(f"Purchase Price:{purchase_price}")
            print(f"Filter:{new_filter}")
            print(f"Number of asset:{num_assets}")
            print("**************************\n")
            db.execute(
                "INSERT INTO snipe_list(name,pur_price,filter,num_asset) VALUES(?,?,?,?)",
                filter_name,
                purchase_price,
                str(new_filter),
                num_assets,
            )
            db.commit()

            choice = input("Would you like to continue?(Y/N)\n")
            if not choice.lower() == "n":
                return main_menu()
            else:
                raise SystemExit

    else:
        parsed_filter = add_new_filter(input_mode, "", gui_filter)
        db.execute(
            "INSERT INTO snipe_list(name,pur_price,filter,num_asset,link,buy_count) VALUES(?,?,?,?,?,?)",
            gui_ftname,
            gui_buy_price,
            str(parsed_filter),
            gui_num_axie,
            gui_filter,
            0,
        )
        db.commit()


def get_snipe_list_name():
    """Get sniper filter names from db"""
    snipe_filters = db.records("SELECT name FROM snipe_list")
    return snipe_filters


def get_filter_by_name(ft_name):
    """Get sniper filter by listing name"""
    filter_data = db.records("SELECT * FROM snipe_list WHERE name=?", ft_name)
    return filter_data


def get_snipe_list():
    """Get the list of sniper filter from DB"""
    snipe_filters = db.records("SELECT * FROM snipe_list")
    return snipe_filters


def ron_list():
    """Get the list of ronin address from DB"""
    ron_add = db.records("SELECT * FROM keys")
    return ron_add


def get_ron_by_add(address):
    """Get the ronin address data by address"""
    ron_data = db.records("SELECT * FROM keys WHERE ron_add=?", address)
    return ron_data


def gui_update(gui_name, pur_price, gui_filt, num):
    """Update filter from GUI"""
    parsed_filter = add_new_filter(1, "", gui_filt)
    db.execute(
        "UPDATE snipe_list SET name=?,pur_price=?,filter=?,num_asset=?,link=? WHERE name =?",
        gui_name,
        pur_price,
        str(parsed_filter),
        num,
        gui_filt,
        gui_name,
    )

    db.commit()


def update_filter_name(name_edit, filter_index):
    """Update filter name on DB"""
    db.execute("UPDATE snipe_list SET name=? WHERE name =?", name_edit, filter_index)
    db.commit()
    print(f"{name_edit} is the new name!")


def update_filter_purchase_price(pur_price_edit, filter_index):
    """Update filter purchase price on DB"""
    db.execute(
        "UPDATE snipe_list SET pur_price=? WHERE name =?",
        pur_price_edit,
        filter_index,
    )
    db.commit()
    print(f"{pur_price_edit} is the new purchase price!")


def update_filter_link(filter_edit, filter_index):
    """Update filter link on DB"""
    db.execute(
        "UPDATE snipe_list SET filter=? WHERE name =?",
        str(filter_edit),
        filter_index,
    )
    db.commit()
    print(f"{filter_edit} is the new filter!")


def update_num_of_asset(num_asset_edit, filter_index):
    """Update number of asset to buy on DB"""
    db.execute(
        "UPDATE snipe_list SET num_asset=? WHERE name =?",
        num_asset_edit,
        filter_index,
    )
    db.commit()
    print(f"{num_asset_edit} is the new number of asset to buy!")


def edit_filter(filter_name="", attempts=0):
    """Edit snipe filter"""
    if filter_name == "":
        snipe_filters = get_snipe_list_name()
        counter = 0
        print("**************************")
        for records in snipe_filters:
            counter += 1
            print(f"#{counter}-{records[0]}")
        print("**************************\n")
        choice = input(
            "Enter the number of snipe filter you want to edit. Or leave blank to return to main menu.\n"
        )
        if choice == "":
            return main_menu()
        try:
            choice = int(choice)
            if not (0 < choice <= counter):
                print("The filter you entered does not exist, please try again.")
                return edit_filter()

        except:
            print("The filter you entered does not exist, please try again.")
            return edit_filter()

    filter_index = snipe_filters[choice - 1][0]
    print("**************************")
    print(f"{filter_index}")
    print("**************************")
    print("#1-Filter name")
    print("#2-Filter price")
    print("#3-Filter data")
    print("#4-Filter numAssets")
    print("**************************\n")
    choice = input("What would you like to edit?\n")
    if not choice in ["1", "2", "3", "4"]:
        if attempts < 2:
            print("Invalid entry, please try again.")
            return edit_filter(filter_name, attempts + 1)
        else:
            print("Failed input 3 times. Returning to Main Menu.")
            return main_menu()

    if choice == "1":
        name_edit = add_name()
        if name_edit == "":
            return add_name
        else:
            update_filter_name(name_edit, filter_index)
            return main_menu()

    if choice == "2":
        pur_price_edit = add_purchase_price()
        if pur_price_edit == "":
            return add_purchase_price
        else:
            update_filter_purchase_price(pur_price_edit, filter_index)
            return main_menu()

    if choice == "3":
        filter_edit = add_new_filter()
        if filter_edit == "":
            return add_new_filter
        else:
            update_filter_link(filter_edit, filter_index)
            return main_menu()

    if choice == "4":
        num_asset_edit = add_num_asset()
        if num_asset_edit == "":
            return add_num_asset
        else:
            update_num_of_asset(num_asset_edit, filter_index)
            return main_menu()


def view_filter():
    """View list of filter"""
    filter_list = get_snipe_list()
    counter = 0
    print("****************************")
    for flist in filter_list:
        counter += 1
        print(
            f"#{counter}-Name:{flist[0]}\n   Purchase price:{flist[1]}\n   Filter:{flist[2]}\n   Number of asset:{flist[3]}\n"
        )
    print("****************************\n")


def delete_filter(filter_name):
    """Deleting filter"""
    db.execute("DELETE FROM snipe_list WHERE name=?", filter_name)
    db.commit()


def delete_ronin(ronin_add):
    """Deleting ronin address"""
    db.execute("DELETE FROM keys WHERE ron_add=?", ronin_add)
    db.commit()


def main_menu(attempts=0):
    """This is the main menu for the general input"""
    print("Main Menu")
    print("****************************")
    print("1. Create new filter")
    print("2. Edit existing filter")
    print("3. View existing filter")
    print("4. Delete existing filter")
    print("5. Exit")
    print("****************************")
    choice = input("\nWhat would you like to do?\n")
    if not choice in ["1", "2", "3", "4", "5"]:
        if attempts < 2:
            print("Invalid entry, please try again.")
            return main_menu(attempts + 1)
        else:
            print("Failed input 3 times. Exiting.")
            raise SystemExit
    if choice == "1":
        return create_filter()
    elif choice == "2":
        return edit_filter()
    elif choice == "3":
        view_filter()
        choice = input("Would you like to continue?(Y/N)\n")
        if not choice.lower() == "y":
            raise SystemExit
        else:
            return main_menu()

    elif choice == "4":
        view_filter()
        choice = int(input("\nWhat would you like to delete?\n"))
        snipe_filter = get_snipe_list()
        ft_name = snipe_filter[choice - 1][0]
        delete_filter(ft_name)
        print(f"Filter {ft_name} is sucessfully deleted!")

    elif choice == "5":
        raise SystemExit
    else:
        return main_menu(attempts + 1)
