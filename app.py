from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from departments import humanities_departments, science_departments
from score_converter import convert_to_hongik_score, is_humanities

app = Flask(__name__)

def evaluate_admission_chances(total_score, department):
    departments = humanities_departments if is_humanities(department) else science_departments
    
    if department not in departments:
        return {
            "status": "error",
            "message": "학과 정보를 찾을 수 없습니다."
        }
    
    cutoffs = departments[department]
    
    if total_score >= cutoffs["safe"]:
        return {
            "status": "safe",
            "probability": 90,
            "message": "안정권입니다.",
            "color": "#28a745"
        }
    elif total_score >= cutoffs["expected"]:
        return {
            "status": "expected",
            "probability": 70,
            "message": "예상 합격권입니다.",
            "color": "#17a2b8"
        }
    elif total_score >= cutoffs["challenge"]:
        return {
            "status": "challenge",
            "probability": 30,
            "message": "소신 지원권입니다.",
            "color": "#ffc107"
        }
    else:
        return {
            "status": "risky",
            "probability": 10,
            "message": "합격 확률이 매우 낮습니다.",
            "color": "#dc3545"
        }

@app.route('/')
def home():
    humanities = list(humanities_departments.keys())
    sciences = list(science_departments.keys())
    return render_template('index.html', humanities=humanities, sciences=sciences)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    
    # 점수 변환
    converted_scores = convert_to_hongik_score(data)
    if "error" in converted_scores:
        return jsonify(converted_scores), 400
        
    # 학과별 합격 가능성 평가
    total_score = converted_scores["total_score"]
    department = data["department"]
    
    result = evaluate_admission_chances(total_score, department)
    result.update(converted_scores)
    
    return jsonify(result)

# Vercel Serverless Functions를 위한 WSGI 앱 노출
app.debug = True
