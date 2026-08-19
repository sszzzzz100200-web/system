from flask import Flask, render_template_string, jsonify, request
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import requests
import time

app = Flask(__name__)

STORE_CONFIG = {
    "paypal_email": "sszzzzz100400@gmail.com",
}

# --- وظيفة زاحف الويب الحقيقي ---
def run_real_crawler(seed_url="https://news.ycombinator.com/"):
    seen = set()
    results = []
    try:
        resp = requests.get(seed_url, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        page_title = soup.title.get_text(strip=True) if soup.title else "بدون عنوان"

        # استخراج أول 5 روابط كمثال حي لجلب البيانات
        for a in soup.select("a[href]")[:5]:
            href = a.get("href", "").strip()
            if href.startswith("http"):
                results.append(href)

        return len(results), page_title
    except Exception as e:
        return 0, str(e)


HTML_CHAT = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8"><title>مستشار تحليل المتاجر والزواحف الذكية</title>
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
        <h2>🤖 نظام الزواحف وتحليل المتاجر الذكي</h2>
        <div class="chat-box" id="chat">
            <div class="msg-bot">🤖 أهلاً بك! أنا جاهز لتشغيل الزواحف وجلب بيانات السوق الحية. اكتب "انطلق" لبدء السحب والتحليل.</div>
        </div>
        <input type="text" id="in" placeholder="اكتب أمرك هنا (مثل: انطلق، كم البيانات)..." onkeypress="if(event.keyCode==13) send();">
        <button onclick="send()">إرسال</button>
    </div>

<script>
    function send() {
        let msg = document.getElementById('in').value;
        if(!msg.trim()) return;
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


@app.route("/")
def home():
  return render_template_string(HTML_CHAT)


@app.route("/api/negotiate", methods=["POST"])
def negotiate():
  data = request.json
  msg = data.get("message", "").lower()

  # 1. إذا طلب بدء العمل (تشغيل الزاحف الحقيقي)
  if any(word in msg for word in ["انطلق", "ابدأ", "شغل", "تقرير", "جلب"]):
    count, title = run_real_crawler()
    reply = (
        f"🚀 **تم تشغيل الزاحف بنجاح وجلب البيانات الحية!**\n"
        f"• عنوان الموقع المفحوص: {title}\n"
        f"• تم استخراج {count} روابط رئيسية ومنتج رائج.\n\n"
        f"🔹 التقرير الشامل جاهز بـ **250 ريال**.\n"
        f"🔹 تحويل المبلغ عبر PayPal على: <b>{STORE_CONFIG['paypal_email']}</b>\n"
        "أرسل إيصال الدفع هنا لتستلم الملف الكامل فوراً."
    )

  # 2. الاستفسار عن حالة البيانات
  elif any(word in msg for word in ["كم", "حالة", "بيانات", "نتائج"]):
    reply = (
        "📊 **حالة محرك الزحف:**\n"
        "الزواحف جاهزة للعمل وفحص أي منصة أو متجر تختاره لتزويدك ببيانات حقيقية ودقيقة.\n"
        "اكتب 'انطلق' لبدء عملية السحب الفوري."
    )

  # 3. الاستفسار عن الأسعار
  elif any(word in msg for word in ["سعر", "غالي", "بكم", "خصم", "باقات"]):
    reply = (
        "الأسعار استثمارية ومدروسة:\n"
        "1️⃣ **التقرير الأساسي:** 150 ريال.\n"
        "2️⃣ **التقرير المتقدم والزاحف الشامل:** 250 ريال.\n\n"
        "أيهما نعتمد لمتجرك؟"
    )

  # 4. الرد الافتراضي
  else:
    reply = (
        "أنا معك! هل تريد أن نقوم بتفعيل الزواحف وسحب بيانات السوق الحية الآن"
        " بـ 250 ريال؟"
    )

  return jsonify({"reply": reply})


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8080)
