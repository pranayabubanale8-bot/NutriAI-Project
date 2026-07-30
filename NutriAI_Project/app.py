from flask import Flask, render_template, request ,redirect,url_for  # pyright: ignore[reportMissingImports]
import json

app = Flask(__name__)

users = {
    "admin": "admin123",
    "pranaya": "12345"
}
@app.route('/')
def login_page():
    return render_template("login.html")


@app.route('/login',methods=['POST'])
def login():
    username=request.form['username']
    password=request.form['password']
    if username in users and users[username]==password:
        return redirect(url_for('home'))
    else:
        return "Invalid Username or Password"
   
@app.route('/home')
def home():
    return render_template("index.html")

def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100
    bmi = weight / (height_m ** 2)
    return round(bmi, 2)

def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"
def diet_recommendation(category):

    veg = {
        "Underweight": {
            "Breakfast": ["Banana shake", "Poha"],
            "Lunch": ["Rice with dal", "Paneer curry"],
            "Dinner": ["Chapati with vegetables", "Milk"]
        },

        "Normal": {
            "Breakfast": ["Oats with milk", "Apple"],
            "Lunch": ["Veg pulao", "Salad"],
            "Dinner": ["Chapati with sabzi", "Curd"]
        },

        "Overweight": {
            "Breakfast": ["Green smoothie", "Boiled sprouts"],
            "Lunch": ["Brown rice", "Grilled vegetables"],
            "Dinner": ["Vegetable soup", "Millet roti"]
        },

        "Obese": {
            "Breakfast": ["Oats porridge", "Papaya"],
            "Lunch": ["Steamed vegetables", "Soup"],
            "Dinner": ["Salad", "Low fat curd"]
        }
    }

    nonveg = {
        "Underweight": {
            "Breakfast": ["Egg omelette", "Milk"],
            "Lunch": ["Chicken rice", "Egg curry"],
            "Dinner": ["Fish curry with rice"]
        },

        "Normal": {
            "Breakfast": ["Boiled eggs", "Brown bread"],
            "Lunch": ["Grilled chicken", "Salad"],
            "Dinner": ["Fish curry", "Chapati"]
        },

        "Overweight": {
            "Breakfast": ["Avoid non-veg"],
            "Lunch": ["Avoid non-veg"],
            "Dinner": ["Avoid non-veg"]
        },

        "Obese": {
            "Breakfast": ["Avoid non-veg"],
            "Lunch": ["Avoid non-veg"],
            "Dinner": ["Avoid non-veg"]
        }
    }

    return veg[category], nonveg[category]
@app.route('/result', methods=['POST'])
def result():

    name = request.form['name']
    weight = float(request.form['weight'])
    height = float(request.form['height'])
    diet_choice = request.form['diet']

    bmi = calculate_bmi(weight, height)
    category = get_bmi_category(bmi)

    veg, nonveg = diet_recommendation(category)

    if diet_choice == "veg":
        diet = veg
    elif diet_choice == "nonveg":
        diet = nonveg
    else:
        diet = {
            "Breakfast": veg["Breakfast"] + nonveg["Breakfast"],
            "Lunch": veg["Lunch"] + nonveg["Lunch"],
            "Dinner": veg["Dinner"] + nonveg["Dinner"]
        }

    return render_template(
    "result.html",
    name=name,
    weight=weight,
    height=height,
    bmi=bmi,
    category=category,
    diet=diet
)


if __name__ == "__main__":
    app.run(debug=True)