import streamlit as st
import re
from collections import Counter

# 页面配置
st.set_page_config(page_title="库存 AI 计算器", layout="centered")

# 初始化累计计数器
if 'counter' not in st.session_state:
    st.session_state.counter = Counter()
# 默认输入文本也要在 session_state 里初始化
if 'input_text' not in st.session_state:
    st.session_state.input_text = ""

st.title("📊 累计库存 AI 计算器")

st.markdown("""
请按格式粘贴或输入多行库存数据，每行「产品 code + 数量」。  
示例：  
0304278 2
6030033 2
0304278 5
""")

# 回调：添加数据到累计
def add_to_total():
    text = st.session_state.input_text
    matches = re.findall(r"(\d{7})\s*(\d+)", text)
    if not matches:
        st.warning("❗ 未检测到符合格式的 code+数量，请检查输入。")
        return
    for code, qty in matches:
        st.session_state.counter[code] += int(qty)
    # 清空输入（在回调里安全）
    st.session_state.input_text = ""
    st.success("已将本轮数据累计！")

# 回调：清空所有累计
def clear_all():
    st.session_state.counter = Counter()
    st.success("所有累计数据已清空！")

# 文本输入框，绑定到 session_state.input_text
st.text_area(
    "📋 输入本轮库存列表",
    key="input_text",
    height=200,
    placeholder="例如：\n0304278 2\n6030033 2\n0304278 5"
)

# 两个按钮，各自使用 on_click 指定回调
col1, col2 = st.columns(2)
with col1:
    st.button("✅ 添加到总数", on_click=add_to_total)
with col2:
    st.button("🗑️ 清空所有数据", on_click=clear_all)

# 展示当前累计库存
if st.session_state.counter:
    st.subheader("📈 当前累计库存")
    result = [{"产品 code": k, "总数量": v} for k, v in sorted(st.session_state.counter.items())]
    st.table(result)
