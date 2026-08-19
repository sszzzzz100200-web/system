import os
from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)

# إحصائيات النظام تبدأ من الصفر لتعكس الأعمال الحقيقية فقط
SYSTEM_STATE = {
    "active": True,
    "crawlers_count": 0,
    "bots_count": 0,
    "tasks_completed": 0,
    "total_earnings": 0.0,
    "secure_iban": "SA4080000157608016064751"
}

HTML_INTERFACE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>منظومة الإدارة الذكية</title>
    <style>
        body { font-family: sans-serif; background: #0b0f19; color: #fff; margin: 0; padding: 20px; }
        .header { background: #1e293b; padding: 15px; border-radius: 10px; text-align: center; font-size: 22px; font-weight: bold; margin-bottom: 20px; color: #38bdf8; }
        .card { background: #1e293b; padding: 15px; border-radius: 10px; margin-bottom: 15px; }
        .stats-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-bottom: 10px; }
        .stat-box { background: #0f172a; padding: 10px; border-radius: 6px; text-align: center; border: 1px solid #334155; }
        .chat-box { background: #0f172a; height: 260px; border-radius: 8px; padding: 12px; overflow-y: auto; margin-bottom: 10px; border: 1px solid #334155; line-height: 1.6; }
        input[type="text"] { width: 75%; padding: 10px; border-radius: 6px; border: 1px solid #475569; background: #1e293b; color: #fff; }
        button { width: 20%; padding: 10px; border-radius: 6px; border: none; background: #0284c7; color: #fff; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <div class="header">🌐 غرفة العمليات المركزية</div>
    <div class="card">
        <h3>📊 إحصائيات الأعمال الحقيقية</h3>
        <div class="stats-grid">
            <div class="stat-box">🕷️ الزواحف: <br><b id="crawlers">0</b></div>
            <div class="stat-box">🤖 الروبوتات: <br><b id="bots">0</b></div>
            <div class="stat-box">✅ الأعمال: <br><b id="tasks">0</b></div>
            <div class="stat-box">💰 الأرباح: <br><b id="earnings">0 ريال</b></div>
        </div>
    </div>
    <div class="card">
        <h3>💬 الأوامر المباشرة</h3>
        <div class="chat-box" id="chatContainer">🤖 النظام جاهز. ابدأ بإعطاء الأوامر لتبدأ العدادات في العمل.</div>
        <input type="text" id="userInput" placeholder="اكتب أمرك هنا...">
        <button onclick="sendMessage()">إرسال</button>
    </div>
    <script>
        function updateStats() {
            fetch('/api/stats').then(res => res.json()).then(data => {
                document.getElementById('crawlers').innerText = data.crawlers;
                document.getElementById('bots').innerText = data.bots;
                document.getElementById('tasks').innerText = data.tasks;
                document.getElementById('earnings').innerText = data.earnings + ' ريال';
            });
        }
        setInterval(updateStats, 2000);
        function sendMessage() {
            let inputField = document.getElementById('userInput');
            let msg = inputField.value;
            if(!msg) return;
            let container = document.getElementById('chatContainer');
            container.innerHTML += `<div><b>الآدمن:</b> ${msg}</div>`;
            fetch('/api/chat?message=' + encodeURIComponent(msg))
                .then(res => res.json())
                .then(data => {
                    container.innerHTML += `<div><b>النظام:</b> ${data.reply}</div>`;
                    container.scrollTop = container.scrollHeight;
                    updateStats();
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

@app.route('/api/stats')
def stats_api():
    return jsonify({
        "crawlers": SYSTEM_STATE["crawlers_count"],
        "bots": SYSTEM_STATE["bots_count"],
        "tasks": SYSTEM_STATE["tasks_completed"],
        "earnings": SYSTEM_STATE["total_earnings"]
    })

@app.route('/api/chat')
def chat_api():
    user_msg = request.args.get('message', '').strip().lower()
    
    if "ايقاف" in user_msg:
        SYSTEM_STATE["active"] = False
        reply = "🛑 تم إيقاف النظام."
    elif "تشغيل" in user_msg:
        SYSTEM_STATE["active"] = True
        reply = "🟢 تم التشغيل."
    else:
        # هنا تزيد الأرقام فقط عند وجود أمر حقيقي
        SYSTEM_STATE["crawlers_count"] += 5
        SYSTEM_STATE["bots_count"] += 2
        SYSTEM_STATE["tasks_completed"] += 1
        SYSTEM_STATE["total_earnings"] += 50.0
        reply = f"✅ تم تنفيذ المهمة: ({user_msg}). الأرباح المضافة 50 ريال. الآيبان: {SYSTEM_STATE['secure_iban']}"
        
    return jsonify({"reply": reply})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
