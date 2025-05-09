import streamlit as st
import re
from collections import Counter

# 页面配置
st.set_page_config(page_title="库存 AI 计算器", layout="centered")

# 初始化累计计数器与历史记录栈
if 'counter' not in st.session_state:
    st.session_state.counter = Counter()
if 'history' not in st.session_state:
    # history 存储每次操作前的 counter 副本
    st.session_state.history = []
if 'input_text' not in st.session_state:
    st.session_state.input_text = ""
if 'search_code' not in st.session_state:
    st.session_state.search_code = ""

st.title("📊 累计库存 AI 计算器（支持撤回与搜索）")
st.markdown("""
- 支持输入 7 位或 8 位 code  
- 每次“添加”或“清空”操作前会自动记录历史，方便撤回  
- 可随时查询某个 code 的当前累计数量  
""")

# 回调：添加数据到累计
def add_to_total():
    text = st.session_state.input_text
    matches = re.findall(r"(\d{7,8})\s*(\d+)", text)
    if not matches:
        st.warning("❗ 未检测到符合格式的 code+数量，请检查输入。")
        return
    # 记录当前状态到历史
    st.session_state.history.append(st.session_state.counter.copy())
    # 累加
    for code, qty in matches:
        st.session_state.counter[code] += int(qty)
    st.session_state.input_text = ""
    st.success("✅ 本轮数据已累计")

# 回调：清空所有累计
def clear_all():
    if st.session_state.counter:
        st.session_state.history.append(st.session_state.counter.copy())
    st.session_state.counter = Counter()
    st.success("🗑️ 已清空所有累计数据")

# 回调：撤回上一步
def undo():
    if st.session_state.history:
        # 弹出上一个状态并恢复
        prev = st.session_state.history.pop()
        st.session_state.counter = prev
        st.success("⏪ 已撤回上一步操作")
    else:
        st.warning("⚠️ 无可撤回的操作")

# 文本输入框：本轮数据
st.text_area(
    "📋 输入本轮库存列表",
    key="input_text",
    height=150,
    placeholder="例如：\n0304278 2\n6030033 2\n03042781 1"
)

# 操作按钮区
col1, col2, col3 = st.columns([1,1,1])
with col1:
    st.button("✅ 添加到总数", on_click=add_to_total)
with col2:
    st.button("🗑️ 清空所有数据", on_click=clear_all)
with col3:
    st.button("⏪ 撤回上一步", on_click=undo)

st.markdown("---")

# 搜索功能
st.text_input(
    "🔍 查询某个 code 的数量",
    key="search_code",
    placeholder="在此输入 7 或 8 位 code"
)
if st.session_state.search_code:
    code = st.session_state.search_code.strip()
    qty = st.session_state.counter.get(code, 0)
    st.info(f"🔎 Code **{code}** 的当前累计数量：**{qty}**")

# 展示当前累计库存
if st.session_state.counter:
    st.subheader("📈 当前累计库存总览")
    result = [{"产品 code": k, "总数量": v} for k, v in sorted(st.session_state.counter.items())]
    st.table(result)
