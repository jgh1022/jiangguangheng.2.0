import math 
import streamlit as st
import random
st.set_page_config(page_title="姜广恒",layout="wide")
st.markdown("""
 <style>
 /* 黄色按钮样式 */
 div.stButton > button {
     background-color: #FFD700;
     color: black;
     border-radius: 8px;
     font-weight:bold;
 }
 div.stButton > button:hover {
     background-color:#D4AF00;
 }
 /* 普通文字输入框 st.text_input */
 div.stTextInput > div > div > input {
     background-color: #fffbe6;
     color: #000000;
     border-radius:6px;
     border:1px solid #FFD700;
 }
 /* 数字输入框  */
 div.stNumberInput > div > div > input {
     background-color: #fffbe6;
     color: black;
     border-radius:6px;
     border:1px solid #FFD700;
 }
 input[type="radio"] + div,
 input[type="radio"] + div * {
     font-size: 20px !important;
     font-weight: bold !important;
 }
 </style>
 """, unsafe_allow_html=True)
#爆破振动（萨道夫斯基公式）
def sdfsj(Q_max,R,alpha,K):
    v = K*pow((pow(Q_max,1/3)/R),alpha)
    return v
#爆破空气冲击波超压
def chongjibo(Q_max,R,Kp,beta):
    dp = Kp*pow((pow(Q_max,1/3)/R),beta)
    return dp
#爆破噪声（声压级衰减）
def zaosheng(R,Lp0,R0):
    Lp = Lp0-20*math.log10(R/R0)
    return Lp
#爆破粉尘评估
def fenchen(Gdust,Kd,A,w,Qtotal):
    Gremain = Kd*Qtotal*math.exp(-A*w)
    return Gremain
#爆破有毒炮烟（CO一氧化碳）
def duyan(kco,Qtotal):
    Mco = kco*Qtotal
    return Mco



st.title("露天爆破危害效应评估模拟器")
st.divider()
st.subheader("引言")
st.markdown("""
<p style=\"color:#2980B9\">爆炸是一类剧烈的快速氧化还原化学反应。炸药（含能材料）内部本身同时携带氧化剂与可燃组分，无需外界氧气参与，在起爆刺激下，化学键瞬间断裂重组，在微秒级时间内完成反应，释放大量热能并生成高温高压气态产物。
急剧膨胀的气体向外做功，就形成爆破现象，并衍生出地震波、空气冲击波、爆破飞石、爆破噪声、爆破粉尘五大有害效应，
而这五大效应需要在专业人员的评估合格后才能使相关工程通过审批，这类专业人员就是爆破安全评估工程师。首先先向你介绍一下爆破安全评估工程师的职责，爆破安全评估工程师是审核爆破设计方案，出具相关安全评估报告，他们主要负责评估爆破五大有害效应是否超标，是否符合标准
那同学想不想体验一下爆破安全工程师的部分工作，假如你现在就是一名爆破安全工程师，希望通过这个评估模拟器你能进一步了解爆炸化学反应的评估，提高对爆破专业的兴趣与热爱</p>
""",unsafe_allow_html=True)
st.markdown("现在有一个爆破项目需要你去评估这五项效应，点击下方按钮即可查看")
if "scene" not in st.session_state:
    st.session_state.scene = None
if st.button("项目数据记录"):
    Q_max = random.uniform(5,200)
    R = random.uniform(10,300)
    K = random.uniform(50,300)
    alpha = random.uniform(1.2,2.0)
    Kp = random.uniform(1.0,15.0)
    beta = random.uniform(1.0,1.3)
    Kd = random.uniform(0.02,0.12)
    w = random.uniform(0.5,3.0)
    kco = random.uniform(0.005,0.030)
    st.session_state.scene = {
        "Q_max" : Q_max,
        "R" : R,
        "K" : K,
        "alpha" : alpha,
        "Kp" : Kp,
        "beta" : beta,
        "w" : w,
        "kco" : kco,

    }
    s = st.session_state.scene
    st.info("""
    某区内，由于扩建需要将电厂内一座100米高的钢筋混凝土烟囱拆除，经过设计研讨现公布爆破参数设计，工程队根据施工经验对单孔的装药量为{:.2f}Kg,经过现场勘探，本次的现场测量距离为{:.2f}m，
    ，且得知当地的场地系数为{:.2f}，以质点振动速度衰减指数为{:.2f}，超压系数为{:.2f}，经验系数2为{:.2f}为标准，预设计的单位喷水量为{:.2f}Kg，且预估一氧化碳的产尘系数为{:.2f}
               注：本数据为程序随机生成，不具有实际意义，仅供仿真模拟


    """.format(s["Q_max"],s["R"],s["K"],s["alpha"],s["Kp"],s["beta"],s["w"],s["kco"]))

st.markdown("<p style=\"color:#FF0000\">注意：重复点击会导致数据刷新！【这里仅作为实例，如有其他数据可忽略系统生成的随机数据】</p>",unsafe_allow_html=True)

st.divider()
st.markdown('<p style="font-size:20px;font-weight:bold">从以下五个选项中选择相应测试界面即可进行评估 </p>',unsafe_allow_html=True)
select_item = st.radio(
    "请选择需要评估的项目:",
    ["爆破振动评估","爆破空气冲击波评估","爆破噪声评估","爆破粉尘评估","爆破毒烟一氧化碳含量评估"]
)
if select_item == "爆破振动评估":
    st.subheader("爆破振动")
    st.markdown("""
    同学们首先想到的爆破效果应该就振动，那同学知道爆炸为什么会产生振动吗？是因为炸药化学能释放，导致介质瞬间受热膨胀、晶体结构挤压错位，
    化学能转化为机械能，向岩土内部传递应力波。但是同学们知道爆炸振动应该怎么评估吗？
    计算爆破振动就需要我们用到萨道夫斯基公式，我们要计算的就是质点峰值振动速度，通过计算结果我们就可以大体评估弹药量对民用建筑的影响是否达标了
    下列就是具体参数介绍：<br>
    R:测点到爆源的距离<br>
    K:场地系数<br>
    alpha:衰减指数
    """,unsafe_allow_html=True)
    st.markdown("现在我们来试试第一个有害效应的评估工作吧！")
#用户输入
    Q_max = st.number_input(label="最大一段起爆量Q_max(Kg)",value=5.0,min_value=0.0,key="Q1")
    R = st.number_input(label="保护距离R(m)",value=50.0,min_value=10.0,key="R1")
    alpha = st.number_input(label="衰减指数alpha",value=1.4,min_value=0.0)
    K = st.number_input(label="场地系数",value=100.0,min_value=0.00)
    st.divider()
    
    btn1 = st.button("开始计算质点振动速度")
    if btn1:
        v = K*pow((pow(Q_max,1/3)/R),alpha)
        st.write("经计算得到的质点振动速度为",v)
        if v <= 2.5:
            st.success("振动指标合格！")
        elif v <= 5:
            st.warning("振动指标有点高哦，需要密切观察！")
        else:
            st.error("振动超标，需减少弹药量！")
        st.markdown("""通常算出的振速会和国家标准允许振速对比，土窑洞、砖房、钢筋混凝土建筑限值都不一样，以上是以民用建筑为例进行的粗略计算，在这里还要向同学们补充一下该指标评估的意义：爆破地震本质是爆炸化学反应能量向大地传递，化学反应能量越大，岩土质点振动速度越高，
        化学能量失控会导致墙体开裂、地基损伤，必须通过化学能量公式定量评估振动强度。
        """)
    
    
elif select_item == "爆破空气冲击波评估":
    st.subheader("爆破空气冲击波超压的评估")
    st.markdown("""
先恭喜同学完成了第一个指标的评估，现在我们就要进行第二项指标即爆破空气冲击波超压的评估了，其原理是爆炸反应生成超高压气态产物，气体在裂隙、孔隙中极速膨胀、突破岩石结构，
岩石被化学能产生的高压气体撕裂、推出，形成飞石。
且这种冲击波会随距离快速衰减，
爆破安全评估工程师就需要计算检查爆炸产生的空气波会不会吹碎门窗玻璃、掀翻围栏、伤人、损坏设备，而评估空气冲击波超压也有相应的经验公式，这个公式包含了dp、Q_max、R、beta这几个变化量<br>
dp:冲击波超压(MPa)<br>
Kp:经验系数<br>
beta:经验系数<br>
(通常台阶填塞爆破取Kp=0.8,beta=2)
""",unsafe_allow_html=True)
    st.markdown("现在请同学动手试试吧！")
    Q_max = st.number_input(label="最大一段起爆量Q_max(Kg)",value=5.0,min_value=0.0,key="Q2")
    R = st.number_input(label="保护距离R(m)",value=50.0,min_value=10.0,key="R2")
    Kp = st.number_input(label="超压系数",value=0.8,min_value=0.0)
    beta = st.number_input(label="经验系数2",value=0.8,min_value=0.0)
    st.divider()
    
    btn2 = st.button("开始计算冲击波超压")
    if btn2:
        dp = chongjibo(Q_max,R,Kp,beta)
        st.write("计算得到的冲击波超压为",dp)
        if dp <= 0.02:
            st.success("超压较小，周围建筑门窗安全，该指项达标")
        elif dp <= 0.05:
            st.warning("超压偏大，周围建筑门窗可能开裂，需要注意")
        else:
            st.error("超压不达标，易击碎玻璃，破坏墙体，不符合标准")
        st.markdown("""知识拓展：爆破冲击波不是地震波，一个是以空气为介质，一个是以土壤为介质,且飞石不是“力气大”，是爆炸化学反应产气压力超过岩石强度导致的，
药量配比（化学当量配比）不合理、氧化反应不完全、产气压力过大，都会造成远距离飞石，
化学能量计算是飞石安全距离评估的核心依据。""")
    
    
elif select_item == "爆破噪声评估":
    st.subheader("爆破噪声的评估")
    st.markdown("""
    评估工作已经到了一半路程，接下来就是同学们容易想到的噪声问题，炸药爆炸的声音可是一个不可忽视的问题，爆炸化学反应瞬间产生数千摄氏度高温气体，与常温空气发生极速热交换、热震荡，
    高温气体快速膨胀、收缩，产生强烈空气脉动声波。
    那么一般是怎么评估爆破噪声问题呢?其原理是冲击波衰减之后转化为强噪声，噪声级和弹药量正相关，和距离负相关，经计算得到噪声分贝值，对照《声环境质量标准》<br>
    Lp0:爆源声级<br>
    R:测点到爆源的距离(m)<br>
    Lp:距离R处噪声值
    """,unsafe_allow_html=True)
    st.markdown("现在我们动手试试吧")
    R = st.number_input(label="保护距离R(m)",value=50.0,min_value=0.0,key="R3")
    Lp0 = st.number_input(label="爆源声级(默认以150dB为参考数)",value=150.0,min_value=0.0)
    R0 = st.number_input(label="距离(默认以1m为参考数)",value=1.0,min_value=0.0)
    st.divider()
  
    btn3 = st.button("开始计算爆破噪声")
    if btn3:
        Lp = zaosheng(R,Lp0,R0)
        if Lp <= 70:
            st.success("昼间达标")
        elif Lp <= 85:
            st.warning("具有扰民风险")
        else:
            st.error("严重超标，请及时注意")
        st.markdown("""知识拓展：一般工程措施是通过多空微差起爆、填塞好炮孔、避开夜间爆破以降低噪声,噪声大小直接取决于炸药化学反应放热速率,
        反应越剧烈、升温越快，噪声峰值越高。
        评估噪声本质就是评估爆炸化学反应剧烈程度，保护人体听觉与周边生活环境。""")
        
elif select_item == "爆破粉尘评估":
    st.subheader("爆破粉尘评估")
    st.markdown("""
    众所周知，爆炸往往会伴随着大量的粉尘颗粒，
    1. 爆炸高温使岩石中硅酸盐、碳酸盐矿物热分解<br>
    2. 高温冲击使大分子矿物结构键断裂、破碎成超细颗粒<br>
    3. 爆炸反应产生的水汽、氧化物气溶胶吸附粉尘，形成悬浮污染气溶胶体系<br>
    这些粉尘不会凭空消失，我们能做的就是尽量减少粉尘的扩散，但处理粉尘的效果怎么评估呢?
    那么我们就要估算粉尘TSP总悬浮颗粒物浓度和粉尘影响半径，其和风速、岩性、是否洒水降尘有关，通过评估处理后的最终粉尘量来评估抑尘效果，判断会不会污染空气，影响周围人呼吸<br>
    Gdust:总产尘质量(kg)<br>
    Kd:产尘系数<br>
    Gremain:治理后剩余粉尘量(kg)<br>
    A:水雾系数<br>
    w:单位喷水量
    """,unsafe_allow_html=True)
    st.markdown("同学们开始操作吧")
    Gdust = st.number_input(label="总产尘量(kg)",value=100.0,min_value=0.0)
    Kd = st.number_input(label="产尘系数",value=2.0,min_value=0.0)
    A = st.number_input(label="水雾系数",value=10.0,min_value=0.0)
    w  = st.number_input(label="单位喷水量(Kg)",value=50.0,min_value=0.0)
    Qtotal = st.number_input(label="气体体积(立方米)",value=50.0,min_value=0.0,key="Qt1")
    st.divider()
    
    btn4 = st.button("开始评估粉尘指标")
    if btn4:
        Gremain = fenchen(Gdust,Kd,A,w,Qtotal)
        n = 1-math.exp(-A*w)
        if n < 0.5:
            st.error("抑尘不足，需要加大水量")
        elif n <0.75:
            st.warning("效果一般")
        else:
            st.success("抑尘效果不错")
        st.markdown("""知识拓展：抑尘措施一般有炮口注水、爆前洒水、喷雾降尘、泡沫降尘,爆破粉尘不是单纯石头灰，是矿物高温化学反应产物,
        含 SiO₂、CaO、MgO、碳酸盐分解微粒，吸入有害人体、污染空气。
        绿色爆破、低尘爆破本质就是控制爆炸化学反应温度与产气产物。""")
    
    
elif select_item == "爆破毒烟一氧化碳含量评估":
    st.subheader("爆破有毒气体评估")
    st.markdown("""
    同学们，坚持到这我们终于迎来了最后一项评估，爆炸是关于化学反应，其会产生一氧化碳、氮氧化物，这就给环境带来了一系列问题
    我们以一氧化碳为例进行评估，首先需要知道CO的产污系数kco，将它与气体总量相乘就可以得到CO的粗略产量
    """)
    st.markdown("同学们准备好了吗")
    kco = st.number_input(label="一氧化碳产生系数",value=0.03,min_value=0.01)
    Qtotal = st.number_input(label="气体总量",value=50.0,min_value=0.0,key="Qt2")
    st.divider()
    
    btn5 = st.button("开始评估一氧化碳含量")
    if btn5:
        Mco = duyan(kco,Qtotal)
        if Mco <= 0.05*Qtotal:
            st.success("毒烟控制较好")
        elif 0.05*Qtotal < Mco <=0.1*Qtotal:
            st.warning("注意低洼区域通风警戒")
        else:
            st.error("毒烟量大，风险高")
        st.markdown("知识拓展：爆破后必须等待足够通风时间，人员才能进入爆区，这里只是科普演示，有害气体产量实际还与与炸药类型、填塞质量和通风条件有关")
rock_type = st.selectbox("岩性参考表，仅作为补充",["点击即可查看","花岗岩:K=150,alpha=1.8,kd=1.0","砂岩:K=120,alpha=1.6,kd=0.7","石灰岩:K=100,alpha=1.4,kd=0.5,K=60,alpha=1.2,kd=0.3","风化岩:K=60,alpha=1.2,kd=0.3"])
st.divider()
st.subheader("结束语")
st.markdown("""
<p style=\"color:#2980B9\">
爆破工程并非简单的破岩拆除技术，而是支撑我国交通强国、能源强国、新型城镇化、国防安全建设的基础性关键工程技术，深度服务于国家重大发展战略。所有大型基建工程、矿山能源开发、城市更新改造、水利通道建设，都离不开安全、精准、可控的爆破技术作为底层支撑。</p>
<p style=\"color:#2980B9\">
在国家高质量发展战略背景下，传统粗放爆破模式已无法满足新时代安全环保要求。爆破振动、空气冲击波、噪声、粉尘、有毒气体五项有害效应的精准评估，正是实现“绿色爆破、精细爆破、安全爆破”的核心技术环节。精准的爆破参数计算与风险评估，能够最大限度降低工程对周边建筑、生态环境、人员设备的影响，实现工程建设与生态保护、公共安全的协调统一，契合国家安全生产、生态环保、绿色建造的顶层政策导向。</p>
 <p style=\"color:#2980B9\">
从国家战略高度来看，爆破技术不仅服务民用基建，更深度支撑国防地下工程、战略防护工程、深部资源开发、重大国防基础设施建设等国家安全任务。精细爆破、精准灾害评估、有害效应可控化技术，是我国国防工程安全、地下空间战略利用、重大工程韧性建设的重要科技基础。</p>
 <p style=\"color:#2980B9\">
本项目设计是希望能够帮助对该领域感兴趣的同学们初步了解爆破评估的部分工作，提高对该领域专业的兴趣和喜爱</p>
""",unsafe_allow_html=True)
st.divider()
st.caption("项目说明：本微型模拟器为安徽理工大学化工与爆破学院化学创新大赛仿真演示作品，公式与系数均采用文献经验简化模型，所有计算结果严禁用于实际爆破工程设计与施工")
st.caption("开发方向：智能爆破有害效应仿真评估，模拟爆破工程师勘测、录入参数和安全校验流程")
st.caption("参考文献：[1]爆破安全规程GB 6722 [2]露天爆破粉尘与有毒气体扩散相关文献 [3]爆破振动、空气冲击波经验公式相关教材 [4]相关爆炸化学知识文献")
st.caption("特别鸣谢计算机科学与工程学院王艳老师的指导")
st.caption("开发者：姜广恒    |    安徽理工大学   弹药工程与爆炸技术26级4班")
