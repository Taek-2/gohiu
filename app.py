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
    return render_template('index.html', 
                         humanities=humanities_departments.keys(),
                         sciences=science_departments.keys())

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    
    # 수능 원점수를 홍대식 점수로 변환
    raw_scores = {
        'korean': float(data['korean']),
        'math': float(data['math']),
        'english': int(data['english']),
        'history': int(data['history']),
        'select1': float(data['select1']),
        'select2': float(data['select2']),
        'department': data['department']
    }
    
    converted = convert_to_hongik_score(raw_scores)
    result = evaluate_admission_chances(converted['total_score'], data['department'])
    
    return jsonify({
        'total_score': converted['total_score'],
        'converted_scores': converted['converted_scores'],
        **result
    })

if __name__ == '__main__':
    app.run(debug=True)
