@app.route('/api/negotiate', methods=['POST'])
def negotiate():
    data = request.json
    msg = data.get('message', '').lower()
    
    # 1. فهم طلب بدء العمل
    if any(word in msg for word in ["انطلق", "ابدأ", "جيب", "تحليلات", "نتائج"]):
        reply = (f"🚀 جاري إطلاق 10 زواحف ذكية لمسح السوق وتحليل المنتجات الأكثر مبيعاً الآن... "
                 f"سيجهز التقرير المتقدم الشامل (250 ريال) خلال دقائق. "
                 f"هل تود تأكيد الطلب بالتحويل على PayPal: {STORE_CONFIG['paypal_email']}؟")
    
    # 2. فهم الاستفسار عن الأسعار
    elif any(word in msg for word in ["غالي", "سعر", "بكم", "خصم"]):
        reply = ("لدينا تقرير أساسي بـ 150 ريال، وتقرير متقدم وشامل بـ 250 ريال. "
                 "التقرير المتقدم يعطيك بيانات حقيقية عن الموردين وحجم الطلب المتوقع. أيهما تختار؟")
    
    # 3. التأكيد النهائي
    elif "250" in msg or "متقدم" in msg:
        reply = f"اختيار ممتاز! حول 250 ريال على PayPal: {STORE_CONFIG['paypal_email']} وأرسل الإيصال لنباشر العمل فوراً."
    elif "150" in msg or "أساسي" in msg:
        reply = f"تم الحجز! حول 150 ريال على PayPal: {STORE_CONFIG['paypal_email']} وأرسل الإيصال لنبدأ بالتقرير الأساسي."
    
    else:
        reply = "أنا هنا لمساعدتك في الحصول على تقرير تحليل سوق احترافي. هل نطلق الزواحف ونبدأ التحليل الآن بـ 250 ريال (متقدم)؟"
        
    return jsonify({"reply": reply})
