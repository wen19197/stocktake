import streamlit as st
import re
from collections import Counter

# 页面配置
st.set_page_config(page_title="库存 AI 计算器", layout="centered")

# 标题
st.title("📊 库存 AI 计算器")
st.markdown("""
请按格式粘贴或输入多行库存数据，每行「产品 code + 数量」。  
示例：
0304278 2
6030033 2
0304278 5
""")

# 数据输入区
text = st.text_area(
    "📋 库存列表",
    height=200,
    placeholder="例如：\n0304278 2\n6030033 2\n0304278 5"
)

# 点击按钮后处理
if st.button("开始统计"):
    # 提取所有 7 位 code + 数量
    matches = re.findall(r"(\d{7})\s*(\d+)", text)
    if not matches:
        st.warning("❗ 未检测到符合格式的 code+数量，请检查输入。")
    else:
        # 汇总
        counter = Counter()
        for code, qty in matches:
            counter[code] += int(qty)
        # 构建结果列表并展示
        result = [{"产品 code": k, "总数量": v} for k, v in sorted(counter.items())]
        st.success("✅ 统计完成！")
        st.table(result)
