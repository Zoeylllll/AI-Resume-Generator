import streamlit as st
import json
from core.generator import polish_resume_text
from core.translator import translate_text
from core.exporter import export_to_pdf, export_to_docx
from core.history import save_resume_history
from core.email_sender import send_email
from config.lang_texts import LANG_TEXTS

st.set_page_config(page_title="AI Resume Generator", page_icon="🧠")

# 设置 UI 语言
language = st.selectbox("🌐 Select UI Language / 선택할 언어:", ["中文", "English", "한국어"])
lang_map = {"中文": "zh", "English": "en", "한국어": "ko"}
lang_code = lang_map[language]
texts = LANG_TEXTS[lang_code]

st.title(texts["title"])

# 简历原文输入
text_input = st.text_area(texts["input_placeholder"], height=300)

# 简历风格选择
template = st.selectbox(texts["select_template"], ["技术风格", "商务风格", "学术风格"])
template_map = {
    "技术风格": "tech",
    "商务风格": "business",
    "学术风格": "academic"
}
template_code = template_map[template]

# 风格预览图
template_images = {
    "tech": "static/template_tech.png",
    "business": "static/template_business.png",
    "academic": "static/template_academic.png"
}
st.image(template_images[template_code], caption=f"{template} 风格预览", use_column_width=True)

# 目标语言
target_language = st.selectbox(texts["select_language"], ["英文", "中文", "韩文"])
target_lang_map = {"英文": "en", "中文": "zh", "韩文": "ko"}
target_lang = target_lang_map[target_language]

# 一键澄滞
if st.button(texts["polish_button"]):
    if text_input.strip():
        save_resume_history(text_input, target_lang, template_code)
        with st.spinner(texts["spinner_polish"]):
            result = polish_resume_text(text_input, target_lang, template_code)
            st.success("✅ Done!")
            st.text_area("🌟 澄滞结果：", result, height=300)

# 一键翻译
if st.button(texts["translate_button"]):
    if text_input.strip():
        save_resume_history(text_input, target_lang, template_code)
        with st.spinner(texts["spinner_translate"]):
            result = translate_text(text_input, target_lang)
            st.success("✅ Done!")
            st.text_area("🌟 翻译结果：", result, height=300)

# 导出 PDF
if st.button(texts["export_button"]):
    if text_input.strip():
        save_resume_history(text_input, target_lang, template_code)
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

# 导出 Word
if st.button("🖍️ 导出为 Word (.docx)"):
    if text_input.strip():
        save_resume_history(text_input, target_lang, template_code)
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

# 历史记录查看
if st.checkbox("📜 查看历史记录"):
    try:
        with open("resume_history.json", "r", encoding="utf-8") as f:
            records = json.load(f)
            for r in records[-5:][::-1]:
                st.markdown(f"**{r['timestamp']} | 模板：{r['template']} | 语言：{r['lang']}**")
                st.code(r["content"])
    except:
        st.warning("暂无记录或文件未创建")

# 邮件发送
with st.expander("📩 发送简历到邮箱"):
    email_input = st.text_input("输入接收邮箱地址")
    if st.button("📤 一键发送 PDF 简历"):
        if email_input and text_input:
            pdf_filename = export_to_pdf(text_input, template_code)
            send_email(email_input, pdf_filename)
            st.success("✅ 邮件已发送成功！")
        else:
            st.warning("请先填写邮箱或输入简历内容。")
