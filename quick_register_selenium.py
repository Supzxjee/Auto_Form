"""
HSK Quick Register - SELENIUM VERSION
Tự động dùng Chrome đã đăng nhập của bạn!
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import json
import os
import time

CONFIG_FILE = "registration_info.json"

def load_info():
    """Đọc thông tin đã lưu"""
    if not os.path.exists(CONFIG_FILE):
        print("⚠️  Chưa có thông tin! Chạy: python quick_register.py --setup")
        return None
    
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def quick_register():
    """Đăng ký nhanh với Selenium"""
    info = load_info()
    if not info:
        return
    
    print("\n" + "="*60)
    print("🚀 ĐĂNG KÝ NHANH - SELENIUM")
    print("="*60)
    print(f"\n📋 Thông tin:")
    print(f"   {info['full_name']} | {info['id_type'].upper()} {info['id_number']}")
    print(f"   {info['gender'].upper()} | {info['nationality'].upper()} | {info['phone']}")
    
    # Nhập URL
    print("\n" + "="*60)
    form_url = input("📎 Paste URL form CHÍNH THỨC:\n   ").strip()
    
    if not form_url:
        print("❌ Chưa nhập URL!")
        return
    
    print("\n🚀 Đang khởi động Chrome với profile của bạn...")
    
    # Tìm Chrome profile
    chrome_user_data = os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data')
    
    # Tạo Chrome options
    chrome_options = Options()
    chrome_options.add_argument(f"user-data-dir={chrome_user_data}")
    chrome_options.add_argument("--profile-directory=Default")  # Hoặc Profile 1, Profile 2...
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    try:
        # Khởi động Chrome
        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 10)
        
        # Mở form
        print("📄 Đang mở form...")
        driver.get(form_url)
        time.sleep(3)
        
        print("\n" + "="*60)
        print("✅ Chrome đã mở với tài khoản của bạn!")
        print("="*60)
        print("\nKiểm tra:")
        print("1️⃣  Bạn đã đăng nhập Google chưa?")
        print("2️⃣  Form đã tải đủ chưa?")
        
        input("\n⏸️  Nhấn Enter để bắt đầu tự động điền...")
        
        print("\n⚡ Đang điền form...")
        
        def click_next():
            """Click nút Tiếp/Next"""
            buttons = driver.find_elements(By.CSS_SELECTOR, '[role="button"]')
            for btn in buttons:
                if 'Tiếp' in btn.text or 'Next' in btn.text:
                    btn.click()
                    return True
            return False
        
        def click_radio(index):
            """Click radio button"""
            radios = driver.find_elements(By.CSS_SELECTOR, '[role="radio"]')
            if index < len(radios):
                radios[index].click()
                return True
            return False
        
        def fill_text(value):
            """Điền text input"""
            inp = driver.find_element(By.CSS_SELECTOR, 'input[type="text"]')
            inp.clear()
            inp.send_keys(value)
        
        # Page 1: Email checkbox
        try:
            checkbox = driver.find_element(By.CSS_SELECTOR, '[role="checkbox"]')
            if checkbox.get_attribute('aria-checked') != 'true':
                checkbox.click()
                time.sleep(0.3)
            click_next()
            time.sleep(2)
            print("  ✓ Trang 1")
        except:
            pass
        
        # Page 2: NO SPAM
        try:
            click_next()
            time.sleep(2)
            print("  ✓ Trang 2")
        except:
            pass
        
        # Page 3: Exam level
        try:
            click_radio(0)
            time.sleep(0.3)
            click_next()
            time.sleep(2)
            print("  ✓ Trang 3: Cấp độ")
        except:
            pass
        
        # Page 4: Full name
        fill_text(info['full_name'])
        time.sleep(0.3)
        click_next()
        time.sleep(2)
        print(f"  ✓ Trang 4: {info['full_name']}")
        
        # Page 5: ID type and number
        if info['id_type'] == 'passport':
            click_radio(0)
        else:
            click_radio(1)
        time.sleep(0.5)
        fill_text(info['id_number'])
        time.sleep(0.3)
        click_next()
        time.sleep(2)
        print(f"  ✓ Trang 5: {info['id_number']}")
        
        # Page 6: Gender
        if info['gender'] == 'nam':
            click_radio(0)
        else:
            click_radio(1)
        time.sleep(0.3)
        click_next()
        time.sleep(2)
        print(f"  ✓ Trang 6: {info['gender']}")
        
        # Page 7: Nationality
        if info['nationality'] == 'vietnam':
            click_radio(0)
        else:
            click_radio(1)
        time.sleep(0.3)
        click_next()
        time.sleep(2)
        print(f"  ✓ Trang 7: {info['nationality']}")
        
        # Page 8: Phone
        fill_text(info['phone'])
        time.sleep(0.3)
        click_next()
        time.sleep(2)
        print(f"  ✓ Trang 8: {info['phone']}")
        
        # Page 9: Notice
        try:
            click_next()
            time.sleep(2)
            print("  ✓ Trang 9")
        except:
            pass
        
        # Page 10: Optional
        try:
            click_next()
            time.sleep(2)
            print("  ✓ Trang 10")
        except:
            pass
        
        # Page 11: Commitment
        try:
            click_radio(0)
            time.sleep(0.3)
            click_next()
            time.sleep(2)
            print("  ✓ Trang 11: Cam kết")
        except:
            pass
        
        # Done
        print("\n" + "="*60)
        print("✅ HOÀN TẤT!")
        print("="*60)
        print("\n🎯 Bây giờ:")
        print("1️⃣  Điền câu xác thực (trang 12)")
        print("2️⃣  Kiểm tra lại thông tin")
        print("3️⃣  Nhấn 'Gửi'")
        print("\n💡 Chrome sẽ mở để bạn hoàn tất.\n")
        
        input("⏸️  Nhấn Enter sau khi submit xong...")
        
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        print("💡 Nếu lỗi 'Chrome đang chạy', đóng hết Chrome và chạy lại.\n")
        input("Nhấn Enter để tiếp tục...")
    
    finally:
        try:
            driver.quit()
        except:
            pass
        print("\n✅ Xong! Chúc mừng! 🎉\n")

if __name__ == "__main__":
    import sys
    
    if '--setup' in sys.argv:
        # Import setup function from quick_register.py
        from quick_register import save_info
        save_info()
    else:
        quick_register()
