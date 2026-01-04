// ==UserScript==
// @name         HSK Form Auto Fill
// @namespace    http://tampermonkey.net/
// @version      1.5
// @description  Tự động điền form đăng ký thi HSK/HSKK - SIÊU NHANH!
// @author       Le Duc Anh
// @homepage     https://github.com/leducanh
// @match        *://docs.google.com/forms/*
// @match        *://forms.gle/*
// @run-at       document-end
// @license      MIT
// ==/UserScript==

/*
 * ╔═══════════════════════════════════════════════════════════════╗
 * ║                                                               ║
 * ║   🎯 HSK FORM AUTO FILL TOOL                                  ║
 * ║                                                               ║
 * ║   Created by: LE DUC ANH                                      ║
 * ║   Date: January 2026                                          ║
 * ║   Version: 1.5                                                ║
 * ║                                                               ║
 * ║   📧 Email: leducanhbvh0@gmail.com                            ║
 * ║                                                               ║
 * ║   Công cụ tự động điền form đăng ký thi HSK/HSKK              ║
 * ║   Tiết kiệm thời gian, đăng ký nhanh chóng!                   ║
 * ║                                                               ║
 * ╚═══════════════════════════════════════════════════════════════╝
 */

(function () {
    'use strict';

    // THÔNG TIN - SỬA Ở ĐÂY!
    const INFO = {
        fullName: "LE DUC ANH",
        idType: "cmnd",
        idNumber: "075205017934",
        gender: "nam",
        nationality: "vietnam",
        phone: "0347384670",

        // ⚡ CẤP ĐỘ THI - Sửa text này cho đúng với form chính thức!
        // Ví dụ: "MÔ PHỎNG", "HSK5", "HSK5 + HSKK 高级", "HSK4", v.v.
        examLevel: "HSK 5 + HSKK 高级: 1.900.000đ"
    };

    const sleep = ms => new Promise(r => setTimeout(r, ms));

    const clickNext = () => {
        for (const b of document.querySelectorAll('[role="button"]')) {
            if (b.textContent.includes('Tiếp')) { b.click(); return true; }
        }
        return false;
    };

    // Tìm và click radio theo text
    const clickRadioByText = (text) => {
        const radios = document.querySelectorAll('[role="radio"]');
        for (const r of radios) {
            if (r.textContent.includes(text) || r.getAttribute('aria-label')?.includes(text)) {
                r.click();
                return true;
            }
        }
        return false;
    };

    const clickRadio = i => {
        const r = document.querySelectorAll('[role="radio"]');
        if (r[i]) { r[i].click(); return true; }
        return false;
    };

    const fill = v => {
        const inp = document.querySelector('input[type="text"]');
        if (inp) {
            inp.value = v;
            inp.dispatchEvent(new Event('input', { bubbles: true }));
            inp.dispatchEvent(new Event('change', { bubbles: true }));
            return true;
        }
        return false;
    };

    async function run() {
        const page = parseInt(localStorage.getItem('hsk_page') || '0');
        if (page === 0) return; // Chưa bắt đầu

        await sleep(300);
        console.log('HSK: Trang', page);

        try {
            if (page === 1) {
                const cb = document.querySelector('[role="checkbox"]');
                if (cb && cb.getAttribute('aria-checked') !== 'true') cb.click();
                await sleep(50);
                localStorage.setItem('hsk_page', '2');
                clickNext();
            }
            else if (page === 2) {
                localStorage.setItem('hsk_page', '3');
                clickNext();
            }
            else if (page === 3) {
                await sleep(150);
                // Tìm và click cấp độ thi theo text
                if (!clickRadioByText(INFO.examLevel)) {
                    // Nếu không tìm thấy, thử click radio đầu tiên
                    clickRadio(0);
                }
                await sleep(100);
                localStorage.setItem('hsk_page', '4');
                clickNext();
            }
            else if (page === 4) {
                fill(INFO.fullName);
                await sleep(50);
                localStorage.setItem('hsk_page', '5');
                clickNext();
            }
            else if (page === 5) {
                await sleep(100);
                clickRadio(INFO.idType === 'passport' ? 0 : 1);
                await sleep(150);
                // Sau khi chọn loại giấy tờ, ô input mới xuất hiện
                const inp = document.querySelector('input[type="text"]');
                if (inp) {
                    inp.value = '';
                    inp.focus();
                    inp.value = INFO.idNumber;
                    inp.dispatchEvent(new Event('input', { bubbles: true }));
                    inp.dispatchEvent(new Event('change', { bubbles: true }));
                }
                await sleep(100);
                localStorage.setItem('hsk_page', '6');
                clickNext();
            }
            else if (page === 6) {
                clickRadio(INFO.gender === 'nam' ? 0 : 1);
                await sleep(50);
                localStorage.setItem('hsk_page', '7');
                clickNext();
            }
            else if (page === 7) {
                clickRadio(INFO.nationality === 'vietnam' ? 0 : 1);
                await sleep(50);
                localStorage.setItem('hsk_page', '8');
                clickNext();
            }
            else if (page === 8) {
                fill(INFO.phone);
                await sleep(50);
                localStorage.setItem('hsk_page', '9');
                clickNext();
            }
            else if (page === 9 || page === 10) {
                localStorage.setItem('hsk_page', String(page + 1));
                clickNext();
            }
            else if (page === 11) {
                clickRadio(0);
                await sleep(200);
                localStorage.setItem('hsk_page', '12');
                clickNext();
            }
            else if (page >= 12) {
                localStorage.removeItem('hsk_page');
                console.log('HSK: ✅ Hoàn tất!');
            }
        } catch (e) {
            console.error('HSK Error:', e);
        }
    }

    // Chỉ tạo nút START ở trang đầu tiên (chưa bắt đầu)
    const page = parseInt(localStorage.getItem('hsk_page') || '0');

    if (page === 0) {
        // Tạo nút START nhỏ gọn
        const btn = document.createElement('button');
        btn.textContent = '🚀 START';
        btn.style.cssText = 'position:fixed;top:10px;right:10px;z-index:99999;padding:10px 20px;background:#667eea;color:#fff;border:none;border-radius:8px;font-weight:bold;cursor:pointer;';
        document.body.appendChild(btn);

        btn.onclick = () => {
            localStorage.setItem('hsk_page', '1');
            btn.remove();
            run();
        };
    } else {
        // Đang giữa chừng - tự động tiếp tục
        run();
    }
})();
