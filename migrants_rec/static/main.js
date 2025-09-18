console.log("Frontend loaded. Ready for interactive magic!");

// Example of a simple interactive feature
document.addEventListener('DOMContentLoaded', () => {
    const cards = document.querySelectorAll('.migrant-card');
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.style.opacity = 1;
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
});