def parse_user_input_to_structure(text_input):
    # Mocked version until GPT is hooked up
    return {
        "credit_utilization": 0.7,
        "late_payments": 1,
        "inquiries": 2,
        "credit_age": 1.5,
        "has_credit_mix": False
    }

def generate_credit_advice(input_data):
    return "Try reducing your credit card usage to below 30% and avoid new credit inquiries for a few months."