from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from flask import Flask, jsonify, request
from flask_cors import CORS


# 환경변수 로드
load_dotenv(verbose=True)

# 모델과 프롬프트 설정
model = ChatOpenAI(model='gpt-4')
system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template), ("user", "{text}")]
)
parser = StrOutputParser()

# Flask 애플리케이션 생성 및 CORS 설정
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

### 루트 엔드포인트
@app.route('/')
def index():
    return "번역 API 입니다."

### 번역 요청을 처리하는 엔드포인트
@app.route('/translate', methods=["GET", "POST"])
def translate():
    # 요청된 데이터를 JSON 형태로 받음
    data = request.json

    # JSON에서 language와 text를 추출
    language = data['language']
    text = data['text']

    # 입력이 잘못되었을 경우 에러 처리
    if not language or not text:
        return jsonify({"error": "language와 text는 필수 입력입니다."}), 400
    
    # 생성형 AI 모델을 통해 번역 수행
    chain = prompt_template | model | parser
    result = chain.invoke({"language": language, "text": text})

    # 결과를 JSON 형태로 반환
    data = {"requested": "request"}
    data['language'] = language
    data['text'] = text
    data['result'] = result

    return jsonify(data)

if __name__ == "__main__":
    app.run()