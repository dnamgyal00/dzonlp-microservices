import base64

# Example log entry with base64-encoded Dzongkha text
log_entry = {
    "port": "1213/translate",
    "ip": "127.0.0.1",
    "service": "GET-dz_to_en",
    "params": {
        "text": "4L2m4L6Q4L204LyL4L2C4L2f4L204L2C4L2m4LyL4L2W4L2f4L2E4LyL4L2B4L6x4L284L2R4LyL4L2C4LyL4L2R4L264LyL4L2m4L6m4L264LyL4L2h4L284L2RPw=="
    }
}

# Extract the base64-encoded Dzongkha text from the log entry
encoded_text = log_entry["params"]["text"]

# Decode the base64-encoded text back to its original form
decoded_text = base64.b64decode(encoded_text).decode('utf-8')

print(decoded_text)
