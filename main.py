@app.route('/api/negotiate', methods=['POST'])
def negotiate():
    data = request.json
    msg = data.get('message', '').lower()
    
    # تحسين الفحص: إذا وجد أي حرف من كلماتك في رسالة المستخدم
    if any(word in msg for word in ["انطلق", "ابدأ", "شغل", "زاحف", "تحليلات", "تقرير"]):
        return jsonify({"reply": f"🚀 جاري إطلاق الزواحف! تم رصد 10 فرص تجارية في السوق الآن. التقرير المتقدم جاهز بـ 250 ريال. حول على PayPal: {STORE_CONFIG['paypal_email']} وأرسل الإيصال."})
    
    elif any(word in msg for word in ["سعر", "غالي", "بكم", "خصم", "ميزانية"]):
        return jsonify({"reply": "الأسعار استثمارية: 150 للأساسي، و250 للمتقدم. كل ريال تدفعه سيعود عليك بأضعاف في مبيعات متجرك. أيهما نعتمد؟"})
    
    else:
        # رد متنوع في حال لم يفهم الكلمة
        return jsonify({"reply": "أنا معك، اسمعك. هل نبدأ بـ 150 (أساسي) أو 250 (متقدم)؟"})
