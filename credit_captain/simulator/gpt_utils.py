import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def parse_user_input_to_structure(text_input):
    prompt = f"""
Extract these values from the following description:
- credit_utilization (float from 0 to 1)
- late_payments (int)
- inquiries (int)
- credit_age (float, in years)
- has_credit_mix (true or false)

Text: "{text_input}"

Respond only with a valid Python dictionary.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    output = response['choices'][0]['message']['content']
    try:
        return eval(output)
    except:
        return {
            "credit_utilization": 0.7,
            "late_payments": 1,
            "inquiries": 1,
            "credit_age": 1.5,
            "has_credit_mix": False
        }

def generate_credit_advice(data):
    prompt = f"""
A user has:
- Utilization: {data['credit_utilization']*100:.0f}%
- Late payments: {data['late_payments']}
- Inquiries: {data['inquiries']}
- Credit age: {data['credit_age']} years
- Credit mix: {data['has_credit_mix']}

Give them 2-3 clear and helpful tips to improve their credit score.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )

    return response['choices'][0]['message']['content']