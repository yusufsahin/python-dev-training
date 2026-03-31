document.addEventListener("submit", (event) => {
    const form = event.target;
    if (!(form instanceof HTMLFormElement)) {
        return;
    }

    if (form.classList.contains("danger-form")) {
        const confirmed = window.confirm("Are you sure you want to delete this record?");
        if (!confirmed) {
            event.preventDefault();
        }
    }
});
