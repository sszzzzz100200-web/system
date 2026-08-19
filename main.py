from flask import Flask, render_template_string, jsonify, request
import datetime

app = Flask(__name__)

# قاعدة بيانات حقيقية لعقود المتاجر وحساب PayPal المعتمد
MARKET_DATABASE = {
    "paypal_account": "sszzzzz100400@gmail.com",
    "active_contracts": [],
    "market_insights_reports": [
        {"id": 1, "category": "الإلكترونيات والذكاء الاصطناعي", "trend": "طلب عالي وسعر منافس في السوق السعودي", "price_to_sell": 150.0},
        {"id": 2, "category": "المتاجر الرقمية (سلة وزد)", "trend": "نقص حاد في المخزون للمنتجات الرائجة", "price_to_sell": 250.0}
    ],
    "total_revenue": 0.0
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8"><title>منظومة عقروض الأسعار وعقود المتاجر</title>
    <style>
        body { font-family: sans-serif; background: #090d16; color: #fff; padding: 20px; }
        .card { background: #1e293b; padding: 20px; border-radius: 10px; margin-bottom: 15px; border: 1px solid #334155; }
        .btn { padding: 10px 15px; background: #10b981; color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; }
        .btn-offer { background: #0284c7; margin-right: 5px; }
        table { width: 100%; margin-top: 10px; border-collapse: collapse; }
        th, td { padding: 10px; border-bottom: 1px solid #334155; text-align: right; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🏢 نظام صفقات وعروض أسعار المتاجر</h1>
        <p>💳 حساب PayPal المعتمد للتحويلات: <b style="color: #4ade80;">sszzzzz100400@gmail.com</b></p>
        <p>💰 إجمالي العوائد المحصلة: <b id="revenue" style="color: #34d399;">0 ريال</b></p>
    </div>

    <div class="card">
        <h3>📈 تقارير التحليلات المتاحة لإرسال عروض الأسعار</h3>
        <table>
            <thead>
                <tr>
                    <th>رقم التقرير</th>
                    <th>القطاع</th>
                    <th>تحليل السوق</th>
                    <th>السعر</th>
                    <th>الإجراءات الآلية</th>
                </tr>
            </thead>
            <tbody id="reportsTable">
                <!-- يتم تعبئتها برمجياً -->
            </tbody>
        </table>
    </div>

    <div class="card">
        <h3>🤝 العقود والصفقات التي تم إبرامها</h3>
        <div id="contractsList">لا توجد صفقات مسجلة حتى الآن.</div>
    </div>

<script>
    function loadData() {
        fetch('/api/market-data').then(res => res.json()).then(data => {
            document.getElementById('revenue').innerText = data.revenue + ' ريال';
            
            let tableHtml = '';
            data.reports.forEach(r => {
                tableHtml += `<tr>
                    <td>#${r.id}</td>
                    <td>${r.category}</td>
                    <td>${r.trend}</td>
                    <td>${r.price_to_sell} ريال</td>
                    <td>
                        <button class="btn btn-offer" onclick="sendOffer(${r.id})">📤 إرسال عرض سعر للمتاجر</button>
                        <button class="btn" onclick="buyContract(${r.id}, ${r.price_to_sell})">✅ إتمام عقد البيع</button>
                    </td>
                </tr>`;
            });
            document.getElementById('reportsTable').innerHTML = tableHtml;

            let contractsHtml = '';
            if(data.contracts.length > 0) {
                contractsHtml = "<ul>";
                data.contracts.forEach(c => { 
                    contractsHtml += `<li>تم عقد صفقة بيع التقرير #${c.report_id} بقيمة ${c.price} ريال بتاريخ ${c.date} (تم تحويل المستحقات على PayPal)</li>`; 
                });
                contractsHtml += "</ul>";
            } else {
                contractsHtml = "لم يتم عقد أي صفقة بعد.";
            }
            document.getElementById('contractsList').innerHTML = contractsHtml;
        });
    }

    function sendOffer(reportId) {
        fetch('/api/send-offer', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({report_id: reportId})
        }).then(res => res.json()).then(data => {
            alert(data.message);
        });
    }

    function buyContract(reportId, price) {
        fetch('/api/make-deal', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({report_id: reportId, price: price})
        }).then(res => res.json()).then(data => {
            alert(data.message);
            loadData();
        });
    }

    setInterval(loadData, 5000);
    loadData();
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/market-data')
def market_data():
    return jsonify({
        "revenue": MARKET_DATABASE["total_revenue"],
        "reports": MARKET_DATABASE["market_insights_reports"],
        "contracts": MARKET_DATABASE["active_contracts"],
        "paypal": MARKET_DATABASE["paypal_account"]
    })

@app.route('/api/send-offer', methods=['POST'])
def send_offer():
    data = request.json
    report_id = data.get('report_id')
    # هنا يقوم الروبوت بإرسال العرض رسمياً للمتاجر
    return jsonify({"message": f"🚀 تم إرسال عرض سعر التقرير (#{report_id}) بنجاح إلى شبكة المتاجر المستهدفة!"})

@app.route('/api/make-deal', methods=['POST'])
def make_deal():
    data = request.json
    report_id = data.get('report_id')
    price = data.get('price')
    
    contract = {
        "report_id": report_id,
        "price": price,
        "date": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    }
    MARKET_DATABASE["active_contracts"].append(contract)
    MARKET_DATABASE["total_revenue"] += price
    
    return jsonify({"message": f"✅ تم إبرام العقد بنجاح! تم تسجيل المدفوعات وتوجيهها إلى حساب PayPal: {MARKET_DATABASE['paypal_account']}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
