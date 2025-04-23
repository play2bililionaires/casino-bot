from flask import Flask, render_template, request, jsonify
import random
import os
import threading

from os import getenv
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()

app = Flask(__name__)

# Slot symbols and payouts
SYMBOLS = ["7️⃣", "💎", "🎰", "🔔", "👞", "🍋", "🍉", "❤️", "🍒"]
PAYOUTS = {
    "7️⃣": {3: 500, 2: 25},
    "💎": {3: 25, 2: 10},
    "🎰": {3: 5, 2: 3},
    "🔔": {3: 3, 2: 2},
    "👞": {3: 2, 2: 1},
    "🍋": {3: 1, 2: 1},
    "🍉": {3: 0.75, 2: 1},
    "❤️": {3: 0.5, 2: 0.75},
    "🍒": {3: 0.5, 2: 0.25},
}

# Flask routes
@app.route("/")
def hello_world():
    return render_template("index.html", title="Hello")

@app.route("/slots", methods=["POST"])
def slots():
    bet = request.json.get("bet", 1)  # Default bet is 1 if not provided
    if not isinstance(bet, (int, float)) or bet <= 0:
        return jsonify({"error": "Invalid bet amount"}), 400

    # Simulate slot machine spin
    spin = [random.choice(SYMBOLS) for _ in range(3)]

    # Calculate payout
    counts = {symbol: spin.count(symbol) for symbol in set(spin)}
    payout = 0
    for symbol, count in counts.items():
        if count in PAYOUTS[symbol]:
            payout = max(payout, bet * PAYOUTS[symbol][count])

    return jsonify({"spin": spin, "payout": payout})

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True  
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def spin(ctx, bet: float = 1.0):
    if bet <= 0:
        await ctx.send("Invalid bet amount. Bet must be greater than 0.")
        return

    # Simulate slot machine spin
    spin = [random.choice(SYMBOLS) for _ in range(3)]

    # Calculate payout
    counts = {symbol: spin.count(symbol) for symbol in set(spin)}
    payout = 0
    for symbol, count in counts.items():
        if count in PAYOUTS[symbol]:
            payout = max(payout, bet * PAYOUTS[symbol][count])

    await ctx.send(f"Spin result: {' '.join(spin)}\nPayout: {payout}")

# Run both Flask and Discord bot
def run_flask():
    app.run(host="127.0.0.1", port=8080, debug=True, use_reloader=False)

def run_discord():
    bot.run(getenv("TOKEN"))

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    run_discord()
