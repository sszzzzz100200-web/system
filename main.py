import random

@app.route('/api/negotiate', methods=['POST'])
def negotiate():
    data = request.json
    msg = data.get('message', '').lower()
    
    # ردود متنوعة (Randomized Responses) لكسر التكرار
    responses = {
        "start": [
            "🚀 بدأت فعلياً! الزواحف تعمل الآن، التقرير المتقدم بـ 250 ريال، جاهز للبدء؟",
            "تم إطلاق محركات التحليل. التقرير بانتظار تأكيدك (250 ريال). حول على PayPal وأرسل الإيصال.",
            "جاري مسح بيانات السوق... التقرير المتقدم (250) هو خيارك الأفضل للنتائج الحقيقية. نعتمد؟"
        ],
        "price": [
            "السعر 150 للأساسي أو 250 للمتقدم. البيانات التي ستحصل عليها تساوي أضعاف هذا المبلغ في أرباحك.",
            "ميزانيتك في محل تقدير، ولكن تذكر أن التقرير يوفر عليك خسائر البضاعة الراكدة. 150 أم 250 ريال؟",
            "استثمار بسيط مقابل معرفة 'الذهب' في السوق. أيهما يناسب متجرك الآن؟"
        ],
        "fallback": [
            "أسمعك، هل نبدأ بـ 150 أم 250 ريال؟",
            "القرار بيدك، هل نعتمد التقرير المتقدم (250 ريال) وننطلق؟",
            "أنا جاهز، هل نبدأ بالأساسي (150) أو المتقدم (250)؟"
        ]
    }

    # اختيار الرد بناءً على محتوى الرسالة
    if any(word in msg for word in ["انطلق", "ابدأ", "شغل", "تقرير"]):
        return jsonify({"reply": random.choice(responses["start"])})
    
    elif any(word in msg for word in ["سعر", "غالي", "بكم", "خصم"]):
        return jsonify({"reply": random.choice(responses["price"])})
    
    else:
        return jsonify({"reply": random.choice(responses["fallback"])})
