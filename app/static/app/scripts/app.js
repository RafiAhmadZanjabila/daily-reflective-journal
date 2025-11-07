document.addEventListener('DOMContentLoaded', () => {
    const greetingElement = document.getElementById('greeting');
    if (greetingElement && typeof firstName !== 'undefined') {
        const now = new Date();
        const hour = now.getHours();
        let greeting;

        if (hour < 12 && hour >= 5) {
            greeting = 'Good morning';
        } else if (hour < 18 && hour >= 12) {
            greeting = 'Good afternoon';
        } else {
            greeting = 'Good evening';
        }

        greetingElement.textContent = `${greeting}, ${firstName}`;
    }
});
