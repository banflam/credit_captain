from django.shortcuts import render
from .gpt_utils import parse_user_input_to_structure, generate_credit_advice

def calculate_credit_score(data):
    # Set defaults if keys are missing or values are None
    credit_utilization = data.get("credit_utilization") or 0.3
    late_payments = data.get("late_payments") or 0
    inquiries = data.get("inquiries") or 1
    credit_age = data.get("credit_age") or 2.0
    has_credit_mix = data.get("has_credit_mix")
    if has_credit_mix is None:
        has_credit_mix = False

    score = 680 # sane starting score

    # Utilization: High impact
    if credit_utilization >= 0.9:
        score -= 120
    elif credit_utilization >= 0.75:
        score -= 90
    elif credit_utilization >= 0.5:
        score -= 60
    elif credit_utilization >= 0.3:
        score -= 30
    else:
        score += 10  # Reward for low utilization

    # Late payments: Major impact
    score -= late_payments * 50

    # Credit inquiries: Moderate
    score -= inquiries * 10

    # Credit age: Older is better
    if credit_age < 1:
        score -= 40
    elif credit_age < 3:
        score -= 20
    elif credit_age > 5:
        score += 10

    # Credit mix: Minor boost
    if has_credit_mix:
        score += 10

    return max(300, min(score, 850))

def get_score_tier(score):
    if score >= 800: return "Excellent"
    elif score >= 740: return "Very Good"
    elif score >= 670: return "Good"
    elif score >= 580: return "Fair"
    else: return "Poor"

def home(request):
    score = None
    explanation = None
    advice = None
    user_input = ""
    tier = None

    if request.method == "POST":
        user_input = request.POST.get("input_text", "")
        result = parse_user_input_to_structure(user_input)
        data = result["structured"]
        explanation = result["explanation"]
        score = calculate_credit_score(data)
        tier = get_score_tier(score)
        advice = generate_credit_advice(data)
        
    context = {
        "score": score,
        "tier": tier,
        "explanation": explanation,
        "advice": advice,
        "user_input": user_input,
    }

    return render(request, "simulator/home.html", context)