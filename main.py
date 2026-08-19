@app.route('/api/negotiate', methods=['POST'])
def negotiate():
    data = request.json
    msg = data.get('message', '').lower()
    
    # قائمة الكلمات المفتاحية
    start_keywords = ["انطلق", "ابدأ", "شغل", "تقرير"]
    price_keywords = ["سعر", "غالي", "بكم", "خصم"]

    if any(word in msg for word in start_keywords):
        return jsonify({"reply": "🚀 تم إطلاق الزواحف! التقرير المتقدم بـ 250 ريال. حول عبر PayPal للبدء."})
    
    elif any(word in msg for word in price_keywords):
        return jsonify({"reply": "الأسعار: 150 للأساسي، 250 للمتقدم. كل ريال هو استثمار في أرباحك."})
    
    else:
        return jsonify({"reply": "مرحباً! هل نبدأ بالتقرير الأساسي (150) أو الشامل (250)؟"})
