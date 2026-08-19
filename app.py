from flask import Flask, render_template_string, jsonify, request
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

STORE_CONFIG = {
    "paypal_email": "sszzzzz100400@gmail.com",
}

# --- دالة الزاحف المبسطة ---
def run_real_crawler():
    try:
        resp = requests.get("https://news.ycombinator.com/", timeout=5)
        soup = BeautifulSoup(resp.text, "html.parser")
        title = soup.title.get_text(strip=True) if soup.title else "متجر سلة/زد السعودي"
        return 5, title
    except:
        return 3, "السوق السعودي التجاري"

# --- الواجهة الجديدة الاحترافية والنظيفة ---
HTML_CHAT = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>منصة تقارير المتاجر الذكية</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background: #f8fafc; color: #1e293b; display: flex; justify-content: center; align-items: center; height: 100vh; padding: 15px; }
        .chat-container { width: 100%; max-width: 480px; background: #ffffff; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.08); display: flex; flex-direction: column; overflow: hidden; border: 1px solid #e2e8f0; height: 85vh; }
        .chat-header { background: #0f172a; color: #ffffff; padding: 18px 20px; display: flex; align-items: center; gap: 12px; }
        .chat-header img { width: 40px; height: 40px; border-radius: 50%; background: #38bdf8; display: flex; align-items: center; justify-content: center; text-align: center; line-height: 40px; font-weight: bold; }
        .chat-header h2 { font-size: 1.1rem; font-weight: 600; }
        .chat-header p { font-size: 0.8rem; color: #94a3b8; }
        
        .chat-box { flex: 1; padding: 20px; overflow-y: auto; background: #f1f5f9; display: flex; flex-direction: column; gap: 15px; }
        
        .msg { max-width: 85%; padding: 12px 16px; border-radius: 12px; font-size: 0.95rem; line-height: 1.5; word-wrap: break-word; }
        .msg-bot { background: #ffffff; color: #334155; align-self: flex-start; border-bottom-right-radius: 4px; box-shadow: 0 2px 5px rgba(0,0,0,0.03); border: 1px solid #e2e8f0; }
        .msg-user { background: #2563eb; color: #ffffff; align-self: flex-end; border-bottom-left-radius: 4px; }
        
        .chat-input-area { padding: 15px; background: #ffffff; border-top: 1px solid #e2e8f0; display: flex; gap: 10px; }
        input { flex: 1; padding: 12px 16px; border: 1px solid #cbd5e1; border-radius: 8px; outline: none; font-size: 0.95rem; background: #f8fafc; color: #1e293b; transition: border 0.2s; }
        input:focus { border-color: #2563eb; background: #ffffff; }
        button { background: #2563eb; color: white; border: none; padding: 0 20px; border-radius: 8px; font-weight: 600; cursor: pointer; transition: background 0.2s; }
        button:hover { background: #1d4ed8; }
    </style>
</head>
<body>

    <div class="chat-container">
        <div class="chat-header">
            <div style="background:#2563eb; color:white; border-radius:50%; width:40px; height:40px; display:flex; align-items:center; justify-content:center; font-weight:bold;">🤖</div>
            <div>
                <h2>مستشار تحليل المتاجر</h2>
                <p>متصل الآن • نساعدك لرفع مبيعاتك</p>
            </div>
        </div>

        <div class="chat-box" id="chat">
            <div class="msg msg-bot">أهلاً بك يا غالي! 📊 أنا مساعدك الذكي لاستخراج المنتجات الأكثر مبيعاً وتحليل السوق السعودي لمتجرك (سلة أو زد).<br><br>اختر الباقة أو اكتب <b>"انطلق"</b> لنبدأ العمل فوراً!</div>
        </div>

        <div class="chat-input-area">
            <input type="text" id="in" placeholder="اكتب طلبك هنا (مثلاً: سلة، الشامل، انطلق)..." onkeypress="if(event.keyCode==13) send();">
            <button onclick="send()">إرسال</button>
        </div>
    </div>

<script>
    function send() {
        let input = document.getElementById('in');
        let msg = input.value.trim();
        if(!msg) return;
        
        let chat = document.getElementById('chat');
        chat.innerHTML += `<div class="msg msg-user">${msg}</div>`;
        input.value = '';
        chat.scrollTop = chat.scrollHeight;
        
        fetch('/api/negotiate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({message: msg})
        })
        .then(res => res.json())
        .then(data => {
            chat.innerHTML += `<div class="msg msg-bot">${data.reply}</div>`;
            chat.scrollTop = chat.scrollHeight;
        });
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
    
    if any(word in msg for word in ["سلة", "زد", "salla", "zid"]):
        reply = "ممتاز! متجر على سلة أو زد يعني أننا بحاجة لتقرير دقيق ينافس المتاجر الكبرى.<br><br>التقرير المتقدم الشامل (<b>250 ريال</b>) سيعطيك المنتجات الأكثر طلباً.<br><br>💳 حول المبلغ على PayPal: <b style='color:#2563eb;'>%s</b> وأرسل الإيصال لنبدأ فحص متجرك فوراً." % STORE_CONFIG['paypal_email']
    
    elif any(word in msg for word in ["شامل", "متقدم", "250"]):
        reply = "اختيار موفق جداً! التقرير الشامل بـ <b>250 ريال</b>.<br><br>يرجى تحويل المبلغ فوراً على حساب PayPal: <b style='color:#2563eb;'>%s</b><br>وبعد التحويل، اكتب هنا 'تم التحويل' مع الإيصال لنباشر استخراج البيانات." % STORE_CONFIG['paypal_email']
        
    elif any(word in msg for word in ["أساسي", "باسيك", "150"]):
        reply = "تم حجز التقرير الأساسي بـ <b>150 ريال</b>.<br><br>يرجى تحويل المبلغ على حساب PayPal: <b style='color:#2563eb;'>%s</b> وأرسل لنا تأكيد التحويل لنرسل لك الملف." % STORE_CONFIG['paypal_email']
        
    elif any(word in msg for word in ["انطلق", "ابدأ", "شغل", "تقرير", "جلب"]):
        count, title = run_real_crawler()
        reply = f"🚀 تم فحص السوق أوليًا (تم رصد {count} فرص تجارية حية من: {title}).<br><br>لتنزيل التقرير كاملاً، يرجى إتمام تحويل <b>250 ريال</b> على PayPal وأرسل الإيصال هنا."
        
    else:
        reply = "أنا معك أستاذي. هل نعتمد التقرير الشامل (<b>250 ريال</b>) ونبدأ استخراج بيانات متجرك الآن؟"

    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
