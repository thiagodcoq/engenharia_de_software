function toggleModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.toggle('hidden');
    }
}

// Fecha qualquer modal ativo se o usuário clicar no background escuro (overlay)
window.addEventListener('click', function(event) {
    const overlays = document.querySelectorAll('.modal-overlay');
    overlays.forEach(overlay => {
        if (event.target === overlay) {
            overlay.classList.add('hidden');
        }
    });
});

// Desaparecimento automático de alertas (Flash Toasts)
document.addEventListener('DOMContentLoaded', () => {
    const toasts = document.querySelectorAll('.toast');
    toasts.forEach(toast => {
        setTimeout(() => {
            toast.style.opacity = '0';
            setTimeout(() => toast.remove(), 300);
        }, 3500);
    });
});