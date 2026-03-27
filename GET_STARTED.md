# 🎓 GET STARTED - สำหรับผู้เริ่มต้น

## คู่มือเริ่มต้นแบบ Step-by-Step (ภาษาไทย)

---

## 🎯 เป้าหมาย

ภายใน 30 นาที คุณจะมี:
- ✅ Backend API ที่ทำงานได้
- ✅ Frontend สำหรับแชทกับ AI
- ✅ ความเข้าใจการทำงานของระบบ
- ✅ ความพร้อมสำหรับ interview

---

## 📚 Phase 1: เตรียมความพร้อม (5 นาที)

### ขั้นตอนที่ 1: เช็คว่ามี Python หรือยัง

เปิด Command Prompt หรือ Terminal แล้วพิมพ์:

```bash
python --version
```

ถ้าขึ้น `Python 3.11.x` หรือสูงกว่า = พร้อมแล้ว ✅

ถ้ายังไม่มี:
1. ดาวน์โหลดจาก: https://www.python.org/downloads/
2. ติดตั้ง (เลือก "Add Python to PATH" ด้วย!)
3. เช็คอีกครั้ง

### ขั้นตอนที่ 2: เตรียม OpenAI API Key

1. ไปที่ https://platform.openai.com/
2. สร้างบัญชี (ถ้ายังไม่มี)
3. ไปที่ API Keys: https://platform.openai.com/api-keys
4. กด "Create new secret key"
5. คัดลอก key (เก็บไว้ ต้องใช้ในขั้นตอนถัดไป)

**ค่าใช้จ่าย**: ~$0.20 สำหรับ 100 ครั้ง (ถูกมาก!)

**ฟรีหรือเปล่า?**
- มี free credit $5 สำหรับบัญชีใหม่
- พอทดสอบได้ประมาณ 2,500 ครั้ง

---

## 🛠️ Phase 2: ติดตั้ง Backend (10 นาที)

### ขั้นตอนที่ 1: ไปที่โฟลเดอร์โปรเจค

```bash
cd E:\Cloud_Engineer_Project\azure-ai-automation
dir  # เช็คว่ามีโฟลเดอร์ backend, frontend, docs
```

### ขั้นตอนที่ 2: ไปที่โฟลเดอร์ backend

```bash
cd backend
dir  # ควรเห็น app, requirements.txt, .env.example
```

### ขั้นตอนที่ 3: สร้าง Virtual Environment

```bash
# สร้าง virtual environment
python -m venv venv

# เปิดใช้งาน (Windows)
venv\Scripts\activate

# เปิดใช้งาน (Mac/Linux)
source venv/bin/activate

# จะเห็น (venv) ขึ้นหน้า command prompt
```

**ทำไมต้องใช้ venv?**
- แยก dependencies ของโปรเจคนี้ออกจากระบบ
- ไม่รบกวน Python projects อื่นๆ
- ง่ายต่อการลบทิ้ง (แค่ลบโฟลเดอร์ venv)

### ขั้นตอนที่ 4: ติดตั้ง Dependencies

```bash
# ติดตั้งไลบรารีทั้งหมด
pip install -r requirements.txt

# จะใช้เวลา 1-2 นาที
# จะเห็นข้อความติดตั้งไฟล์ต่างๆ

# เช็คว่าติดตั้งสำเร็จ
pip list | findstr fastapi
# ควรเห็น fastapi อยู่ในรายการ
```

### ขั้นตอนที่ 5: ตั้งค่า Environment Variables

```bash
# คัดลอกไฟล์ตัวอย่าง
copy .env.example .env

# เปิดไฟล์ .env ด้วย notepad
notepad .env
```

**แก้ไขใน .env**:

```bash
# เปลี่ยนบรรทัดนี้:
OPENAI_API_KEY=sk-your-openai-api-key-here

# เป็น (วาง API key ที่คุณคัดลอกไว้):
OPENAI_API_KEY=sk-proj-xxx...xxx

# เซฟไฟล์ (Ctrl+S)
```

**ส่วนอื่นๆ ให้ไว้ตามนี้**:
```bash
ENABLE_MOCK_MODE=true  # เป็น mock mode (ไม่ใช้เงิน)
MONTHLY_BUDGET_LIMIT=10.0
```

### ขั้นตอนที่ 6: เริ่ม Backend Server

```bash
# รันเซิร์ฟเวอร์
uvicorn app.main:app --reload
```

**ถ้าสำเร็จจะเห็น**:
```
🚀 Starting Azure AI Automation v1.0.0
📊 Mode: MOCK
Azure Configured: ❌
OpenAI Configured: ✅
Budget Limit: $10.00/month
============================================

INFO:     Uvicorn running on http://127.0.0.1:8000
```

**🎉 Backend พร้อมใช้งานแล้ว!**

---

## 🎨 Phase 3: เปิด Frontend (2 นาที)

### วิธีที่ 1: เปิดไฟล์ HTML โดยตรง (ง่ายที่สุด)

1. เปิด File Explorer
2. ไปที่ `E:\Cloud_Engineer_Project\azure-ai-automation\frontend\simple-html`
3. ดับเบิลคลิก `index.html`
4. จะเปิดใน Browser

### วิธีที่ 2: ใช้ Python HTTP Server (แนะนำ)

```bash
# เปิด Terminal/CMD ใหม่ (ไม่ต้องปิดของเดิม)
cd E:\Cloud_Engineer_Project\azure-ai-automation\frontend\simple-html

# รัน HTTP server
python -m http.server 3000
```

เปิด Browser ไปที่: `http://localhost:3000`

**🎉 Frontend พร้อมใช้งานแล้ว!**

---

## 🎮 Phase 4: ทดสอบระบบ (10 นาที)

### ทดสอบที่ 1: สร้าง VM

พิมพ์ในช่องแชท:
```
Create a small VM for testing
```

**สิ่งที่ควรเกิดขึ้น**:
1. ข้อความคุณปรากฏในแชท
2. AI ตอบว่ากำลังสร้าง VM
3. Budget widget อัปเดต (แสดง ~$7.59)
4. VM ปรากฏในรายการ Resources
5. สถานะเป็น "running"

### ทดสอบที่ 2: ดูรายการ VM

พิมพ์:
```
What VMs do I have?
```

**ควรเห็น**: AI บอกรายชื่อ VM ทั้งหมด พร้อมรายละเอียด

### ทดสอบที่ 3: เช็ค Budget

พิมพ์:
```
What's my budget status?
```

**ควรเห็น**: AI บอก budget ที่ใช้ไป, เหลือ, เปอร์เซ็นต์

### ทดสอบที่ 4: หยุด VM (ประหยัดเงิน)

พิมพ์:
```
Stop the test VM
```

**ควรเห็น**: AI confirm ว่าหยุด VM แล้ว

### ทดสอบที่ 5: ลบ VM

พิมพ์:
```
Delete test-vm-001
```

**ควรเห็น**: AI confirm ว่าลบแล้ว, Budget ลดลง

---

## 🧠 Phase 5: เข้าใจการทำงาน (5 นาที)

### แนวคิดหลัก: AI Function Calling

**แบบเก่า (ไม่ดี)**:
```python
if "create vm" in message:
    create_vm()
elif "สร้าง vm" in message:
    create_vm()
elif "ขอ vm" in message:
    create_vm()
# ต้องเขียนทุก case!
```

**แบบใหม่ (ใช้ AI)**:
```python
# 1. บอก AI ว่ามี function อะไรบ้าง
tools = [{
    "name": "create_vm",
    "description": "สร้าง VM ใน Azure",
    "parameters": {"name": "...", "size": "..."}
}]

# 2. AI วิเคราะห์ message
user_message = "ขอเครื่องเซิร์ฟเวอร์ตัวเล็กๆ หน่อย"

# 3. AI ตัดสินใจเอง!
AI decides:
  - Function: create_vm
  - Parameters: size="B1s", region="southeastasia"

# 4. ระบบเรียก function
create_vm(size="B1s", region="southeastasia")
```

**ข้อดี**:
- ไม่ต้อง hardcode logic
- รองรับภาษาอะไรก็ได้
- เพิ่ม function ใหม่ง่าย
- AI เข้าใจ context

### Data Flow (การไหลของข้อมูล)

```
1. User พิมพ์: "Create a VM"
        ↓
2. Frontend ส่งไป Backend: POST /api/chat
        ↓
3. Backend ส่งให้ AI Agent
        ↓
4. AI Agent:
   - ส่งไปหา OpenAI
   - OpenAI วิเคราะห์
   - OpenAI ตอบ: "เรียก create_vm()"
        ↓
5. Backend:
   - เช็ค Budget ก่อน
   - ถ้าพอ → สร้าง VM (mock mode = จำลอง)
   - บันทึกข้อมูล
        ↓
6. Backend ส่งผลกลับให้ AI
        ↓
7. AI เขียนข้อความตอบ User
        ↓
8. Frontend แสดงข้อความ
```

### ไฟล์สำคัญ

| ไฟล์ | หน้าที่ |
|------|---------|
| `app/main.py` | API endpoints (รับ HTTP requests) |
| `app/ai_agent.py` | สมอง AI ที่ตัดสินใจเรียก function |
| `app/azure_functions.py` | จัดการ Azure (สร้าง/หยุด/ลบ VM) |
| `app/budget_control.py` | เช็คและควบคุมงบประมาณ |
| `app/models.py` | โครงสร้างข้อมูล (Request/Response) |
| `app/config.py` | ตั้งค่าระบบ (อ่านจาก .env) |

---

## 🔍 Phase 6: ทดสอบ API โดยตรง (Optional)

### ใช้ Browser

ไปที่: `http://localhost:8000/docs`

**จะเห็น**:
- รายการ API endpoints ทั้งหมด
- สามารถทดสอบได้เลย (กด "Try it out")
- เห็น Request/Response format

### ทดสอบด้วย curl

```bash
# ส่งข้อความให้ AI
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"Create a VM\"}"

# ดูรายการ resources
curl "http://localhost:8000/api/resources"

# เช็ค budget
curl "http://localhost:8000/api/budget"

# สร้าง VM โดยตรง (ไม่ผ่าน AI)
curl -X POST "http://localhost:8000/api/vm/create" \
  -H "Content-Type: application/json" \
  -d "{\"name\": \"direct-vm\", \"size\": \"B1s\", \"region\": \"southeastasia\"}"
```

---

## 💰 ค่าใช้จ่าย

### Mock Mode (ที่คุณใช้อยู่ตอนนี้)

| รายการ | ราคา |
|--------|------|
| Backend Server | ฟรี (รันบนเครื่องตัวเอง) |
| Frontend | ฟรี |
| Azure Resources | $0 (เป็น simulation) |
| OpenAI API | ~$0.002 ต่อ request |
| **รวม** | **~$0.20 สำหรับ 100 ครั้ง** |

### Azure Mode (เมื่อเชื่อม Azure จริง)

| รายการ | ราคา/เดือน |
|--------|------------|
| B1s VM (24/7) | $7.59 |
| B1s VM (8 ชม./วัน) | $2.53 |
| OpenAI API | $0.20 |
| Azure Storage | $0.10 |
| **รวม** | **$3-8** |

**ทิป ประหยัดเงิน**:
- หยุด VM เมื่อไม่ใช้
- ใช้ Free tier ของ Azure ($200 credit เดือนแรก)
- ตั้ง Budget Alert ใน Azure Portal

---

## 🎯 ถัดไป: เตรียมตัว Interview

### 1. อ่านเอกสาร

| เอกสาร | เวลาที่ต้องใช้ | สำคัญระดับ |
|--------|----------------|-----------|
| [INTERVIEW_GUIDE.md](docs/INTERVIEW_GUIDE.md) | 30 นาที | ⭐⭐⭐⭐⭐ |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | 20 นาที | ⭐⭐⭐⭐ |
| [DEMO_SCRIPT.md](docs/DEMO_SCRIPT.md) | 15 นาที | ⭐⭐⭐⭐ |

### 2. ฝึกพูดอธิบายโปรเจค

**30-second pitch**:
> "ผมสร้างระบบ AI ที่ช่วยจัดการ Azure infrastructure ผ่านการสนทนา ใช้ GPT-4 function calling เพื่อให้ AI เข้าใจความต้องการของ user แล้วเรียก Azure SDK ทำงานโดยอัตโนมัติ มีระบบควบคุม budget เพื่อไม่ให้เกินงบ backend ใช้ FastAPI กับ Azure SDK ส่วน frontend เป็น React แสดงผล chat interface"

**ฝึกให้ได้ภายใน 30 วินาที!**

### 3. เตรียมตัวตอบคำถาม

**คำถามที่มักถูกถาม**:

**Q: "ทำไมใช้ AI แทนที่จะเขียน if/else?"**
> "เพราะ if/else จะยาวมาก ไม่ยืดหยุ่น และไม่รองรับการพูดแบบธรรมชาติ ในขณะที่ AI สามารถเข้าใจความหมายและเลือก function ที่เหมาะสมได้เอง"

**Q: "ถ้า AI ทำผิดล่ะ?"**
> "ผมมีหลายชั้นป้องกัน: 1) Good function descriptions ทำให้ AI เข้าใจถูก 2) Pydantic validation เช็คข้อมูล 3) Budget control ป้องกันการทำงานที่แพงเกินไป 4) ใน production จะเพิ่ม confirmation สำหรับการลบหรือ operations ที่เสี่ยง"

**Q: "Scale ได้ไงถ้าเป็น production?"**
> "ต้องเพิ่ม: Database เก็บ history, Message Queue สำหรับ long operations, Redis cache, Authentication ด้วย Azure AD, Monitoring ด้วย Application Insights, และ deploy บน Azure App Service หรือ AKS ที่ scale ได้"

### 4. Demo ให้คล่อง

- ฝึก demo 5 ครั้ง
- จับเวลาให้ได้ไม่เกิน 3 นาที
- เตรียม screenshot ไว้สำรอง
- รู้ว่าจะเปิดไฟล์ไหนถ้าถูกถาม

---

## 🐛 แก้ปัญหา (Troubleshooting)

### Backend ไม่ start

**Error**: `ModuleNotFoundError`
```bash
# ลืม activate venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Error**: `Port 8000 already in use`
```bash
# เปลี่ยน port
uvicorn app.main:app --reload --port 8001
```

### AI ไม่ตอบ

**เช็ค**:
1. OPENAI_API_KEY ถูกต้องหรือไม่?
2. มี credit ใน OpenAI account หรือไม่?
3. เปิด backend แล้วหรือยัง?

**วิธีเช็ค**:
```bash
# ไปที่ http://localhost:8000/health
# ถ้า ai_enabled: true = OK
# ถ้า ai_enabled: false = API key ผิด
```

### Frontend ไม่ connect Backend

**เช็ค**:
1. Backend รันที่ port 8000 หรือไม่?
2. ใน index.html, API_BASE_URL เป็น `http://localhost:8000` หรือไม่?
3. ลอง refresh browser (Ctrl+F5)

---

## ✅ Checklist ก่อน Interview

- [ ] Backend start ได้ไม่มี error
- [ ] Frontend เปิดได้
- [ ] ส่งข้อความให้ AI ได้
- [ ] Budget update ถูกต้อง
- [ ] Resource list แสดงผล
- [ ] อ่าน INTERVIEW_GUIDE แล้ว
- [ ] ฝึก 30-second pitch แล้ว
- [ ] Demo ได้คล่อง (3 นาที)
- [ ] เข้าใจ code ทุกส่วน
- [ ] รู้จะตอบคำถามยังไง

---

## 🎓 สรุป

คุณได้อะไรจากโปรเจคนี้:

### Technical Skills
- ✅ Azure SDK & Cloud Management
- ✅ AI/LLM Integration (Function Calling)
- ✅ Backend Development (FastAPI)
- ✅ API Design (RESTful)
- ✅ Cost Optimization (FinOps)
- ✅ Security Best Practices

### Soft Skills
- ✅ System Architecture Design
- ✅ Problem Solving
- ✅ Documentation
- ✅ Portfolio Presentation

### Portfolio Value
- ✅ Modern tech stack (AI + Cloud)
- ✅ Production-ready patterns
- ✅ Cost-conscious design
- ✅ Full-stack implementation
- ✅ Well-documented

---

## 🚀 พร้อมไปสัมภาษณ์แล้ว!

คุณมีโปรเจคที่:
- ใช้เทคโนโลยีทันสมัย (AI + Azure)
- แก้ปัญหาจริง (Cloud automation)
- ออกแบบดี (Architecture, Security, Cost)
- พร้อม demo ได้เลย

**ขอให้โชคดีกับการสัมภาษณ์!** 🎯

---

**หากมีปัญหา**:
1. อ่าน docs/ ในโฟลเดอร์ docs
2. เช็ค logs ใน terminal
3. ลอง restart backend
4. เปิด /docs endpoint ดู API

**Resources เพิ่มเติม**:
- Azure Pricing: https://azure.microsoft.com/pricing/
- OpenAI Function Calling: https://platform.openai.com/docs/guides/function-calling
- FastAPI Tutorial: https://fastapi.tiangolo.com/tutorial/
