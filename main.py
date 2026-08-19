from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)

STORE_CONFIG = {
    "paypal_email": "sszzzzz100400@gmail.com",
    "prices": {
        "basic": 150.0,
        "advanced": 250.0
    }
}

HTML_CHAT = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8"><title>مساعد مبيعات التحليلات الذكي</title>
    <style>
        body { font-family: sans-serif; background: #0f172a; color: #fff; padding: 20px; }
        .card { background: #1e293b; padding: 20px; border-radius: 10px; border: 1px solid #334155; max-width: 600px; margin: auto; }
        .chat-box { background: #0b0f19; height: 300px; border-radius: 8px; padding: 15px; overflow-y: auto; margin-bottom: 15px; border: 1px solid #334155; }
        .msg-bot { color: #38bdf8; margin-bottom: 10px; }
        .msg-user { color: #4ade80; margin-bottom: 10px; text-align: left; }
        input { width: 75%; padding: 10px; background: #1e293b; color: #fff; border: 1px solid #475569; border-radius: 6px; }
        button { width: 20%; padding: 10px; background: #0284c7; color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🤖 مفاوض مبيعات تقارير السوق</h2>
        <div class="chat-box" id="chat">
            <div class="msg-bot">🤖 أهلاً بك! أنا هنا لمساعدتك في اختيار تحليل السوق المناسب لمتجرك لزيادة مبيعاتك. كيف يمكنني خدمتك اليوم؟</div>
        </div>
        <input type="text" id="in" placeholder="اكتب ردك أو سؤالك عن السعر هنا...">
        <button onclick="send()">إرسال</button>
    </div>

<script>
    function send() {
        let msg = document.getElementById('in').value;
        if(!msg) return;
        let chat = document.getElementById('chat');
        chat.innerHTML += `<div class="msg-user">👤 أنت: ${msg}</div>`;
        
        fetch('/api/negotiate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({message: msg})
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
    
    # منطق التفاوض والردود الذكية
    if "غالي" in msg or "خفض" in msg or "خصم" in msg or "سعر" in msg:
        reply = (f"أقدر حرصك على ميزانية متجرك! لكن تذكر أن تقرير تحليل السوق يوفر عليك آلاف الريالات من الخسائر في بضاعة قد لا تُباع. "
                 f"لدينا باقتان: التقرير الأساسي بـ 150 ريال، والتقرير المتقدم الشامل بـ 250 ريال. "
                 f"أي الباقتين تفضل لنجهّزها لك فوراً وتحول رسومها عبر PayPal على: {STORE_CONFIG['paypal_email']}؟")
    elif "150" in msg or "باسيك" in msg or "الأساسي" in msg:
        reply = f"اختيار ممتاز! التقرير الأساسي بـ 150 ريال. يرجى تحويل المبلغ فوراً على حساب PayPal: <b>{STORE_CONFIG['paypal_email']}</b>، وبعد التحويل أرسل لي إيصال الدفع هنا لأرسل لك التقرير حالاً."
    elif "250" in msg or "متقدم" in msg or "الشامل" in msg:
        reply = f"اختيار احترافي يعطيك نظرة شاملة وكاملة للسوق! التقرير المتقدم بـ 250 ريال. حول المبلغ على PayPal: <b>{STORE_CONFIG['paypal_email']}</b> وأرسل الإيصال لنبدأ العمل."
    else:
        reply = "نحن نقدم تحليلات سوق حقيقية ترفع أرباح متجرك على سلة أو زد. هل تحب نبدأ بالتقرير الأساسي بـ 150 ريال أم التقرير الشامل بـ 250 ريال؟"
        
    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
