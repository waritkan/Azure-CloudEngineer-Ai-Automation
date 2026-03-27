# 🔑 OpenRouter Setup Guide

## ทำไมใช้ OpenRouter?

### ข้อดี:
- ✅ **ราคาถูกกว่า** OpenAI โดยตรง (บางโมเดลถึง 50-80% ถูกกว่า)
- ✅ **เลือกได้หลาย models** - GPT-4, Claude, Gemini, Llama ผ่าน API เดียว
- ✅ **API เหมือน OpenAI** - ใช้ OpenAI SDK ได้เลย
- ✅ **มี free models** - Gemini Pro ฟรี!
- ✅ **Pay-as-you-go** - จ่ายเท่าที่ใช้ ไม่มีค่าธรรมเนียมรายเดือน

### เปรียบเทียบราคา (per 1M tokens):

| Model | OpenAI Direct | OpenRouter | ประหยัด |
|-------|---------------|------------|---------|
| GPT-4 Turbo | $10 | $10 | เท่ากัน |
| GPT-3.5 Turbo | $0.50 | $0.50 | เท่ากัน |
| Claude 3.5 Sonnet | N/A | $3 | มีเฉพาะที่นี่! |
| Gemini Pro | N/A | **ฟรี!** | 100% |

---

## 🚀 Quick Setup (5 นาที)

### Step 1: สร้างบัญชี OpenRouter

1. ไปที่: https://openrouter.ai/
2. กด **"Sign In"** (ใช้ Google account ได้)
3. ยืนยัน email

### Step 2: เติมเงิน (Credit)

1. ไปที่: https://openrouter.ai/credits
2. กด **"Add Credits"**
3. เติมขั้นต่ำ **$5** (พอทดสอบนาน)

**ทิป**: $5 ใช้ได้นานมากถ้าใช้ GPT-3.5 หรือ Gemini Pro!

### Step 3: สร้าง API Key

1. ไปที่: https://openrouter.ai/keys
2. กด **"Create Key"**
3. ใส่ชื่อ: `azure-ai-automation`
4. คัดลอก key (จะขึ้น `sk-or-v1-...`)

⚠️ **สำคัญ**: เก็บ key ไว้ จะไม่แสดงอีก!

### Step 4: ตั้งค่าในโปรเจค

```bash
# ไปที่โฟลเดอร์ backend
cd E:\Cloud_Engineer_Project\azure-ai-automation\backend

# เปิดไฟล์ .env
notepad .env
```

**แก้ไขใน .env**:
```bash
# วาง API key ของคุณ
OPENAI_API_KEY=sk-or-v1-your-actual-key-here

# ใช้ base URL ของ OpenRouter
OPENAI_BASE_URL=https://openrouter.ai/api/v1

# เลือก model (แนะนำ)
OPENAI_MODEL=openai/gpt-4-turbo

# Optional: ข้อมูลแอป (สำหรับ analytics)
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
✅ AI Agent initialized with OpenRouter (openai/gpt-4-turbo)
```

---

## 🎯 แนะนำ Models

### สำหรับ Production (ใช้จริง):

#### 1. **GPT-4 Turbo** (แนะนำสุด!)
```bash
OPENAI_MODEL=openai/gpt-4-turbo
```
- **ราคา**: ~$10/1M input tokens
- **ข้อดี**: ฉลาดที่สุด, function calling แม่นมาก
- **เหมาะกับ**: งานสำคัญ, production
- **ค่าใช้จ่ายจริง**: ~$0.01 ต่อ 100 requests

#### 2. **Claude 3.5 Sonnet** (เทพมาก!)
```bash
OPENAI_MODEL=anthropic/claude-3.5-sonnet
```
- **ราคา**: ~$3/1M input tokens
- **ข้อดี**: ถูกกว่า GPT-4, ฉลาดพอๆ กัน
- **เหมาะกับ**: ทุกงาน, ดีมาก
- **ค่าใช้จ่ายจริง**: ~$0.003 ต่อ 100 requests

### สำหรับ Development (ทดสอบ):

#### 3. **GPT-3.5 Turbo** (เร็ว + ถูก)
```bash
OPENAI_MODEL=openai/gpt-3.5-turbo
```
- **ราคา**: ~$0.50/1M tokens
- **ข้อดี**: เร็วมาก, ถูกมาก
- **ข้อเสีย**: ไม่ฉลาดเท่า GPT-4
- **เหมาะกับ**: testing, development
- **ค่าใช้จ่ายจริง**: ~$0.0005 ต่อ 100 requests

#### 4. **Gemini Pro** (ฟรี! 🎉)
```bash
OPENAI_MODEL=google/gemini-pro
```
- **ราคา**: **ฟรี!** (มี rate limit)
- **ข้อดี**: ไม่เสียเงิน, ใช้ได้ดี
- **ข้อเสีย**: rate limit, อาจช้ากว่า
- **เหมาะกับ**: ทดสอบ, demo, เรียนรู้

### ตารางเปรียบเทียบ:

| Model | ราคา/100 reqs | ความฉลาด | ความเร็ว | Use Case |
|-------|---------------|----------|----------|----------|
| GPT-4 Turbo | $0.01 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Production |
| Claude 3.5 | $0.003 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Production (แนะนำ!) |
| GPT-3.5 | $0.0005 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Development |
| Gemini Pro | ฟรี | ⭐⭐⭐⭐ | ⭐⭐⭐ | Testing/Demo |

---

## 💰 การคำนวณค่าใช้จ่าย

### ตัวอย่างการใช้งาน:

```
1 request (chat) ≈ 500 tokens (input + output)

ถ้าใช้ GPT-4 Turbo:
- 100 requests = 50,000 tokens = $0.50
- 1,000 requests = 500,000 tokens = $5.00

ถ้าใช้ Claude 3.5 Sonnet:
- 100 requests = $0.15
- 1,000 requests = $1.50

ถ้าใช้ GPT-3.5 Turbo:
- 100 requests = $0.025
- 1,000 requests = $0.25

ถ้าใช้ Gemini Pro:
- ไม่จำกัด requests = ฟรี! (ภายใน rate limit)
```

### แนะนำเริ่มต้น:

**Phase 1: Development (ใช้ Gemini Pro)**
```bash
OPENAI_MODEL=google/gemini-pro
```
- ค่าใช้จ่าย: **$0**
- ทดสอบได้เต็มที่

**Phase 2: Testing (ใช้ GPT-3.5)**
```bash
OPENAI_MODEL=openai/gpt-3.5-turbo
```
- ค่าใช้จ่าย: ~$1-2/เดือน
- ทดสอบ function calling จริงจัง

**Phase 3: Production (ใช้ Claude 3.5)**
```bash
OPENAI_MODEL=anthropic/claude-3.5-sonnet
```
- ค่าใช้จ่าย: ~$3-5/เดือน
- ใช้จริง คุ้มค่าที่สุด

---

## 🔧 การเปลี่ยน Model

### วิธีที่ 1: แก้ใน .env (แนะนำ)

```bash
# เปิด .env
notepad .env

# เปลี่ยน model
OPENAI_MODEL=anthropic/claude-3.5-sonnet

# Save และ restart backend
```

### วิธีที่ 2: Environment Variable

```bash
# Windows
set OPENAI_MODEL=google/gemini-pro
uvicorn app.main:app --reload

# Linux/Mac
export OPENAI_MODEL=google/gemini-pro
uvicorn app.main:app --reload
```

---

## 📊 ดู Usage และค่าใช้จ่าย

### ใน OpenRouter Dashboard

1. ไปที่: https://openrouter.ai/activity
2. เห็น:
   - จำนวน requests
   - Tokens ที่ใช้
   - ค่าใช้จ่ายรวม
   - Model ที่ใช้

### ตั้ง Budget Alert

1. ไปที่: https://openrouter.ai/credits
2. กด **"Set Limit"**
3. ตั้ง:
   - Daily limit: $1
   - Monthly limit: $10
4. จะได้ email เมื่อใกล้เกิน

---

## 🌟 Models ที่แนะนำ (เพิ่มเติม)

### สำหรับประหยัดสุดๆ:

```bash
# Llama 3.1 70B (ฟรี!)
OPENAI_MODEL=meta-llama/llama-3.1-70b-instruct:free

# Mixtral 8x7B (ฟรี!)
OPENAI_MODEL=mistralai/mixtral-8x7b-instruct:free
```

### สำหรับความเร็ว:

```bash
# GPT-3.5 Turbo 16k (ถูก + เร็ว)
OPENAI_MODEL=openai/gpt-3.5-turbo-16k

# Claude Instant (เร็วมาก)
OPENAI_MODEL=anthropic/claude-instant-1.2
```

### สำหรับงานหนัก:

```bash
# GPT-4 128k (context ยาว)
OPENAI_MODEL=openai/gpt-4-turbo

# Claude 3 Opus (ฉลาดที่สุด)
OPENAI_MODEL=anthropic/claude-3-opus
```

---

## 🐛 Troubleshooting

### Error: "Insufficient credits"

**แก้**: เติมเงินที่ https://openrouter.ai/credits

### Error: "Invalid API key"

**เช็ค**:
1. API key ขึ้นต้นด้วย `sk-or-v1-` หรือไม่?
2. คัดลอกถูกต้องหรือไม่ (ไม่มีช่องว่าง)?
3. Key ถูกลบแล้วหรือไม่?

### Error: "Model not found"

**เช็ค**:
- Model name ถูกต้องหรือไม่?
- ดูรายชื่อ model: https://openrouter.ai/models
- Format: `provider/model-name` เช่น `openai/gpt-4-turbo`

### Error: "Rate limit exceeded"

**แก้**:
1. ใช้ model อื่น (ที่ไม่ฟรี)
2. รอสักครู่ (rate limit reset)
3. Upgrade plan ใน OpenRouter

---

## 🎯 สรุปการตั้งค่า

### ไฟล์ .env ที่แนะนำ:

```bash
# ========================================
# AI Configuration (OpenRouter)
# ========================================

# API Key (จาก https://openrouter.ai/keys)
OPENAI_API_KEY=sk-or-v1-your-actual-key-here

# Base URL (ห้ามเปลี่ยน!)
OPENAI_BASE_URL=https://openrouter.ai/api/v1

# Model Selection:
# เริ่มต้น (ฟรี): google/gemini-pro
# Development (ถูก): openai/gpt-3.5-turbo
# Production (แนะนำ): anthropic/claude-3.5-sonnet
# Best (แพง): openai/gpt-4-turbo
OPENAI_MODEL=anthropic/claude-3.5-sonnet

# App Info (สำหรับ analytics)
APP_URL=https://github.com/your-username/azure-ai-automation
APP_TITLE=Azure AI Automation

# ========================================
# Other Settings (เหมือนเดิม)
# ========================================
ENABLE_MOCK_MODE=true
MONTHLY_BUDGET_LIMIT=10.0
```

---

## 📚 Resources

- **OpenRouter Homepage**: https://openrouter.ai/
- **Model List**: https://openrouter.ai/models
- **Pricing**: https://openrouter.ai/docs#models
- **API Docs**: https://openrouter.ai/docs
- **Discord Community**: https://discord.gg/openrouter

---

## ✅ Checklist

- [ ] สร้างบัญชี OpenRouter
- [ ] เติมเงิน $5
- [ ] สร้าง API key
- [ ] แก้ไข .env file
- [ ] เลือก model ที่เหมาะสม
- [ ] ทดสอบ backend
- [ ] ตั้ง budget alert

---

## 🎉 พร้อมใช้งาน!

ตอนนี้คุณใช้ OpenRouter แล้ว!

**ข้อดี**:
- ✅ ราคาถูกกว่า (หรือฟรี!)
- ✅ เลือก model ได้หลายตัว
- ✅ Pay-as-you-go
- ✅ ง่ายต่อการเปลี่ยน model

**แนะนำเริ่มต้นด้วย**: `google/gemini-pro` (ฟรี!)

ขอให้สนุกกับการพัฒนา! 🚀
