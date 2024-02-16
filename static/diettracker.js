document.addEventListener('DOMContentLoaded', function () {
    console.log('DOM content loaded');

    const itemNameInput = document.getElementById('item_name');
    console.log('Item name input:', itemNameInput);

    itemNameInput.addEventListener('input', function (event) {
        const searchQuery = event.target.value.trim();
        console.log('Search query:', searchQuery);

        if (searchQuery !== '') {
            searchFood(searchQuery);
        } else {
            clearDropdown();
            clearFormFields();
        }
    });
})

function clearFormFields() {
    document.getElementById('serving_size').value = '';
    document.getElementById('serving_measurement').value = '';
    document.getElementById('calorie_total').value = '';
    document.getElementById('protein').value = '';
    document.getElementById('fat').value = '';
    document.getElementById('carb').value = '';
}

function searchFood(query) {
    const apiKey = '2A3ZTZdTx5O5y605VbLnIxJoNnDB9BJhmnGxM0hy';
    const apiUrl = `https://api.nal.usda.gov/fdc/v1/foods/search?api_key=${apiKey}&query=${encodeURIComponent(query)}&pageSize=100`;

    fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch data');
            }
            return response.json();
        })
        .then(data => {
            console.log('***********************API data:', data); 
            populateDropdown(data.foods);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function populateDropdown(foods) {
    const dropdownMenu = document.getElementById('food-dropdown');
    dropdownMenu.innerHTML = '';

    foods.forEach(food => {
        if(food.brandName){
            const option = document.createElement('option');
        option.value = `${food.description} ${food.fdcId}`;
        option.textContent = `${food.brandName} ${food.description} ${food.fdcId}`; 
        dropdownMenu.appendChild(option);
        }
    });

    dropdownMenu.style.display = 'block';
}

function clearDropdown() {
    const dropdownMenu = document.getElementById('food-dropdown');
    dropdownMenu.innerHTML = '';
    dropdownMenu.style.display = 'none';
}

document.getElementById('food-dropdown').addEventListener('change', function (event) {
    const selectedOption = event.target.value;
    autofillForm(selectedOption);
});

async function autofillForm(selectedOption) {
    const itemNameInput = document.getElementById('item_name');
    itemNameInput.value = selectedOption;

    const fdcId = selectedOption.split(' ').pop(); 

    try {
        const data = await fetchFoodDetails(fdcId);
        console.log('Fetched food details:', data);

        if (data && data.labelNutrients && data.labelNutrients.calories) {
            const servingSizeInput = document.getElementById('serving_size');
            servingSizeInput.value = parseInt(data.servingSize) || 0;

            const servingSizeMeasurementInput = document.getElementById('serving_measurement');
            servingSizeMeasurementInput.value = data.servingSizeUnit || 'NA';

            const calorieTotalInput = document.getElementById('calorie_total');
            calorieTotalInput.value = parseInt(data.labelNutrients.calories.value) || 0;

            const proteinInput = document.getElementById('protein');
            proteinInput.value = parseInt(data.labelNutrients.protein.value) || 0;

            const fatInput = document.getElementById('fat');
            fatInput.value = parseInt(data.labelNutrients.fat.value) || 0;

            const carbInput = document.getElementById('carb');
            carbInput.value = parseInt(data.labelNutrients.carbohydrates.value) || 0;
        } else {
            console.error('Missing or invalid data received:', data);
            clearFormFields();
        }
    } catch (error) {
        console.error('Error fetching food details:', error);
        clearFormFields();
    }
}





function fetchFoodDetails(fdcId) {
    const apiUrl = `https://api.nal.usda.gov/fdc/v1/food/${fdcId}?api_key=2A3ZTZdTx5O5y605VbLnIxJoNnDB9BJhmnGxM0hy`;

    console.log('Fetching food details for fdcId:', fdcId);
    console.log('API URL:', apiUrl);

    return fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                console.error('Failed to fetch food details. Response status:', response.status);
                throw new Error('Failed to fetch food details');
            }
            return response.json();
        })
        .then(data => {
            console.log('Received food details:', data); 
            return data; 
        })
        .catch(error => {
            console.error('Error fetching food details:', error);
            throw error;
        });
}