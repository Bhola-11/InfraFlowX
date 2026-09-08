"""
Citizen Complaint NLP Keyword & Urgency Classifier
Scans incident and complaint narratives for public safety keywords and prioritizes SLA escalation.
"""
import re


class HelpdeskNLPEngine:
    KEYWORD_WEIGHTS = {
        'COLLAPSE': 10,
        'SINKHOLE': 10,
        'EXPLOSION': 10,
        'FLOOD': 8,
        'HAZARD': 7,
        'INJURY': 9,
        'ACCIDENT': 8,
        'CRACK': 6,
        'DEEP POTHOLE': 7,
        'GAS LEAK': 10,
        'WATER MAIN': 7,
        'OUTAGE': 5,
        'BROKEN': 4,
        'LIGHTING': 3,
        'GRAFFITI': 1
    }

    @classmethod
    def analyze_complaint_urgency(cls, text_content):
        text = text_content.upper()
        total_score = 0
        matched_keywords = []

        for kw, weight in cls.KEYWORD_WEIGHTS.items():
            if re.search(rf"{kw}", text):
                total_score += weight
                matched_keywords.append(kw)

        if total_score >= 15:
            priority = 'CRITICAL'
            sla_hours = 4
        elif total_score >= 8:
            priority = 'HIGH'
            sla_hours = 12
        elif total_score >= 4:
            priority = 'MEDIUM'
            sla_hours = 48
        else:
            priority = 'LOW'
            sla_hours = 96

        return {
            'urgency_score': total_score,
            'matched_keywords': matched_keywords,
            'recommended_priority': priority,
            'target_sla_response_hours': sla_hours
        }
