document.addEventListener("DOMContentLoaded", function () {
    // Ensure forms are validated before submission
    const forms = document.querySelectorAll("form");
    forms.forEach((form) => {
        form.addEventListener("submit", function (event) {
            let isValid = true;
            const inputs = form.querySelectorAll("input");
            
            inputs.forEach((input) => {
                if (!input.value.trim()) {
                    isValid = false;
                    alert("Please fill out all fields.");
                }
            });

            if (!isValid) {
                event.preventDefault(); // Prevent form submission if invalid
            }
        });
    });

    // Show/hide password toggle
    const passwordFields = document.querySelectorAll("input[type='password']");
    passwordFields.forEach((passwordField) => {
        let toggleBtn = document.createElement("button");
        toggleBtn.textContent = "👁";
        toggleBtn.style.marginLeft = "10px";
        toggleBtn.style.cursor = "pointer";

        toggleBtn.addEventListener("click", function (e) {
            e.preventDefault();
            if (passwordField.type === "password") {
                passwordField.type = "text";
                toggleBtn.textContent = "🙈";
            } else {
                passwordField.type = "password";
                toggleBtn.textContent = "👁";
            }
        });

        passwordField.parentNode.insertBefore(toggleBtn, passwordField.nextSibling);
    });

    // Smooth scroll for page navigation
    const smoothScrollLinks = document.querySelectorAll("a[href^='#']");
    smoothScrollLinks.forEach((link) => {
        link.addEventListener("click", function (e) {
            e.preventDefault();
            const targetId = this.getAttribute("href").substring(1);
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({ behavior: "smooth" });
            }
        });
    });
});
