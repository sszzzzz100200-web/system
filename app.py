from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/')
def home():
  return 'أهلاً بك يا عثمان! نظام المهام الخارجية يعمل بنجاح على السيرفر السحابي.'


@app.route('/webhook', methods=['POST'])
def webhook_task():
  try:
    data = request.json
    # معالجة البيانات والمهام الواردة من الخارج
    print('تم استلام بيانات المهام الخارجية:', data)

    return (
        jsonify({
            'status': 'success',
            'message': 'تم استلام وتجهيز المهام الخارجية بنجاح',
            'data': data,
        }),
        200,
    )
  except Exception as e:
    return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)
