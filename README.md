# moodle-auto-clock

<img width="1196" height="672" alt="grafik" src="https://github.com/user-attachments/assets/a50fa16a-04bb-471f-ba4e-0b67a496eb37" />


A simple attendance tracking automation script for Moodle platforms. This tool automatically clocks users in/out using web scraping, as Moodle doesn't provide a standardized API for attendance tracking.

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

### Windows:
[Docker install guide](https://docs.docker.com/desktop/install/windows-install/)

### Linux:
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
Next, copy `credentials.json` to `credentials.local.json` and configure it with your Moodle instance and credentials:

```json
{
    "subdomain": "your-subdomain",
    "domain": "example.com",
    "username": "your_moodle_username",
    "password": "your_moodle_password",
    "bot_mail": "bot_gmail@gmail.com",
    "bot_pswd": "your_gmail_app_password",
    "user_mail": "your_email@gmail.com"
}
```

**Configuration fields:**
- `subdomain`: The subdomain of your Moodle instance (e.g., "lernplattform")
- `domain`: The domain of your Moodle instance (e.g., "example.com")
  - Together these build the URL: `https://subdomain.domain`
- `username`: Your Moodle login username
- `password`: Your Moodle login password
- `bot_mail`: Gmail address to send notification emails from
- `bot_pswd`: Gmail [App Password](https://myaccount.google.com/apppasswords) (not regular password)
- `user_mail`: Email address to receive notifications

Now you need to configure the docker compose.
just go to the project folder `cd moodle-auto-clock` and run this command:
```sh
docker compose build
```
In this way a docker image will be created with the name *moodle-auto-clock_image*.

#### SSH
you can simple run
```sh
ssh user@server "docker run --rm -e ACTION=starten moodle-auto-clock_image"
```
you can use `starten` (it will clock you in) or `beenden` (it will clock you out) as variable valuer on `ACTION`. But our goal here is to make it happen automatically.

___

## Phone
#### Iphone
On your Shortcuts go to **automation** and select the trigger. It can be the time or place.

Then select the **action** *run ssh command*, input your informations (hostname, username, password) and in the area of **scripting** insert this command `docker run --rm -e ACTION=starten moodle-auto-clock_image`.

#### Android


*Unfortunately, there is no built-in feature for Android, so we need to use an app. If I am mistaken, please correct me ([Coffmann](https://github.com/Coffmann)).*

##### Installation

There are many apps available.
Example apps:
- Tasker [Google Play](https://play.google.com/store/apps/details?id=net.dinglisch.android.taskerm&hl=de&gl=US)
- MacroDroid [Google Play](https://play.google.com/store/apps/details?id=com.arlosoft.macrodroid&hl=en&gl=US)
- Termux [GitHub](https://github.com/termux/termux-app)

But for these instructions, we will use the free app "MacroDroid"

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
9. Now, insert the command `docker run --rm -e ACTION=starten moodle-auto-clock_image`, then press "OK".
10. OPTIONAL: Customize constraints using the plus (+) symbol within the green tile labeled "Constraints".
11. Press the "Back" arrow in the top-left corner, then click "Save" in the pop-up message. You're done!

To view all your saved macros, navigate to the "Macros" tab at the bottom of the Main Menu.

---

## Usage Notice

This tool was developed solely for educational purposes as part of my vocational
training as an Application Development IT Specialist. It is a private project.

Use of this tool is at your own risk. I assume no liability for any consequences
that may arise from using this tool, such as technical issues, violations of
institutional guidelines, or conflicts with organizations.

Please ensure that the use of this tool complies with the rules and policies of
your school, organization, or learning platform.

## Hinweis zur Nutzung

Dieses Tool wurde ausschließlich zu Bildungszwecken im Rahmen meiner Weiterbildung
als Fachinformatiker Anwendungsentwicklung entwickelt. Es handelt sich um ein
privates Projekt.

Die Nutzung erfolgt auf eigene Verantwortung. Ich übernehme keinerlei Haftung
für Konsequenzen, die durch den Einsatz dieses Tools entstehen können, wie
beispielsweise technische Probleme, Richtlinienverstöße oder Konflikte mit
Organisationen.

Bitte stelle sicher, dass der Einsatz dieses Tools mit den geltenden Regeln
deiner Schule, Organisation oder Lernplattform vereinbar ist.
