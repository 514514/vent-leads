import requests, re, time, random, csv, os
from datetime import datetime

# ==================== 配置区 ====================
PUSHPLUS_TOKEN = "你的PushPlus_Token"  # 必须填，否则收不到微信
# ================================================

NEGATIVE_KEYWORDS = ["办理", "认证", "网查", "社保", "换群", "拼多多", "淘宝", "京东", "刷单", "兼职日结", "免费领取", "加微信领", "扫码", "点击链接", "红包", "投票", "助力", "砍价", "微商", "招代理", "游戏推广", "群发助手", "测试消息", "系统消息", "互换", "接活", "保洁", "兼职", "征婚", "网红", "论文", "自学", "家具", "名片", "小店", "发明", "专利", "支架", "护照", "撤回", "境外", "早安", "销售", "清洗", "拖欠", "特种", "投标", "广告", "操作机器", "普工", "船厂", "标签", "标牌", "考试", "水箱", "朋友圈", "帮助", "救救", "求求", "回国", "证书", "太阳", "小程序", "报名", "出国", "印尼", "化工", "河道", "白班", "形象", "欠债", "经济", "宣传", "海外", "鄂尔多斯", "泥瓦匠", "木条", "含胶", "标书", "免税", "时光", "冷静", "王者", "小天鹅", "云欢", "电泳线", "海目星", "摘盒工", "主播", "好工作", "推荐", "视频面试", "维修", "线上面试", "高薪", "外账", "钳工", "总店", "童车", "设计", "岗位", "三轮车", "四轮车", "坐班", "长白班", "临时工", "跟单员", "打包", "客服", "泰国", "注塑厂", "车业", "汉堡", "水电费", "锂电池", "汽车", "宝妈", "银行", "垫资", "龙岗", "分切工", "快递", "风水", "顺风车", "鲜花", "隔断", "爆破", "座椅", "资料", "居家", "官方", "婚姻", "债务", "宽带", "运营商", "汽配厂", "扣保险", "送货员", "信用", "水利", "培训", "抖音", "物流", "装卸", "食品厂", "分装", "乌木", "麻柳", "两班倒", "操作工", "银行卡", "污染", "口感", "一级房建", "演唱会", "电视", "发货", "安保", "工作轻松", "美的", "轴皮", "锂电", "奥克斯", "搬运工", "冷暖机", "洗衣机", "净化器", "柜机", "天然气", "燃气", "硫酸", "玻璃", "发票", "破产", "中介", "驾校", "新到货", "保险", "审车", "车企", "门店", "服务", "水电平摊", "建造师", "盛会", "省电", "机遇", "秒杀", "大促销", "三班倒", "出租", "流量卡", "领取", "秒发", "特价", "破价", "九阳", "罚款", "阻燃", "防虫", "压力", "搭建", "舞台", "全国资源", "你的项目", "说明会", "投资人", "正泰", "双玻", "包膜机", "夜班", "净水", "成色", "卤菜", "养生", "天合", "晶科", "准新机", "鸿泰", "抗震", "格力", "海信", "爆款", "畅销", "枪手", "美容", "学习", "机构", "线上型号", "国补", "找钱", "找圈子", "智慧", "保姆", "住家", "阿姨", "冰箱", "洗碗机", "松下", "专票", "体验", "商保", "疲劳", "疗程", "内机", "侧出风", "进口", "卡萨帝", "到货", "自行车", "投资", "资金", "捡药材", "货车", "司机", "驾照", "小红书", "添可", "代办", "车找人", "洗车工", "纸箱厂", "电缆", "年终奖", "报错", "光缆", "促销", "便利店", "顺路", "退税", "人找车", "兼职群", "视频", "线上", "大量出", "价低", "导购员", "印刷厂", "外快", "辅导员", "翻译", "零活", "电动车", "养殖", "送安", "堵漏", "漏水", "执行", "管理员", "新版本", "储罐", "加气站设备", "执照", "石材", "荒料", "铲车", "课程", "日结", "押金", "介绍活", "阳光棚", "坚果", "谷物", "承接", "创维", "画框", "效果图", "案例", "渠道", "吸气", "空气", "火灾", "探测器", "平纹", "精纺", "黑丝", "精准", "题库", "二手", "求购", "液化", "日产", "手续", "欢迎老板", "家电", "安检", "美妆", "护肤", "网约车", "到家", "烤鱼", "烧烤", "事务所", "备案", "供应商", "订单", "开槽", "科技", "水质", "化妆", "服装", "面霜", "家务", "肩膀", "花生油", "食用", "近视", "镜片", "深度", "日订单", "矿山", "测试机", "铲墙", "信息", "化学品", "金属", "轻松班", "甜品", "拉面", "青春没有售价", "光伏", "水管", "土方", "挖运", "面粉", "主营", "怕查", "非偏", "化学", "工业", "电子", "心情", "颈椎病", "包车", "约车", "面包", "工位", "扎心", "引进", "茶水", "动物", "领养", "开水", "水龙头", "东芝", "红娘", "婚恋", "肩颈", "不舒服", "穴位", "数字", "平台", "明星", "对象", "换着发", "别逗我", "精神小伙"]
STRONG_KEYWORDS = ["招", "聘", "师傅", "大工", "中工", "清工", "外包", "小工", "找工人", "急招", "诚聘", "安装", "风管", "通风", "铁皮", "合管", "排烟", "白铁", "暖通", "队伍", "班组", "包工", "工地", "干活", "工资", "需人", "缺人"]
SEEKER_BLACKLIST = ["找活", "求职", "找工作", "求带走", "本人找", "想找个", "现有人员", "班组空出", "人员空出", "待业", "求收留", "找份活", "求活干", "哪个老板要", "现有风管", "现有通风", "工地完工", "专业合管团队", "专业队伍", "随时出发", "求包", "本人从事", "找工作", "找点事", "接点活"]
SPAM_BLACKLIST = ["厂家", "回收", "批发", "生产", "产品", "批量", "定制", "现货", "货源", "包邮", "成本价", "专产", "出售", "钢管", "配套", "加工", "铝合金", "风口", "燃热", "派单", "收银", "一体机", "加盟", "直出", "专业加工", "直销", "供应", "厂价", "厂家直销", "材料厂"]

PHONE_RE = re.compile(r"1[3-9]\d[\s\-]*\d{4}[\s\-]*\d{4}")
# 直接请求 Jina，让 Jina 去对付国内的反爬
JINA_PREFIX = "https://r.jina.ai/"

def check_text_pass(text):
    if any(kw in text for kw in SEEKER_BLACKLIST): return False, "求职/找活"
    if any(kw in text for kw in SPAM_BLACKLIST): return False, "推销/材料"
    if not any(kw in text for kw in STRONG_KEYWORDS): return False, "非目标行业"
    for kw in NEGATIVE_KEYWORDS:
        if kw in text: return False, "命中负向词"
    return True, "通过"

def fetch_via_jina(url):
    """通过 Jina 代理获取网页纯文本"""
    try:
        print(f"  正在穿透抓取: {url}")
        r = requests.get(JINA_PREFIX + url, timeout=30)
        if r.status_code == 200:
            return r.text
    except Exception as e:
        print(f"  穿透失败: {e}")
    return ""

def scrape_tieba_jina():
    """穿透抓取贴吧"""
    rows = []
    # 我们直接去抓贴吧搜索页的文本
    keywords = ["通风 招工", "风管 安装 电话", "成都 通风"]
    for kw in keywords:
        url = f"https://tieba.baidu.com/f/search/res?ie=utf-8&qw={kw}"
        text = fetch_via_jina(url)
        if not text: continue
        
        # 提取所有手机号
        phones = [re.sub(r"[\s\-]", "", p) for p in PHONE_RE.findall(text)]
        if phones:
            # Jina 返回的是一整页文本，我们按行分割，尝试找到带电话的行
            for line in text.split('\n'):
                if any(p in line for p in phones):
                    is_pass, _ = check_text_pass(line)
                    if is_pass:
                        for p in phones:
                            if p in line:
                                rows.append({"源": "贴吧(穿透)", "标题": line[:50].strip(), "链接": url, "号码": p, "时间": datetime.now().strftime("%m-%d")})
                                break
    return rows

def scrape_ybrc_jina():
    """穿透抓取宜宾人才网"""
    rows = []
    urls = [
        "https://www.ybrc128.com/recruit/search?keyword=通风",
        "https://www.ybrc128.com/recruit/search?keyword=暖通"
    ]
    for url in urls:
        text = fetch_via_jina(url)
        if not text: continue
        
        # 由于 Jina 返回的是整页纯文本（类似 Markdown），直接正则找带电话的段落
        phones = [re.sub(r"[\s\-]", "", p) for p in PHONE_RE.findall(text)]
        for phone in set(phones):
            # 找到包含该电话的上下文
            match = re.search(f".{{0,50}}{phone}.{{0,50}}", text)
            if match:
                context = match.group(0).replace("\n", " ")
                is_pass, _ = check_text_pass(context)
                if is_pass:
                    rows.append({"源": "宜宾人才网(穿透)", "标题": context[:50], "链接": url, "号码": phone, "时间": datetime.now().strftime("%m-%d")})
    return rows

def generate_html(rows):
    html = """<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>招聘数据看板</title>
    <style>body{font-family:sans-serif;padding:10px;background:#f0f2f5;color:#333;}
    .card{background:#fff;padding:15px;margin-bottom:10px;border-radius:8px;box-shadow:0 1px 3px rgba(0,0,0,0.1);}
    .title{font-weight:bold;font-size:16px;margin-bottom:5px;}
    .phone{color:#e53935;font-weight:bold;font-size:18px;margin:10px 0;}
    .link{color:#1976d2;text-decoration:none;font-size:12px;}</style></head><body>
    <h2>🔥 通风招工最新线索</h2>"""
    if not rows: html += "<div class='card'>今日无符合安检条件的数据。</div>"
    else:
        for r in rows:
            html += f"""<div class="card"><div class="title">{r['标题']}</div>
            <div class="phone">📞 {r['号码']}</div>
            <a class="link" href="{r['链接']}" target="_blank">查看原帖</a>
            <span style="float:right;color:#999;font-size:12px;">{r['源']} | {r['时间']}</span></div>"""
    html += "</body></html>"
    with open("index.html", "w", encoding="utf-8") as f: f.write(html)

def push_wechat(rows):
    if not PUSHPLUS_TOKEN: return
    content = f"今日更新 {len(rows)} 条线索，点击查看详情。" if rows else "今日未发现符合条件的数据。"
    data = {"token": PUSHPLUS_TOKEN, "title": f"通风招聘 - {datetime.now().strftime('%m-%d')}", "content": content}
    try:
        requests.post("http://www.pushplus.plus/send", json=data)
    except: pass

if __name__ == "__main__":
    print("🚀 启动云端代理穿透采集...")
    all_rows = []
    
    all_rows.extend(scrape_tieba_jina())
    all_rows.extend(scrape_ybrc_jina())
    
    # 去重
    unique_rows = {r['号码']: r for r in all_rows}.values()
    
    generate_html(unique_rows)
    with open("leads.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=["源", "标题", "链接", "号码", "时间"])
        w.writeheader()
        w.writerows(unique_rows)
        
    push_wechat(unique_rows)
    print(f"🏁 运行结束！共抓取 {len(unique_rows)} 条数据。")
