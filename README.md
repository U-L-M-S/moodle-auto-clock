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