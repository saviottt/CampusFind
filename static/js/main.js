// ═══════════════════════════════════════════════════════
//  CAMPUSFIND — MAIN JS
// ═══════════════════════════════════════════════════════

document.addEventListener('DOMContentLoaded', () => {

  // ── Hamburger Menu ───────────────────────────────────
  const hamburger = document.getElementById('hamburger');
  const mobileMenu = document.getElementById('mobileMenu');
  if (hamburger && mobileMenu) {
    hamburger.addEventListener('click', () => {
      mobileMenu.classList.toggle('open');
      const spans = hamburger.querySelectorAll('span');
      const isOpen = mobileMenu.classList.contains('open');
      spans[0].style.transform = isOpen ? 'rotate(45deg) translate(5px, 5px)' : '';
      spans[1].style.opacity = isOpen ? '0' : '1';
      spans[2].style.transform = isOpen ? 'rotate(-45deg) translate(5px, -5px)' : '';
    });
  }

  // ── Auto-dismiss flash messages ──────────────────────
  document.querySelectorAll('.flash').forEach(flash => {
    setTimeout(() => {
      flash.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
      flash.style.opacity = '0';
      flash.style.transform = 'translateX(20px)';
      setTimeout(() => flash.remove(), 400);
    }, 5000);
  });

  // ── Password Strength Indicator ──────────────────────
  const pwd1 = document.getElementById('pwd1');
  const strengthBar = document.getElementById('pwdStrength');
  if (pwd1 && strengthBar) {
    pwd1.addEventListener('input', () => {
      const val = pwd1.value;
      let score = 0;
      if (val.length >= 8) score++;
      if (/[A-Z]/.test(val)) score++;
      if (/[0-9]/.test(val)) score++;
      if (/[^A-Za-z0-9]/.test(val)) score++;
      const colors = ['', '#e74c3c', '#f4a261', '#f1c40f', '#2d6a4f'];
      const widths = ['0%', '25%', '50%', '75%', '100%'];
      strengthBar.style.background = colors[score] || '#e5e5e5';
      strengthBar.style.width = widths[score];
    });
  }

  // ── Confirm password visual match ────────────────────
  const pwd2 = document.getElementById('pwd2');
  if (pwd1 && pwd2) {
    function checkMatch() {
      if (!pwd2.value) return;
      if (pwd1.value === pwd2.value) {
        pwd2.style.borderColor = '#2d6a4f';
      } else {
        pwd2.style.borderColor = '#c1392b';
      }
    }
    pwd1.addEventListener('input', checkMatch);
    pwd2.addEventListener('input', checkMatch);
  }

  // ── Scroll to messages thread ─────────────────────────
  const thread = document.getElementById('msgThread');
  if (thread) {
    thread.scrollTop = thread.scrollHeight;
  }

  // ── Animate stat numbers ──────────────────────────────
  document.querySelectorAll('.stat-number').forEach(el => {
    const target = parseInt(el.textContent) || 0;
    let current = 0;
    const step = Math.ceil(target / 30);
    const timer = setInterval(() => {
      current = Math.min(current + step, target);
      el.textContent = current;
      if (current >= target) clearInterval(timer);
    }, 40);
  });

  // ── Item card hover ripple ────────────────────────────
  document.querySelectorAll('.item-card').forEach(card => {
    card.addEventListener('mouseenter', () => {
      card.style.borderColor = 'var(--primary)';
    });
    card.addEventListener('mouseleave', () => {
      card.style.borderColor = 'var(--border)';
    });
  });

  // ── Form validation feedback ──────────────────────────
  const forms = document.querySelectorAll('form');
  forms.forEach(form => {
    form.addEventListener('submit', (e) => {
      const required = form.querySelectorAll('[required]');
      let valid = true;
      required.forEach(field => {
        if (!field.value.trim()) {
          field.style.borderColor = '#c1392b';
          valid = false;
          field.addEventListener('input', () => {
            field.style.borderColor = '';
          }, { once: true });
        }
      });
      if (!valid) {
        e.preventDefault();
        const firstInvalid = form.querySelector('[required]:invalid, [required][style*="red"]');
        if (firstInvalid) firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    });
  });

});

// ── Password Toggle (global) ──────────────────────────────────
function togglePwd(inputId, btn) {
  const input = document.getElementById(inputId);
  if (!input) return;
  if (input.type === 'password') {
    input.type = 'text';
    btn.textContent = '🙈';
  } else {
    input.type = 'password';
    btn.textContent = '👁';
  }
}
