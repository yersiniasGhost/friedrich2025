// Common JavaScript functionality
document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle (already in navbar.html)
    
    // Close flash messages
    document.querySelectorAll('.alert button').forEach(button => {
        button.addEventListener('click', function() {
            this.parentElement.style.display = 'none';
        });
    });
    
    // Additional interactive functionality can be added here
});
