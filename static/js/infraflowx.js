/**
 * InfraFlowX Enterprise JavaScript Core
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Sidebar Mobile Toggle
    const sidebarToggle = document.getElementById('sidebarToggle');
    const appSidebar = document.querySelector('.app-sidebar');
    
    if (sidebarToggle && appSidebar) {
        sidebarToggle.addEventListener('click', (e) => {
            e.stopPropagation();
            appSidebar.classList.toggle('show');
        });

        document.addEventListener('click', (e) => {
            if (window.innerWidth < 992 && !appSidebar.contains(e.target) && !sidebarToggle.contains(e.target)) {
                appSidebar.classList.remove('show');
            }
        });
    }

    // 2. Initialize Bootstrap Tooltips & Popovers
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));

    // 3. Auto-dismiss Alert Toasts after 5 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alert => {
        setTimeout(() => {
            try {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            } catch (err) {}
        }, 6000);
    });

    // 4. Global Search Keyboard Shortcut (Ctrl + / or Cmd + /)
    document.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === '/') {
            e.preventDefault();
            const searchInput = document.getElementById('globalSearchInput');
            if (searchInput) searchInput.focus();
        }
    });

    // 5. CSRF Helper for AJAX Requests
    window.getCookie = function(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    };

    window.csrfFetch = function(url, options = {}) {
        const csrftoken = window.getCookie('csrftoken');
        const defaultHeaders = {
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json'
        };
        options.headers = { ...defaultHeaders, ...options.headers };
        return fetch(url, options);
    };
});
