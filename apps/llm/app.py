import os, string, sys
from flask import Flask, jsonify, request
from haystack.components.generators import HuggingFaceAPIGenerator
from haystack.utils import Secret

sys.path.insert(0, os.path.dirname(__file__))


def get_reply_from_llm(concept: str, token: str) -> str:
    generator = HuggingFaceAPIGenerator(
        api_type="serverless_inference_api",
        api_params={"model": "meta-llama/Meta-Llama-3-8B-Instruct"},
        token=Secret.from_token(token),
    )
    result = generator.run(
        prompt=f"Is the following string a philosophical concept? String: {concept}. Answer with 'yes' or 'no' only. Answer: ",
        generation_kwargs={"max_new_tokens": 8},
    )
    reply = result["replies"][0]
    concept_is_philosophical = "yes" in reply.lower()
    if concept_is_philosophical:
        result = generator.run(
            prompt=f"Here is a short paragraph of philosophical wisdom in the style of Spinoza on the topic of {concept}: ",
            generation_kwargs={"max_new_tokens": 100},
        )
        reply = (
            ".".join(result["replies"][0].split(".")[:-1])
            .replace('"', "")
            .replace("“", "")
            .lstrip(string.whitespace)
        ) + "."
    else:
        reply = f"'{concept}' is not a philosophical concept."
    return reply


app = Flask(__name__)


@app.route("/")
def welcome():
    return "<p>The LLM app is running.</p>"


@app.route("/run-python", methods=["POST"])
def run_python():
    concept = request.json.get("input_value")
    try:
        reply = get_reply_from_llm(concept, os.environ.get("HF_ACCESS_TOKEN"))
        return jsonify({"result": reply})
    except Exception as e:
        return (
            jsonify({"error": f"Unfortunately, the philosopher is currently asleep."}),
            400,
        )


if __name__ == "__main__":
    app.run(debug=False)
