import sys
import random
import streamlit as st

# Авто-запуск локального сервера Streamlit
if "__streamlit_run_local__" not in sys.argv:
    import subprocess
    print("Запускаем твой онлайн-стол для Дурака...")
    subprocess.Popen([sys.executable, "-m", "streamlit", "run", sys.argv[0], "--", "__streamlit_run_local__"])
    sys.exit()

# Конфигурация страницы — делаем её красивой и адаптивной
st.set_page_config(
    page_title="Durak Online | fonyafay", 
    page_icon="🃏", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- УЛЬТРА СТИЛЬНЫЙ ИНТЕРФЕЙС (CSS) ---
st.markdown("""
    <style>Ё
        /* Общий темный фон */
        .stApp {
            background-color: #0b0f19;
            color: #f3f4f6;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        /* Заголовок в стиле неонового киберпанка */
        .neon-title {
            text-align: center;
            font-size: 50px;
            font-weight: 900;
            color: #fff;
            text-shadow: 0 0 10px #10b981, 0 0 20px #10b981, 0 0 40px #10b981;
            margin-bottom: 5px;
            letter-spacing: 2px;
        }
        
        .subtitle {
            text-align: center;
            color: #9ca3af;
            font-size: 16px;
            margin-bottom: 30px;
        }

        /* Настоящий суконный игровой стол */
        .poker-table {
            background: radial-gradient(circle, #0f5132 0%, #082d1c 100%);
            border: 10px solid #1f1f1f;
            border-radius: 30px;
            padding: 30px;
            box-shadow: inset 0 0 50px rgba(0,0,0,0.8), 0 10px 30px rgba(0,0,0,0.7);
            margin-bottom: 25px;
            position: relative;
        }

        /* Оформление карт */
        .card-container {
            display: inline-block;
            background: linear-gradient(145deg, #ffffff, #e5e7eb);
            color: #111827;
            border-radius: 12px;
            width: 85px;
            height: 125px;
            margin: 8px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.4);
            border: 2px solid #374151;
            transition: transform 0.2s, box-shadow 0.2s;
            position: relative;
        }
        
        .card-container:hover {
            transform: translateY(-10px);
            box-shadow: 0 0 15px #10b981;
            border-color: #10b981;
            cursor: pointer;
        }

        /* Красные масти */
        .red-suit {
            color: #ef4444 !important;
        }
        
        /* Черные масти */
        .black-suit {
            color: #1f2937 !important;
        }

        /* Кнопки управления */
        .stButton>button {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 30px !important;
            padding: 12px 35px !important;
            font-size: 16px !important;
            font-weight: bold !important;
            box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4) !important;
            transition: all 0.3s !important;
        }
        
        .stButton>button:hover {
            transform: scale(1.05) !important;
            box-shadow: 0 0 25px rgba(16, 185, 129, 0.8) !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- ЛОГИКА ОНЛАЙН СИНХРОНИЗАЦИИ ---
if "room_id" not in st.session_state:
    st.session_state.room_id = ""
if "player_name" not in st.session_state:
    st.session_state.player_name = ""
if "opponent_name" not in st.session_state:
    st.session_state.opponent_name = ""
if "game_started" not in st.session_state:
    st.session_state.game_started = False

# Экран входа / лобби
if not st.session_state.game_started:
    st.markdown("<div class='neon-title'>DURAK ONLINE</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Премиальный карточный клуб fonyafay</div>", unsafe_allow_html=True)
    
    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("### 🔑 Создать или войти в комнату")
        name = st.text_input("Твой никнейм:", placeholder="Например, fonya")
        room = st.text_input("ID Комнаты (любые цифры):", placeholder="Например, 777")
        role = st.selectbox("Кто ты?", ["Игрок 1 (Хозяин)", "Игрок 2 (Гость)"])
        
        if st.button("🚀 Начать игру"):
            if name and room:
                st.session_state.player_name = name
                st.session_state.room_id = room
                st.session_state.role = role
                st.session_state.game_started = True
                st.rerun()
            else:
                st.error("Пожалуйста, введи ник и номер комнаты!")
                
    with col_r:
        st.markdown("### 📜 Правила и Особенности")
        st.info("""
        🤖 **Как играть с другом?**
        1. Запусти этот сайт.
        2. Введи свой ник и ID комнаты (например, 123). Выбери роль "Игрок 1".
        3. Твой друг должен сделать то же самое на своем ПК, выбрав тот же ID комнаты и роль "Игрок 2".
        4. крч заепал давай бысрее
        """)
    st.stop()

# --- САМА ИГРА ---
RANKS = ["6", "7", "8", "9", "10", "J", "Q", "K", "A"]
SUITS = ["♠", "♥", "♦", "♣"]
RANK_VALUES = {rank: i for i, rank in enumerate(RANKS)}

# Генерация колоды
if "online_deck" not in st.session_state:
    deck = [f"{r}{s}" for r in RANKS for s in SUITS]
    random.shuffle(deck)
    st.session_state.online_deck = deck
    st.session_state.online_trump = random.choice(SUITS)
    st.session_state.p1_hand = [st.session_state.online_deck.pop() for _ in range(6)]
    st.session_state.p2_hand = [st.session_state.online_deck.pop() for _ in range(6)]
    st.session_state.table = []  # Пары на столе
    st.session_state.turn = "p1"  # Чей ход

# Назначаем руки согласно роли
if st.session_state.role == "Игрок 1 (Хозяин)":
    my_hand = st.session_state.p1_hand
    opp_hand = st.session_state.p2_hand
    my_id = "p1"
    opp_id = "p2"
    my_name = st.session_state.player_name
    opp_name = "Друг (Игрок 2)"
else:
    my_hand = st.session_state.p2_hand
    opp_hand = st.session_state.p1_hand
    my_id = "p2"
    opp_id = "p1"
    my_name = st.session_state.player_name
    opp_name = "Хозяин (Игрок 1)"

# Шапка игры
st.markdown(f"<div class='neon-title' style='font-size: 30px;'>КОМНАТА: {st.session_state.room_id}</div>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #10b981;'>Вы вошли как: <b>{my_name}</b></p>", unsafe_allow_html=True)

# Красивая отрисовка карт через HTML
def render_card_html(card):
    rank = card[:-1]
    suit = card[-1]
    suit_class = "red-suit" if suit in ["♥", "♦"] else "black-suit"
    
    return f"""
    <div class="card-container">
        <div style="position: absolute; top: 10px; left: 10px; font-size: 20px; font-weight: bold;" class="{suit_class}">{rank}</div>
        <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 40px;" class="{suit_class}">{suit}</div>
        <div style="position: absolute; bottom: 10px; right: 10px; font-size: 20px; font-weight: bold; transform: rotate(180deg);" class="{suit_class}">{rank}</div>
    </div>
    """

def parse_card(card_str):
    for r in RANKS:
        if card_str.startswith(r):
            suit = card_str.replace(r, "")
            return r, suit
    return None, None

def can_beat(card_a, card_b, trump_suit):
    r_a, s_a = parse_card(card_a)
    r_b, s_b = parse_card(card_b)
    if s_a == s_b:
        return RANK_VALUES[r_a] > RANK_VALUES[r_b]
    if s_a == trump_suit and s_b != trump_suit:
        return True
    return False

# --- ИГРОВОЙ СТОЛ ---
st.markdown("<div class='poker-table'>", unsafe_allow_html=True)

col_info, col_board = st.columns([1, 3])

with col_info:
    st.markdown("### 📊 Статус")
    st.markdown(f"🃏 **Козырь:** <span style='font-size: 28px; color: #10b981;'>{st.session_state.online_trump}</span>", unsafe_allow_html=True)
    st.write(f"🎴 Карт в колоде: **{len(st.session_state.online_deck)}**")
    st.write(f"👤 Оппонент ({opp_name}): **{len(opp_hand)} карт**")
    
    if st.session_state.turn == my_id:
        st.success("🟢 ТВОЙ ХОД! Ходи!")
    else:
        st.warning("🔴 Ход соперника. Отбивайся!")

with col_board:
    st.markdown("### ⚔️ Стол")
    if not st.session_state.table:
        st.write("На столе пусто. Сделайте ход!")
    else:
        cols_table = st.columns(len(st.session_state.table) + 1)
        for idx, (attack, defend) in enumerate(st.session_state.table):
            with cols_table[idx]:
                st.markdown(render_card_html(attack), unsafe_allow_html=True)
                if defend:
                    st.markdown("<div style='text-align:center; margin: -5px 0; color: #10b981;'>▲ БИТА ▲</div>", unsafe_allow_html=True)
                    st.markdown(render_card_html(defend), unsafe_allow_html=True)
                else:
                    st.markdown("<div style='text-align:center; color: #ef4444; font-weight: bold;'>Ждет защиты...</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# --- КНОПКИ ДЕЙСТВИЙ ---
action_col1, action_col2, _ = st.columns([1, 1, 4])

with action_col1:
    if st.session_state.turn == my_id:
        if st.button("🗑️ Бито (Закончить ход)"):
            if st.session_state.table:
                unbeaten = any(defend is None for _, defend in st.session_state.table)
                if unbeaten:
                    st.error("Соперник еще не все отбил!")
                else:
                    st.session_state.table = []
                    while len(st.session_state.p1_hand) < 6 and st.session_state.online_deck:
                        st.session_state.p1_hand.append(st.session_state.online_deck.pop())
                    while len(st.session_state.p2_hand) < 6 and st.session_state.online_deck:
                        st.session_state.p2_hand.append(st.session_state.online_deck.pop())
                    st.session_state.turn = opp_id
                    st.rerun()
    else:
        if st.button("📥 Забрать карты"):
            for attack, defend in st.session_state.table:
                my_hand.append(attack)
                if defend:
                    my_hand.append(defend)
            st.session_state.table = []
            while len(opp_hand) < 6 and st.session_state.online_deck:
                opp_hand.append(st.session_state.online_deck.pop())
            st.session_state.turn = opp_id
            st.rerun()

# --- КАРТЫ В РУКЕ ИГРОКА ---
st.markdown("### 🖐️ Твои карты (нажми, чтобы сыграть):")
cols_hand = st.columns(max(len(my_hand), 1))

for idx, card in enumerate(my_hand):
    with cols_hand[idx]:
        st.markdown(render_card_html(card), unsafe_allow_html=True)
        if st.button("Сыграть", key=f"play_{idx}"):
            if st.session_state.turn == my_id:
                if not st.session_state.table:
                    st.session_state.table.append((card, None))
                    my_hand.remove(card)
                    st.rerun()
                else:
                    ranks_on_table = []
                    for att, deff in st.session_state.table:
                        ranks_on_table.append(parse_card(att)[0])
                        if deff:
                            ranks_on_table.append(parse_card(deff)[0])
                    if parse_card(card)[0] in ranks_on_table:
                        st.session_state.table.append((card, None))
                        my_hand.remove(card)
                        st.rerun()
                    else:
                        st.error("Этого номинала нет на столе!")
            else:
                unbeaten_idx = None
                for i, (_, defend) in enumerate(st.session_state.table):
                    if defend is None:
                        unbeaten_idx = i
                        break
                if unbeaten_idx is not None:
                    to_beat = st.session_state.table[unbeaten_idx][0]
                    if can_beat(card, to_beat, st.session_state.online_trump):
                        st.session_state.table[unbeaten_idx] = (to_beat, card)
                        my_hand.remove(card)
                        st.rerun()
                    else:
                        st.error("Эта карта не побьет карту соперника!")

# Сброс игры
st.markdown("<br><hr style='border-color: #1f2937;'><br>", unsafe_allow_html=True)
if st.button("🔄 Начать игру заново"):
    st.session_state.clear()
    st.rerun()