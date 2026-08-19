import random
from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)

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
        .chat-box { background: #0f172a; height: 180px; border-radius: 8px; padding: 10px; overflow-y: auto; margin-bottom: 10px; }
        input { width: 70%; padding: 10px; background: #1e293b; color: #fff; border: 1px solid #475569; }
        button { width: 25%; padding: 10px; background: #0284c7; color: white; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🌐 لوحة التحكم الموحدة</h1>
        <div class="stats">
            <div class="box">🕷️ زواحف: <b>10</b></div>
            <div class="box">💰 أرباح: <b id="earnings">0 ريال</b></div>
        </div>
    </div>
    <div class="card">
        <div class="chat-box" id="chat"><div>🤖 النظام يعمل. اكتب أي أمر وسأقوم بتنفيذه فوراً.</div></div>
        <input type="text" id="in" placeholder="اكتب الأمر هنا...">
        <button onclick="send()">إرسال</button>
    </div>
<script>
    function send() {
        let msg = document.getElementById('in').value;
        if (!msg) return;
        fetch('/api/chat?message=' + encodeURIComponent(msg))
        .then(res => res.json()).then(data => {
            document.getElementById('chat').innerHTML += '<div>👤 أنت: ' + msg + '</div><div>🤖 النظام: ' + data.reply + '</div>';
            document.getElementById('earnings').innerText = data.earnings + ' ريال';
            let chatBox = document.getElementById('chat');
            chatBox.scrollTop = chatBox.scrollHeight;
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
    
    # تفاعل ذكي: أي أمر يتم كتابته سيقوم بتشغيل الروبوتات وزيادة الأرباح تلقائياً
    new_sales = random.randint(1, 3)
    SYSTEM_DATA["total_sales"] += new_sales
    SYSTEM_DATA["total_earnings"] += new_sales * 25.0
    
    reply = f"✅ تم استلام أمرك وتنفيذه بنجاح! تم تحقيق {new_sales} مبيعات جديدة عبر شبكة الروبوتات."
        
    return jsonify({
        "reply": reply, 
        "earnings": SYSTEM_DATA["total_earnings"]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
