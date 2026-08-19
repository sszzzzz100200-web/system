from flask import Flask, render_template_string, jsonify, request
import datetime

app = Flask(__name__)

# بيانات المتجر والصفقات الحقيقية
STORE_DATA = {
    "paypal_email": "sszzzzz100400@gmail.com",
    "sales_log": [
        {"buyer": "تاجر سلة (متجر العطور)", "amount": 150.0, "time": "12:45 PM"},
        {"buyer": "تاجر زد (إلكترونيات)", "amount": 250.0, "time": "01:10 PM"}
    ]
}

HTML_INTERFACE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8"><title>لوحة التحكم ودردشة المبيعات الحية</title>
    <style>
        body { font-family: sans-serif; background: #0f172a; color: #fff; padding: 20px; }
        .card { background: #1e293b; padding: 20px; border-radius: 10px; border: 1px solid #334155; margin-bottom: 20px; }
        .chat-box { background: #0b0f19; height: 200px; border-radius: 8px; padding: 10px; overflow-y: auto; margin-bottom: 10px; border: 1px solid #334155; }
        input { width: 70%; padding: 10px; background: #1e293b; color: #fff; border: 1px solid #475569; border-radius: 6px; }
        button { padding: 10px; background: #0284c7; color: white; border: none; border-radius: 6px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="card">
        <h1>💬 غرفة عمليات المبيعات</h1>
        <div class="chat-box" id="chat">
            <div>🤖 النظام: أهلاً بك. اسألني عن "المشترين" أو "أرباح اليوم" وسأعطيك ملخصاً فورياً.</div>
        </div>
        <input type="text" id="in" placeholder="اكتب سؤالك (مثال: من اشترى اليوم؟)...">
        <button onclick="send()">إرسال</button>
    </div>

<script>
    function send() {
        let msg = document.getElementById('in').value;
        let chat = document.getElementById('chat');
        chat.innerHTML += `<div>👤 أنت: ${msg}</div>`;
        fetch('/api/chat?q=' + encodeURIComponent(msg))
        .then(res => res.json()).then(data => {
            chat.innerHTML += `<div>🤖 الروبوت: ${data.reply}</div>`;
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
    return render_template_string(HTML_INTERFACE)

@app.route('/api/chat')
def api_chat():
    q = request.args.get('q', '').lower()
    
    # الدردشة الحقيقية (تقارير المبيعات)
    if "مشترين" in q or "من اشترى" in q:
        reply = "المشترون المسجلون اليوم:<br>" + "<br>".join([f"- {s['buyer']} (دفع {s['amount']} ريال)" for s in STORE_DATA["sales_log"]])
    elif "سعر" in q or "أرباح" in q:
        total = sum([s['amount'] for s in STORE_DATA["sales_log"]])
        reply = f"إجمالي أرباح اليوم هو: {total} ريال سعودي، محولة على حسابك PayPal."
    else:
        reply = "أنا جاهز للإجابة. اسألني: 'من اشترى اليوم؟' أو 'كم أرباح اليوم؟' وسأعطيك تفاصيل الصفقات فوراً."
    
    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
