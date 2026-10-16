import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"

print("Loading AI model...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype="auto"
)

print("AI model loaded successfully!")


def understand_request(user_request):
    system_prompt = """
You are an attendance management assistant.

Convert the user's request into exactly one JSON object.

Supported actions:
- mark_attendance
- remove_attendance
- get_attendance
- class_average

For mark_attendance, use:
action, roll_no, date, status.

For remove_attendance, use:
action, roll_no, date.

For get_attendance, use:
action, roll_no.

For class_average, use:
action.

Dates must use YYYY-MM-DD.
Status must be Present or Absent.
Do not invent missing information.
If information is missing or unclear, return:
{"error": "Please provide the missing information"}

Return JSON only.
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_request}
    ]

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt"
    ).to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=150,
            do_sample=False
        )

    new_tokens = outputs[0][inputs["input_ids"].shape[1]:]

    response = tokenizer.decode(
        new_tokens,
        skip_special_tokens=True
    )

    return response.strip()


if __name__ == "__main__":
    request = input("Enter attendance request: ")
    result = understand_request(request)

    print("\nAI JSON output:")
    print(result)

    # Check whether the model returned valid JSON
    try:
        parsed = json.loads(result)
        print("\nValid JSON received!")
        print(json.dumps(parsed, indent=2))
    except json.JSONDecodeError:
        print("\nThe AI output is not valid JSON.")