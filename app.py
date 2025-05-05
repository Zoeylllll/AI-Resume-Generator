import streamlit as st
from core.generator import polish_resume_text
from core.translator import translate_text
from core.exporter import export_to_pdf
from config.lang_texts import LANG_TEXTS

st.set_page_config(page_title="AI Resume Generator", page_icon="🧠")

# 设置界面语言
language = st.selectbox("🌐 Select UI Language / 선택할 언어:", ["中文", "English", "한국어"])
lang_map = {"中文": "zh", "English": "en", "한국어": "ko"}
lang_code = lang_map[language]
texts = LANG_TEXTS[lang_code]

st.title(texts["title"])

# 简历内容输入
text_input = st.text_area(texts["input_placeholder"], height=300)

# 简历风格选择（模板切换）
template = st.selectbox(texts["select_template"], ["技术风格", "商务风格", "学术风格"])
template_map = {
    "技术风格": "tech",
    "商务风格": "business",
    "学术风格": "academic"
}
template_code = template_map[template]

# 目标语言选择
target_language = st.selectbox(texts["select_language"], ["英文", "中文", "韩文"])
target_lang_map = {"英文": "en", "中文": "zh", "韩文": "ko"}
target_lang = target_lang_map[target_language]

# 智能润色按钮
if st.button(texts["polish_button"]):
    if text_input.strip():
        with st.spinner(texts["spinner_polish"]):
            result = polish_resume_text(text_input, target_lang, template_code)
            st.success("✅ Done!")
            st.text_area("🎯 润色结果：", result, height=300)

# 翻译按钮
if st.button(texts["translate_button"]):
    if text_input.strip():
        with st.spinner(texts["spinner_translate"]):
            result = translate_text(text_input, target_lang)
            st.success("✅ Done!")
            st.text_area("🎯 翻译结果：", result, height=300)

# 导出 PDF 按钮
if st.button(texts["export_button"]):
    if text_input.strip():
        with st.spinner(texts["spinner_export"]):
            pdf_filename = export_to_pdf(text_input, template_code)
            st.success(texts["export_success"])
            with open(pdf_filename, "rb") as f:
                st.download_button(
                    label=texts["download_label"],
                    data=f,
                    file_name=pdf_filename,
                    mime="application/pdf"
                )

if st.button("📝 导出为 Word (.docx)"):
    if text_input.strip():
        with st.spinner("正在生成 Word 文件..."):
            word_filename = export_to_docx(text_input)
            st.success("✅ Word 文件已生成！")
            with open(word_filename, "rb") as f:
                st.download_button(
                    label="⬇️ 下载 Word 简历",
                    data=f,
                    file_name=word_filename,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
