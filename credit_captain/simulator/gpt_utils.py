import os
import json
import openai
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

system_prompt = """
You are a financial assistant. Given a user's natural language input describing recent financial actions, 
extract structured data needed to simulate a credit score. Respond ONLY with a JSON object in this format:

{
  "credit_utilization": float (0.0 - 1.0),
  "late_payments": integer,
  "inquiries": integer,
  "credit_age": float (in years),
  "has_credit_mix": boolean
}

If a field is not clearly stated, use a smart default:
- credit_utilization: 0.3
- late_payments: 0
- inquiries: 1
- credit_age: 2.0
- has_credit_mix: false

Never explain or add text. Just output the JSON.
"""

def parse_user_input_to_structure(user_input):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input},
        ],
        temperature=0.2,
    )

    content = response.choices[0].message.content.strip()
    try:
        data = json.loads(content)
        print("GPT parsed data:", data)
        return data
    except json.JSONDecodeError:
        print("JSON parse error from GPT:", content)
        return {
            "credit_utilization": 0.3,
            "late_payments": 0,
            "inquiries": 1,
            "credit_age": 2.0,
            "has_credit_mix": False,
        }
        
def generate_credit_advice(data):
    prompt = f"""
    You're a financial advisor. Based on this user's credit profile, give them friendly advice on improving their credit score.

    User profile:
    - Late payments: {data.get("late_payments")}
    - Credit utilization: {data.get("credit_utilization")}
    - Inquiries: {data.get("inquiries")}
    - Credit age: {data.get("credit_age")}
    - Has credit mix: {data.get("has_credit_mix")}

    Advice:
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content