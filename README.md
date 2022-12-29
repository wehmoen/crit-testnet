# BloodMoon Sniper Bot

### Description

Bloodmoon Sniper Bot is an automatic buying application for axies on the marketplace that lets you add
sniper listing and also add multiple ronin accounts for your every transaction.

### Installation

- Once the code is downloaded run `py -m pip install -r requirements.txt` to install all the required dependencies.
- On the `data\kek.txt` enter your desired password and salt for encrypting your private keys.(Note:You can move this file anywhere you want if you are not using the bot for security purposes)
- On your command line run `py bloodmoon_main.py` to start the bot.

---

## Usage

### Setting up your account/s

- On the bot’s landing page you’ll see the File menu bar on the upper left corner.
- You should see the Ronin Accounts option.
- Click on it and another window will pop up.
- You can now setup your ronin accounts by supplying the needed information.
(Note: All of the data stored are encrypted using fernet cryptography module.)
If you want to learn more about fernet crytography you can check out this [link](https://cryptography.io/en/latest/fernet/).
- Once done you can set your active account by clicking the Set as Active button on the right frame of the window.
- You can now close the window to setup your filters.
- Restart the bot to save the changes you made

### Setting up filters

- To setup filters just supply the needed data on the left frame of the application.
- Filter link can be found at Axie Infinity [Marketplace](https://app.axieinfinity.com/marketplace/axies/).
- Once done click Save button.
- You’ll see the list of your filters on the right frame of the window.

### Running the Bot

- On the landing page you’ll see a Run Bot Button. Click on it and the bot will start to loop and buy the axies on you filters list.

### Contact

John Paul Serdan(Ghost🤖#8342)

### License

All intellectual property is assigned to QU3ST and should remain confidential