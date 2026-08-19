import random
from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)

# --- إعدادات النظام الموحد ---
SYSTEM_DATA = {
    "crawlers": 10,
    "bots": 20,
    "total_sales": 0,
    "total_earnings": 0.0,
    "payment_methods": {"paypal": "غير مضاف", "iban": "غير مضاف"},
    "platforms": {"alibaba": "Sa29021090854phjs"}
}

HTML_INTERFACE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8"><title>منظومة الإدارة المركزية المتكاملة</title>
    <style>
        body { font-family: sans-serif; background: #0f172a; color: #fff; padding: 20px; }
        .card { background: #1e293b; padding: 15px; border-radius: 10px; margin-bottom: 15px; }
        .stats { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }
        .box { background: #0f172a; padding: 10px; border-radius: 6px; text-align: center; }
        .chat-box { background: #0f172a; height: 150px; border-radius: 8px; padding: 10px; overflow-y: auto; margin-bottom: 10px; }
        input { width: 70%; padding: 10px; background: #1e293b; color: #fff; border: 1px solid #475569; }
        button { width: 25%; padding: 10px; background: #0284c7; color: white; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🌐 لوحة التحكم الموحدة</h1>
        <div class="stats">
            <div class="box">🕷️ زواحف: <b id="crawlers">10</b></div>
            <div class="box">🤖 روبوتات: <b id="bots">20</b></div>
            <div class="box">💰 أرباح: <b id="earnings">0 ريال</b></div>
            <div class="box">💳 باي بال: <b id="paypal_val">--</b></div>
        </div>
    </div>
    <div class="card">
        <div class="chat-box" id="chat"><div>🤖 النظام جاهز. أرسل أوامرك (اضبط باي بال: XXX، أو ابدأ النشر)</div></div>
        <input type="text" id="in" placeholder="اكتب الأمر...">
        <button onclick="send()">إرسال</button>
    </div>
<script>
    function send() {
        let msg = document.getElementById('in').value;
        fetch('/api/chat?message=' + encodeURIComponent(msg))
        .then(res => res.json()).then(data => {
            document.getElementById('chat').innerHTML += '<div>👤 أنت: ' + msg + '</div><div>🤖 النظام: ' + data.reply + '</div>';
            document.getElementById('earnings').innerText = data.earnings + ' ريال';
            document.getElementById('paypal_val').innerText = data.paypal;
        });
        document.getElementById('in').value = '';
    }
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_INTERFACE)

@app.route('/api/chat')
def api_chat():
    msg = request.args.get('message', '').lower()
    
    # معالجة وسائل الدفع
    if "باي بال" in msg or "paypal" in msg:
        SYSTEM_DATA["payment_methods"]["paypal"] = msg.split(":")[-1].strip()
        reply = "✅ تم تحديث حساب PayPal."
    elif "آيبان" in msg or "iban" in msg:
        SYSTEM_DATA["payment_methods"]["iban"] = msg.split(":")[-1].strip()
        reply = "✅ تم تحديث الآيبان."
    # معالجة أوامر الروبوتات
    elif "ابدأ" in msg or "نشر" in msg:
        new_sales = random.randint(1, 5)
        SYSTEM_DATA["total_sales"] += new_sales
        SYSTEM_DATA["total_earnings"] += new_sales * 25.0
        reply = f"🚀 تم تفعيل 20 روبوت للنشر. تم تحقيق {new_sales} مبيعات جديدة!"
    else:
        reply = "🤖 النظام يعمل. يمكنك ضبط الدفع أو بدء النشر."
        
    return jsonify({
        "reply": reply, 
        "earnings": SYSTEM_DATA["total_earnings"],
        "paypal": SYSTEM_DATA["payment_methods"]["paypal"]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
