"""
HSK Quick Register - EDGE VERSION
Dùng Edge đã đăng nhập của bạn!
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
import json
import os
import time

CONFIG_FILE = "registration_info.json"

def load_info():
    if not os.path.exists(CONFIG_FILE):
        print("⚠️  Chưa có thông tin! Chạy trước: python quick_register.py --setup")
        return None
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def quick_register():
    info = load_info()
    if not info:
        return
    
    print("\n" + "="*60)
    print("🚀 ĐĂNG KÝ NHANH - EDGE")
    print("="*60)
    print(f"\n📋 Thông tin: {info['full_name']} | {info['phone']}")
    
    form_url = input("\n📎 Paste URL form: ").strip()
    if not form_url:
        print("❌ Chưa nhập URL!")
        return
    
    print("\n🚀 Đang mở Edge với profile của bạn...")
    
    # Edge profile path
    edge_user_data = os.path.join(os.environ['LOCALAPPDATA'], 'Microsoft', 'Edge', 'User Data')
    
    edge_options = Options()
    edge_options.add_argument(f"user-data-dir={edge_user_data}")
    edge_options.add_argument("--profile-directory=Default")
    edge_options.add_argument("--start-maximized")
    edge_options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
    edge_options.add_experimental_option('useAutomationExtension', False)
    
    try:
        driver = webdriver.Edge(options=edge_options)
        
        print("📄 Đang mở form...")
        driver.get(form_url)
        time.sleep(3)
        
        print("\n✅ Edge đã mở!")
        input("⏸️  Nhấn Enter khi form đã load và bạn đã đăng nhập Google...")
        
        print("\n⚡ Đang điền form...")
        
        def click_next():
            for btn in driver.find_elements(By.CSS_SELECTOR, '[role="button"]'):
                if 'Tiếp' in btn.text or 'Next' in btn.text:
                    btn.click()
                    return True
            return False
        
        def click_radio(idx):
            radios = driver.find_elements(By.CSS_SELECTOR, '[role="radio"]')
            if idx < len(radios):
                radios[idx].click()
        
        def fill_text(val):
            driver.find_element(By.CSS_SELECTOR, 'input[type="text"]').send_keys(val)
        
        # Page 1
        try:
            cb = driver.find_element(By.CSS_SELECTOR, '[role="checkbox"]')
            if cb.get_attribute('aria-checked') != 'true':
                cb.click()
            time.sleep(0.3)
            click_next()
            time.sleep(2)
            print("  ✓ Trang 1")
        except: pass
        
        # Page 2
        try:
            click_next()
            time.sleep(2)
            print("  ✓ Trang 2")
        except: pass
        
        # Page 3
        try:
            click_radio(0)
            time.sleep(0.3)
            click_next()
            time.sleep(2)
            print("  ✓ Trang 3")
        except: pass
        
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
        
        # Page 6 - Gender
        click_radio(0 if info['gender'] == 'nam' else 1)
        time.sleep(0.3)
        click_next()
        time.sleep(2)
        print("  ✓ Trang 6")
        
        # Page 7 - Nationality
        click_radio(0 if info['nationality'] == 'vietnam' else 1)
        time.sleep(0.3)
        click_next()
        time.sleep(2)
        print("  ✓ Trang 7")
        
        # Page 8 - Phone
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
            except: pass
        
        # Page 11 - Commitment
        try:
            click_radio(0)
            time.sleep(0.3)
            click_next()
            time.sleep(2)
            print("  ✓ Trang 11")
        except: pass
        
        print("\n" + "="*60)
        print("✅ HOÀN TẤT! Điền câu xác thực và Submit!")
        print("="*60)
        
        input("\n⏸️  Nhấn Enter sau khi submit xong...")
        
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        print("💡 Đóng hết Edge và thử lại!")
        input("Nhấn Enter...")
    
    finally:
        try:
            driver.quit()
        except: pass
        print("\n✅ Xong! 🎉\n")

if __name__ == "__main__":
    quick_register()
