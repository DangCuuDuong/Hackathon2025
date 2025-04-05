// Function to check if "No Ingredients" should be displayed
function updateNoIngredientsMessage(list) {
  if (list.children.length === 0 || (list.children.length === 1 && list.children[0].classList.contains('no-ingredients'))) {
    list.innerHTML = '<li class="no-ingredients text-muted">No Ingredients</li>';
  }
}

// Function to remove "No Ingredients" message if it exists
function removeNoIngredientsMessage(list) {
  const noIngredients = list.querySelector('.no-ingredients');
  if (noIngredients) {
    noIngredients.remove();
  }
}

// Function to add an ingredient to a category
function addIngredientToCategory(ingredient, category) {
  const list = document.getElementById(category);
  removeNoIngredientsMessage(list);
  
  const li = document.createElement('li');
  li.innerHTML = `${ingredient} <span class="float-end remove-item"><i class="fas fa-times text-muted"></i></span>`;
  list.appendChild(li);

  // Show toast notification
  const toast = new bootstrap.Toast(document.getElementById('successToast'));
  toast.show();
}

// Add ingredient manually
document.getElementById('addButton').addEventListener('click', function() {
  const ingredientInput = document.getElementById('ingredientInput');
  const categorySelect = document.getElementById('categorySelect');
  const ingredient = ingredientInput.value.trim();
  const category = categorySelect.value;
  
  // Validate input
  if (!ingredient || !category) {
    alert('Please enter an ingredient and select a category.');
    return;
  }

  addIngredientToCategory(ingredient, category);


  ingredientInput.value = '';
  categorySelect.value = '';
});

// Remove ingredient when clicking the "x"
document.addEventListener('click', function(event) {
  if (event.target.classList.contains('fa-times') || event.target.parentElement.classList.contains('remove-item')) {
    const li = event.target.closest('li');
    const list = li.parentElement;
    li.remove();
    updateNoIngredientsMessage(list);
  }
});

// Handle image upload
const imageUpload = document.getElementById('imageUpload');
const imagePreview = document.getElementById('imagePreview');
const previewImage = document.getElementById('previewImage');
const imageCategory = document.getElementById('imageCategory');
const classifyButton = document.getElementById('classifyButton');

imageUpload.addEventListener('change', function(event) {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function(e) {
      previewImage.src = e.target.result;
      imagePreview.style.display = 'block';
      classifyButton.disabled = false;

      // Simulate image classification based on file name
      // In a real scenario, you'd use an API or ML model here
      const fileName = file.name.toLowerCase();
      let category = '';
      let ingredient = '';

      // Simple classification based on file name (for demo purposes, limited to 3 categories)
      if (fileName.includes('carrot') || fileName.includes('tomato') || fileName.includes('potato')) {
        category = 'vegetables';
        ingredient = fileName.includes('carrot') ? 'Carrot' : fileName.includes('tomato') ? 'Tomato' : 'Potato';
      } else if (fileName.includes('apple') || fileName.includes('banana') || fileName.includes('orange')) {
        category = 'fruits';
        ingredient = fileName.includes('apple') ? 'Apple' : fileName.includes('banana') ? 'Banana' : 'Orange';
      } else if (fileName.includes('chicken') || fileName.includes('beef') || fileName.includes('pork')) {
        category = 'meat';
        ingredient = fileName.includes('chicken') ? 'Chicken' : fileName.includes('beef') ? 'Beef' : 'Pork';
      } else {
        category = 'unknown';
        ingredient = 'Unknown Ingredient';
      }

      // Display the detected category
      imageCategory.textContent = `Detected: ${ingredient} (Category: ${category !== 'unknown' ? category.charAt(0).toUpperCase() + category.slice(1) : 'Unknown'})`;
      
      // Store the detected category and ingredient for later use
      classifyButton.dataset.category = category;
      classifyButton.dataset.ingredient = ingredient;
    };
    reader.readAsDataURL(file);
  }
});

// Classify and add the ingredient from the image
classifyButton.addEventListener('click', function() {
  const category = classifyButton.dataset.category;
  const ingredient = classifyButton.dataset.ingredient;

  if (category === 'unknown') {
    alert('Could not classify the ingredient. Please add manually.');
    return;
  }

  addIngredientToCategory(ingredient, category);

  // Reset the upload section
  imageUpload.value = '';
  imagePreview.style.display = 'none';
  classifyButton.disabled = true;
  imageCategory.textContent = '';
});

// Initialize "No Ingredients" message for empty lists on page load
document.querySelectorAll('.list-unstyled').forEach(list => {
  updateNoIngredientsMessage(list);
});