from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify(status="UP", message="Service is healthy"), 200

if __name__ == "__main__":
    # Run on port 5000 by default
    app.run(host="0.0.0.0", port=5000)
