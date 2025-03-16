# ScreenshotOCR
![alt text](OCRapp/src/icon.ico)<br>
ScreenshotOCR is a Python project that extracts text from images captured from the clipboard and processes them using ChatGPT API. It supports both regular and translated text extraction.

**Openai API key is required**

## Features

- Capture images directly from the clipboard.
- Auto-translate functionality using prompts defined in `prompt.json`.

## Setup and Usage

1. Create conda environment and install required dependencies:
   ```
   conda create -n sOCR python==3.9
   ```
   ```
   conda activate sOCR
   ```
   ```
   pip install -r requirements.txt
   ```
2. Configure your API key and other settings using the UI.
3. Use Windows snipping tool (win+shift+s) to clip an image.
4. Use the defined hotkey (ctrl+alt+x) to trigger OCR process
5. The extracted (and optionally translated) text will be copied to the clipboard.

## Customization

- Modify `prompt.json` to adjust the prompts for translation and output.

