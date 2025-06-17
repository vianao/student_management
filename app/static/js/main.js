// 通用的API调用函数
async function apiCall(method, url, data = null) {
    try {
        const config = {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            }
        };
        
        if (data) {
            config.body = JSON.stringify(data);
        }
        
        const response = await fetch(url, config);
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.message || '操作失败');
        }
        
        return result;
    } catch (error) {
        showError(error.message);
        throw error;
    }
}

// 显示错误信息
function showError(message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-danger alert-dismissible fade show';
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.querySelector('.container').insertBefore(
        alertDiv,
        document.querySelector('.container').firstChild
    );

    // 3秒后自动关闭
    setTimeout(() => {
        alertDiv.remove();
    }, 3000);
}

// 显示成功信息
function showSuccess(message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-success alert-dismissible fade show';
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.querySelector('.container').insertBefore(
        alertDiv,
        document.querySelector('.container').firstChild
    );

    // 3秒后自动关闭
    setTimeout(() => {
        alertDiv.remove();
    }, 3000);
}

// 移动端导航栏管理
class MobileNavigation {
    constructor() {
        this.sidebarToggle = document.getElementById('sidebarToggle');
        this.sidebar = document.querySelector('.sidebar');
        this.content = document.querySelector('.content');
        this.init();
    }

    init() {
        this.setupSidebarToggle();
        this.setupContentClick();
        this.setupSidebarClick();
        this.setupResizeHandler();
    }

    setupSidebarToggle() {
        if (this.sidebarToggle && this.sidebar) {
            this.sidebarToggle.addEventListener('click', (e) => {
                e.stopPropagation();
                this.sidebar.classList.toggle('show');
            });
        }
    }

    setupContentClick() {
        if (this.content && this.sidebar) {
            this.content.addEventListener('click', () => {
                if (window.innerWidth <= 768 && this.sidebar.classList.contains('show')) {
                    this.sidebar.classList.remove('show');
                }
            });
        }
    }

    setupSidebarClick() {
        if (this.sidebar) {
            this.sidebar.addEventListener('click', (e) => {
                e.stopPropagation();
            });
        }
    }

    setupResizeHandler() {
        window.addEventListener('resize', () => {
            if (window.innerWidth > 768 && this.sidebar) {
                this.sidebar.classList.remove('show');
            }
        });
    }
}

// 通用删除确认
function confirmDelete(url, name) {
    return Swal.fire({
        title: '确认删除',
        text: `确定要删除 ${name} 吗？`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#dc3545',
        cancelButtonColor: '#6c757d',
        confirmButtonText: '确定删除',
        cancelButtonText: '取消'
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = url;
        }
        return false;
    });
}

// 表单验证
class FormValidator {
    static init() {
        const forms = document.querySelectorAll('.needs-validation');
        Array.from(forms).forEach(form => {
            form.addEventListener('submit', event => {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    }
}

// 自动隐藏提示消息
class AlertManager {
    static init(timeout = 5000) {
        setTimeout(() => {
            const alerts = document.querySelectorAll('.alert');
            alerts.forEach(alert => {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            });
        }, timeout);
    }
}

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    new MobileNavigation();
    FormValidator.init();
    AlertManager.init();
});

// 格式化日期
function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// 表单验证
function validateForm(form) {
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            isValid = false;
            field.classList.add('is-invalid');
            
            // 添加错误提示
            let errorDiv = field.nextElementSibling;
            if (!errorDiv || !errorDiv.classList.contains('invalid-feedback')) {
                errorDiv = document.createElement('div');
                errorDiv.className = 'invalid-feedback';
                errorDiv.textContent = '此字段是必填的';
                field.parentNode.insertBefore(errorDiv, field.nextSibling);
            }
        } else {
            field.classList.remove('is-invalid');
            
            // 移除错误提示
            const errorDiv = field.nextElementSibling;
            if (errorDiv && errorDiv.classList.contains('invalid-feedback')) {
                errorDiv.remove();
            }
        }
    });
    
    return isValid;
}

// 清除表单验证状态
function clearFormValidation(form) {
    form.querySelectorAll('.is-invalid').forEach(field => {
        field.classList.remove('is-invalid');
        
        // 移除错误提示
        const errorDiv = field.nextElementSibling;
        if (errorDiv && errorDiv.classList.contains('invalid-feedback')) {
            errorDiv.remove();
        }
    });
}

// 重置表单
function resetForm(form) {
    form.reset();
    clearFormValidation(form);
} 