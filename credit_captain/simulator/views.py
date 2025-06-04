from django.shortcuts import render
from .gpt_utils import parse_user_input_to_structure, generate_credit_advice

def calculate_credit_score(data):
    score = 300  # Base score
    if data["late_payments"] > 0:
        score -= data["late_payments"] * 20
    score -= int(data["credit_utilization"] * 100)  # e.g., 0.3 = -30
    score -= data["inquiries"] * 5
    score += data["credit_age"] * 10
    if data["has_credit_mix"]:
        score += 20
    return max(300, min(score, 850))

def get_score_tier(score):
    if score >= 800: return "Excellent"
    elif score >= 740: return "Very Good"
    elif score >= 670: return "Good"
    elif score >= 580: return "Fair"
    else: return "Poor"

def home(request):
    if request.method == 'POST':
        user_input = request.POST.get('input_text')
        structured_data = parse_user_input_to_structure(user_input)
        
        print("GPT DATA:", structured_data)
        
        score = calculate_credit_score(structured_data)
        tier = get_score_tier(score)
        advice = generate_credit_advice(structured_data)

        return render(request, 'simulator/home.html', {
            'score': score,
            'tier': tier,
            'explanation': "Based on your profile, we've estimated your score.",
            'advice': advice,
        })

    return render(request, 'simulator/home.html')