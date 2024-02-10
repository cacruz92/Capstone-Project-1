const API_KEY= 'e2c186a8b8474f8cae53908a06bdf81a';
const API_SECRET = '73333179439f46d9a7deb5f5f5a83a09';


async function getFoodItem(foodId){
    const url = 'https://platform.fatsecret.com/rest/server.api';
    const requestBody = {
        method: 'food.get.v2',
        food_id: foodId,
        format: 'json'
    };

    try {
        cons res = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 
            }
        })
    }
}