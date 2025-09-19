import requests

def main():
    # Flask 接口地址，根据实际部署情况修改
    url = "http://127.0.0.1:5000/analyze"

    # 要发送给接口的内容
    payload = {
        "content": "检查该项目的所有情况"
    }

    try:
        # 发送 POST 请求
        resp = requests.post(url, json=payload, timeout=600)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"请求接口出错: {e}")
        return

    # 解析返回 JSON
    data = resp.json()

    # 取得 result 字段并把字面 \n 转换为真正换行
    result = data.get("result", "")
    #result = result.replace("\\n", "\n")

    # 输出到控制台
    print("\n===== 接口返回结果 =====\n")
    with open("./result.md", "w") as f:
        f.write(result)
    print(result)

if __name__ == "__main__":
    main()
