# moodle-auto-clock

It's a simple script that clocks the user in/out of the Moodle platform. Using Web Scraping. Moodle doesn't provide an API.

## What am I going to learn in this README ?
> **You are NOT going to learn how to setup or create your our server.**
You will learn how to setup the docker container and your mobile phone so it can automatically connect to the docker container.

## Requirements
- Moodle Account
- Bot Gmail / Your own Email (NO needed but recommended)
- Docker
- mobile phone (Android OR Iphone)

___

## Server
First let's install Docker and configure it.
```sh
sudo apt update && sudo apt install docker.io
```
Now, lets start and enable docker automatically everytime when we reboot the server.
```sh
sudo systemctl start docker && sudo systemctl enable docker
```
Once you are done just clone this repository.
```sh
git clone https://github.com/U-L-M-S/moodle-auto-clock.git
```
Next change the credentials.json wiht your credentials

```json
{
    "username": "moodle_mail_for_login@mail.de",
    "password": "moodle_pswd_for_login",
    "bot_mail": "bot_gmail_to_send_email@gmail.de",
    "bot_pswd": "bot_gmail_pswd_to_send_email",
    "user_mail": "your_gmail_to_receive_email@gmail.de"
}
```
You can use your credentials of your own email and send the email (in case of errors) to youself or create a bot and send the errors via the bot to your email. In each case you will need a [gmail app password.](https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fmyaccount.google.com%2Fapppasswords&followup=https%3A%2F%2Fmyaccount.google.com%2Fapppasswords&ifkv=ARZ0qKLgAZL4X5K5J9YlzJWF1WX5iBQSiR26PGBK__-qiL8W4wBWXeIzu8M7OBXkSaZFJ4A0x7--IQ&osid=1&passive=1209600&rart=ANgoxccWtu49xcTR9O_jbYe2oE81ij-AfRR1Hgdf9nc8NKT8VoCeQBNklnQHOdngZJzYwNIIdpX0X3X4DBljU0epmrun6EeSL3zy0NL_HTlmR0BYALO9_Yg&service=accountsettings&flowName=GlifWebSignIn&flowEntry=ServiceLogin&dsh=S1828806382%3A1710924453785456&theme=glif&ddm=0)

Now you need to configure the docker compose.
just go to the project folder `cd moodle-auto-clock` and run this command:
```sh
docker compose build
```
In this way a docker image will be created with the name *moodle-auto-clock-image*.

#### SSH
you can simple run 
```sh
ssh user@server "docker run -e ACTION=starten moodle-auto-clock"
```
you can use `starten` (it will clock you in) or `beenden` (it will clock you out) as variable valuer on `ACTION`. But our goal here is to make it happen automatically.

___

## Phone
#### Iphone
On your Shortcuts go to **automation** and select the trigger. It can be the time or place.

Then select the **action** *run ssh command*, input your informations (hostname, username, password) and in the area of **scripting** insert this command `docker run -e ACTION=starten moodle-auto-clock`.

#### Android


*Unfortunately, there is no built-in feature for Android, so we need to use an app. If I am mistaken, please correct me ([Felix](https://github.com/Felix-From)).*

##### Installation

There are many apps available, but for these instructions, we will use the free app "MacroDroid". Follow these steps to download and install MacroDroid:

- Download and install MacroDroid from an app store of your choice:
  - [Google Play](https://play.google.com/store/apps/details?id=com.arlosoft.macrodroid&hl=en&gl=US)

#### Usage

1. Launch MacroDroid and navigate through the introductory screens.
2. On the Tile Screen or Main Menu, locate and tap the "Create Macro" tab.
3. Name the macro as you prefer.
4. Tap the small plus (+) icon in the upper right corner of the red tile labeled "Trigger".
5. Configure the trigger parameters according to your preferences (e.g., Time, Geofence, Shaking).
6. Once you've set the trigger, return to the Macro Creation Screen and tap the plus (+) symbol on the blue tile labeled "Actions".
7. In the Actions menu, select "Applications", then choose "Shell Script" from the dropdown menu.
8. Enable the "Helper App" feature and switch the access type to "No Root Access".
9. Now, insert the command `docker run -e ACTION=starten moodle-auto-clock`, then press "OK".
10. OPTIONAL: Customize constraints using the plus (+) symbol within the green tile labeled "Constraints".
11. Press the "Back" arrow in the top-left corner, then click "Save" in the pop-up message. You're done!

To view all your saved macros, navigate to the "Macros" tab at the bottom of the Main Menu.
