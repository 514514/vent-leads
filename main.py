import asyncio, csv, re, random, os
from datetime import datetime
from camoufox.async_api import AsyncCamoufox

# ==================== 精准安检词库 ====================
# 1. 负向词库：命中即过滤（过滤掉无关广告、其他行业、废话）
NEGATIVE_KEYWORDS = [
    # 互联网/黑产/杂项
    "办理", "认证", "网查", "社保", "换群", "拼多多", "淘宝", "京东", 
    "刷单", "兼职日结", "免费领取", "加微信领", "扫码", "点击链接", 
    "红包", "投票", "助力", "砍价", "微商", "招代理", "游戏推广", 
    "群发助手", "测试消息", "系统消息", "互换", "接活",
    # 其他无关行业/岗位
    "保洁", "兼职", "征婚", "网红", "论文", "自学", "家具", "名片", 
    "小店", "发明", "专利", "支架", "护照", "撤回", "境外", "早安", 
    "销售", "清洗", "拖欠", "特种", "投标", "广告", "操作机器", 
    "普工", "船厂", "标签", "标牌", "考试", "水箱", "朋友圈", "帮助", 
    "救救", "求求", "回国", "证书", "太阳", "小程序", "报名", "出国", 
    "印尼", "化工", "河道", "白班", "形象", "欠债", "经济", "宣传", 
    "海外", "鄂尔多斯", "泥瓦匠", "木条", "含胶", "标书", "免税", 
    "时光", "冷静", "王者", "小天鹅", "云欢", "电泳线", "海目星", 
    "摘盒工", "主播", "好工作", "推荐", "视频面试", "维修", "线上面试", 
    "高薪", "外账", "钳工", "总店", "童车", "设计", "岗位", "三轮车", 
    "四轮车", "坐班", "长白班", "临时工", "跟单员", "打包", "客服", 
    "泰国", "注塑厂", "车业", "汉堡", "水电费", "锂电池", "汽车", 
    "宝妈", "银行", "垫资", "龙岗", "分切工", "快递", "风水", 
    "顺风车", "鲜花", "隔断", "爆破", "座椅", "资料", "居家", "官方", 
    "婚姻", "债务", "宽带", "运营商", "汽配厂", "扣保险", "送货员", 
    "信用", "水利", "培训", "抖音", "物流", "装卸", "食品厂", "分装", 
    "乌木", "麻柳", "两班倒", "操作工", "银行卡", "污染", "口感", 
    "一级房建", "演唱会", "电视", "发货", "安保", "工作轻松", "美的", 
    "轴皮", "锂电", "奥克斯", "搬运工", "冷暖机", "洗衣机", "净化器", 
    "柜机", "天然气", "燃气", "硫酸", "玻璃", "发票", "破产", 
    "中介", "驾校", "新到货", "保险", "审车", "车企", "门店", 
    "水电平摊", "建造师", "盛会", "省电", "机遇", "秒杀", "大促销", 
    "三班倒", "出租", "流量卡", "领取", "秒发", "特价", "破价", 
    "九阳", "罚款", "阻燃", "防虫", "压力", "搭建", "舞台", 
    "全国资源", "你的项目", "说明会", "投资人", "正泰", "双玻", 
    "包膜机", "夜班", "净水", "成色", "卤菜", "养生", "天合", 
    "晶科", "准新机", "鸿泰", "抗震", "格力", "海信", "爆款", 
    "畅销", "枪手", "美容", "学习", "机构", "线上型号", "国补", 
    "找钱", "找圈子", "智慧", "保姆", "住家", "阿姨", "冰箱", 
    "洗碗机", "松下", "专票", "体验", "商保", "疲劳", "疗程", 
    "内机", "侧出风", "进口", "卡萨帝", "到货", "自行车", "投资", 
    "资金", "捡药材", "货车", "司机", "驾照", "小红书", "添可", 
    "代办", "车找人", "洗车工", "纸箱厂", "电缆", "年终奖", "报错", 
    "光缆", "促销", "便利店", "顺路", "退税", "人找车", "兼职群", 
    "视频", "线上", "大量出", "价低", "导购员", "印刷厂", "外快", 
    "辅导员", "翻译", "零活", "电动车", "养殖", "送安", "堵漏", 
    "漏水", "执行", "管理员", "新版本", "储罐", "加气站设备", 
    "执照", "石材", "荒料", "铲车", "课程", "日结", "押金", 
    "介绍活", "阳光棚", "坚果", "谷物", "承接", "创维", "画框", 
    "效果图", "案例", "渠道", "吸气", "空气", "火灾", "探测器", 
    "平纹", "精纺", "黑丝", "精准", "题库", "二手", "求购", 
    "液化", "日产", "手续", "欢迎老板", "家电", "安检", "美妆", 
    "护肤", "网约车", "到家", "烤鱼", "烧烤", "事务所", "备案", 
    "供应商", "订单", "开槽", "科技", "水质", "化妆", "服装", 
    "面霜", "家务", "肩膀", "花生油", "食用", "近视", "镜片", 
    "深度", "日订单", "矿山", "测试机", "铲墙", "信息", "化学品", 
    "金属", "轻松班", "甜品", "拉面", "青春没有售价", "光伏", 
    "水管", "土方", "挖运", "面粉", "主营", "怕查", "非偏", 
    "化学", "工业", "电子", "心情", "颈椎病", "包车", "约车", 
    "面包", "工位", "扎心", "引进", "茶水", "动物", "领养", 
    "开水", "水龙头", "东芝", "红娘", "婚恋", "肩颈", "不舒服", 
    "穴位", "数字", "平台", "明星", "对象",
    # 闲聊
    "换着发", "别逗我", "精神小伙"
]

# 2. 强权拦截词库：帖子必须包含以下至少一个词，否则直接淘汰（确保是通风行业）
STRONG_KEYWORDS = [
    "招", "聘", "师傅", "大工", "中工", "清工", "外包", "小工", "找工人", "急招", "诚聘",
    "安装", "风管", "通风", "铁皮", "合管", "排烟", "白铁", "暖通",
    "队伍", "班组", "包工", "工地", "干活", "工资", "需人", "缺人"
]

# 3. 极度危险的【求职/找活】词（一票否决：我们是去找老板的，不是找工人的）
SEEKER_BLACKLIST = [
    "找活", "求职", "找工作", "求带走", "本人找", "想找个", "现有人员",
    "班组空出", "人员空出", "待业", "求收留", "找份活", "求活干", "哪个老板要",
    "现有风管", "现有通风", "工地完工", "专业合管团队", "专业队伍", "随时出发",
    "求包", "本人从事", "找工作", "找点事", "接点活"
]

# 4. 极度危险的【推销/材料】词（一票否决：过滤卖材料、卖机器的厂家）
SPAM_BLACKLIST = [
    "厂家", "回收", "批发", "生产", "产品", "批量", "定制", "现货", "货源", "包邮", 
    "成本价", "专产", "出售", "钢管", "配套", "加工", "铝合金", "风口", "燃热", 
    "派单", "收银", "一体机", "加盟", "直出", "专业加工", "直销", "供应", "厂价", 
    "厂家直销", "材料厂"
]
# ================================================

OUT = "leads.csv"
# 手机号正则：支持中间带空格或横杠，如 138 1234 5678 或 138-1234-5678
PHONE_RE = re.compile(r"1[3-9]\d[\s\-]*\d{4}[\s\-]*\d{4}")

async def human_wait(page, min_s=2, max_s=5):
    await asyncio.sleep(random.uniform(min_s, max_s))

def check_text_pass(text):
    """六重安检核心逻辑"""
    # 1. 一票否决：求职/找活
    if any(kw in text for kw in SEEKER_BLACKLIST):
        return False, "求职/找活拦截"
    
    # 2. 一票否决：推销/材料/厂家
    if any(kw in text for kw in SPAM_BLACKLIST):
        return False, "推销/材料拦截"

    # 3. 强权拦截：必须包含至少一个强相关词（确认是通风行业）
    if not any(kw in text for kw in STRONG_KEYWORDS):
        return False, "非目标行业"

    # 4. 负向词库：命中则淘汰（过滤掉无关信息）
    for kw in NEGATIVE_KEYWORDS:
        if kw in text:
            return False, f"命中负向词[{kw}]"

    return True, "通过"

async def main():
    rows = []
    # 搜索词更加精准，提高召回率
    keywords = ["通风 招工", "通风 安装 电话", "风管 招工", "暖通 招聘", "白铁 招工", "排烟 安装", "四川 通风 安装", "成都 通风 招工"]
    
    print("启动云端伪装浏览器...")
    async with AsyncCamoufox(headless=True) as browser:
        page = await browser.new_page()
        
        for kw in keywords:
            print(f"\n🔍 正在搜索: {kw}")
            search_url = f"https://tieba.baidu.com/f/search/res?ie=utf-8&qw={kw}"
            
            try:
                await page.goto(search_url, wait_until="domcontentloaded", timeout=30000)
                await human_wait(page, 3, 6)
            except Exception as e:
                print(f"网络超时跳过: {e}")
                continue

            # 云端遇到验证码无法人工滑动，检测到验证码直接跳过该词
            title_text = await page.title()
            if "安全验证" in title_text or "验证" in title_text:
                print(f"  [跳过] 触发百度风控验证，跳过当前词")
                continue
                
            # 提取链接
            links = await page.locator("a[href*='/p/']").all()
            hrefs = []
            for link in links[:10]: # 每个词最多看前10个帖子
                href = await link.get_attribute("href")
                if href and "/p/" in href:
                    match = re.search(r"/p/(\d+)", href)
                    if match:
                        clean_url = f"https://tieba.baidu.com/p/{match.group(1)}"
                        if clean_url not in hrefs:
                            hrefs.append(clean_url)

            print(f"  -> 找到 {len(hrefs)} 个帖子，开始安检抓取...")

            for url in hrefs:
                try:
                    await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                    await human_wait(page, 2, 4)
                    
                    full_text = await page.inner_text("body")
                    raw_phones = PHONE_RE.findall(full_text)
                    # 清洗号码（去掉空格和横杠）
                    phones = [re.sub(r"[\s\-]", "", p) for p in raw_phones]

                    if phones:
                        post_title = await page.title()
                        # 标题+正文组合检测，防止标题里有电话被漏掉
                        combined_text = post_title + full_text
                        
                        # 进行六重安检
                        is_pass, reason = check_text_pass(combined_text)
                        
                        if is_pass:
                            unique_phones = list(set(phones))
                            rows.append({
                                "源": "贴吧",
                                "关键词": kw,
                                "标题": post_title[:80].replace("\n", ""),
                                "链接": url,
                                "完整号码": "|".join(unique_phones),
                                "采集时间": datetime.now().isoformat()
                            })
                            print(f"    [+] ✅ 成功放行: {unique_phones} | {post_title[:20]}...")
                        else:
                            print(f"    [-] ❌ 拦截: {reason} | 标题: {post_title[:20]}...")
                except Exception:
                    continue
                
                await human_wait(page, 1, 3)

    # 写入数据
    if rows:
        # 去重（避免多个搜索词抓到同一个帖子）
        final_rows = list({r['链接']: r for r in rows}.values())
        
        file_exists = os.path.isfile(OUT)
        with open(OUT, "a", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=final_rows[0].keys())
            if not file_exists:
                w.writeheader()
            w.writerows(final_rows)
        print(f"\n✅ 运行结束！共写入 {len(final_rows)} 条精准线索 -> {OUT}")
    else:
        print("\n❌ 本轮没找到符合安检条件的帖子。")
        # 【兜底机制】：就算没数据，也建一个只有表头的空表，保证 GitHub 能上传 artifact
        with open(OUT, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f)
            w.writerow(["源", "关键词", "标题", "链接", "完整号码", "采集时间"])

if __name__ == "__main__":
    asyncio.run(main())
