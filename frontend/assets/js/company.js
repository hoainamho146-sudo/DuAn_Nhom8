/* ============================================
   COMPANY JAVASCRIPT - Logic giao diện doanh nghiệp & tuyển dụng
   Nhóm 8 - Dự án tuyển dụng (TV2)
   ============================================ */

document.addEventListener('DOMContentLoaded', function () {
  initSidebarToggle();
  initCompanyProfileForm();
  initNotifications();
});

/**
 * Responsive Sidebar Toggle for mobile/tablet
 */
function initSidebarToggle() {
  const sidebar = document.getElementById('sidebar');
  const toggleBtn = document.getElementById('sidebarToggle');

  if (toggleBtn && sidebar) {
    toggleBtn.addEventListener('click', () => {
      sidebar.classList.toggle('open');
    });
  }

  // Close when clicking outside on mobile
  document.addEventListener('click', (e) => {
    if (sidebar && sidebar.classList.contains('open')) {
      if (!sidebar.contains(e.target) && !toggleBtn.contains(e.target)) {
        sidebar.classList.remove('open');
      }
    }
  });
}

/**
 * Handle Company Profile Edit Form (in dashboard.html)
 */
function initCompanyProfileForm() {
  const editCompanyForm = document.getElementById('editCompanyForm');
  if (!editCompanyForm) return;

  editCompanyForm.addEventListener('submit', function (e) {
    e.preventDefault();

    // Collect updated data
    const updatedData = {
      name: document.getElementById('companyNameInput')?.value || 'TechViet Solutions',
      taxCode: document.getElementById('companyTaxInput')?.value || '0123456789',
      industry: document.getElementById('companyIndustryInput')?.value || 'Công nghệ thông tin',
      size: document.getElementById('companySizeInput')?.value || '50-100 nhân viên',
      email: document.getElementById('companyEmailInput')?.value || 'contact@techviet.vn',
      phone: document.getElementById('companyPhoneInput')?.value || '028-1234-5678',
      address: document.getElementById('companyAddressInput')?.value || '123 Nguyễn Huệ, Quận 1, TP.HCM',
      website: document.getElementById('companyWebsiteInput')?.value || 'www.techviet.vn',
      description: document.getElementById('companyDescInput')?.value || ''
    };

    // Update UI elements in profile card if present
    const nameEl = document.getElementById('displayCompanyName');
    if (nameEl) nameEl.textContent = updatedData.name;

    const emailEl = document.getElementById('displayCompanyEmail');
    if (emailEl) emailEl.textContent = updatedData.email;

    const phoneEl = document.getElementById('displayCompanyPhone');
    if (phoneEl) phoneEl.textContent = updatedData.phone;

    const addressEl = document.getElementById('displayCompanyAddress');
    if (addressEl) addressEl.textContent = updatedData.address;

    const websiteEl = document.getElementById('displayCompanyWebsite');
    if (websiteEl) websiteEl.textContent = updatedData.website;

    // Close modal
    closeModal('companyEditModal');

    // Show Toast
    showToast('Thành công', 'Thông tin doanh nghiệp đã được cập nhật!', 'success');
  });
}

/**
 * Generic Modal Helpers
 */
function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
  }
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.remove('active');
    document.body.style.overflow = '';
  }
}

// Close modal when clicking outside modal content
document.addEventListener('click', function (e) {
  if (e.target.classList.contains('modal-overlay')) {
    e.target.classList.remove('active');
    document.body.style.overflow = '';
  }
});

/**
 * Toast Notification System
 */
function showToast(title, message, type = 'info') {
  let toastContainer = document.getElementById('toastContainer');
  if (!toastContainer) {
    toastContainer = document.createElement('div');
    toastContainer.id = 'toastContainer';
    toastContainer.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      z-index: 9999;
      display: flex;
      flex-direction: column;
      gap: 10px;
    `;
    document.body.appendChild(toastContainer);
  }

  const toast = document.createElement('div');
  const colors = {
    success: { bg: '#10b981', border: '#059669', icon: 'fa-check-circle' },
    error: { bg: '#ef4444', border: '#dc2626', icon: 'fa-exclamation-circle' },
    warning: { bg: '#f59e0b', border: '#d97706', icon: 'fa-exclamation-triangle' },
    info: { bg: '#3b82f6', border: '#2563eb', icon: 'fa-info-circle' }
  };
  const color = colors[type] || colors.info;

  toast.style.cssText = `
    background: #ffffff;
    border-left: 4px solid ${color.border};
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    padding: 12px 18px;
    border-radius: 6px;
    min-width: 280px;
    max-width: 360px;
    display: flex;
    align-items: center;
    gap: 12px;
    animation: slideIn 0.3s ease forwards;
  `;

  toast.innerHTML = `
    <i class="fas ${color.icon}" style="color: ${color.bg}; font-size: 20px;"></i>
    <div style="flex: 1;">
      <div style="font-weight: 600; font-size: 13.5px; color: #1e293b;">${title}</div>
      <div style="font-size: 12px; color: #64748b; margin-top: 2px;">${message}</div>
    </div>
  `;

  toastContainer.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(20px)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

function initNotifications() {
  // Global notification listener if needed
}
