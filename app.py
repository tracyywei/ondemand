from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)
client = OpenAI()

@app.route("/")
def start():
    return render_template('index.html')

def provide_resources():
    instructions = """
    Provide me with a list of legal aid housing organizations in Palo Alto with website URL, physical address, phone number, and short description, if available.
    """

    response = client.responses.create(
        model="gpt-4o",
        input=instructions
    )
    return response.output_text

@app.route("/intake_form", methods=["POST"])
def intake_form():
    data = request.get_json()
    transcript = data.get("transcript")
    print("TRANSCRIPT")
    print(transcript)

    instructions = """
    You are an intake form writer. Your goal is to produce an intake form in the (FORM) format using the information from (TRANSCRIPT). As the output, you will ONLY return the intake form. 

    When constructing the 3-4 sentence legal problem summary in the intake form, please use the following instructions:
    1. The first sentence should be a concise, up-front statement that summarizes what the client wants from an attorney
    2. The next sentences should provide only relevant background information
    3. In the end, put the opposing party. For example if the opposing party was John Doe, this would be “OP: John Doe”

    FORM:
    Problem Category: [Insert problem category]

    [Insert legal problem summary here]

    PERSONAL INFORMATION
    Name: [Insert First and Last Name]
    Birth Date: [Insert Birth Date]
    Zip Code: [Insert Zip Code]

    FINANCIAL INFORMATION
    Family Size: [Insert Family Size]
    Annual Income: [Insert Annual Income]
    Percent of FPL: [Calculate percentage their income is of the federal poverty line]

    CONTACT INFORMATION: 
    Phone Number: [Insert Phone Number]
    Voicemail Okay: [Insert if voicemail is okay]
    SMS Okay: [insert if SMS is okay]
    Email: [Insert email]

    TRANSCRIPT:
    {}
    """.format(transcript)

    response = client.responses.create(
        model="gpt-4o",
        input=instructions
    )

    print(response.output_text)

    intake_form = response.output_text
    resources = provide_resources()
    return jsonify({"intake_form": intake_form, "resources": resources})

if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)