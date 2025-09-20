import os
import requests
import pandas as pd
from tqdm import tqdm
from time import sleep


def get_ip_from_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            ips = [line.strip() for line in f if line.strip()]
        print(f"从 {filename} 读取了 {len(ips)} 个IP")
        return ips
    except Exception as e:
        print(f"读取文件 {filename} 时出错: {e}")
        return []


def ipinfoapi(ips: list, session):
    if not ips:
        print("IP列表为空，跳过API调用")
        return []
        
    url = 'http://ip-api.com/batch'
    ips_dict = [{'query': ip, "fields": "city,country,countryCode,isp,org,as,query"} for ip in ips]
    sleep(2)
    try:
        with session.post(url, json=ips_dict) as resp:
            if resp.status_code == 200:
                return resp.json()
            else:
                print(f'获取ip信息失败: {resp.status_code}, {resp.reason}')
                return []
    except Exception as e:
        print(f'requests error:{e}')
        return []


def get_ip_info(ips):
    if not ips:
        print("IP列表为空，跳过信息获取")
        return []
        
    ipsinfo = []
    url = 'http://ip-api.com/batch'

    with tqdm(total=len(ips)) as bar:
        bar.set_description(f"Processed IP: {len(ips)}")
        with requests.Session() as session:
            for i in range(0, len(ips), 100):
                count = min(i + 100, len(ips))
                t = ipinfoapi(ips[i:i + 100], session)
                if t is not None:
                    ipsinfo += t
                bar.update(100)

    return ipsinfo


def gatherip(port):
    port_dir = f"./ips/{port}/"
    
    if not os.path.exists(port_dir) or not os.path.isdir(port_dir):
        print(f"端口 {port} 目录不存在: {port_dir}")
        return []
    
    print(f"找到端口 {port} 目录: {port_dir}")
    
    allips = []
    # 读取目录中的所有txt文件
    for file in os.listdir(port_dir):
        if file.endswith('.txt'):
            file_path = os.path.join(port_dir, file)
            print(f"读取文件: {file_path}")
            allips += get_ip_from_file(file_path)
    
    print(f"总共收集到 {len(allips)} 个IP地址")
    return list(set(allips))


def process_ipinfo(ipinfo, port):
    if not ipinfo:
        print(f"没有获取到IP信息，跳过处理端口 {port}")
        return
        
    save_dir = f"./ip{port}/"

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    try:
        df = pd.DataFrame(ipinfo)
        grouped = df.groupby('countryCode')
        for countryCode, group in grouped:
            only_ip = group['query'].drop_duplicates()
            output_file = os.path.join(save_dir, f"{countryCode}.txt")
            only_ip.to_csv(output_file, header=None, index=False)
            print(f"保存了 {countryCode} 的 {len(only_ip)} 个IP到 {output_file}")
    except KeyError as e:
        print(f"处理IP信息时出错: {e}")
        print(f"IP信息数据结构: {ipinfo[:2] if ipinfo else '空'}")


def copy_and_modify_file():
    file_countries = ["HK", "JP", "KR", "SG", "US"]
    for country in file_countries:
        source_file = os.path.join("ip443", f"{country}.txt")
        target_file = os.path.join("ip443", f"{country}_.txt")
        if os.path.exists(source_file):
            with open(source_file, "r", encoding="utf-8") as source, open(target_file, "w", encoding="utf-8") as target:
                for line in source:
                    target.write(line.strip() + f"#{country}☮\n")
            print(f"已处理 {country} 文件")
        else:
            print(f"源文件 {source_file} 不存在，跳过处理")


def main(port):
    print(f"开始处理端口 {port}")
    ips = gatherip(port)
    print(f"去重后总IP数: {len(ips)}")
    
    if not ips:
        print("没有找到IP地址，跳过API调用")
        # 创建空目录结构
        save_dir = f"./ip{port}/"
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        return
        
    ipinfo = get_ip_info(ips)
    process_ipinfo(ipinfo, port)
    copy_and_modify_file()


if __name__ == "__main__":
    main(443)
    print("Done!")
