function fetchAndDisplayFoodItems() {
    fetch('/get/food-items') 
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const userId = data.user_id;
            displayFoodItems(data.foodItems, userId);
        })
        .catch(error => console.error('Error fetching food items:', error));
}

function createListItem(item, userId) {
    const listItem = document.createElement('li');
    listItem.textContent = `${item.item_name} - ${item.calorie_total} calories`;

    const editLink = document.createElement('a');
    editLink.href = `/${userId}/${item.id}/edit`; // Using item.id here
    const editIcon = document.createElement('i');
    editIcon.classList.add('fa-solid', 'fa-pen');
    editLink.appendChild(editIcon);

    const deleteLink = document.createElement('a');
    deleteLink.href = `/${userId}/${item.id}/delete`; // Using item.id here
    const deleteIcon = document.createElement('i');
    deleteIcon.classList.add('fa-solid', 'fa-trash');
    deleteLink.appendChild(deleteIcon);

    listItem.appendChild(editLink);
    listItem.appendChild(deleteLink);

    return listItem;
}

function displayFoodItems(foodItems, userId) {
    const meals = {
        Breakfast: { items: [], totalCalories: 0 },
        Lunch: { items: [], totalCalories: 0 },
        Dinner: { items: [], totalCalories: 0 },
        Other: { items: [], totalCalories: 0 }
    }; 
    const overallTotal = { totalCalories: 0 }; 

    foodItems.forEach(item => {
        const mealType = item.meal_type;
        if (meals.hasOwnProperty(mealType)) {
            meals[mealType].items.push(item);
            meals[mealType].totalCalories += item.calorie_total;
            overallTotal.totalCalories += item.calorie_total;
        } else {
            meals.Other.items.push(item);
            meals.Other.totalCalories += item.calorie_total;
            overallTotal.totalCalories += item.calorie_total;
        }
    });

    const foodItemsContainer = document.getElementById('food-items-container');
    foodItemsContainer.innerHTML = '';

    const predefinedMealTypes = ['Breakfast', 'Lunch', 'Dinner', 'Other'];
    predefinedMealTypes.forEach(mealType => {
        if (meals[mealType].items.length > 0) {
            const mealSection = document.createElement('div');

            const header = document.createElement('h3');
            header.textContent = mealType;
            mealSection.appendChild(header);

            const itemList = document.createElement('ul');
            meals[mealType].items.forEach(item => {
                const listItem = createListItem(item, userId); // Pass userId and item to createListItem
                itemList.appendChild(listItem);
            });
            mealSection.appendChild(itemList);

            const footer = document.createElement('p');
            footer.textContent = `Total Calories: ${meals[mealType].totalCalories}`;
            mealSection.appendChild(footer);

            foodItemsContainer.appendChild(mealSection);
        }
    });
    const overallTotalLine = document.createElement('p');
    overallTotalLine.textContent = `Overall Total Calories: ${overallTotal.totalCalories}`;
    foodItemsContainer.appendChild(overallTotalLine);
}

document.getElementById('date').addEventListener('input', function(event) {
    event.preventDefault();
    const selectedDate = document.getElementById('date').value;
    fetch('/get/food-items?date=' + selectedDate, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        const userId = data.user_id;
        displayFoodItems(data.foodItems, userId);
    })
    .catch(error => console.error('Error fetching food items:', error));
});
document.getElementById('date').addEventListener('DOMContentLoaded', function(event) {
    event.preventDefault();
    const selectedDate = document.getElementById('date').value;
    fetch('/get/food-items?date=' + selectedDate, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        const userId = data.user_id;
        displayFoodItems(data.foodItems, userId);
    })
    .catch(error => console.error('Error fetching food items:', error));
});

document.addEventListener('DOMContentLoaded', fetchAndDisplayFoodItems);
