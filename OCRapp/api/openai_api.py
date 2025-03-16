import openai
import logging

def call_openai_api(config: dict, system_prompt: str, img_base64: str) -> str:
    try:
        logging.info("calling ChatGPT API...")
        response = openai.chat.completions.create(
            model=config["model"],
            max_tokens=300,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": [{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}}]},
            ],
            temperature=0.0,
        )
        extracted_text = response.choices[0].message.content.strip()
        logging.info(extracted_text)
        return extracted_text
    except Exception as e:
        logging.error(f"Error when calling ChatGPT api: {e}")
        return None
