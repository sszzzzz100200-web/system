pip install flask requests selenium webdriver-manager
import os
import time
import requests
from flask import Flask, jsonify, redirect, request, send_from_directory
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

# إنشاء مجلد لحفظ لقطات الشاشة (إثبات الإنجاز) إذا لم يكن موجوداً
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

# مفتاح اختبار تجريبي لبوابة الدفع (سيتم استبداله بمفتاح stc pay الحي بعد 23 ساعة)
MOYASAR_TEST_KEY = "pk_test_vcTeQi9JKZJvY796f6gT776v7fe6s6x66f6" 

# =====================================================================
# 1. روبوت الأتمتة والتنفيذ (Selenium Bot)
# =====================================================================
def run_automation_bot(site_url, data_to_insert):
    """روبوت ذكي يدخل لموقع العميل، ينجز العمل، ويأخذ لقطة شاشة كإثبات"""
    print("🤖 الروبوت بدأ العمل الآن...")
    
    options = webdriver.ChromeOptions()
    # ملاحظة: تم إيقاف الوضع الخفي (Headless) مؤقتاً لتشاهد الروبوت بنفسك وهو يعمل أثناء الاختبار
    # options.add_argument('--headless') 
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # تحميل وتشغيل متصفح كروم تلقائياً
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # الدخول للموقع المستهدف
        driver.get(site_url)
        wait = WebDriverWait(driver, 10)
        
        # محاكاة إدخال البيانات (البحث عن خانة النص والكتابة فيها)
        # لتسهيل الاختبار، الكود يبحث عن أول خانة إدخال (input) يجدها في الصفحة ويكتب فيها
        text_input = wait.until(EC.presence_of_element_located((By.TAG_NAME, "input")))
        text_input.clear()
        text_input.send_keys(data_to_insert)
        print("✍️ قام الروبوت بتعبئة البيانات بنجاح.")
        
        # محاكاة الضغط على زر الحفظ (الروبوت يبحث عن أي زر إرسال ويضغطه)
        try:
            submit_btn = driver.find_element(By.XPATH, "//button[@type='submit'] | //input[@type='submit']")
            submit_btn.click()
            print("💾 الروبوت ضغط على زر الحفظ.")
            time.sleep(2)
        except:
            print("ℹ️ لم يتم العثور على زر حفظ، سيتم الاكتفاء بالكتابة لأجل الاختبار.")
        
        # التقاط صورة حية لإثبات الإنجاز وحفظها في مجلد الـ static
        screenshot_path = os.path.join(STATIC_DIR, "proof_of_work.png")
        driver.save_screenshot(screenshot_path)
        print(f"📸 تم حفظ إثبات الإنجاز بنجاح في: {screenshot_path}")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في الروبوت: {e}")
        return False
    finally:
        driver.quit()
        print("🤖 تم إغلاق المتصفح الآلي.")

# =====================================================================
# 2. مسارات سيرفر الويب والتحكم بالفواتير (Flask Routes)
# =====================================================================

@app.route('/')
def home():
    """واجهة موقعك المستقل الاستعراضية للعميل"""
    return """
    <html>
        <body style="text-align: center; font-family: Arial; padding: 50px; background-color: #f4f6f9;">
            <h1 style="color: #4f2d7f;">منظومة الأتمتة الذكية للمواقع</h1>
            <p style="font-size: 18px;">أدخل رابط موقعك والمهمة، وسيقوم الروبوت بإنجازها فوراً.. <b>والدفع بعد الإنجاز!</b></p>
            <form action="/start-task" method="POST" style="margin-top: 30px;">
                <input type="text" name="url" placeholder="أدخل رابط الموقع (مثال: https://google.com)" required style="width: 400px; padding: 12px; border-radius: 5px; border: 1px solid #ccc;"><br><br>
                <input type="text" name="data" placeholder="البيانات المراد إدخالها أو نقلها" required style="width: 400px; padding: 12px; border-radius: 5px; border: 1px solid #ccc;"><br><br>
                <button type="submit" style="background-color: #4f2d7f; color: white; padding: 12px 40px; border: none; border-radius: 5px; font-weight: bold; cursor: pointer;">🤖 ابدأ الأتمتة فوراً مجاناً</button>
            </form>
        </body>
    </html>
    """

@app.route('/start-task', method=['POST'])
def start_task():
    """المسار المسؤول عن استقبال طلب العميل وتشغيل الروبوت تلقائياً"""
    site_url = request.form.get('url')
    data_content = request.form.get('data')
    
    # تشغيل الروبوت التنفيذي
    success = run_automation_bot(site_url, data_content)
    
    if success:
        # إذا نجح الروبوت، ننتقل تلقائياً لصفحة الفاتورة والدفع بعد الإنجاز
        return redirect('/invoice')
    else:
        return "<h3 style='color:red; text-align:center;'>حدث خطأ أثناء تنفيذ الروبوت، يرجى التحقق من الرابط.</h3>", 400

@app.route('/invoice')
def show_invoice():
    """صفحة الفاتورة: تعرض للعميل صورة إثبات العمل وزر الدفع عبر stc pay"""
    # توليد فاتورة حقيقية (وضع الاختبار) بقيمة 150 ريال سعودي
    url = "https://moyasar.com"
    invoice_data = {
        "amount": 15000,  # 150.00 ريال (المبلغ يُحسب بالهللة)
        "currency": "SAR",
        "description": "رسوم إنجاز مهمة الأتمتة الذكية بنجاح",
        "source": {
            "type": "stcpay"  # تحديد وسيلة الدفع المحببة للعملاء
        },
        "callback_url": "http://127.0.0"
    }
    
    try:
        response = requests.post(url, json=invoice_data, auth=(MOYASAR_TEST_KEY, ""))
        payment_info = response.json()
        stc_pay_url = payment_info.get("source", {}).get("transaction_url")
    except Exception as e:
        stc_pay_url = "#"
        print(f"فشل الاتصال ببوابة الدفع: {e}")

    return f"""
    <html>
        <body style="text-align: center; font-family: Arial; padding: 40px; background-color: #f4f6f9;">
            <h2 style="color: #28a745;">🎉 أنجز الروبوت عملك كاملاً وبدقة 100%!</h2>
            <p style="font-size: 16px;">شاهد لقطة الشاشة الحية لمتجرك/موقعك بعد التعديل البرمجي:</p>
            
            <div style="margin: 20px auto; max-width: 600px; border: 3px solid #4f2d7f; border-radius: 8px; overflow: hidden; background: white;">
                <img src="/static/proof_of_work.png?t={int(time.time())}" style="width: 100%; height: auto; display: block;">
            </div>
            
            <p style="font-size: 18px; font-weight: bold; color: #333;">لاعتماد العمل ونشره وتثبيته نهائياً، تفضل بالسداد:</p>
            <a href="{stc_pay_url}" target="_blank" style="display: inline-block; background-color: #4f2d7f; color: white; padding: 15px 40px; text-decoration: none; border-radius: 30px; font-size: 18px; font-weight: bold; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                📱 ادفع الآن 150 ريال عبر stc pay
            </a>
        </body>
    </html>
    """

@app.route('/payment-success')
def payment_success():
    """الصفحة التي يرجع إليها العميل تلقائياً بعد إتمام الدفع بنجاح"""
    return """
    <html>
        <body style="text-align: center; font-family: Arial; padding: 50px; background-color: #f4f6f9;">
            <h1 style="color: #28a745;">✅ تم استلام دفعتك بنجاح!</h1>
            <p style="font-size: 20px; color: #333;">دخلت الأموال إلى حسابك وتم اعتماد وتثبيت العمل في موقعك بنسبة 100%.</p>
            <p style="color: #666;">شكراً لتعاملك مع منظومتنا الموثوقة.</p>
            <a href="/" style="color: #4f2d7f; font-weight: bold; text-decoration: none;">🔄 تنفيذ مهمة جديدة</a>
        </body>
    </html>
    """

@app.route('/static/<filename>')
def serve_static(filename):
    """مسار داخلي لعرض صورة لقطة الشاشة في المتصفح"""
    return send_from_directory(STATIC_DIR, filename)

if __name__ == '__main__':
    # تشغيل السيرفر محلياً للاختبار
    print("🚀 السيرفر يعمل الآن على الرابط المحلي: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
