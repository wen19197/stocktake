import streamlit as st
import re
from collections import Counter

# 页面配置
st.set_page_config(page_title="库存 AI 计算器", layout="centered")

# 初始化累计计数器
if 'counter' not in st.session_state:
    st.session_state.counter = Counter()

st.title("📊 累计库存 AI 计算器")
st.markdown("""
请按格式粘贴或输入多行库存数据，每行「产品 code + 数量」。  
示例：
0304278 2
6030033 2
0304278 5
""")

# 输入区域，使用 session_state 保存
text = st.text_area(
    "📋 输入本轮库存列表",
    height=200,
    placeholder="例如：\n0304278 2\n6030033 2\n0304278 5",
    key="input_text"
)

# 操作按钮
col1, col2 = st.columns(2)
with col1:
    if st.button("✅ 添加到总数"):
        matches = re.findall(r"(\d{7})\s*(\d+)", st.session_state.input_text)
        if not matches:
            st.warning("❗ 未检测到符合格式的 code+数量，请检查输入。")
        else:
            for code, qty in matches:
                st.session_state.counter[code] += int(qty)
            st.success("已将本轮数据累计！")
            # 清空输入框
            st.session_state.input_text = ""
with col2:
    if st.button("🗑️ 清空所有数据"):
        st.session_state.counter = Counter()
        st.success("所有累计数据已清空！")

# 展示累计结果
if st.session_state.counter:
    st.subheader("📈 当前累计库存")
    result = [{"产品 code": k, "总数量": v} for k, v in sorted(st.session_state.counter.items())]
    st.table(result)
