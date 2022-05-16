from flask import Flask, redirect, url_for, render_template
from flask_discord import DiscordOAuth2Session, requires_authorization
import os

HYPERLINK = '<a href="{}">{}</a>'
app = Flask(__name__)

app.secret_key = "my_super_secret_key" # TODO: Change this.
os.environ.setdefault("OAUTHLIB_INSECURE_TRANSPORT", "1")

app.config["DISCORD_CLIENT_ID"] = int() # put your client_id here.
app.config["DISCORD_CLIENT_SECRET"] = 'YOUR BOT SECRET HERE'
app.config["DISCORD_BOT_TOKEN"] = 'YOUR BOT TOKEN HERE'
app.config["DISCORD_REDIRECT_URI"] = "http://localhost:5040/callback"

discord = DiscordOAuth2Session(app)

@app.route("/")
def showMain():
    return render_template("main.html", Bot="Aweomse-Bot", login_page=url_for('login'))

@app.route('/login')
def login():
    return discord.create_session(scope=['identify', 'guilds'])

@app.route("/callback")
def callback():
    discord.callback()
    return redirect(url_for('.me'))

@app.route("/me")
@requires_authorization
def me():
    guilds = discord.fetch_guilds()
    return render_template('me.html', guilds=guilds)

if __name__ == "__main__":
    app.run(debug=True, port=5040)