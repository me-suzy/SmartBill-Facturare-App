// SmartBill JavaScript
console.log('🚀 SmartBill Application Loaded');

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM Content Loaded - Initializing SmartBill');

    // Animații pentru carduri
    animateCards();

    // Actualizare statistici
    if (window.location.pathname === '/dashboard') {
        updateStats();
        setInterval(updateStats, 60000); // Update la fiecare minut
    }

    // Efecte interactive
    addInteractiveEffects();

    // Notificare de bun venit
    showWelcomeNotification();
});

function animateCards() {
    const cards = document.querySelectorAll('.stat-card, .activity-card, .quick-actions');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'all 0.6s ease';

        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 150);
    });
}

function updateStats() {
    fetch('/api/dashboard_stats')
        .then(response => response.json())
        .then(data => {
            console.log('📊 Stats updated:', data);
            updateStatValues(data);
        })
        .catch(error => {
            console.warn('⚠️ Error updating stats:', error);
        });
}

function updateStatValues(stats) {
    const elements = {
        'vanzari': stats.vanzari,
        'sold_clienti': stats.sold_clienti,
        'facturi_neincasate': stats.facturi_neincasate,
        'cheltuieli': stats.cheltuieli
    };

    Object.keys(elements).forEach(key => {
        const element = document.querySelector(`[data-stat="${key}"] .stat-value`);
        if (element) {
            animateValue(element, elements[key]);
        }
    });
}

function animateValue(element, newValue) {
    const currentValue = parseFloat(element.textContent.replace(/[^0-9.]/g, '')) || 0;
    const increment = (newValue - currentValue) / 20;
    let current = currentValue;

    const timer = setInterval(() => {
        current += increment;
        if (Math.abs(current - newValue) < Math.abs(increment)) {
            current = newValue;
            clearInterval(timer);
        }

        if (typeof newValue === 'number' && newValue > 100) {
            element.textContent = current.toFixed(2);
        } else {
            element.textContent = Math.round(current);
        }
    }, 50);
}

function addInteractiveEffects() {
    // Hover effects pentru butoane
    document.querySelectorAll('.btn-primary, .action-btn').forEach(btn => {
        btn.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px) scale(1.02)';
        });

        btn.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });

    // Click effects
    document.querySelectorAll('button, .btn-primary').forEach(btn => {
        btn.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;

            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');

            this.appendChild(ripple);

            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });

    // Adaugă CSS pentru ripple effect
    const style = document.createElement('style');
    style.textContent = `
        .ripple {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.6);
            transform: scale(0);
            animation: ripple-animation 0.6s linear;
            pointer-events: none;
        }

        @keyframes ripple-animation {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }

        button, .btn-primary {
            position: relative;
            overflow: hidden;
        }
    `;
    document.head.appendChild(style);
}

function showWelcomeNotification() {
    // Verifică dacă e prima vizită
    if (!localStorage.getItem('smartbill_visited')) {
        setTimeout(() => {
            if (typeof toastr !== 'undefined') {
                toastr.success('🎉 Bun venit la SmartBill! Aplicația ta de facturare este gata de utilizare.');
            }
            localStorage.setItem('smartbill_visited', 'true');
        }, 2000);
    }
}

// Funcții globale
window.SmartBill = {
    updateStats,
    version: '1.0.0'
};

// Log pentru debugging
console.log('✅ SmartBill JavaScript fully loaded');