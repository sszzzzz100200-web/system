from flask import Flask, render_template_string, jsonify, request
import random

app = Flask(__name__)

STORE_CONFIG = {
    "paypal_email": "sszzzzz100400@gmail.com"
}

# ذاكرة مؤقتة لتتبع حالة العميل (لعدم تكرار نفس الرد)
user_sessions = {}

HTML_CHAT = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8"><title>مستشار ذكاء المبيعات</title>
    <style>
        body { font-family: sans-serif; background: #0f172a; color: #fff; padding: 20px; }
        .card { background: #1e293b; padding: 20px; border-radius: 10px; border: 1px solid #334155; max-width: 600px; margin: auto; }
        .chat-box { background: #0b0f19; height: 350px; border-radius: 8px; padding: 15px; overflow-y: auto; margin-bottom: 15px; border: 1px solid #334155; }
        .msg-bot { color: #38bdf8; margin-bottom: 12px; line-height: 1.6; }
        .msg-user { color: #4ade80; margin-bottom: 12px; text-align: left; }
        input { width: 75%; padding: 12px; background: #1e293b; color: #fff; border: 1px solid #475569; border-radius: 6px; }
        button { width: 20%; padding: 12px; background: #059669; color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; }
    </style>
</head>
<body>
    <div class="card">
        <h2>💼 مستشار تحليل المتاجر الذكي</h2>
        <div class="chat-box" id="chat">
            <div class="msg-bot">🤖 أهلاً بك يا غالي! أنا نظام استخبارات السوق. هل حابب نكتشف المنتجات الأكثر مبيعاً اليوم لترفع أرباح متجرك؟ اسألني أو قل "انطلق".</div>
        </div>
        <input type="text" id="in" placeholder="اكتب استفسارك أو طلبك هنا..." onkeypress="if(event.key === 'KeyE' || event.keyCode==13) send();">
        <button onclick="send()">إرسال</button>
    </div>

<script>
    let userId = 'user_' + Math.random(); // معرف جلسة فريد لكل متصفح
    function send() {
        let msg = document.getElementById('in').value;
        if(!msg.trim()) return;
        let chat = document.getElementById('chat');
        chat.innerHTML += `<div class="msg-user">👤 أنت: ${msg}</div>`;
        
        fetch('/api/negotiate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({message: msg, user_id: userId})
        })
        .then(res => res.json())
        .then(data => {
            chat.innerHTML += `<div class="msg-bot">🤖 المساعد: ${data.reply}</div>`;
            chat.scrollTop = chat.scrollHeight;
        });
        document.getElementById('in').value = '';
    }
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_CHAT)

@app.route('/api/negotiate', methods=['POST'])
def negotiate():
    data = request.json
    msg = data.get('message', '').lower()
    user_id = data.get('user_id', 'default')
    
    # تهيئة الذاكرة للجلسة إذا كانت جديدة
    if user_id not in user_sessions:
        user_sessions[user_id] = {"step": 0}
    
    session = user_sessions[user_id]
    session["step"] += 1

    # 1. إذا طلب البدء أو انطلق
    if any(word in msg for word in ["انطلق", "ابدأ", "شغل", "تقرير", "تمام", "اوك", "ايوة"]):
        reply = (
            "🚀 خطوة ممتازة! قمنا بتفعيل محركات البحث والزواحف لاستخراج بيانات السوق الحصرية.\n\n"
            f"🔹 **التقرير المتقدم الشامل:** 250 ريال.\n"
            f"🔹 **طريقة الدفع:** تحويل مباشر على حساب PayPal: <b>{STORE_CONFIG['paypal_email']}</b>\n\n"
            "أرسل لي إيصال التحويل هنا فور إتمامه لنرسل لك التقرير فوراً!"
        )
    # 2. الاستفسار عن السعر أو التخفيض
    elif any(word in msg for word in ["سعر", "غالي", "بكم", "خصم", "كم"]):
        reply = (
            "الأسعار مدروسة لتناسب حجم أرباحك:\n"
            "1️⃣ **التقرير الأساسي:** 150 ريال (يكشف لك المنافسين والترند).\n"
            "2️⃣ **التقرير المتقدم:** 250 ريال (يكشف لك الموردين وأعلى المنتجات ربحية).\n\n"
            "أي الباقتين تفضل أن نجهزها لمتجرك اليوم؟"
        )
    # 3. ردود ذكية ومتنوعة بناءً على عدد المحادثات لكسر التكرار تماماً
    else:
        smart_fallbacks = [
            "أنا معك أستاذي، السوق فيه فرص ذهبية اليوم. هل تحب نبدأ بالتقرير الأساسي (150) أو الشامل (250)؟",
            "فهمت عليك. لكي نبدأ استخراج البيانات الحقيقية لمتجرك، تفضل باختيار الباقة المناسبة وقم بالتحويل على PayPal لنباشر العمل.",
            "كل دقة تحليل توفر عليك خسائر في بضاعة راكدة. هل نعتمد التقرير المتقدم بـ 250 ريال وننطلق؟"
        ]
        reply = smart_fallbacks[session["step"] % len(smart_fallbacks)]

    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
