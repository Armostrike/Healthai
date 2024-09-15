function scrollToSection(id) {
    const section = document.getElementById(id);
    section.scrollIntoView({
        behavior: 'smooth'
    });
}

document.getElementById('contact-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const message = document.getElementById('message').value;

    // Mock response
    document.getElementById('form-response').textContent = 'Thank you for reaching out, ' + name + '! We will get back to you soon.';

    // In a real application, you would handle form submission here (e.g., using AJAX).
});

window.addEventListener('scroll', function() {
    const header = document.querySelector('header');
    if (window.scrollY > 50) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});