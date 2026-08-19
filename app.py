import os, time
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

HTML_INTERFACE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>منظومة الأداة المركزية v33.0</title>
    <style>
        body { font-family: sans-serif; background: #060b13; color: #e2e8f0; padding: 10px; margin: 0; }
        .header { background: #0f172a; padding: 10px; border-radius: 8px; text-align: center; border-bottom: 3px solid #3b82f6; margin-bottom: 10px; }
        .card { background: #1e293b; padding: 12px; border-radius: 8px; margin-bottom: 10px; }
        h3 { color: #38bdf8; font-size: 15px; border-bottom: 1px solid #334155; padding-bottom: 4px; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 13px; }
        .counter-box { background: #0f172a; padding: 8px; border-radius: 6px; text-align: center; }
        .chat-container { background: #020617; border-radius: 6px; padding: 10px; height: 180px; overflow-y: auto; margin-bottom: 10px; }
        .msg { padding: 8px; border-radius: 8px; font-size: 13px; margin-bottom: 5px; }
        .msg.bot { background: #1e3a8a; border-right: 3px solid #3b82f6; }
        .msg.user { background: #0f766e; text-align: left; }
    </style>
</head>
<body>
    <div class="header"><h2>🛠️ الأداة المركزية v33.0</h2></div>
    <div class="card">
        <h3>📊 لوحة المؤشرات</h3>
        <div class="grid">
            <div class="counter-box"><div style="color:#9ca3af;">الزواحف</div><b id="scrapersStatus">3 خاملة</b></div>
            <div class="counter-box"><div style="color:#9ca3af;">البوتات</div><b id="botsStatus">3 متوقفة</b></div>
        </div>
    </div>
    <div class="card">
        <h3>💬 المحادثة</h3>
        <div class="chat-container" id="chatContainer">
            <div class="msg bot">🤖 المنظومة جاهزة. اكتب (شغل الكل) للبدء.</div>
        </div>
        <input type="text" id="userInput" style="width:70%; padding:8px;" placeholder="اكتب الأمر...">
        <button onclick="sendMessage()">إرسال</button>
    </div>
    <script>
        function sendMessage() {
            let inputField = document.getElementById('userInput'); let text = inputField.value;
            fetch('/api/chat?message=' + encodeURIComponent(text)).then(res => res.json()).then(data => {
                document.getElementById('scrapersStatus').innerText = data.scrapers_status;
                document.getElementById('botsStatus').innerText = data.bots_status;
                let container = document.getElementById('chatContainer');
                container.innerHTML += `<div class="msg user">${text}</div>`;
                data.new_responses.forEach(m => container.innerHTML += `<div class="msg bot">${m.text}</div>`);
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home(): return render_template_string(HTML_INTERFACE)

@app.route('/api/chat')
def chat_api():
    user_msg = request.args.get('message', '').lower()
    if "شغل" in user_msg or "الكل" in user_msg:
        return jsonify({"scrapers_status": "6 نشطة", "bots_status": "5 تعمل", "new_responses": [{"text": "تم تفعيل المنظومة بكامل طاقتها!"}]})
    return jsonify({"scrapers_status": "3 خاملة", "bots_status": "3 متوقفة", "new_responses": [{"text": "في انتظار أمر التشغيل."}]})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
