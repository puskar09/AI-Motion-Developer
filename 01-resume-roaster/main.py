# ===== IMPORTS =====
import json
from openai import OpenAI

# ===== GEMINI CLIENT =====
client = None

# ===== MODE SELECTION =====
mode = input("Choose mode (hr / brutal / ats): ").lower()

# ===== SYSTEM PROMPT =====
if mode == "hr":
    system_prompt = """
    You are a professional HR reviewer.
    Focus on clarity, communication, and presentation.
    Be constructive and balanced.
    """

elif mode == "brutal":
    system_prompt = """
    You are a brutally honest startup founder.
    Give harsh, direct feedback.
    No sugarcoating.
    """

elif mode == "ats":
    system_prompt = """
    You are an ATS system.
    Focus on keyword matching and technical relevance.
    Be analytical and precise.
    """

else:
    print("Invalid mode selected")
    exit()

# ===== FILE READING FUNCTION =====
def read_file(path):
    with open(path, "r") as f:
        return f.read()

# ===== LOAD INPUT =====
resume1 = read_file("resume1.txt")
resume2 = read_file("resume2.txt")

jd = read_file("jd.txt")

# ===== INPUT VALIDATION =====
if not resume1.strip():
    print("Resume is empty.")
    exit()
if not resume2.strip():
    print("Resume 2 is empty.")
    exit()
    
if not jd.strip():
    print("Job description is empty.")
    exit()

# ===== USER PROMPT =====
user_prompt = f"""
Compare the following two resumes based on the job description.

Resume 1:
{resume1}

Resume 2:
{resume2}

Job Description:
{jd}

STRICT RULES:
- Output MUST be valid JSON
- No extra text

FORMAT:

{{
  "better_candidate": "resume1 or resume2",
  "reason": "short explanation",
  "resume1_score": number,
  "resume2_score": number
}}
"""

# ===== COMBINE PROMPTS =====
full_prompt = system_prompt + "\n\n" + user_prompt

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
)

raw_output = response.choices[0].message.content
# ===== CLEAN FUNCTION =====
def clean_json_response(text):
    text = text.strip()

    if text.startswith("```"):
        text = text.split("```")[1]

    return text

# ===== AI CALL =====
"""response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=full_prompt
)

raw_output = response.text"""

# ===== CLEAN + PARSE =====
cleaned = clean_json_response(raw_output)

try:
    data = json.loads(cleaned)
except json.JSONDecodeError:
    print("\n⚠️ Failed to parse JSON. Raw output:\n")
    print(raw_output)
    exit()

# ===== PRINT OUTPUT =====
print("\n=== STRUCTURED OUTPUT ===\n")

print("\n=== COMPARISON RESULT ===\n")

print("Better Candidate:", data["better_candidate"])
print("Reason:", data["reason"])

print("\nResume 1 Score:", data["resume1_score"])
print("Resume 2 Score:", data["resume2_score"])

# ===== SAVE OUTPUT =====
with open("output.json", "w") as f:
    json.dump(data, f, indent=4)

print("\nSaved to output.json")
