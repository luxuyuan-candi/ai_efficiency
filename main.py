import re
import io
import requests
from flask import Flask, request, jsonify, send_file, make_response
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

agents_url = {
    "env": "http://127.0.0.1:5000/analyze"
}

def call_agent(url, prompt, timeout):
    payload = {
        "content": prompt
    }

    try:
        resp = requests.post(url, json=payload, timeout=timeout)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"清求接口出错: {e}")
        return

    data = resp.json()

    result = data.get("result", "")
    return result


@app.route('/upload', methods=['POST'])
def upload_markdown():
    """
    接收一个 markdown 文件, 搜索并替换形如 <agent@xxx:xxxxxxxxx> 的内容,
    返回替换后的 markdown 文件。
    """
    # 检查文件
    if 'file' not in request.files:
        return jsonify({'error': '未找到上传文件字段 file'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '文件名为空'}), 400

    # 读取文件内容 (假定 UTF-8 编码)
    text = file.read().decode('utf-8')

    # 正则匹配形如 <agent@xxx:xxxxxxxxx>
    # xxx: 不包含空格和冒号
    # xxxxxxxxx: 不包含 > 号
    pattern = r"<agent@([^:\s]+):([^>]+)>"

    # 查找所有匹配内容
    matches = re.findall(pattern, text)
    
    # 保存匹配到的内容
    found_list = matches
   
    if not matches:
        # 没有匹配直接返回原文件
        output_stream = io.BytesIO(text.encode('utf-8'))
        output_stream.seek(0)
        return send_file(
            output_stream,
            as_attachment=True,
            download_name='processed.md',
            mimetype='text/markdown',
            etag=False
        )
    # 构建从原始完整匹配到替换内容的映射
    replacements = {}
    for match in matches:
        name, code = match  # 分别提取 xxx 和 xxxxxxxx
        url = agents_url.get(name, "")
        timeout = 600
        new_value = call_agent(url, code, timeout)
        # 完整占位符文本
        full_placeholder = f"<agent@{name}:{code}>"
        replacements[full_placeholder] = new_value

    # 按照映射依次替换
    replaced_text = text
    for placeholder, new_val in replacements.items():
        replaced_text = replaced_text.replace(placeholder, new_val)

    # 生成新的 Markdown 文件
    output_stream = io.BytesIO(replaced_text.encode('utf-8'))
    output_stream.seek(0)

    # 返回替换后的文件，并返回提取信息
    resp = make_response(send_file(
        output_stream,
        as_attachment=True,
        download_name='processed.md',
        mimetype='text/markdown',
        etag=False
    ))

    # 在 header 中仅返回 ASCII 安全信息，比如数量
    resp.headers['X-Found-Count'] = str(len(matches))
    return resp

@app.route('/upload-list', methods=['POST'])
def upload_list():
    """
    如果只想看提取到的参数列表，可调用这个接口
    返回 [{name: xxx, code: xxxxxxxx}, ...]
    """
    if 'file' not in request.files:
        return jsonify({'error': '未找到上传文件字段 file'}), 400

    file = request.files['file']
    text = file.read().decode('utf-8')
    pattern = r"<agent@([^:\s]+):([^>]+)>"
    matches = re.findall(pattern, text)

    results = [{"name": name, "code": code} for name, code in matches]
    return jsonify({'found': results})

if __name__ == '__main__':
    # 生产环境建议使用 gunicorn/uwsgi 等启动
    app.run(host='0.0.0.0', port=5001, debug=True)
