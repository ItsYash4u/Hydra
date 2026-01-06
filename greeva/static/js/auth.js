function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', function () {
    const csrftoken = getCookie('csrftoken');

    // --- UTILS ---
    function checkFormValidity(formId, btnId) {
        const form = document.getElementById(formId);
        const btn = document.getElementById(btnId);
        if (!form || !btn) return;

        const inputs = form.querySelectorAll('input:required, select:required');

        function validate() {
            let isValid = true;
            inputs.forEach(input => {
                const val = input.value.trim();
                const isCheckbox = input.type === 'checkbox';
                if ((!isCheckbox && !val) || (isCheckbox && !input.checked)) {
                    isValid = false;
                }
            });
            // Specific check for password match in signup
            if (formId === 'signupForm') {
                const p1 = document.getElementById('signupPassword').value;
                const p2 = document.getElementById('signupConfirmPassword').value;
                if (p1 && p2 && p1 !== p2) isValid = false;
            }

            btn.disabled = !isValid;
        }

        inputs.forEach(input => {
            input.addEventListener('input', validate);
            input.addEventListener('change', validate);
        });

        // Initial check
        validate();
    }

    // Initialize disabling
    checkFormValidity('signupForm', 'signupBtn');
    checkFormValidity('loginForm', 'loginBtn');
    // --- SIGNUP LOGIC ---
    const signupForm = document.getElementById('signupForm');
    if (signupForm) {
        signupForm.addEventListener('submit', function (e) {
            e.preventDefault();

            const password = document.getElementById('signupPassword').value;
            const confirmPassword = document.getElementById('signupConfirmPassword').value;
            const passwordError = document.getElementById('passwordError');

            if (password !== confirmPassword) {
                document.getElementById('signupConfirmPassword').classList.add('is-invalid');
                passwordError.style.display = 'block';
                return;
            } else {
                document.getElementById('signupConfirmPassword').classList.remove('is-invalid');
                passwordError.style.display = 'none';
            }

            const data = {
                name: document.getElementById('signupName').value,
                email: document.getElementById('signupEmail').value,
                user_type: document.getElementById('signupUserType').value,
                password: password
            };

            const btn = document.getElementById('signupBtn');
            const originalBtnText = btn.innerText;
            btn.innerText = 'Signing up...';
            btn.disabled = true;

            fetch('/api/auth/signup/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify(data)
            })
                .then(response => response.json().then(data => ({ status: response.status, body: data })))
                .then(res => {
                    btn.innerText = originalBtnText;
                    // Don't re-enable if success, we are switching modals
                    if (res.status === 201) {
                        const signupModalEl = document.getElementById('signupModal');
                        const signupModal = bootstrap.Modal.getInstance(signupModalEl);
                        signupModal.hide();

                        document.getElementById('otpEmailSpan').innerText = res.body.email;

                        const otpModal = new bootstrap.Modal(document.getElementById('otpModal'));
                        otpModal.show();

                        startOtpTimer();
                    } else {
                        btn.disabled = false;
                        alert(res.body.error || 'Signup failed');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    btn.innerText = originalBtnText;
                    btn.disabled = false;
                    alert('An error occurred. Please try again.');
                });
        });
    }

    // --- LOGIN LOGIC ---
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        const loginBtn = document.getElementById('loginBtn'); // ID needs to be added to HTML

        loginForm.addEventListener('submit', function (e) {
            e.preventDefault();

            const email = document.getElementById('loginEmail').value;
            const password = document.getElementById('loginPassword').value;

            const data = { email, password };

            // Visual feedback
            const btn = loginForm.querySelector('button[type="submit"]');
            const originalText = btn.innerText;
            btn.innerText = "Verifying...";
            btn.disabled = true;

            fetch('/api/auth/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify(data)
            })
                .then(response => response.json().then(data => ({ status: response.status, body: data })))
                .then(res => {
                    btn.innerText = originalText;

                    if (res.status === 200) {
                        // Success, show OTP modal
                        const loginModalEl = document.getElementById('loginModal');
                        const loginModal = bootstrap.Modal.getInstance(loginModalEl);
                        loginModal.hide();

                        document.getElementById('otpEmailSpan').innerText = res.body.email;

                        const otpModal = new bootstrap.Modal(document.getElementById('otpModal'));
                        otpModal.show();

                        startOtpTimer();
                    } else {
                        btn.disabled = false;
                        alert(res.body.error || 'Login failed');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    btn.innerText = originalText;
                    btn.disabled = false;
                    alert('An error occurred.');
                });
        });
    }

    // --- OTP LOGIC ---
    const otpForm = document.getElementById('otpForm');
    if (otpForm) {
        otpForm.addEventListener('submit', function (e) {
            e.preventDefault();

            // Trim whitespace!
            const otp = document.getElementById('otpInput').value.trim();
            const email = document.getElementById('otpEmailSpan').innerText;

            const btn = otpForm.querySelector('button[type="submit"]');
            btn.disabled = true;
            btn.innerText = "Checking...";

            fetch('/api/auth/verify-otp/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({ email, otp })
            })
                .then(response => response.json().then(data => ({ status: response.status, body: data })))
                .then(res => {
                    if (res.status === 200) {
                        window.location.href = res.body.redirect_url;
                    } else {
                        btn.disabled = false;
                        btn.innerText = "Verify";
                        alert(res.body.error || 'Invalid OTP');
                    }
                })
                .catch(error => {
                    console.error(error);
                    btn.disabled = false;
                    btn.innerText = "Verify";
                    alert('Error verifying OTP');
                });
        });
    }

    // --- OTP TIMER ---
    let timerInterval;
    function startOtpTimer() {
        let timeLeft = 120; // 2 minutes
        const timerDisplay = document.getElementById('otpTimer');
        const resendLink = document.getElementById('resendLink');

        resendLink.classList.add('disabled');
        resendLink.style.pointerEvents = 'none';

        if (timerInterval) clearInterval(timerInterval);

        timerInterval = setInterval(() => {
            const minutes = Math.floor(timeLeft / 60);
            let seconds = timeLeft % 60;
            seconds = seconds < 10 ? '0' + seconds : seconds;

            timerDisplay.innerText = `0${minutes}:${seconds}`;

            if (timeLeft <= 0) {
                clearInterval(timerInterval);
                resendLink.classList.remove('disabled');
                resendLink.style.pointerEvents = 'auto';
                timerDisplay.innerText = "00:00";
            }
            timeLeft -= 1;
        }, 1000);
    }

    // --- RESEND OTP ---
    const resendLink = document.getElementById('resendLink');
    if (resendLink) {
        resendLink.addEventListener('click', function (e) {
            e.preventDefault();
            const email = document.getElementById('otpEmailSpan').innerText;

            fetch('/api/auth/resend-otp/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({ email })
            })
                .then(res => {
                    if (res.ok) {
                        startOtpTimer();
                        alert('OTP resent!');
                    } else {
                        alert('Failed to resend OTP');
                    }
                });
        });
    }

});
