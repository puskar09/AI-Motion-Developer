user_prompt = f"""
Evaluate the following resume against the job description.

Resume:
{resume}

Job Description:
{jd}

STRICT RULES:
- Output MUST be valid JSON
- Do NOT include any extra text
- Do NOT explain anything
- Only return JSON

FORMAT:

{{
  "score": number,
  "strengths": ["point", "point"],
  "weaknesses": ["point", "point"],
  "improvements": ["point", "point"]
}}
"""


print(response.text)
