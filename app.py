from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def dashboard():
    if request.method == "POST":
        age = int(request.form["age"])
        cricket_hours = int(request.form["cricket"])
        gaming_hours = int(request.form["gaming"])

        hobbies = {"cricket": cricket_hours, "gaming": gaming_hours}

        def time_hobbies():
            return cricket_hours + gaming_hours

        total_hours = time_hobbies()

        def custom_joke():
            if age >= 6:
                return "I'm reading a book on gravity, and I just can't put it down"

        return render_template_string("""
            <h1>Life Dashboard</h1>
            <p>Age: {{ age }}</p>
            {% for i in hobbies %}
                <p>{{ i }}: {{ hobbies[i] }} hours</p>
            {% endfor %}
            <h2>Total Hobby Hours: {{ total_hours }}</h2>
            <p>{{ joke }}</p>
        """, age=age, hobbies=hobbies,
             total_hours=total_hours, joke=custom_joke())

    return """
        <h1>Life Dashboard</h1>
        <form method="POST">
            Age: <input name="age" type="number" required><br><br>
            Cricket hours: <input name="cricket" type="number" required><br><br>
            Gaming hours: <input name="gaming" type="number" required><br><br>
            <button type="submit">Submit</button>
        </form>
    """

if __name__ == "__main__":
    app.run(debug=True)