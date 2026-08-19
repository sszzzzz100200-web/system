import os
from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)

HTML_INTERFACE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>الأداة المركزية v33.0</title>
    <style>
        body { font-family: sans-serif; background: #0b0f19; color: #fff; margin: 0; padding: 20px; }
        .header { background: #1e293b; padding: 15px; border-radius: 10px; text-align: center; font-size: 22px; font-weight: bold; margin-bottom: 20px; color: #38bdf8; }
        .card { background: #1e293b; padding: 15px; border-radius: 10px; margin-bottom: 15px; }
        .chat-box { background: #0f172a; height: 200px; border-radius: 8px; padding: 10px; overflow-y: auto; margin-bottom: 10px; border: 1px solid #334155; }
        input[type="text"] { width: 75%; padding: 10px; border-radius: 6px; border: 1px solid #475569; background: #1e293b; color: #fff; }
        button { width: 20%; padding: 10px; border-radius: 6px; border: none; background: #0284c7; color: #fff; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <div class="header">🛠️ الأداة المركزية v33.0</div>
    <div class="card">
        <h3>📊 لوحة المؤشرات</h3>
        <div id="status-display">الزواحف نشطة | البوتات تعمل</div>
    </div>
    <div class="card">
        <h3>💬 المحادثة وطلب التقارير</h3>
        <div class="chat-box" id="chatContainer">🤖 المنظومة جاهزة. اكتب 'تقرير' أو 'تسليم العمل'.</div>
        <input type="text" id="userInput" placeholder="اكتب الأمر...">
        <button onclick="sendMessage()">إرسال</button>
    </div>
    <script>
        function sendMessage() {
            let inputField = document.getElementById('userInput');
            let msg = inputField.value;
            if(!msg) return;
            let container = document.getElementById('chatContainer');
            container.innerHTML += `<div><b>أنت:</b> ${msg}</div>`;
            fetch('/api/chat?message=' + encodeURIComponent(msg))
                .then(res => res.json())
                .then(data => {
                    container.innerHTML += `<div><b>المنظومة:</b> ${data.reply}</div>`;
                    container.scrollTop = container.scrollHeight;
                });
            inputField.value = '';
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_INTERFACE)

@app.route('/api/chat')
def chat_api():
    user_msg = request.args.get('message', '').strip()
    secure_iban = os.environ.get('SECRET_IBAN', 'الآيبان غير متاح حالياً')
    
    if "تقرير" in user_msg or "الارباح" in user_msg:
        reply = "📊 <b>تقرير اليوم:</b><br>- تم تمشيط المواقع بنجاح.<br>- الأعمال المنجزة: نشطة<br>- الأرباح قيد التحصيل بانتظار تحويل العملاء البشريين."
    elif "تسليم العمل" in user_msg or "الدفع" in user_msg:
        reply = f"✅ تم إنجاز العمل وتسليمه للعميل.<br>💳 <b>الآيبان المعتمد للتحويل:</b> {secure_iban}"
    else:
        reply = f"🤖 تم استلام أمرك: ({user_msg}). المنظومة تعمل والزواحف تمسح المواقع الخارجية بنجاح."
    return jsonify({"reply": reply})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
