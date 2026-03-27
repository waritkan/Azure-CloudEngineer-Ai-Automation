# 🔄 เปลี่ยนเป็นใช้ OpenRouter แล้ว!

## สรุปการเปลี่ยนแปลง

โปรเจคนี้ได้อัพเกรดเป็นใช้ **OpenRouter** แทน OpenAI โดยตรง! 🎉

---

## 🎯 ทำไมเปลี่ยน?

### ข้อดีของ OpenRouter:

| ฟีเจอร์ | OpenAI Direct | OpenRouter |
|---------|---------------|------------|
| **ราคา GPT-4** | $10/1M tokens | $10/1M tokens |
| **ราคา Claude 3.5** | ไม่มี | $3/1M tokens ⭐ |
| **Gemini Pro** | ไม่มี | **ฟรี!** 🎉 |
| **เปลี่ยน Model** | ต้องสมัครหลายที่ | เปลี่ยนได้เลย |
| **API Format** | OpenAI only | OpenAI compatible |
| **Free Models** | ❌ | ✅ มีหลายตัว |

### สรุป:
- ✅ **ประหยัดเงิน** - มี free models และ models ถูกกว่า
- ✅ **เลือกได้หลาย AI** - GPT-4, Claude, Gemini, Llama ผ่าน API เดียว
- ✅ **ง่ายต่อการทดสอบ** - ใช้ Gemini Pro ฟรีได้เลย!
- ✅ **API เหมือนเดิม** - ไม่ต้องเปลี่ยนโค้ดมาก

---

## 📝 ไฟล์ที่เปลี่ยนแปลง

### 1. `backend/app/config.py`
```python
# เพิ่ม
OPENAI_BASE_URL: str = "https://openrouter.ai/api/v1"
APP_URL: str = "..."
APP_TITLE: str = "..."
```

### 2. `backend/app/ai_agent.py`
```python
# เพิ่ม OpenRouter headers
self.client = AsyncOpenAI(
    api_key=settings.OPENAI_API_KEY,
    base_url=settings.OPENAI_BASE_URL,  # ← ใหม่
    default_headers={                    # ← ใหม่
        "HTTP-Referer": settings.APP_URL,
        "X-Title": settings.APP_TITLE,
    }
)
```

### 3. `backend/.env.example`
```bash
# เปลี่ยน comments และ format
OPENAI_API_KEY=sk-or-v1-...  # ← OpenRouter format
OPENAI_BASE_URL=https://openrouter.ai/api/v1
OPENAI_MODEL=openai/gpt-4-turbo  # ← format ใหม่
```

### 4. เอกสารใหม่
- `docs/OPENROUTER_SETUP.md` - คู่มือการใช้งาน OpenRouter
- `OPENROUTER_MIGRATION.md` - ไฟล์นี้

---

## 🚀 วิธีเริ่มใช้งาน

### Step 1: สร้างบัญชี OpenRouter

1. ไปที่ https://openrouter.ai/
2. Sign in ด้วย Google account
3. ยืนยัน email

### Step 2: เติมเงิน (ถ้าต้องการใช้ paid models)

1. ไปที่ https://openrouter.ai/credits
2. เติมขั้นต่ำ $5
3. หรือข้ามไปถ้าจะใช้ free models

### Step 3: สร้าง API Key

1. ไปที่ https://openrouter.ai/keys
2. กด "Create Key"
3. ตั้งชื่อ: `azure-ai-automation`
4. คัดลอก key (รูปแบบ: `sk-or-v1-...`)

### Step 4: แก้ไข .env

```bash
cd backend
notepad .env
```

**วางค่าเหล่านี้**:
```bash
# OpenRouter API Key (จาก Step 3)
OPENAI_API_KEY=sk-or-v1-your-actual-key-here

# Base URL (ห้ามเปลี่ยน!)
OPENAI_BASE_URL=https://openrouter.ai/api/v1

# เลือก Model ที่ต้องการ:
# ฟรี (แนะนำเริ่มต้น):
OPENAI_MODEL=google/gemini-pro

# หรือ Paid (ฉลาดกว่า):
# OPENAI_MODEL=anthropic/claude-3.5-sonnet
# OPENAI_MODEL=openai/gpt-4-turbo

# App Info (optional)
APP_URL=https://github.com/your-username/azure-ai-automation
APP_TITLE=Azure AI Automation
```

### Step 5: ทดสอบ

```bash
# รัน backend
uvicorn app.main:app --reload
```

**ถ้าสำเร็จจะเห็น**:
```
✅ AI Agent initialized with OpenRouter (google/gemini-pro)
```

---

## 🎯 แนะนำ Model

### เริ่มต้น (ฟรี):
```bash
OPENAI_MODEL=google/gemini-pro
```
- **ราคา**: ฟรี!
- **ดี**: ฉลาด, ทดสอบได้เต็มที่
- **เหมาะกับ**: Development, Demo, Testing

### Production (จ่ายตามใช้):

#### Claude 3.5 Sonnet (แนะนำสุด! ⭐)
```bash
OPENAI_MODEL=anthropic/claude-3.5-sonnet
```
- **ราคา**: ~$3/1M tokens (~$0.003/100 requests)
- **ดี**: ฉลาดมาก, function calling แม่น, ถูกกว่า GPT-4
- **เหมาะกับ**: Production, Interview Demo

#### GPT-4 Turbo
```bash
OPENAI_MODEL=openai/gpt-4-turbo
```
- **ราคา**: ~$10/1M tokens (~$0.01/100 requests)
- **ดี**: ฉลาดที่สุด, function calling ดีที่สุด
- **เหมาะกับ**: Production (ถ้างบพอ)

#### GPT-3.5 Turbo (ถูก + เร็ว)
```bash
OPENAI_MODEL=openai/gpt-3.5-turbo
```
- **ราคา**: ~$0.5/1M tokens (~$0.0005/100 requests)
- **ดี**: เร็ว, ถูกมาก
- **เหมาะกับ**: Development, High-volume

---

## 💰 เปรียบเทียบค่าใช้จ่าย

### สมมติใช้ 1,000 requests:

| Model | OpenAI Direct | OpenRouter | ประหยัด |
|-------|---------------|------------|---------|
| GPT-4 Turbo | $10 | $10 | - |
| Claude 3.5 | ไม่มี | **$3** | ใช้ได้เฉพาะที่นี่! |
| GPT-3.5 | $0.50 | $0.50 | - |
| Gemini Pro | ไม่มี | **ฟรี!** | 100% |

**สรุป**: ถ้าใช้ Claude 3.5 แทน GPT-4 → ประหยัด 70%!

---

## 🔄 การเปลี่ยน Model

### วิธีที่ 1: แก้ .env (แนะนำ)

```bash
notepad backend\.env

# เปลี่ยนบรรทัดนี้:
OPENAI_MODEL=google/gemini-pro

# Restart backend
```

### วิธีที่ 2: Environment Variable

```bash
# Windows
set OPENAI_MODEL=anthropic/claude-3.5-sonnet
uvicorn app.main:app --reload

# Linux/Mac
export OPENAI_MODEL=anthropic/claude-3.5-sonnet
uvicorn app.main:app --reload
```

### ทดสอบ Model ต่างๆ:

```bash
# Gemini Pro (ฟรี)
OPENAI_MODEL=google/gemini-pro

# Claude 3.5 (แนะนำ)
OPENAI_MODEL=anthropic/claude-3.5-sonnet

# GPT-4 Turbo
OPENAI_MODEL=openai/gpt-4-turbo

# GPT-3.5 (ถูก)
OPENAI_MODEL=openai/gpt-3.5-turbo
```

---

## 📊 ดู Usage

### OpenRouter Dashboard:

1. ไปที่ https://openrouter.ai/activity
2. เห็น:
   - จำนวน requests
   - Tokens ที่ใช้
   - ค่าใช้จ่ายแยกตาม model
   - Cost per request

### ตั้ง Budget Alert:

1. https://openrouter.ai/credits
2. Set Limit:
   - Daily: $1
   - Monthly: $10
3. ได้ email alert เมื่อใกล้เกิน

---

## 🎓 Tips & Tricks

### 1. เริ่มต้นด้วย Free Model

```bash
# ใช้ Gemini Pro ฟรีๆ ก่อน
OPENAI_MODEL=google/gemini-pro
```

- ทดสอบได้ไม่จำกัด (ภายใน rate limit)
- เมื่อพอใจแล้วค่อยเปลี่ยนเป็น paid model

### 2. Development vs Production

```bash
# Development (.env.development)
OPENAI_MODEL=google/gemini-pro  # ฟรี

# Production (.env.production)
OPENAI_MODEL=anthropic/claude-3.5-sonnet  # ดีที่สุด
```

### 3. ทดสอบหลาย Models

```python
# สร้างสคริปต์ทดสอบ
models = [
    "google/gemini-pro",
    "openai/gpt-3.5-turbo",
    "anthropic/claude-3.5-sonnet",
    "openai/gpt-4-turbo"
]

for model in models:
    # ทดสอบแต่ละ model
    # เปรียบเทียบผลลัพธ์
```

### 4. Monitor Costs

- เช็ค dashboard ทุกวัน
- ตั้ง budget alert
- ใช้ free model สำหรับ testing

---

## 🐛 Troubleshooting

### ❌ Error: "Invalid API key"

**ตรวจสอบ**:
1. API key ขึ้นต้นด้วย `sk-or-v1-` หรือไม่?
2. คัดลอกถูกต้อง (ไม่มีช่องว่าง)?
3. เซฟไฟล์ .env แล้วหรือยัง?

### ❌ Error: "Model not found"

**ตรวจสอบ**:
1. Model name format: `provider/model-name`
2. ดูรายชื่อ: https://openrouter.ai/models

**ตัวอย่างที่ถูก**:
```bash
✅ openai/gpt-4-turbo
✅ anthropic/claude-3.5-sonnet
✅ google/gemini-pro

❌ gpt-4-turbo (ขาด provider)
❌ claude-3.5-sonnet (ขาด provider)
```

### ❌ Error: "Insufficient credits"

**แก้**:
1. เติมเงินที่ https://openrouter.ai/credits
2. หรือใช้ free model:
   ```bash
   OPENAI_MODEL=google/gemini-pro
   ```

### ❌ AI ไม่ตอบ / ช้า

**ลองเปลี่ยน model**:
```bash
# จาก Gemini Pro (อาจมี rate limit)
OPENAI_MODEL=google/gemini-pro

# เป็น GPT-3.5 (เร็ว)
OPENAI_MODEL=openai/gpt-3.5-turbo
```

---

## ✅ Checklist

- [ ] สร้างบัญชี OpenRouter
- [ ] สร้าง API Key
- [ ] แก้ไข .env file
- [ ] ตั้งค่า OPENAI_BASE_URL
- [ ] เลือก model (แนะนำ: gemini-pro)
- [ ] ทดสอบ backend
- [ ] ลองส่งข้อความ
- [ ] เช็ค dashboard
- [ ] ตั้ง budget alert (ถ้าใช้ paid)

---

## 📚 เอกสารเพิ่มเติม

- [OPENROUTER_SETUP.md](docs/OPENROUTER_SETUP.md) - คู่มือละเอียด
- [OpenRouter Docs](https://openrouter.ai/docs) - เอกสารอย่างเป็นทางการ
- [Model List](https://openrouter.ai/models) - รายชื่อ models ทั้งหมด
- [Pricing](https://openrouter.ai/docs#models) - ราคา models

---

## 🎉 เสร็จแล้ว!

ตอนนี้โปรเจคของคุณ:
- ✅ ใช้ OpenRouter แทน OpenAI
- ✅ เลือก AI model ได้หลายตัว
- ✅ ประหยัดเงิน (หรือใช้ฟรี!)
- ✅ API เหมือนเดิมทุกอย่าง

**แนะนำเริ่มต้นด้วย**:
```bash
OPENAI_MODEL=google/gemini-pro  # ฟรี!
```

เมื่อพร้อม production:
```bash
OPENAI_MODEL=anthropic/claude-3.5-sonnet  # ดีที่สุด!
```

---

## 💬 Need Help?

1. อ่าน [OPENROUTER_SETUP.md](docs/OPENROUTER_SETUP.md)
2. เช็ค [OpenRouter Docs](https://openrouter.ai/docs)
3. ดู logs ใน terminal
4. ลอง restart backend

**Happy coding!** 🚀
