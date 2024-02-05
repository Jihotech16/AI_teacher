import streamlit as st
import requests
from PyPDF2 import PdfReader
import openai

# 환경 변수에서 OPENAI_API_KEY를 읽어옵니다.
openai_api_key = st.secrets["api_key"]

def download_file(url, filename=''):
    """주어진 URL에서 파일을 다운로드하고 저장합니다."""
    if filename == '':
        filename = url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return filename

def extract_text_from_pdf(filename):
    """PDF 파일에서 텍스트를 추출합니다."""
    reader = PdfReader(filename)
    raw_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            raw_text += text
    return raw_text

def ask_question_to_model(question, document):
    """문서 내용을 참조하여 질문에 답변합니다."""
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{document}"},
            {"role": "user", "content": f"Question: {question}"},
        ],
    )
    return response.choices[0].message['content']

# Streamlit 앱 구성
st.title('PDF 기반 AI 챗봇')

pdf_url = "https://github.com/Jihotech16/t.e._AI_teacher/raw/main/%EC%A4%91_%EA%B8%B0%EC%88%A0%EA%B0%80%EC%A0%95%E2%91%A0(%EC%B5%9C%EC%9C%A0%ED%98%84)_%EA%B5%90%EA%B3%BC%EC%84%9C%20%EB%B3%B8%EB%AC%B8(pdf).pdf"
question = st.text_input('질문을 입력하세요:', '')

if st.button('답변 생성'):
    if pdf_url and question:
        # 파일 다운로드
        filename = download_file(pdf_url)
        # PDF에서 텍스트 추출
        document_text = extract_text_from_pdf(filename)
        # 질문에 답변
        answer = ask_question_to_model(question, document_text[:4000])  # GPT의 토큰 제한을 고려하여 텍스트를 자릅니다.
        st.text_area("답변:", value=answer, height=200)
    else:
        st.error('PDF 파일 URL과 질문을 모두 입력해주세요.')

