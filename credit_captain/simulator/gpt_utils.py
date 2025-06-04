import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def parse_user_input_to_structure(text_input):
    prompt = f"""
Extract the following data from this user input:
- credit_utilization (float from 0.0 to 1.0)
- late_payments (int)
- inquiries (int)
- credit_age (float, in years)
- has_credit_mix (true/false)

Respond with only a valid Python dictionary.

Input:
{text_input}
"""

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
    )

    result_text = response.choices[0].message.content.strip()

    try:
        return eval(result_text)
    except:
        return {
            "credit_utilization": 0.6,
            "late_payments": 1,
            "inquiries": 1,
            "credit_age": 1.5,
            "has_credit_mix": False
        }

def generate_credit_advice(data):
    prompt = f"""
A user has:
- Credit Utilization: {data['credit_utilization']*100:.0f}%
- Late Payments: {data['late_payments']}
- Inquiries: {data['inquiries']}
- Credit Age: {data['credit_age']} years
- Credit Mix: {'Yes' if data['has_credit_mix'] else 'No'}

Give 2-3 friendly, practical suggestions to help improve their credit score.
"""

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
    )

    return response.choices[0].message.content.strip()