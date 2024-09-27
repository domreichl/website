import os, sys
from flask import Flask, jsonify, request

sys.path.insert(0, os.path.dirname(__file__))

app = Flask(__name__)


@app.route("/")
def welcome():
    return "<p>Welcome to my app.</p>"


@app.route("/run-python", methods=["POST"])
def run_python():
    concept = request.json.get("input_value")

    concept_is_valid = concept in ["freedom", "morality"]

    if concept_is_valid:
        return jsonify({"result": f"You chose '{concept}'"})
    else:
        return (
            jsonify({"error": f"Invalid input value: {concept}; {type(concept)}"}),
            400,
        )


if __name__ == "__main__":
    app.run(debug=False)
