import os
from urllib.parse import quote_from_bytes

import openai
from dotenv import load_dotenv
from flask import Flask, request, jsonify

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)


# Load OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_SECRET_KEY')
if not openai.api_key:
    raise ValueError('OpenAI API key not set. Set the OPENAI_SECRET_KEY environment variable.')

engine = "gpt-3.5-turbo-instruct",
expected_api_key = os.getenv('EXPECTED_API_KEY')  # Replace with your expected API key


@app.route('/gpt/', methods=['POST'])
def get_gpt_response():
    try:
        # Get API key from request header
        provided_api_key = request.json.get('api_key')

        # Verify API key
        if provided_api_key != expected_api_key:
            return jsonify({'error': 'Invalid API key.'}), 401

        # Get input_text from the request
        input_text = request.json.get('input_text')
        print("Input text:", input_text)

        # Ensure input_text is not empty
        if not input_text:
            return jsonify({'error': 'Input text not provided.'}), 400

            # Encode input_text to bytes
        input_bytes = input_text.encode('utf-8')

        # Construct user context
        user_context = f"As a Kerala farmer, I need assistance with agricultural irrigation and related activities. {quote_from_bytes(input_bytes)}"

        # Generate GPT response
        print("Generating GPT response...", user_context)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use the appropriate model name
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user",
                 "content": f"As a Kerala farmer, I need assistance with agricultural irrigation and related activities. {input_text}. "
                            f"Dont use any kind of formatting in response make it  short also"}
            ],
            max_tokens=150,  # Adjust as needed
            temperature=0.7,  # Adjust as needed
            stop=None  # Custom stopping criteria if needed
        )
        print(type(response))

        gpt_response = response.choices[0]['message']['content']
        print(gpt_response)

        # Return the GPT response
        return jsonify({'gpt_response': gpt_response})

    except Exception as e:
        print(f'An error occurred: {str(e)}')
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True)
