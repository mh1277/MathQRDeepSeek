import os
import requests
import time
from dotenv import load_dotenv

# تحميل مفتاح API من ملف .env
load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

def read_text_file(file_path):
    """قراءة محتوى ملف نصي"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"خطأ: الملف {file_path} غير موجود!")
        return None
    except Exception as e:
        print(f"خطأ أثناء قراءة الملف: {str(e)}")
        return None

def ask_deepseek(question):
    """إرسال سؤال إلى DeepSeek API"""
    headers = {"Authorization": f"Bearer {API_KEY}"}
    data = {
        "model": "deepseek/deepseek-chat:free",
        "messages": [
            {"role": "system", "content": "أنت أستاذ رياضيات متخصص في التحليل العقدي."},
            {"role": "user", "content": question}
        ]
    }
    
    try:
        response = requests.post(API_URL, json=data, headers=headers, timeout=60)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        print(f"خطأ في الاتصال بالخادم: {str(e)}")
        return None
    except Exception as e:
        print(f"خطأ غير متوقع: {str(e)}")
        return None

def save_results(content, output_path):
    """حفظ النتائج في ملف"""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"خطأ أثناء حفظ النتائج: {str(e)}")
        return False

def process_questions(input_content):
    """معالجة الأسئلة وإرسالها"""
    if not input_content:
        return "لا يوجد محتوى للمعالجة"
    
    questions = input_content.split('\n')
    results = []
    
    for i, q in enumerate(questions):
        if q.strip():  # تجاهل الأسطر الفارغة
            print(f"[{i+1}/{len(questions)}] معالجة السؤال: {q[:50]}...")
            
            # إرسال السؤال مع إعادة المحاولة عند الفشل
            for attempt in range(3):
                answer = ask_deepseek(q)
                if answer:
                    results.append(f"س: {q}\nج: {answer}\n{'='*50}\n")
                    time.sleep(1)  # تجنب تجاوز حد الطلبات
                    break
                else:
                    print(f"المحاولة {attempt+1} فشلت. إعادة المحاولة...")
                    time.sleep(2)
            else:
                results.append(f"س: {q}\nج: فشل في الحصول على إجابة بعد 3 محاولات\n{'='*50}\n")
    
    return ''.join(results)

# المعالجة الرئيسية
if __name__ == "__main__":
    # 1. إعداد المسارات
    input_file = "input.txt"
    output_file = "output.txt"
    
    print("="*50)
    print("بدء معالجة الأسئلة الرياضية باستخدام DeepSeek API")
    print("="*50)
    
    # 2. قراءة ملف الإدخال
    print(f"جاري قراءة الملف: {input_file}")
    input_content = read_text_file(input_file)
    
    if input_content is None:
        input("اضغط Enter للخروج...")
        exit()
    
    # 3. معالجة الأسئلة
    print(f"تم العثور على {len(input_content.splitlines())} سؤال")
    print("بدأت عملية الإرسال إلى DeepSeek API...")
    processed_content = process_questions(input_content)
    
    # 4. حفظ النتائج
    print(f"جاري حفظ النتائج في: {output_file}")
    if save_results(processed_content, output_file):
        print("تم الحفظ بنجاح!")
    else:
        print("حدث خطأ أثناء الحفظ")
    
    print("="*50)
    input("اكتملت العملية. اضغط Enter للخروج...")