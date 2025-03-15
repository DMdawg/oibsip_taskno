import time


BMI_CATEGORIES = [
    (0, 18.5, "Underweight", "You may need to increase your calorie intake and focus on nutrient-rich foods."),
    (18.5, 24.9, "Normal weight", "Maintain a balanced diet and regular exercise for optimal health."),
    (25, 29.9, "Overweight", "Consider adopting a more active lifestyle and healthier eating habits."),
    (30, 34.9, "Obesity (Class 1)", "A structured diet and exercise plan can improve your health."),
    (35, 39.9, "Obesity (Class 2)", "It's recommended to consult a healthcare provider for guidance."),
    (40, float('inf'), "Severe Obesity (Class 3)", "Medical supervision is strongly advised for better health.")
]


def calculate_bmi(weight, height):
    return round(weight / (height ** 2), 2)


def get_bmi_category(bmi):
    for lower, upper, category, advice in BMI_CATEGORIES:
        if lower <= bmi < upper:
            return category, advice
    return "Unknown", "No advice available."


def get_valid_input(prompt, min_value, max_value, input_type="float"):
    while True:
        try:
            value = input(prompt)
            if input_type == "float":
                value = float(value)
            elif input_type == "int":
                value = int(value)
            
            if min_value <= value <= max_value:
                return value
            else:
                print(f"❗ Please enter a value between {min_value} and {max_value}.")
        except ValueError:
            print("❗ Invalid input. Please enter a number.")


def save_results(weight, height, bmi, category, advice):
    with open("bmi_results.txt", "a") as file:
        file.write(f"Weight: {weight} kg, Height: {height} m, BMI: {bmi}, Category: {category}\n")
        file.write(f"Advice: {advice}\n\n")
    print("✅ Results saved to 'bmi_results.txt'.")


def main():
    print("===== 🧮 BMI CALCULATOR 🧮 =====")
    time.sleep(0.5)

    while True:
        
        weight_unit = input("Enter weight unit (kg/lb): ").strip().lower()
        if weight_unit not in ["kg", "lb"]:
            print("❗ Invalid unit. Please enter 'kg' or 'lb'.")
            continue

       
        weight = get_valid_input(f"Enter your weight ({weight_unit}): ", 20, 300)
        if weight_unit == "lb":
            weight = weight * 0.453592  

        
        height_unit = input("Enter height unit (m/cm): ").strip().lower()
        if height_unit not in ["m", "cm"]:
            print("❗ Invalid unit. Please enter 'm' or 'cm'.")
            continue

        
        height = get_valid_input(f"Enter your height ({height_unit}): ", 1.0, 300 if height_unit == "cm" else 2.5)
        if height_unit == "cm":
            height = height / 100 

        
        bmi = calculate_bmi(weight, height)
        category, advice = get_bmi_category(bmi)

        print(f"\n➡️ Your BMI is: {bmi} ({category})")
        print(f"💡 {advice}\n")

       
        save_results(weight, height, bmi, category, advice)

       
        retry = input("Would you like to calculate again? (yes/no): ").strip().lower()
        if retry != 'yes':
            print("\nThank you for using the BMI Calculator! Stay healthy! 💪")
            break


if __name__ == "__main__":
    main()
