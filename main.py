import asyncio, csv, re, random, os, json, time, requests
from datetime import datetime
from camoufox.async_api import AsyncCamoufox
from urllib.parse import urljoin

# ==================== 你的微信测试号配置 ====================
WX_APP_ID = "wx70e0f1177aa8c3e0"
WX_APP_SECRET = "3c0dce6997413add7ae2e22ce1ec526f"
WX_OPEN_ID = "ooFK72w1l2q8diiEQ8jVv19RTpvI"
WX_TEMPLATE_ID = "3vMtn-A5bH-48Ki8B565kqvpWLYpka2KCtkCAfaeAwQ"

# 你的 GitHub 用户名和仓库名（用来生成网页链接）
GH_USER = "514514" 
GH_REPO = "vent-leads"
# ==========================================================

# 词库省略，保持你原来的六重安检词库即可...
NEGATIVE_KEYWORDS = ["厂家", "回收", "办理", "认证", "网查", "社保", "换群", "拼多多", "淘宝", "京东", "刷单", "兼职日结", "免费领取", "加微信领", "扫码", "点击链接", "红包", "投票", "助力", "砍价", "微商", "招代理", "游戏推广", "注册送", "群发助手", "测试消息", "系统消息", "保洁", "兼职", "征婚", "批发", "生产", "产品", "批量", "网红", "装修", "论文", "个人接单", "自学", "定制", "家具", "名片", "小店", "发明", "专利", "支架", "msg", "优质群", "质量好", "价格低", "护照", "市场", "客户", "撤回", "钻孔", "开孔", "互换", "接活", "境外", "负责人", "早安", "销售", "清洗", "拖欠", "特种", "投标", "广告", "酒", "处理", "操作机器", "普工", "船厂", "标签", "标牌", "免费", "预算", "考试", "低价", "水箱", "朋友圈", "帮助", "救救", "求求", "回国", "低价格", "一手", "俄罗斯", "有机", "出境", "证书", "太阳", "现货", "环氧", "高效", "小程序", "增压", "货源", "包邮", "单台", "成本价", "松川", "link", "抽气罩", "专产", "报名", "出国", "印尼", "化工", "河道", "白班", "形象", "欠债", "经济", "宣传", "海外", "鄂尔多斯", "出售", "钢管", "泥瓦匠", "木条", "含胶", "配套", "标书", "高温", "免税", "时光", "冷静", "王者", "小天鹅", "云欢", "电泳线", "除尘系统", "海目星", "摘盒工", "主播", "好工作", "推荐", "视频面试", "维修", "线上面试", "高薪", "外账", "钳工", "总店", "童车", "设计", "岗位", "三轮车", "四轮车", "坐班", "长白班", "临时工", "跟单员", "打包", "客服", "泰国", "注塑厂", "车业", "汉堡", "水电费", "锂电池", "汽车", "宝妈", "银行", "垫资", "龙岗", "分切工", "快递", "风水", "顺风车", "鲜花", "隔断", "爆破", "座椅", "资料", "居家", "官方", "婚姻", "债务", "宽带", "运营商", "汽配厂", "扣保险", "送货员", "信用", "水利", "培训", "抖音", "物流", "装卸", "食品厂", "分装", "乌木", "麻柳", "两班倒", "操作工", "银行卡", "污染", "口感", "一级房建", "演唱会", "电视", "价格", "发货", "安保", "工作轻松", "美的", "轴皮", "锂电", "奥克斯", "搬运工", "冷暖机", "洗衣机", "净化器", "柜机", "天然气", "燃气", "硫酸", "玻璃", "发票", "破产", "中介", "优质", "民营", "驾校", "新到货", "保险", "审车", "车企", "门店", "服务", "水电平摊", "建造师", "盛会", "省电", "机遇", "秒杀", "大促销", "三班倒", "出租", "流量卡", "领取", "秒发", "特价", "破价", "九阳", "罚款", "阻燃", "防虫", "压力", "搭建", "舞台", "全国资源", "你的项目", "说明会", "投资人", "正泰", "双玻", "包膜机", "夜班", "净水", "成色", "卤菜", "养生", "天合", "晶科", "准新机", "鸿泰", "抗震", "格力", "海信", "爆款", "畅销", "枪手", "美容", "学习", "机构", "线上型号", "国补", "找钱", "找圈子", "智慧", "保姆", "住家", "阿姨", "冰箱", "洗碗机", "松下", "专票", "体验", "商保", "疲劳", "疗程", "内机", "侧出风", "进口", "卡萨帝", "到货", "自行车", "投资", "资金", "捡药材", "货车", "司机", "驾照", "小红书", "添可", "代办", "车找人", "洗车工", "纸箱厂", "电缆", "年终奖", "报错", "光缆", "促销", "便利店", "顺路", "退税", "人找车", "兼职群", "视频", "线上", "大量出", "价低", "导购员", "印刷厂", "外快", "辅导员", "翻译", "零活", "电动车", "养殖", "送安", "堵漏", "漏水", "执行", "管理员", "新版本", "储罐", "加气站设备", "执照", "石材", "荒料", "铲车", "课程", "日结", "押金", "介绍活", "阳光棚", "坚果", "谷物", "承接", "创维", "画框", "效果图", "案例", "渠道", "吸气", "空气", "火灾", "探测器", "平纹", "精纺", "黑丝", "精准", "题库", "二手", "求购", "液化", "日产", "手续", "欢迎老板", "家电", "安检", "美妆", "护肤", "网约车", "到家", "烤鱼", "烧烤", "事务所", "备案", "供应商", "订单", "开槽", "科技", "水质", "化妆", "服装", "面霜", "家务", "肩膀", "花生油", "食用", "近视", "镜片", "深度", "日订单", "矿山", "测试机", "铲墙", "信息", "化学品", "金属", "轻松班", "甜品", "拉面", "青春没有售价", "光伏", "水管", "土方", "挖运", "面粉", "主营", "怕查", "非偏", "化学", "工业", "电子", "心情", "颈椎病", "包车", "约车", "面包", "工位", "扎心", "引进", "茶水", "动物", "领养", "开水", "水龙头", "东芝", "红娘", "婚恋", "肩颈", "不舒服", "穴位", "数字", "平台", "明星", "对象", "换着发", "别逗我", "精神小伙"]
STRONG_KEYWORDS = ["招", "聘", "师傅", "大工", "中工", "清工", "外包", "小工", "找工人", "急招", "诚聘", "安装", "风管", "通风", "铁皮", "合管", "排烟", "白铁", "暖通", "队伍", "班组", "包工", "工地", "干活", "工资", "需人", "缺人"]
SEEKER_BLACKLIST = ["找活", "求职", "找工作", "求带走", "本人找", "想找个", "现有人员", "班组空出", "人员空出", "待业", "求收留", "找份活", "求活干", "哪个老板要", "现有风管", "现有通风", "工地完工", "专业合管团队", "专业队伍", "随时出发", "求包", "本人从事", "找工作", "找点事", "接点活"]
SPAM_BLACKLIST = ["厂家", "回收", "批发", "生产", "产品", "批量", "定制", "现货", "货源", "包邮", "成本价", "专产", "出售", "钢管", "配套", "加工", "铝合金", "风口", "燃热", "派单", "收银", "一体机", "加盟", "直出", "专业加工", "直销", "供应", "厂价", "厂家直销", "材料厂"]

OUT = "leads.csv"
PHONE_RE = re.compile(r"1[3-9]\d[\s\-]*\d{4}[\s\-]*\d{4}")

async def human_wait(page, min_s=2, max_s=5):
    await asyncio.sleep(random.uniform(min_s, max_s))

def check_text_pass(text):
    if any(kw in text for kw in SEEKER_BLACKLIST): return False, "求职/找活拦截"
    if any(kw in text for kw in SPAM_BLACKLIST): return False, "推销/材料拦截"
    if not any(kw in text for kw in STRONG_KEYWORDS): return False, "非目标行业"
    for kw in NEGATIVE_KEYWORDS:
        if kw in text: return False, f"命中负向词[{kw}]"
    return True, "通过"

# 抓取代码（贴吧 + 宜宾人才网）为了阅读体验，这里做了折叠，和你之前跑的逻辑一样
async def scrape_all(page):
    rows = []
    # 抓取贴吧
    for kw in ["通风 招工", "风管 招工"]:
        try:
            await page.goto(f"https://tieba.baidu.com/f/search/res?ie=utf-8&qw={kw}", wait_until="domcontentloaded", timeout=20000)
            await human_wait(page, 2, 4)
            if "验证" in await page.title(): continue
            links = await page.locator("a[href*='/p/']").all()
            hrefs = []
            for l in links[:5]:
                href = await l.get_attribute('href')
                if href and '/p/' in href:
                    m = re.search(r"/p/(\d+)", href)
                    if m: hrefs.append(f"https://tieba.baidu.com/p/{m.group(1)}")
            for url in hrefs:
                await page.goto(url, wait_until="domcontentloaded", timeout=20000)
                await human_wait(page, 1, 3)
                text = await page.inner_text("body")
                phones = [re.sub(r"[\s\-]", "", p) for p in PHONE_RE.findall(text)]
                if phones:
                    title = await page.title()
                    is_pass, _ = check_text_pass(title + text)
                    if is_pass: rows.append({"源": "贴吧", "标题": title[:50].replace("\n",""), "链接": url, "号码": "|".join(set(phones)), "时间": datetime.now().strftime("%m-%d")})
        except Exception: pass
    return rows

def generate_html(rows):
    """生成漂亮的数据展示网页"""
    html = """<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>招聘数据看板</title>
    <style>
        body{font-family:sans-serif;padding:10px;background:#f0f2f5;color:#333;}
        .card{background:#fff;padding:15px;margin-bottom:10px;border-radius:8px;box-shadow:0 1px 3px rgba(0,0,0,0.1);}
        .title{font-weight:bold;font-size:16px;margin-bottom:5px;}
        .phone{color:#e53935;font-weight:bold;font-size:18px;margin:10px 0;}
        .link{color:#1976d2;text-decoration:none;font-size:12px;}
    </style></head><body>
    <h2>🔥 通风招工最新线索</h2>"""
    
    if not rows:
        html += "<div class='card'>今日无符合安检条件的数据，程序运行正常。</div>"
    else:
        for r in rows:
            html += f"""
            <div class="card">
                <div class="title">{r['标题']}</div>
                <div class="phone">📞 {r['号码']}</div>
                <a class="link" href="{r['链接']}" target="_blank">点击查看原帖</a>
                <span style="float:right;color:#999;font-size:12px;">{r['源']} | {r['时间']}</span>
            </div>"""
    
    html += "</body></html>"
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

def push_wechat(rows):
    """发送微信模板消息卡片"""
    if not WX_APP_ID or not WX_APP_SECRET: return

    # 1. 获取 access_token
    token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={WX_APP_ID}&secret={WX_APP_SECRET}"
    try:
        token = requests.get(token_url).json().get("access_token")
        if not token: return

        # 2. 组装网页链接 (利用 Github Pages)
        web_url = f"https://{GH_USER}.github.io/{GH_REPO}/index.html"
        
        # 3. 发送模板消息
        msg_url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={token}"
        payload = {
            "touser": WX_OPEN_ID,
            "template_id": WX_TEMPLATE_ID,
            "url": web_url,
            "data": {
                "keyword1": {"value": datetime.now().strftime("%Y-%m-%d %H:%M"), "color": "#173177"},
                "keyword2": {"value": f"今日更新 {len(rows)} 条数据，点击查看", "color": "#e53935"}
            }
        }
        res = requests.post(msg_url, json=payload).json()
        print(f"微信推送结果: {res}")
    except Exception as e:
        print(f"推送失败: {e}")

async def main():
    all_rows = []
    print("启动云端伪装浏览器...")
    async with AsyncCamoufox(headless=True) as browser:
        page = await browser.new_page()
        try: all_rows.extend(await scrape_all(page))
        except Exception: pass

    # 1. 生成 HTML 页面
    generate_html(all_rows)
    print("✅ 网页生成完毕 -> index.html")

    # 2. 保存 CSV (作为备份)
    with open(OUT, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=["源", "标题", "链接", "号码", "时间"])
        w.writeheader()
        w.writerows(all_rows)

    # 3. 发送微信卡片
    push_wechat(all_rows)

if __name__ == "__main__":
    asyncio.run(main())
