document.addEventListener('DOMContentLoaded', () => {
    const prevButton = document.getElementById('prevButton');
    const nextButton = document.getElementById('nextButton');

    // The current page and query are passed as data attributes
    const currentPage = parseInt(prevButton.dataset.page);
    const query = prevButton.dataset.query;

    prevButton.addEventListener('click', function () {
        if (currentPage > 1) {
            window.location.href = `/data?query=${query}&page=${currentPage - 1}`;
        }
    });

    nextButton.addEventListener('click', function () {
        window.location.href = `/data?query=${query}&page=${currentPage + 1}`;
    });
})