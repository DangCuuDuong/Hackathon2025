// Sample recipes database (for demo purposes)
const recipesDatabase = [
    {
      name: "Oil and Salt Grilled Mushroom",
      ingredients: ["Mushroom", "Oil", "Salt"],
      category: "Vegetables",
      description: "Grilled mushrooms with a touch of oil and salt.",
      steps: [
        "Wash and dry the mushrooms.",
        "Toss mushrooms with oil and salt.",
        "Grill on medium heat for 5 minutes per side.",
        "Serve hot."
      ],
      nutrition: {
        calories: "120 kcal",
        fat: "8g",
        protein: "3g",
        carbs: "10g",
        fiber: "2g",
        sugar: "3g",
        sodium: "300mg"
      },
      image: "https://via.placeholder.com/300x200?text=Grilled+Mushroom"
    },
    {
      name: "Vegetable Stir-Fry",
      ingredients: ["Carrot", "Tomato", "Mushroom"],
      category: "Vegetables",
      description: "A colorful stir-fry with various ingredients.",
      steps: [
        "Chop all vegetables into bite-sized pieces.",
        "Heat oil in a pan over medium heat.",
        "Add vegetables and stir-fry for 5-7 minutes.",
        "Season with salt and pepper, then serve."
      ],
      nutrition: {
        calories: "150 kcal",
        fat: "5g",
        protein: "4g",
        carbs: "20g",
        fiber: "5g",
        sugar: "8g",
        sodium: "400mg"
      },
      image: "https://via.placeholder.com/300x200?text=Vegetable+Stir-Fry"
    },
    {
      name: "Mushroom and Lettuce Salad",
      ingredients: ["Mushroom", "Lettuce", "Oil", "Salt"],
      category: "Vegetables",
      description: "A fresh salad made with mushrooms and crunchy lettuce.",
      steps: [
        "Wash and chop the lettuce.",
        "Clean and slice the mushrooms.",
        "In a bowl, combine lettuce and mushrooms.",
        "Drizzle oil and sprinkle salt over the salad.",
        "Toss and serve immediately."
      ],
      nutrition: {
        calories: "150 kcal",
        fat: "10g",
        protein: "3g",
        carbs: "5g",
        fiber: "2g",
        sugar: "1g",
        sodium: "200mg"
      },
      image: "https://via.placeholder.com/300x200?text=Mushroom+Salad"
    },
    {
      name: "Carrot and Mushroom Soup",
      ingredients: ["Carrot", "Mushroom"],
      category: "Vegetables",
      description: "A smooth soup made with carrot and mushrooms.",
      steps: [
        "Peel and chop the carrots.",
        "Clean and slice the mushrooms.",
        "Boil carrots and mushrooms in water until soft.",
        "Blend until smooth, season with salt, and serve."
      ],
      nutrition: {
        calories: "100 kcal",
        fat: "2g",
        protein: "3g",
        carbs: "15g",
        fiber: "4g",
        sugar: "6g",
        sodium: "350mg"
      },
      image: "https://via.placeholder.com/300x200?text=Carrot+Soup"
    },
    {
      name: "Mushroom Beef Kebabs",
      ingredients: ["Beef", "Mushroom"],
      category: "Meat",
      description: "Kebabs made with beef and mushrooms.",
      steps: [
        "Cut beef and mushrooms into chunks.",
        "Skewer beef and mushrooms alternately.",
        "Grill for 10 minutes, turning occasionally.",
        "Serve with a side of sauce."
      ],
      nutrition: {
        calories: "300 kcal",
        fat: "15g",
        protein: "25g",
        carbs: "5g",
        fiber: "1g",
        sugar: "2g",
        sodium: "500mg"
      },
      image: "https://via.placeholder.com/300x200?text=Beef+Kebabs"
    },
    {
      name: "Beef Stir-Fry with Mushrooms",
      ingredients: ["Beef", "Mushroom", "Carrot"],
      category: "Meat",
      description: "A quick and tasty stir-fry made with beef and mushrooms.",
      steps: [
        "Slice beef thinly and chop vegetables.",
        "Heat oil in a pan and stir-fry beef until browned.",
        "Add mushrooms and carrots, cook for 5 minutes.",
        "Season with soy sauce and serve."
      ],
      nutrition: {
        calories: "350 kcal",
        fat: "20g",
        protein: "30g",
        carbs: "10g",
        fiber: "3g",
        sugar: "4g",
        sodium: "600mg"
      },
      image: "https://via.placeholder.com/300x200?text=Beef+Stir-Fry"
    },
    {
      name: "Curry Mushroom Soup",
      ingredients: ["Mushroom", "Carrot"],
      category: "Vegetables",
      description: "A comforting soup infused with curry and mushrooms.",
      steps: [
        "Chop carrots and mushrooms.",
        "Sauté in a pot with curry powder.",
        "Add water and simmer for 20 minutes.",
        "Blend until smooth and serve hot."
      ],
      nutrition: {
        calories: "120 kcal",
        fat: "3g",
        protein: "4g",
        carbs: "18g",
        fiber: "5g",
        sugar: "7g",
        sodium: "400mg"
      },
      image: "https://via.placeholder.com/300x200?text=Curry+Soup"
    },
    {
      name: "Curry Beef Lettuce Wrap",
      ingredients: ["Beef", "Lettuce"],
      category: "Meat",
      description: "Delicious beef curry served in fresh lettuce leaves.",
      steps: [
        "Cook beef with curry spices until tender.",
        "Wash and separate lettuce leaves.",
        "Spoon beef curry into lettuce leaves.",
        "Wrap and serve immediately."
      ],
      nutrition: {
        calories: "280 kcal",
        fat: "15g",
        protein: "20g",
        carbs: "10g",
        fiber: "2g",
        sugar: "3g",
        sodium: "450mg"
      },
      image: "https://via.placeholder.com/300x200?text=Beef+Wrap"
    }
  ];
  
  // Load recipes when the page loads
  document.addEventListener('DOMContentLoaded', function() {
    const recipesList = document.getElementById('recipesList');
    const searchRecipe = document.getElementById('searchRecipe');
  
    // Function to display recipes
    function displayRecipes(recipes) {
      recipesList.innerHTML = '';
      if (recipes.length === 0) {
        recipesList.innerHTML = '<p class="text-muted text-center">No recipes found.</p>';
        return;
      }
  
      recipes.forEach(recipe => {
        const recipeCard = document.createElement('div');
        recipeCard.className = 'col-md-3';
        recipeCard.innerHTML = `
          <div class="card recipe-card" data-bs-toggle="modal" data-bs-target="#recipeModal" data-recipe='${JSON.stringify(recipe)}'>
            <img src="${recipe.image}" class="card-img-top" alt="${recipe.name}">
            <div class="card-body">
              <h5 class="card-title">${recipe.name}</h5>
              <p class="card-text">${recipe.description}</p>
            </div>
          </div>
        `;
        recipesList.appendChild(recipeCard);
      });
    }
  
    // Initial display of all recipes
    displayRecipes(recipesDatabase);
  
    // Search functionality
    searchRecipe.addEventListener('input', function() {
      const searchTerm = searchRecipe.value.toLowerCase();
      const filteredRecipes = recipesDatabase.filter(recipe => 
        recipe.name.toLowerCase().includes(searchTerm) || 
        recipe.description.toLowerCase().includes(searchTerm)
      );
      displayRecipes(filteredRecipes);
    });
  
    // Modal content population
    recipesList.addEventListener('click', function(event) {
      const card = event.target.closest('.recipe-card');
      if (card) {
        const recipe = JSON.parse(card.dataset.recipe);
        document.getElementById('recipeModalLabel').textContent = recipe.name;
        document.getElementById('modalImage').src = recipe.image;
        document.getElementById('modalIngredients').textContent = recipe.ingredients.join(', ');
        
        const stepsList = document.getElementById('modalSteps');
        stepsList.innerHTML = '';
        recipe.steps.forEach(step => {
          const li = document.createElement('li');
          li.textContent = step;
          stepsList.appendChild(li);
        });
  
        document.getElementById('modalDescription').textContent = recipe.description;
        document.getElementById('modalCalories').textContent = recipe.nutrition.calories;
        document.getElementById('modalFat').textContent = recipe.nutrition.fat;
        document.getElementById('modalProtein').textContent = recipe.nutrition.protein;
        document.getElementById('modalCarbs').textContent = recipe.nutrition.carbs;
        document.getElementById('modalFiber').textContent = recipe.nutrition.fiber;
        document.getElementById('modalSugar').textContent = recipe.nutrition.sugar;
        document.getElementById('modalSodium').textContent = recipe.nutrition.sodium;
      }
    });
  });