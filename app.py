from flask import Flask, render_template, request, jsonify
import random

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

if __name__ == "__main__":
    app.run(debug=True)
