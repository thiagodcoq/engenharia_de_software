function toggleModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        if (modal.classList.contains('hidden')) {
            modal.classList.remove('hidden');
        } else {
            modal.classList.add('hidden');
        }
    }
}

// Fechar modais ao clicar fora do formulário (no overlay escuro)
window.onclick = function(event) {
    const modais = document.querySelectorAll('[id^="modal-"]');
    modais.forEach(modal => {
        if (event.target === modal) {
            modal.classList.add('hidden');
        }
    });
}

// Auto-destruição dos Toasts após 3.5 segundos
document.addEventListener('DOMContentLoaded', () => {
    const toasts = document.querySelectorAll('.toast');
    toasts.forEach(toast => {
        setTimeout(() => {
            toast.style.opacity = '0';
            setTimeout(() => toast.remove(), 300); // Aguarda a transição css
        }, 3500);
    });
});