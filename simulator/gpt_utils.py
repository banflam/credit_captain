import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def parse_user_input_to_structure(user_input):
    prompt = f"""
You are a financial assistant. Given the user's natural language description of their financial behavior, do the following:

1. Extract structured data needed to simulate a credit score.
2. Write a brief explanation to help the user understand how these behaviors affect their score.

Output your response using this exact format:

<json>
{{
  "credit_utilization": float (0.0 - 1.0),
  "late_payments": integer,
  "inquiries": integer,
  "credit_age": float (in years),
  "has_credit_mix": boolean
}}
</json>
<explanation>
Explanation in 2-3 sentences.
</explanation>

User input: "{user_input}"
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that outputs structured JSON and explanations."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
    )

    content = response.choices[0].message.content

    try:
        json_start = content.find("<json>") + len("<json>")
        json_end = content.find("</json>")
        explanation_start = content.find("<explanation>") + len("<explanation>")
        explanation_end = content.find("</explanation>")

        structured_data = json.loads(content[json_start:json_end].strip())
        explanation = content[explanation_start:explanation_end].strip()

        print("GPT structured data:", structured_data)
        print("GPT explanation:", explanation)

        return {
            "structured": structured_data,
            "explanation": explanation
        }

    except Exception as e:
        print("Error parsing GPT response:", e)
        return {
            "structured": {
                "credit_utilization": 0.3,
                "late_payments": 0,
                "inquiries": 1,
                "credit_age": 2.0,
                "has_credit_mix": False
            },
            "explanation": "Default values were used due to a parsing issue. Try rephrasing your input."
        }

def generate_credit_advice(data):
    prompt = f"""
You’re a financial advisor. Based on this user's credit profile, give them short, friendly advice to improve their credit score.

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
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()