from django.shortcuts import render
from .gpt_utils import parse_user_input_to_structure, generate_credit_advice

def calculate_credit_score(data):
    score = 680
    if data["late_payments"] > 0:
        score -= data["late_payments"] * 15
    if data["credit_utilization"] > 0.3:
        score -= int((data["credit_utilization"] - 0.3) * 100)
    if data["credit_age"] < 2:
        score -= 20
    score -= data["inquiries"] * 5
    if data["has_credit_mix"]:
        score += 10
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