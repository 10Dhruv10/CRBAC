// Add event listener for file input validation
document.addEventListener('DOMContentLoaded', function() {
    const videoInput = document.querySelector('input[type="file"]');
    if (videoInput) {
        videoInput.addEventListener('change', function() {
            const file = this.files[0];
            const fileSize = file.size / 1024 / 1024; // Convert to MB
            if (fileSize > 100) {
                alert('File size should not exceed 100MB');
                this.value = '';
            }
        });
    }
});