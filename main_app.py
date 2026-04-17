import streamlit as st
import random
import time
from streamlit_image_coordinates import streamlit_image_coordinates

# ==========================================
# 1. การตั้งค่าพื้นฐานและสไตล์ (Universal Design)
# ==========================================
st.set_page_config(page_title="สมองใส ใจเบิกบานกับนายเท่ง", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #FDF5E6; }
    .stButton>button {
        width: 100%;
        height: 100px;
        font-size: 28px !important;
        border-radius: 20px;
        border: 4px solid #1E90FF;
        background-color: #FFFFFF;
        color: #1E90FF;
        font-weight: bold;
        margin-bottom: 15px;
    }
    .question-box {
        background-color: #FFFFFF;
        padding: 25px;
        border-radius: 20px;
        border: 3px solid #D2B48C;
        text-align: center;
        font-size: 26px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

def play_sound(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        st.audio(data, format="audio/mp3", autoplay=True)
    except:
        pass

# ==========================================
# 2. ฟังก์ชันเกมทั้ง 5 ด่าน
# ==========================================

# --- เกมที่ 1: ไปหลาด (ความจำ) ---
def game_1():
    st.header("🛒 เกมไปหลาดตามหาของหรอย")
    items_info = [
        {"name": "ลอกอ", "img": "images/ลอกอ.png"},
        {"name": "ชมโพ่หย้าผู้", "img": "images/ชมโพ่หย้าผู้.png"},
        {"name": "น้ำเต้า", "img": "images/น้ำเต้า.png"}
    ]
    if 'g1_setup' not in st.session_state:
        deck = items_info * 2
        random.shuffle(deck)
        st.session_state.g1_cards = deck
        st.session_state.g1_matched = []
        st.session_state.g1_opened = []
        play_sound("audio/rule_game1.mp3")
        st.session_state.g1_setup = True

    cols = st.columns(3)
    for i in range(6):
        with cols[i % 3]:
            card = st.session_state.g1_cards[i]
            if i in st.session_state.g1_matched:
                st.image(card["img"], width=200)
                st.button(f"✅ {card['name']}", key=f"g1_m_{i}", disabled=True)
            elif i in st.session_state.g1_opened:
                st.image(card["img"], width=200)
                st.button(card["name"], key=f"g1_o_{i}")
            else:
                if st.button("❓", key=f"g1_b_{i}"):
                    st.session_state.g1_opened.append(i)
                    if len(st.session_state.g1_opened) == 2:
                        idx1, idx2 = st.session_state.g1_opened
                        if st.session_state.g1_cards[idx1]["name"] == st.session_state.g1_cards[idx2]["name"]:
                            st.session_state.g1_matched.extend([idx1, idx2])
                            play_sound(f"audio/{card['name']}.mp3")
                        else:
                            play_sound("audio/try_again.mp3")
                        time.sleep(0.5)
                        st.session_state.g1_opened = []
                    st.rerun()
    if len(st.session_state.g1_matched) == 6:
        time.sleep(1)
        st.session_state.page = "SUMMARY"
        st.rerun()

# --- เกมที่ 2: เกมตาไว (สมาธิ) ---
def game_2():
    st.header("👁️ เกมตาไว (ตามหาของดีเมืองอ่าวลึก)")
    
    # พิกัด x, y ของสถานที่ในภาพตลาด
    locations = {
        "วัดบางโทง": {"x": 245, "y": 150, "audio": "audio/วัดบางโทง.mp3"},
        "น้ำตกธารโบกขรณี": {"x": 120, "y": 380, "audio": "audio/น้ำตกธารโบกขรณี.mp3"},
        "มิสเตอร์อ่าวลึก": {"x": 580, "y": 420, "audio": "audio/มิสเตอร์อ่าวลึก.mp3"}
    }
    
    if 'g2_setup' not in st.session_state:
        play_sound("audio/rule_game2.mp3")
        st.session_state.g2_found = []
        st.session_state.g2_setup = True
    
    remaining = [name for name in locations.keys() if name not in st.session_state.g2_found]
    
    if remaining:
        target_name = remaining[0]
        target_data = locations[target_name]
        
        # แสดงโจทย์เป็นข้อความตัวหนาและสีสันชัดเจน แทนการใช้รูปภาพ (เพื่อป้องกัน FileNotFoundError)
        st.markdown(f"""
            <div style='text-align:center; background-color:#FFF3E0; padding:20px; border-radius:15px; border:3px solid #FF9800;'>
                <span style='font-size:32px; color:#E65100;'>ตอนนี้ลองหา: <b>"{target_name}"</b></span><br>
                <span style='font-size:20px; color:#5D4037;'>ซ่อนอยู่ในภาพตลาดข้างล่างนี้ครับเติ้ล!</span>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("") 

        # ระบบเรียกภาพตลาด (ตรวจสอบนามสกุลไฟล์ให้ตรงกับใน GitHub ของคุณ)
        # ถ้าใน GitHub เป็น .png ให้เปลี่ยนบรรทัดล่างจาก .jpg เป็น .png นะครับ
        try:
            value = streamlit_image_coordinates("images/market_aoluek.jpg", key="g2_img")
            
            if value:
                # ตรวจสอบการจิ้ม (ขยายระยะเป็น 80 pixels เพื่อให้กดง่ายสำหรับผู้สูงอายุ)
                if abs(value["x"] - target_data["x"]) < 80 and abs(value["y"] - target_data["y"]) < 80:
                    st.session_state.g2_found.append(target_name)
                    play_sound(target_data["audio"])
                    st.toast(f"เก่งจังฮู้! เจอ {target_name} แล้ว", icon="🌟")
                    time.sleep(1)
                    st.rerun()
        except Exception as e:
            st.error("ขออภัยครับ นายเท่งหาภาพตลาด 'images/market_aoluek.jpg' ไม่เจอในระบบ")
            st.info("วิธีแก้: โปรดตรวจสอบว่ามีไฟล์ชื่อ market_aoluek.jpg อยู่ในโฟลเดอร์ images บน GitHub หรือยัง?")
            
    else:
        st.balloons()
        st.success("สุดยอดเลย! หาเจอครบทั้ง 3 แห่งแล้ว")
        time.sleep(2)
        st.session_state.page = "SUMMARY"
        st.rerun()

# --- เกมที่ 3: นายเท่งตามหาเงา (มิติสัมพันธ์) ---
def game_3():
    st.header("👥 เกมนายเท่งตามหาเงา")
    char_data = {
        "นายสะหม้อ": {"shadow": "images/samor_sh.png", "color": "images/samor_co.png"},
        "นายทอง": {"shadow": "images/thong_sh.png", "color": "images/thong_co.png"},
        "หนูนุ้ย": {"shadow": "images/nui_sh.png", "color": "images/nui_co.png"}
    }
    if 'g3_setup' not in st.session_state:
        play_sound("audio/rule_game3.mp3")
        st.session_state.g3_target = random.choice(list(char_data.keys()))
        st.session_state.g3_count = 0
        st.session_state.g3_setup = True

    target = st.session_state.g3_target
    st.image(char_data[target]["shadow"], width=250)
    st.markdown(f"<div class='question-box'>นี่คือเงาของใครกันนะเติ้ล? ({st.session_state.g3_count + 1}/3)</div>", unsafe_allow_html=True)
    
    cols = st.columns(3)
    names = list(char_data.keys())
    for i, name in enumerate(names):
        with cols[i]:
            st.image(char_data[name]["color"], width=150)
            if st.button(f"นี่คือ {name}", key=f"g3_{i}"):
                if name == target:
                    play_sound("audio/correct.mp3")
                    st.session_state.g3_count += 1
                    if st.session_state.g3_count >= 3:
                        st.session_state.page = "SUMMARY"
                    else:
                        st.session_state.g3_target = random.choice([n for n in names if n != target])
                    st.rerun()
                else:
                    play_sound("audio/try_again.mp3")

# --- เกมที่ 4: เข้าครัวทำแกง (การบริหารจัดการ) ---
def game_4():
    st.header("🥘 เกมเข้าครัวทำแกง")
    cooking_steps = [
        {"name": "หม้อ", "img": "images/step_1.png"},
        {"name": "เครื่องแกง", "img": "images/step_2.png"},
        {"name": "ปลาย่าง", "img": "images/step_3.png"},
        {"name": "ผัก", "img": "images/step_4.png"},
        {"name": "ถ้วยแกง", "img": "images/step_5.png"}
    ]
    if 'g4_step' not in st.session_state:
        st.session_state.g4_step = 0
        play_sound("audio/rule_game4.mp3")
    
    st.markdown(f"<div class='question-box'>ลำดับที่ {st.session_state.g4_step + 1}: ใส่ <b>{cooking_steps[st.session_state.g4_step]['name']}</b></div>", unsafe_allow_html=True)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(cooking_steps[i]["img"], width=150)
            if st.button(cooking_steps[i]["name"], key=f"cook_{i}"):
                if i == st.session_state.g4_step:
                    st.session_state.g4_step += 1
                    play_sound("audio/correct.mp3")
                    if st.session_state.g4_step == 5:
                        st.session_state.page = "SUMMARY"
                    st.rerun()
                else:
                    play_sound("audio/wrong_order.mp3")

# --- เกมที่ 5: จ่ายหลาด (คำนวณ) ---
def game_5():
    st.header("💰 เกมจ่ายหลาดกับนายเท่ง")
    if 'g5_setup' not in st.session_state:
        play_sound("audio/rule_game5.mp3")
        st.session_state.g5_setup = True
    st.markdown("<div class='question-box'>ตางค์ 100 บาท ซื้อของ 95 บาท เหลือทอนกี่บาท?</div>", unsafe_allow_html=True)
    cols = st.columns(2)
    if cols[0].button("15 บาท"): play_sound("audio/try_again.mp3")
    if cols[1].button("5 บาท"):
        play_sound("audio/correct.mp3")
        st.session_state.page = "SUMMARY"
        st.rerun()

# ==========================================
# 3. ระบบควบคุมหน้าจอ (Navigation)
# ==========================================

if 'page' not in st.session_state:
    st.session_state.page = "LANDING"

# --- หน้าแรกสุด (Pre-Landing) ---
if st.session_state.page == "LANDING":
    st.image("images/landing_teng.png", width='stretch')
    if 'landing_played' not in st.session_state:
        play_sound("audio/landing_welcome.mp3")
        st.session_state.landing_played = True
    if st.button("🟢 เข้าสู่ระบบอัตโนมัติ", type="primary"):
        play_sound("audio/let_go.mp3")
        st.session_state.page = "HOME"
        st.rerun()

# --- หน้า HOME ---
elif st.session_state.page == "HOME":
    st.image("images/splash_logo.png", width=300)
    st.title("สมองใส ใจเบิกบานกับนายเท่ง")
    if not st.session_state.get('welcomed', False):
        play_sound("audio/welcome_teng.mp3")
        st.session_state.welcomed = True
    
    if st.button("🟢 เริ่มเล่นเกม"):
        play_sound("audio/let_go.mp3")
        st.session_state.page = "GAME_SELECT"
        st.rerun()
    if st.button("🟡 ดูคะแนนของฉัน"):
        play_sound("audio/score_check.mp3")
        st.session_state.page = "SCORE"
        st.rerun()
    if st.button("🔴 ติดต่อพยาบาล"):
        play_sound("audio/contact_nurse.mp3")
        st.session_state.page = "CONTACT"
        st.rerun()

# --- หน้าเลือกเกม ---
elif st.session_state.page == "GAME_SELECT":
    st.image("images/menu_background.png", width='stretch')
    st.header("เลือกด่านที่ต้องการฝึกนะเติ้ล")
    games = [("1. ไปหลาด", "G1"), ("2. ตาไว", "G2"), ("3. หาเงา", "G3"), ("4. เข้าครัว", "G4"), ("5. จ่ายหลาด", "G5")]
    for name, p in games:
        if st.button(name):
            play_sound("audio/let_go.mp3")
            st.session_state.page = p
            st.rerun()
    if st.button("⬅️ กลับหน้าหลัก"):
        st.session_state.page = "HOME"
        st.rerun()

# --- หน้าสรุปผล ---
elif st.session_state.page == "SUMMARY":
    st.image("images/award_leamsak.png", width='stretch')
    st.balloons()
    play_sound("audio/congratulations.mp3")
    if st.button("🔄 เล่นอีกครั้ง"):
        for key in list(st.session_state.keys()):
            if key != 'page': del st.session_state[key]
        st.session_state.page = "GAME_SELECT"
        st.rerun()
    if st.button("🏠 กลับหน้าหลัก"):
        for key in list(st.session_state.keys()):
            if key != 'page': del st.session_state[key]
        st.session_state.page = "HOME"
        st.rerun()

# --- ฟีเจอร์เสริม ---
elif st.session_state.page == "SCORE":
    st.header("คะแนนสะสม")
    st.info("วันนี้คุณทำได้ยอดเยี่ยมมาก!")
    if st.button("⬅️ กลับ"): st.session_state.page = "HOME"; st.rerun()

elif st.session_state.page == "CONTACT":
    st.header("ติดต่อพยาบาลประจำคลินิก")
    st.image("images/nurse_pic.png", width=300) 
    st.error("📞 เบอร์โทรติดต่อ: 089-736-6039")
    if st.button("⬅️ กลับ"): st.session_state.page = "HOME"; st.rerun()

# --- เรียกฟังก์ชันเกม ---
elif st.session_state.page == "G1": game_1()
elif st.session_state.page == "G2": game_2()
elif st.session_state.page == "G3": game_3()
elif st.session_state.page == "G4": game_4()
elif st.session_state.page == "G5": game_5()