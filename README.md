# jarvis

## Configuration

Set `GROQ_API_KEY` to your Groq API key before starting the assistant. Set
`JARVIS_WHATSAPP_NUMBER` to the phone number (including country code) that the
WhatsApp command should message. Keep these values in your environment; do not
commit credentials.

On Windows PowerShell, set them for the current terminal session with:

```powershell
$env:GROQ_API_KEY = "your-groq-api-key"
$env:JARVIS_WHATSAPP_NUMBER = "+<country-code><number>"
```

The WhatsApp message command is disabled until `JARVIS_WHATSAPP_NUMBER` is set.
Personal notes, the PyWhatKit message history, screenshots, and generated audio
are kept local and are excluded from Git.