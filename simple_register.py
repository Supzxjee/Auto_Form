"""
HSK SUPER SIMPLE - Đăng nhập 1 lần, điền tự động!
"""
from playwright.sync_api import sync_playwright
import json
import os
import time

CONFIG_FILE = "registration_info.json"

def load_info():
    if not os.path.exists(CONFIG_FILE):
        return None
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    info = load_info()
    if not info:
        print("⚠️ Chạy trước: python quick_register.py --setup")
        return
    
    print("\n" + "="*60)
    print("🚀 HSK SUPER SIMPLE REGISTER")
    print("="*60)
    print(f"\n📋 {info['full_name']} | {info['phone']}")
    
    form_url = input("\n📎 Paste URL form: ").strip()
    if not form_url:
        return
    
    print("\n🚀 Đang mở browser MỚI...")
    print("📌 Bạn sẽ cần đăng nhập Google 1 lần trong browser này\n")
    
    with sync_playwright() as p:
        # Mở browser MỚI, không dùng profile
        browser = p.chromium.launch(headless=False, args=['--start-maximized'])
        page = browser.new_page()
        
        # Bước 1: Đăng nhập Google trước
        print("="*60)
        print("BƯỚC 1: ĐĂNG NHẬP GOOGLE")
        print("="*60)
        page.goto("https://accounts.google.com/signin")
        
        print("\n👉 Trong cửa sổ browser vừa mở:")
        print("   1. Đăng nhập tài khoản Google của bạn")
        print("   2. Sau khi đăng nhập xong, quay lại đây")
        
        input("\n⏸️  Nhấn Enter sau khi ĐÃ ĐĂNG NHẬP xong...")
        
        # Bước 2: Mở form và điền
        print("\n" + "="*60)
        print("BƯỚC 2: TỰ ĐỘNG ĐIỀN FORM")
        print("="*60)
        
        page.goto(form_url)
        time.sleep(3)
        
        print("\n⚡ Đang điền form...")
        
        def click_next():
            btns = page.locator('[role="button"]').all()
            for b in btns:
                if 'Tiếp' in b.inner_text():
                    b.click()
                    return
        
        def click_radio(i):
            page.locator('[role="radio"]').nth(i).click()
        
        def fill_text(v):
            page.locator('input[type="text"]').first.fill(v)
        
        try:
            # Page 1
            cb = page.locator('[role="checkbox"]').first
            if cb.is_visible() and cb.get_attribute('aria-checked') != 'true':
                cb.click()
            time.sleep(0.3)
            click_next()
            time.sleep(2)
            print("  ✓ Trang 1")
            
            # Page 2
            click_next()
            time.sleep(2)
            print("  ✓ Trang 2")
            
            # Page 3
            click_radio(0)
            time.sleep(0.3)
            click_next()
            time.sleep(2)
            print("  ✓ Trang 3")
            
            # Page 4 - Name
            fill_text(info['full_name'])
            time.sleep(0.3)
            click_next()
            time.sleep(2)
            print(f"  ✓ Trang 4: {info['full_name']}")
            
            # Page 5 - ID
            click_radio(0 if info['id_type'] == 'passport' else 1)
            time.sleep(0.5)
            fill_text(info['id_number'])
            time.sleep(0.3)
            click_next()
            time.sleep(2)
            print(f"  ✓ Trang 5: {info['id_number']}")
            
            # Page 6
            click_radio(0 if info['gender'] == 'nam' else 1)
            time.sleep(0.3)
            click_next()
            time.sleep(2)
            print("  ✓ Trang 6")
            
            # Page 7
            click_radio(0 if info['nationality'] == 'vietnam' else 1)
            time.sleep(0.3)
            click_next()
            time.sleep(2)
            print("  ✓ Trang 7")
            
            # Page 8
            fill_text(info['phone'])
            time.sleep(0.3)
            click_next()
            time.sleep(2)
            print(f"  ✓ Trang 8: {info['phone']}")
            
            # Page 9, 10
            for i in [9, 10]:
                try:
                    click_next()
                    time.sleep(2)
                    print(f"  ✓ Trang {i}")
                except:
                    pass
            
            # Page 11
            click_radio(0)
            time.sleep(0.3)
            click_next()
            time.sleep(2)
            print("  ✓ Trang 11")
            
            print("\n" + "="*60)
            print("✅ HOÀN TẤT!")
            print("="*60)
            print("\n🎯 Chỉ cần điền câu xác thực và Submit!")
            
        except Exception as e:
            print(f"\n⚠️ Lỗi: {e}")
            print("💡 Tiếp tục điền thủ công trong browser!")
        
        input("\n⏸️  Nhấn Enter sau khi submit xong để đóng...")
        browser.close()
    
    print("\n✅ Xong! Chúc mừng! 🎉\n")

if __name__ == "__main__":
    main()
