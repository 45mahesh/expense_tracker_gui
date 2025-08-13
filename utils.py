from datetime import datetime

def get_today():
    return datetime.today().strftime('%Y-%m-%d')
