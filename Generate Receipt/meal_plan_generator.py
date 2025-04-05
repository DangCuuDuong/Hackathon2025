import openai
import json
import re
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

client = openai

# Template for a single recipe
recipe_form = {
    "name": "Dish name",
    "description": "Short description of the dish.",
    "nutrition": {
        "calories": "230 kcal",
        "protein": "15g",
        "carbs": "30g",
        "fat": "10g",
        "fiber": "4g",
        "sugar": "6g",
        "sodium": "450mg"
    },
    "ingredients": [
        {"name": "example", "quantity": "100g"}
    ],
    "steps": ["Step 1", "Step 2"],
    "spice_level": "medium",
    "diet_type": "eat clean",
    "suitable_for": ["muscle gain"],
    "highlighted_ingredients": ["chicken breast"],
    "avoided_ingredients": ["butter"],
    "reference": "https://example.com"
}


def build_meal_plan_prompt(ingredients, preferences, health):
    return f"""
You are a professional nutrition assistant. Please create a **3-day meal plan** for one person based on the information below:

📦 **Available ingredients in the fridge:**  
{json.dumps(ingredients, indent=2, ensure_ascii=False)}

❤️ **Personal preferences:**  
- Preferred spice level: {preferences.get("spice_level", "medium")}
- Diet type: {preferences.get("diet_type", "eat clean")}
- Allergies / dislikes: {', '.join(preferences.get("allergies_or_dislikes", []))}
- Favorite foods: {', '.join(preferences.get("favorite_foods", []))}

💪 **Health condition:**  
- Health status: {health.get("health_status", "gym")}
- Goals: {health.get("health_goals", "muscle gain")}
- Nutrition targets: {json.dumps(health.get("nutrition_targets", {}), ensure_ascii=False)}

---

🧠 **Meal planning rules:**
- Create a plan for 5 full days.
- Each day MUST include 2 to 3 meals: **breakfast, lunch, and dinner**.
- 🔥 Each meal MUST contain **2 to 3 different dishes (recipes)**. Do NOT generate only 1 dish per meal.
- You MAY reuse dishes within the same day to save cooking effort.
- Prioritize using the available ingredients as much as possible.
- Avoid allergens and respect food dislikes.
- Ensure nutritional targets are reasonably met.
- Keep each recipe enough detailed and add numbers to each steps, healthy, and suitable for daily home cooking.

---

✍️ **Output JSON format:**
[
  {{
    "day": "Day 1",
    "meals": [
      {{
        "meal_name": "Breakfast",
        "recipes": [
          {json.dumps(recipe_form, indent=4, ensure_ascii=False)},
          ...
        ]
      }},
      ...
    ]
  }},
  ...
]

Please strictly follow the rules above. Make sure **each meal includes at least 2 recipes**.
"""


def get_meal_plan(ingredients, preferences, health):
    prompt = build_meal_plan_prompt(ingredients, preferences, health)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    content = response.choices[0].message.content

    content = re.sub(r"```json\n(.*?)\n```", r"\1", content, flags=re.DOTALL).strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        print("❌ JSON decode error:", e)
        return None


def load_json_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    try:
        ingredients = load_json_file("main.json")
        preferences = load_json_file("preferences.json")
        health = load_json_file("health.json")
    except Exception as e:
        print("❌ Error loading input files:", e)
        return

    meal_plan = get_meal_plan(ingredients, preferences, health)

    if meal_plan:
        with open("meal_plan.json", "w", encoding="utf-8") as f:
            json.dump(meal_plan, f, indent=4, ensure_ascii=False)
        print("✅ Meal plan successfully generated and saved to meal_plan.json")
    else:
        print("⚠️ Failed to generate meal plan.")


if __name__ == "__main__":
    main()
