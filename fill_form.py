"""
HSK Form Auto-Filler - Python Script
Tự động điền form HSK/HSKK nhanh chóng
"""
from playwright.sync_api import sync_playwright
import time

# ============================================
# NHẬP THÔNG TIN CỦA BẠN VÀO ĐÂY
# ============================================
FULL_NAME = "NGUYEN VAN A"  # IN HOA KHÔNG DẤU
ID_TYPE = "cmnd"  # "cmnd" hoặc "passport"
ID_NUMBER = "001234567890"
GENDER = "nam"  # "nam" hoặc "nữ"
NATIONALITY = "vietnam"  # "vietnam" hoặc "other"
PHONE = "0901234567"

# URL form
FORM_URL = "https://forms.gle/fQh8tta49UMDJxcZA"

def fill_form():
    print("🚀 Đang khởi động browser với tài khoản đã đăng nhập...")
    
    with sync_playwright() as p:
        # Sử dụng Chrome profile đã đăng nhập của user
        # Tìm Chrome user data directory
        import os
        user_data_dir = os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data')
        
        browser = p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            channel="chrome",  # Sử dụng Chrome thay vì Chromium
            args=[
                '--start-maximized',
                '--disable-blink-features=AutomationControlled'
            ]
        )
        
        page = browser.pages[0] if browser.pages else browser.new_page()
        
        try:
            # Mở form
            print(f"📄 Đang mở form: {FORM_URL}")
            page.goto(FORM_URL)
            time.sleep(2)
            
            # Trang 1: Email checkbox
            print("📄 Trang 1: Email confirmation")
            checkbox = page.locator('[role="checkbox"]').first
            if checkbox.is_visible():
                if checkbox.get_attribute('aria-checked') != 'true':
                    checkbox.click()
                    time.sleep(0.3)
            
            click_next(page)
            time.sleep(2)
            
            # Trang 2: NO SPAM
            print("📄 Trang 2: NO SPAM")
            click_next(page)
            time.sleep(2)
            
            # Trang 3: Cấp độ thi (MÔ PHỎNG)
            print("📄 Trang 3: Cấp độ thi - MÔ PHỎNG")
            page.locator('[role="radio"]').first.click()
            time.sleep(0.3)
            click_next(page)
            time.sleep(2)
            
            # Trang 4: Họ và tên
            print(f"📄 Trang 4: Họ và tên - {FULL_NAME}")
            page.locator('input[type="text"]').first.fill(FULL_NAME)
            time.sleep(0.3)
            click_next(page)
            time.sleep(2)
            
            # Trang 5: Giấy tờ tùy thân
            print(f"📄 Trang 5: Giấy tờ - {ID_TYPE.upper()} - {ID_NUMBER}")
            radios = page.locator('[role="radio"]').all()
            if ID_TYPE == "passport":
                radios[0].click()  # Hộ chiếu
            else:
                radios[1].click()  # CMND-CCCD
            time.sleep(0.5)
            page.locator('input[type="text"]').first.fill(ID_NUMBER)
            time.sleep(0.3)
            click_next(page)
            time.sleep(2)
            
            # Trang 6: Giới tính
            print(f"📄 Trang 6: Giới tính - {GENDER.upper()}")
            radios = page.locator('[role="radio"]').all()
            if GENDER == "nam":
                radios[0].click()
            else:
                radios[1].click()
            time.sleep(0.3)
            click_next(page)
            time.sleep(2)
            
            # Trang 7: Quốc tịch
            print(f"📄 Trang 7: Quốc tịch - {NATIONALITY.upper()}")
            radios = page.locator('[role="radio"]').all()
            if NATIONALITY == "vietnam":
                radios[0].click()
            else:
                radios[1].click()
            time.sleep(0.3)
            click_next(page)
            time.sleep(2)
            
            # Trang 8: Số điện thoại
            print(f"📄 Trang 8: Số điện thoại - {PHONE}")
            page.locator('input[type="text"]').first.fill(PHONE)
            time.sleep(0.3)
            click_next(page)
            time.sleep(2)
            
            # Trang 9: Thông báo ngày sinh
            print("📄 Trang 9: Thông báo ngày sinh")
            click_next(page)
            time.sleep(2)
            
            # Trang 10: Thông tin bổ sung (bỏ qua)
            print("📄 Trang 10: Thông tin bổ sung (bỏ qua)")
            click_next(page)
            time.sleep(2)
            
            # Trang 11: Cam kết
            print("📄 Trang 11: Cam kết")
            page.locator('[role="radio"]').first.click()
            time.sleep(0.3)
            click_next(page)
            time.sleep(2)
            
            # Trang 12: Xác thực
            print("\n" + "="*60)
            print("✅ HOÀN TẤT! Đã điền đến trang 12")
            print("="*60)
            print("\n⚠️  BÂY GIỜ BẠN CẦN:")
            print("1️⃣  Điền câu hỏi xác thực (nó thay đổi mỗi lần)")
            print("2️⃣  Kiểm tra lại thông tin")
            print("3️⃣  Nhấn nút 'Gửi' để submit form")
            print("\n💡 Browser sẽ mở cho bạn hoàn tất bước cuối.\n")
            
            # Giữ browser mở để user tự submit
            input("⏸️  Nhấn Enter sau khi bạn đã submit xong...")
            
        except Exception as e:
            print(f"\n❌ LỖI: {e}")
            print("\n💡 Đừng lo! Browser vẫn đang mở.")
            print("   Bạn có thể tiếp tục điền thủ công từ trang hiện tại.\n")
            input("⏸️  Nhấn Enter để đóng browser...")
        
        finally:
            browser.close()
            print("\n✅ Đã đóng browser. Chúc bạn thi tốt! 🎉\n")

def click_next(page):
    """Click nút Tiếp"""
    buttons = page.locator('[role="button"]').all()
    for btn in buttons:
        if 'Tiếp' in btn.inner_text():
            btn.click()
            return
    raise Exception("Không tìm thấy nút 'Tiếp'")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🎯 HSK FORM AUTO-FILLER")
    print("="*60)
    print(f"\n📋 Thông tin sẽ điền:")
    print(f"   Họ tên: {FULL_NAME}")
    print(f"   Loại giấy tờ: {ID_TYPE.upper()}")
    print(f"   Số giấy tờ: {ID_NUMBER}")
    print(f"   Giới tính: {GENDER.upper()}")
    print(f"   Quốc tịch: {NATIONALITY.upper()}")
    print(f"   SĐT: {PHONE}")
    print("\n⚠️  Kiểm tra kỹ thông tin trên!")
    
    confirm = input("\n▶️  Nhấn Enter để bắt đầu (hoặc Ctrl+C để hủy)... ")
    
    fill_form()
