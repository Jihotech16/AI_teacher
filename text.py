from openai import OpenAI
import os


# 환경 변수에서 OpenAI API 키를 불러옵니다.
client = OpenAI(api_key="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"],)
if not client:
    raise ValueError("OPENAI_API_KEY not recognized")

def generate_text(prompt):
    try:
        # GPT-3 모델을 사용하여 텍스트를 생성합니다.
        response = openai.Completion.create(
          model="text-davinci-003",  # 사용할 모델을 지정합니다.
          prompt=prompt,  # 사용자의 프롬프트
          max_tokens=50,  # 생성할 최대 토큰 수
          n=1,  # 생성할 완료 항목의 수
          stop=None,  # 텍스트 생성을 중단할 토큰
          temperature=0.5  # 생성의 창의성을 결정하는 파라미터
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return str(e)

# 사용자의 프롬프트
prompt = "What is the capital of France?"

# 생성된 텍스트를 출력합니다.
print(generate_text(prompt))
