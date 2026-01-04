// Auto-fill tool script
const generateBtn = document.getElementById('generateBtn');
const copyBtn = document.getElementById('copyBtn');
const codeOutput = document.getElementById('codeOutput');

// Generate auto-fill code
generateBtn.addEventListener('click', () => {
    // Get form values
    const fullName = document.getElementById('fullName').value.trim();
    const idType = document.querySelector('input[name="idType"]:checked').value;
    const idNumber = document.getElementById('idNumber').value.trim();
    const gender = document.querySelector('input[name="gender"]:checked').value;
    const nationality = document.querySelector('input[name="nationality"]:checked').value;
    const phone = document.getElementById('phone').value.trim();

    // Optional fields
    const studyDuration = document.getElementById('studyDuration').value;
    const purpose = document.getElementById('purpose').value;
    const method = document.getElementById('method').value;

    // Validate required fields
    if (!fullName || !idNumber || !phone) {
        alert('⚠️ Vui lòng điền đầy đủ các trường bắt buộc (*)');
        return;
    }

    // Check if name is uppercase without diacritics
    if (fullName !== fullName.toUpperCase()) {
        alert('⚠️ Họ tên phải viết IN HOA');
        return;
    }

    // Generate the JavaScript code
    const code = generateAutoFillCode({
        fullName,
        idType,
        idNumber,
        gender,
        nationality,
        phone,
        studyDuration,
        purpose,
        method
    });

    // Display code
    codeOutput.textContent = code;
    copyBtn.disabled = false;

    // Visual feedback
    generateBtn.textContent = '✅ Đã tạo mã!';
    generateBtn.style.background = 'linear-gradient(135deg, #10b981 0%, #059669 100%)';

    setTimeout(() => {
        generateBtn.textContent = '⚡ Tạo mã Auto-Fill';
        generateBtn.style.background = '';
    }, 2000);
});

// Copy code to clipboard
copyBtn.addEventListener('click', async () => {
    const code = codeOutput.textContent;

    try {
        await navigator.clipboard.writeText(code);

        copyBtn.textContent = '✅ Đã copy!';
        copyBtn.classList.add('copied');

        setTimeout(() => {
            copyBtn.textContent = '📋 Copy Code';
            copyBtn.classList.remove('copied');
        }, 2000);
    } catch (err) {
        alert('Lỗi khi copy. Vui lòng copy thủ công.');
    }
});

// Generate the auto-fill JavaScript code
function generateAutoFillCode(data) {
    return `(async function() {
    console.log('🚀 Bắt đầu tự động điền form HSK...');
    
    const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));
    
    const clickNext = () => {
        const buttons = Array.from(document.querySelectorAll('[role="button"]'));
        const nextBtn = buttons.find(b => b.textContent.trim() === 'Tiếp' || b.innerText.trim() === 'Tiếp');
        if (nextBtn) {
            nextBtn.click();
            return true;
        }
        return false;
    };
    
    const clickRadio = (index) => {
        const radios = document.querySelectorAll('[role="radio"]');
        if (radios[index]) {
            radios[index].click();
            return true;
        }
        return false;
    };
    
    const fillInput = (value) => {
        const input = document.querySelector('input[type="text"]');
        if (input) {
            input.value = value;
            input.dispatchEvent(new Event('input', { bubbles: true }));
            input.dispatchEvent(new Event('change', { bubbles: true }));
            input.dispatchEvent(new Event('blur', { bubbles: true }));
            return true;
        }
        return false;
    };
    
    try {
        // Page 1: Email checkbox
        console.log('📄 Trang 1: Email confirmation');
        await sleep(500);
        const emailCheckbox = document.querySelector('[role="checkbox"]');
        if (emailCheckbox && emailCheckbox.getAttribute('aria-checked') !== 'true') {
            emailCheckbox.click();
        }
        await sleep(300);
        clickNext();
        await sleep(2500);
        
        // Page 2: NO SPAM image (just click next)
        console.log('📄 Trang 2: NO SPAM');
        await sleep(500);
        clickNext();
        await sleep(2500);
        
        // Page 3: Exam level - Select "MÔ PHỎNG"
        console.log('📄 Trang 3: Cấp độ thi');
        await sleep(500);
        clickRadio(0); // MÔ PHỎNG option
        await sleep(300);
        clickNext();
        await sleep(2500);
        
        // Page 4: Full name
        console.log('📄 Trang 4: Họ và tên');
        await sleep(500);
        fillInput('${data.fullName}');
        await sleep(300);
        clickNext();
        await sleep(2500);
        
        // Page 5: ID type and number
        console.log('📄 Trang 5: Giấy tờ tùy thân');
        await sleep(500);
        ${data.idType === 'passport' ? 'clickRadio(0); // Passport' : 'clickRadio(1); // CMND-CCCD'}
        await sleep(500);
        fillInput('${data.idNumber}');
        await sleep(300);
        clickNext();
        await sleep(2500);
        
        // Page 6: Gender
        console.log('📄 Trang 6: Giới tính');
        await sleep(500);
        ${data.gender === 'male' ? 'clickRadio(0); // Nam' : 'clickRadio(1); // Nữ'}
        await sleep(300);
        clickNext();
        await sleep(2500);
        
        // Page 7: Nationality
        console.log('📄 Trang 7: Quốc tịch');
        await sleep(500);
        ${data.nationality === 'vietnam' ? 'clickRadio(0); // Việt Nam' : 'clickRadio(1); // Khác'}
        await sleep(300);
        clickNext();
        await sleep(2500);
        
        // Page 8: Phone number
        console.log('📄 Trang 8: Số điện thoại');
        await sleep(500);
        fillInput('${data.phone}');
        await sleep(300);
        clickNext();
        await sleep(2500);
        
        // Page 9: Birth date notice (just click next)
        console.log('📄 Trang 9: Thông báo ngày sinh');
        await sleep(500);
        clickNext();
        await sleep(2500);
        
        // Page 10: Optional background info
        console.log('📄 Trang 10: Thông tin bổ sung (tùy chọn)');
        await sleep(500);
        ${data.studyDuration ? `clickRadio(${data.studyDuration}); await sleep(500);` : '// Skip study duration'}
        ${data.purpose ? `
        const radios10 = document.querySelectorAll('[role="radio"]');
        const purposeStartIndex = ${data.studyDuration ? '5' : '0'};
        if (radios10[purposeStartIndex + ${data.purpose}]) {
            radios10[purposeStartIndex + ${data.purpose}].click();
            await sleep(500);
        }` : '// Skip purpose'}
        ${data.method ? `
        const radios10b = document.querySelectorAll('[role="radio"]');
        const methodStartIndex = ${data.studyDuration && data.purpose ? '10' : data.studyDuration || data.purpose ? '5' : '0'};
        if (radios10b[methodStartIndex + ${data.method}]) {
            radios10b[methodStartIndex + ${data.method}].click();
            await sleep(500);
        }` : '// Skip method'}
        clickNext();
        await sleep(2500);
        
        // Page 11: Commitment
        console.log('📄 Trang 11: Cam kết');
        await sleep(500);
        clickRadio(0); // Agree
        await sleep(300);
        clickNext();
        await sleep(2500);
        
        // Page 12: Xác thực - BẠN TỰ ĐIỀN VÀ SUBMIT
        console.log('✅ Hoàn tất! Vui lòng tự điền câu hỏi xác thực và nhấn Submit.');
        console.log('💡 Câu hỏi xác thực sẽ thay đổi mỗi lần đăng ký.');
        
    } catch (error) {
        console.error('❌ Lỗi:', error);
        alert('Có lỗi xảy ra: ' + error.message);
    }
})();`;
}

// Auto-convert name to uppercase
document.getElementById('fullName').addEventListener('input', function (e) {
    this.value = this.value.toUpperCase();
});
