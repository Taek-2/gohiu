from departments import humanities_departments, science_departments, english_conversion, history_conversion

def is_humanities(department):
    """학과가 인문계열인지 확인"""
    return department in humanities_departments

def convert_to_hongik_score(raw_scores):
    """
    수능 표준점수를 홍익대학교 환산점수로 변환
    
    raw_scores = {
        'korean': 표준점수(0-200),
        'math': 표준점수(0-200),
        'english': 등급(1-9),
        'history': 등급(1-9),
        'select1': 표준점수(0-200),
        'select2': 표준점수(0-200),
        'department': 학과명
    }
    """
    
    # 영어 등급별 환산점수
    english_score = english_conversion[raw_scores['english'] - 1]
    
    # 한국사 등급별 가산점
    history_score = history_conversion[raw_scores['history'] - 1]
    
    # 인문/자연 구분
    is_human = is_humanities(raw_scores['department'])
    
    # 기본 점수 변환
    if is_human:
        # 인문계열 점수 계산
        converted = {
            'korean': raw_scores['korean'] * 0.3,    # 국어 30%
            'math': raw_scores['math'] * 0.3,        # 수학 30%
            'select': (raw_scores['select1'] + raw_scores['select2']) * 0.25,  # 탐구 25%
            'english': english_score * 0.15,         # 영어 15%
            'history': history_score                 # 한국사 가산점
        }
    else:
        # 자연계열 점수 계산
        converted = {
            'korean': raw_scores['korean'] * 0.2,    # 국어 20%
            'math': raw_scores['math'] * 0.35,       # 수학 35%
            'select': (raw_scores['select1'] + raw_scores['select2']) * 0.3,   # 탐구 30%
            'english': english_score * 0.15,         # 영어 15%
            'history': history_score                 # 한국사 가산점
        }
    
    # 총점 계산
    total_score = (
        converted['korean'] +
        converted['math'] +
        converted['select'] +
        converted['english'] +
        converted['history']
    )
    
    return {
        'converted_scores': converted,
        'total_score': round(total_score, 2)
    }
