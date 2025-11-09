document.addEventListener('DOMContentLoaded', () => {
    const trendListContainer = document.getElementById('trend-list-container');
    const lastUpdatedElement = document.getElementById('last-updated');
    const categoryButtons = document.querySelectorAll('.category-btn');

    let trendsData = {};
    let currentCategory = 'tech_news'; // Default category

    // Function to render the trend list for a given category
    function renderTrends(category) {
        // Clear previous list
        trendListContainer.innerHTML = '';

        const items = trendsData.categories[category];

        if (!items || items.length === 0) {
            trendListContainer.innerHTML = '<p>No trending items found for this category.</p>';
            return;
        }

        items.forEach(item => {
            const trendItemHTML = `
                <div class="trend-item">
                    <a href="${item.source_link}" target="_blank" rel="noopener noreferrer">
                        <div class="trend-rank">#${item.rank}</div>
                        <img src="${item.image}" alt="${item.title}" class="trend-image">
                        <div class="trend-content">
                            <h3>${item.title}</h3>
                            <p>${item.description}</p>
                        </div>
                    </a>
                </div>
            `;
            trendListContainer.insertAdjacentHTML('beforeend', trendItemHTML);
        });
    }

    // Function to fetch the data and initialize the page
    async function initialize() {
        try {
            const response = await fetch('./data/trends.json');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            trendsData = await response.json();
            
            // Update timestamp and render the default category
            lastUpdatedElement.textContent = `Updated: ${trendsData.last_updated}`;
            renderTrends(currentCategory);

        } catch (error) {
            console.error("Could not fetch trend data:", error);
            lastUpdatedElement.textContent = 'Could not load data.';
            trendListContainer.innerHTML = '<p>There was an error fetching the latest trends. Please try again later.</p>';
        }
    }

    // Add click event listeners to category buttons
    categoryButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Update active state
            categoryButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');

            // Render the new category
            currentCategory = button.dataset.category;
            renderTrends(currentCategory);
        });
    });

    // Initial load
    initialize();
});