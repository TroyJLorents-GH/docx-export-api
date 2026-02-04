# DOCX Export API for GPT Actions

A simple API that generates ATS-friendly DOCX documents from resume/cover letter content.

## Quick Start

### 1. Deploy to Render.com (Free)

**Option A: One-Click Deploy**
1. Push this folder to a GitHub repo
2. Go to [render.com](https://render.com) → New → Web Service
3. Connect your GitHub repo
4. Render auto-detects settings from `render.yaml`
5. Click "Create Web Service"
6. Your URL will be: `https://your-app-name.onrender.com`

**Option B: Manual Setup**
1. Go to [render.com](https://render.com) → New → Web Service
2. Connect repo or use "Deploy from Git URL"
3. Settings:
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

> ⚠️ **Free Tier Note**: Render free tier sleeps after 15 min of inactivity. First request after sleep takes ~30-50 seconds. Consider upgrading to $7/mo for always-on.

### 2. Other Free Hosting Options

| Platform | Pros | Cons |
|----------|------|------|
| **Render.com** | Easy, auto-deploy | Sleeps on free tier |
| **Railway.app** | $5 free credits/mo | Limited hours |
| **Fly.io** | Fast, generous free tier | Slightly more setup |
| **Vercel** | Great for serverless | Need to adapt code |
| **Replit** | Easy testing | Can be slow |

### 3. Configure Your GPT

1. Go to [ChatGPT](https://chat.openai.com) → Explore GPTs → Create
2. In the **Configure** tab, scroll to **Actions**
3. Click **Create new action**
4. Paste the contents of `openapi-schema-for-gpt.yaml`
5. **Replace** `YOUR-APP-NAME.onrender.com` with your actual URL
6. Set Authentication to **None** (or add API key if you want)
7. Save

### 4. GPT Instructions Example

Add this to your GPT's instructions:

```
When the user wants to export their resume or cover letter to a Word document:

1. Gather the content and organize it into sections
2. Call the exportDocx action with:
   - doc_type: "resume" or "cover_letter"
   - title: The person's name
   - subtitle: Contact info on one line
   - sections: Array of {heading, content} objects
   - file_name: A descriptive filename

3. When you receive the base64 response, tell the user:
   "I've generated your document. Unfortunately, I can't provide a direct download link, but I can give you the file content. Would you like me to show you how to convert it, or would you prefer I display the content in a formatted way you can copy?"

Note: Currently GPT Actions cannot directly provide file downloads. The base64 can be used with a file converter or decoded locally.
```

## API Usage

### Endpoint: POST /export/docx

**Request:**
```json
{
  "doc_type": "resume",
  "file_name": "john_doe_resume",
  "title": "John Doe",
  "subtitle": "john@email.com | (555) 123-4567 | San Francisco, CA",
  "sections": [
    {
      "heading": "Summary",
      "content": "Experienced software engineer with 5+ years building scalable web applications."
    },
    {
      "heading": "Experience",
      "content": "**Senior Software Engineer** at TechCorp (2021-Present)\n- Led development of microservices architecture\n- Reduced API latency by 40%\n- Mentored 3 junior developers\n\n**Software Engineer** at StartupXYZ (2019-2021)\n- Built React frontend from scratch\n- Implemented CI/CD pipeline"
    },
    {
      "heading": "Education",
      "content": "**B.S. Computer Science**, State University (2019)\n- GPA: 3.8/4.0\n- Dean's List"
    },
    {
      "heading": "Skills",
      "content": "Python, JavaScript, React, Node.js, AWS, Docker, PostgreSQL, MongoDB"
    }
  ],
  "return_format": "base64"
}
```

**Response:**
```json
{
  "file_name": "john_doe_resume.docx",
  "file_base64": "UEsDBBQAAAAIAO1YX1...",
  "mime_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  "message": "Document generated successfully."
}
```

### Markdown Support

The API supports simple markdown in content:
- `**bold text**` → **bold**
- `*italic text*` → *italic*
- `- bullet point` → bullet lists
- `## Heading` → section heading (when using content field)

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn main:app --reload

# Test at http://localhost:8000
# API docs at http://localhost:8000/docs
```

## Limitations

1. **PDF Export**: Not implemented in v1 due to LibreOffice dependency. Users can convert DOCX→PDF in Word/Google Docs.

2. **GPT Download Links**: GPT Actions can't directly create download links. The base64 response needs to be decoded by the user or processed through additional tooling.

3. **Formatting**: Keeps formatting simple for ATS compatibility. Complex layouts may not render perfectly.

## Future Improvements

- [ ] PDF export via cloud service
- [ ] Template selection
- [ ] Custom fonts/styling
- [ ] File URL with short-lived download links (requires storage)
