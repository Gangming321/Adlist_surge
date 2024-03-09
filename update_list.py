import requests
import subprocess
import datetime

# 定义你的URL列表
urls = [
    "https://share.is26.com/subscribe/adblock.hosts",
    "https://big.oisd.nl",
    "https://anti-ad.net/domains.txt"
]

# 获取和处理数据
def get_and_process_data(urls):
    processed_data = ""
    for url in urls:
        # 从URL获取内容
        response = requests.get(url)
        domains = response.text.splitlines()
        
        # 编辑内容格式，并删除 || 和 ^
        for domain in domains:
            # 删除 || 和 ^
            domain_cleaned = domain.replace("||", "").replace("^", "")
            processed_data += f"DOMAIN,{domain_cleaned}\n"
    return processed_data


# 保存数据到文件
def save_data_to_file(data, file_name):
    with open(file_name, 'w') as file:
        file.write(data)

# Git命令函数
def run_git_commands(file_name):
    subprocess.run(["git", "pull"], check=True)  # 更新本地仓库
    subprocess.run(["git", "add", file_name], check=True)  # 添加文件到暂存区
    subprocess.run(["git", "commit", "-m", f"Update data for {datetime.date.today()}"], check=True)  # 提交更改
    subprocess.run(["git", "push"], check=True)  # 推送更改到GitHub

data = get_and_process_data(urls)
file_name = "data.txt"  # 定义文件名
save_data_to_file(data, file_name)
run_git_commands(file_name)
