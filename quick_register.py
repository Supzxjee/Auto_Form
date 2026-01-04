"""
HSK Quick Register - ĐĂNG KÝ CỰC NHANH
Chuẩn bị thông tin trước, khi form mở chỉ việc chạy!
"""
from playwright.sync_api import sync_playwright
import json
import os
import time

CONFIG_FILE = "registration_info.json"

def save_info():
    """Lưu thông tin đăng ký"""
    print("\n" + "="*60)
    print("📝 NHẬP THÔNG TIN ĐĂNG KÝ (chỉ 1 lần)")
    print("="*60)
    
    info = {
        "full_name": input("\n👤 Họ và tên (IN HOA KHÔNG DẤU): ").strip().upper(),
        "id_type": input("📄 Loại giấy tờ (passport/cmnd): ").strip().lower(),
        "id_number": input("🔢 Số giấy tờ: ").strip(),
        "gender": input("⚥  Giới tính (nam/nữ): ").strip().lower(),
        "nationality": input("🌍 Quốc tịch (vietnam/other): ").strip().lower(),
        "phone": input("📱 Số điện thoại: ").strip()
    }
    
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(info, f, ensure_ascii=False, indent=2)
    
    print("\n✅ Đã lưu thông tin vào file:", CONFIG_FILE)
    print("\n💡 Bây giờ khi form chính thức mở, chỉ cần chạy:")
    print("   python quick_register.py")
    print("\n")

def load_info():
    """Đọc thông tin đã lưu"""
    if not os.path.exists(CONFIG_FILE):
        return None
    
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def quick_register():
    """Đăng ký nhanh"""
    info = load_info()
    
    if not info:
        print("\n⚠️  Chưa có thông tin lưu sẵn!")
        print("   Chạy: python quick_register.py --setup")
        return
    
    print("\n" + "="*60)
    print("🚀 ĐĂNG KÝ NHANH")
    print("="*60)
    print(f"\n📋 Thông tin sẽ dùng:")
    print(f"   Họ tên: {info['full_name']}")
    print(f"   Giấy tờ: {info['id_type'].upper()} - {info['id_number']}")
    print(f"   Giới tính: {info['gender'].upper()}")
    print(f"   Quốc tịch: {info['nationality'].upper()}")
    print(f"   SĐT: {info['phone']}")
    
    # Nhập URL form chính thức
    print("\n" + "="*60)
    form_url = input("📎 Paste URL form CHÍNH THỨC vào đây và nhấn Enter:\n   ").strip()
    
    if not form_url:
        print("❌ Chưa nhập URL!")
        return
    
    print("\n🚀 Đang khởi động browser và điền form...")
    print("⏱️  Ước tính: 25-30 giây\n")
    
    with sync_playwright() as p:
        # Launch browser đơn giản, không dùng profile
        browser = p.chromium.launch(
            headless=False,
            args=['--start-maximized']
        )
        page = browser.new_page()
        
        try:
            # Mở form
            print("📄 Đang mở form...")
            page.goto(form_url, timeout=15000)
            time.sleep(3)
            
            # Kiểm tra xem có cần đăng nhập không
            print("\n" + "="*60)
            print("⚠️  QUAN TRỌNG: ĐĂNG NHẬP GOOGLE")
            print("="*60)
            print("\n1️⃣  Nếu browser yêu cầu đăng nhập Google:")
            print("   → Đăng nhập ngay bây giờ trong cửa sổ Chrome vừa mở")
            print("\n2️⃣  Sau khi đăng nhập xong (hoặc đã đăng nhập sẵn):")
            print("   → Quay lại Terminal này")
            print("   → Nhấn Enter để bắt đầu tự động điền\n")
            
            input("⏸️  Nhấn Enter khi đã đăng nhập Google và sẵn sàng...")
            
            print("\n⚡ Bắt đầu tự động điền form...")
            time.sleep(1)
            
            # Helper functions
            def click_next():
                buttons = page.locator('[role="button"]').all()
                for btn in buttons:
                    if 'Tiếp' in btn.inner_text() or 'Next' in btn.inner_text():
                        btn.click()
                        return
            
            def click_radio(index):
                radios = page.locator('[role="radio"]').all()
                if index < len(radios):
                    radios[index].click()
            
            def fill_text(value):
                page.locator('input[type="text"]').first.fill(value)
            
            # Bắt đầu điền form
            print("⚡ Đang tự động điền...")
            
            # Page 1: Email checkbox (nếu có)
            try:
                checkbox = page.locator('[role="checkbox"]').first
                if checkbox.is_visible(timeout=2000):
                    if checkbox.get_attribute('aria-checked') != 'true':
                        checkbox.click()
                        time.sleep(0.3)
                    click_next()
                    time.sleep(2)
                    print("  ✓ Trang 1")
            except:
                pass  # Skip nếu không có
            
            # Page 2: NO SPAM or intro (nếu có)
            try:
                click_next()
                time.sleep(2)
                print("  ✓ Trang 2")
            except:
                pass
            
            # Page 3: Exam level
            try:
                click_radio(0)  # Chọn option đầu tiên
                time.sleep(0.3)
                click_next()
                time.sleep(2)
                print("  ✓ Trang 3: Cấp độ thi")
            except:
                pass
            
            # Page 4: Full name
            fill_text(info['full_name'])
            time.sleep(0.3)
            click_next()
            time.sleep(2)
            print(f"  ✓ Trang 4: Tên - {info['full_name']}")
            
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
            print(f"  ✓ Trang 5: Giấy tờ - {info['id_number']}")
            
            # Page 6: Gender
            if info['gender'] == 'nam':
                click_radio(0)
            else:
                click_radio(1)
            time.sleep(0.3)
            click_next()
            time.sleep(2)
            print(f"  ✓ Trang 6: Giới tính - {info['gender']}")
            
            # Page 7: Nationality
            if info['nationality'] == 'vietnam':
                click_radio(0)
            else:
                click_radio(1)
            time.sleep(0.3)
            click_next()
            time.sleep(2)
            print(f"  ✓ Trang 7: Quốc tịch - {info['nationality']}")
            
            # Page 8: Phone
            fill_text(info['phone'])
            time.sleep(0.3)
            click_next()
            time.sleep(2)
            print(f"  ✓ Trang 8: SĐT - {info['phone']}")
            
            # Page 9: Notice (if any)
            try:
                click_next()
                time.sleep(2)
                print("  ✓ Trang 9")
            except:
                pass
            
            # Page 10: Optional info
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
            
            # Page 12: Verification question
            print("\n" + "="*60)
            print("✅ ĐÃ ĐIỀN ĐẾN TRANG CUỐI!")
            print("="*60)
            print("\n⚠️  BẠN CẦN:")
            print("1️⃣  Điền câu hỏi xác thực")
            print("2️⃣  Kiểm tra lại thông tin")
            print("3️⃣  Nhấn 'Gửi' để hoàn tất")
            print("\n💡 Browser sẽ mở để bạn hoàn tất.\n")
            
            input("⏸️  Nhấn Enter sau khi submit xong...")
            
        except Exception as e:
            print(f"\n❌ Có lỗi: {e}")
            print("💡 Browser vẫn mở, bạn có thể tiếp tục thủ công!\n")
            input("⏸️  Nhấn Enter để đóng...")
        
        finally:
            browser.close()
            print("\n✅ Hoàn tất! Chúc mừng bạn đã đăng ký! 🎉\n")

if __name__ == "__main__":
    import sys
    
    if '--setup' in sys.argv or not os.path.exists(CONFIG_FILE):
        save_info()
    else:
        quick_register()
