from flask import Flask, request, jsonify
import pandas as pd
import random

app = Flask(__name__)

# טעינת המאגרים לזיכרון (מהירות תגובה מקסימלית)
try:
    # 1. טעינת המאגר המסונן (הקובץ החדש) - המקור היחיד לצירופים מאושרים
    # אנחנו הופכים אותו ל-Set של Tuples כדי לאפשר בדיקת קיום (Look-up) ב-O(1)
    potential_df = pd.read_csv('Potential_Wins.csv')
    # ממירים כל שורה ל-tuple ממוין כדי שהחיפוש יהיה מדויק
    approved_combos = set(tuple(sorted(row)) for row in potential_df.values)
    
    # 2. טעינת ההיסטוריה (רק לצורך מתן הסבר למה משהו נפסל)
    history_df = pd.read_csv('Lotto.csv')
    history_sets = [set(map(int, row)) for row in history_df.iloc[:, 2:8].values]
    
    print(f"Server Ready. Loaded {len(approved_combos)} approved combinations.")
except Exception as e:
    print(f"Error initializing server: {e}")

# --- לוגיקה לבדיקת סיבת הפסילה ---
def get_rejection_reason(nums):
    user_set = set(nums)
    # בדיקה אם זה זכה בעבר
    for i, hist in enumerate(history_sets):
        match = len(user_set.intersection(hist))
        if match == 6:
            return f"נפסל: הצירוף זכה בעבר (הגרלה {history_df.iloc[i, 0]})"
        if match == 5:
            return "נפסל: דמיון גבוה מדי (5 מספרים) לזכייה היסטורית"
    
    # אם לא נמצא בהיסטוריה אבל עדיין לא ב-approved, סימן שנפסל בגלל מבנה
    return "נפסל: מבנה סטטיסטי חלש (רצפים, פיזור לא תקין או דמיון ל-100 האחרונות)"

# --- API Endpoints ---

@app.route('/api/check', methods=['POST'])
def check_numbers():
    """
    אפשרות 1: בדיקה אם הצירוף קיים בקובץ החדש
    קלט: {"numbers": [1, 2, 3, 4, 5, 6]}
    """
    data = request.json
    nums = sorted(data.get('numbers', []))
    
    if len(nums) != 6:
        return jsonify({"status": "error", "message": "יש לספק 6 מספרים"}), 400

    combo_tuple = tuple(nums)
    
    if combo_tuple in approved_combos:
        return jsonify({
            "status": "approved",
            "message": "הצירוף מאושר! הוא נמצא במאגר הצירופים בעלי הפוטנציאל הגבוה."
        })
    else:
        reason = get_rejection_reason(nums)
        return jsonify({
            "status": "rejected",
            "message": reason
        })

@app.route('/api/suggest/coverage', methods=['GET'])
def get_coverage():
    """
    אפשרות 2: 200 מספרים עם הכיסוי הגדול ביותר
    """
    count = int(request.args.get('count', 200))
    # דגימה מתוך הרשימה הלבנה
    sample = random.sample(list(approved_combos), min(count, len(approved_combos)))
    return jsonify({"suggestions": sample})

@app.route('/api/suggest/top-stat', methods=['GET'])
def get_top_stat():
    """
    אפשרות 3: הצירופים מהקובץ החדש שמכילים את המספרים הכי נפוצים
    """
    # מציאת 10 המספרים הכי נפוצים בהיסטוריה
    all_past_nums = [n for s in history_sets for n in s]
    top_10 = pd.Series(all_past_nums).value_counts().head(10).index.tolist()
    
    # חיפוש צירופים במאגר החדש שמכילים לפחות 3 מהמספרים האלו
    results = []
    top_10_set = set(top_10)
    for combo in approved_combos:
        if len(set(combo).intersection(top_10_set)) >= 3:
            results.append(combo)
        if len(results) >= 50: break
            
    return jsonify({"top_statistical_suggestions": results})

if __name__ == '__main__':
    # הרצה על פורט 5000
    app.run(host='0.0.0.0', port=5000)