
from flask import Flask, request, render_template_string
from datetime import date

app = Flask(__name__)

# Weekly planning targets (hours)
ACTIVITIES = {
    "Sleep": (56, 70),
    "School / Classes": (30, 40),
    "Homework / Studying": (5, 15),
    "Sports / Physical Activity": (7, 14),
    "Gaming": (0, 14),
    "TV / Entertainment": (0, 14),
    "Reading": (1, 7),
    "Socializing": (2, 14),
    "Creative Hobbies": (1, 10),
    "Chores / Responsibilities": (1, 10)
}

PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Life Dashboard</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #eef2f7;
            color: #222;
            padding: 25px;
        }

        .container {
            max-width: 800px;
            margin: auto;
            background: white;
            padding: 25px;
            border-radius: 14px;
            box-shadow: 0 3px 12px #0001;
        }

        h1 { color: #315be8; }

        .activity {
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            justify-content: space-between;
            gap: 10px;
            padding: 13px 5px;
            border-bottom: 1px solid #eee;
        }

        input {
            padding: 9px;
            border: 1px solid #ccc;
            border-radius: 6px;
            max-width: 110px;
        }

        button {
            background: #315be8;
            color: white;
            padding: 11px 16px;
            border: none;
            border-radius: 7px;
            cursor: pointer;
            margin: 10px 5px 10px 0;
        }

        button:hover { background: #2045bd; }

        .green {
            background: #d8f5df;
            border-left: 5px solid #239b45;
        }

        .red {
            background: #ffe0e0;
            border-left: 5px solid #dc3535;
        }

        .result {
            padding: 14px;
            margin: 12px 0;
            border-radius: 8px;
        }

        .small {
            color: #666;
            font-size: 13px;
        }

        .custom-limits {
            display: flex;
            gap: 5px;
            flex-wrap: wrap;
        }
    </style>
</head>

<body>
<div class="container">

    <h1>Life Dashboard</h1>
    <p>Track how you spend your time every week!</p>

    <h2>How to Use</h2>
    <ol>
        <li>Choose the starting date of your week.</li>
        <li>Enter your weekly hours for each activity.</li>
        <li>Add your own activities if needed.</li>
        <li>Press Submit to see your results.</li>
    </ol>

    <form method="POST">

        <h3>Week Starting Date</h3>
        <input type="date" name="week"
               value="{{ week }}" required>

        <h3>Weekly Activities</h3>

        <div id="activities">

            {% for name, limits in activities.items() %}
            <div class="activity">

                <div>
                    <strong>{{ name }}</strong><br>
                    <span class="small">
                        Target: {{ limits[0] }}–{{ limits[1] }} hours
                    </span>
                </div>

                <input type="number"
                       name="hours"
                       min="0" max="168" step="0.5"
                       placeholder="Hours"
                       required>

                <input type="hidden"
                       name="activity_names"
                       value="{{ name }}">

                <input type="hidden"
                       name="activity_types"
                       value="fixed">

            </div>
            {% endfor %}

        </div>

        <button type="button" onclick="addActivity()">
            + Add Your Own Activity
        </button>

        <br>

        <button type="submit">
            View My Dashboard
        </button>

    </form>

    {% if results is not none %}

        <hr>

        <h2>Your Weekly Dashboard</h2>

        <p><strong>Week starting:</strong> {{ selected_week }}</p>

        <h3>Total Tracked Hours: {{ total }} / 168</h3>

        {% if total > 168 %}
        <div class="result red">
            Your tracked hours exceed the 168 hours in a week.
            Check for overlapping activities.
        </div>
        {% endif %}

        {% for item in results %}
        <div class="result {{ item.color }}">
            <strong>{{ item.name }}: {{ item.hours }} hours</strong>
            <p>{{ item.message }}</p>
            <p class="small">{{ item.target }}</p>
        </div>
        {% endfor %}

        <p class="small">
            These weekly targets are general planning suggestions,
            not guaranteed medical safety limits. Individual needs vary.
        </p>

    {% endif %}

    <hr>

    <h3>About Life Dashboard</h3>

    <p>
        Life Dashboard helps high school students track their weekly
        time across school, sleep, sports, entertainment, hobbies,
        and responsibilities.
    </p>

</div>

<script>
function addActivity() {
    const name = prompt("Enter your activity name:");

    if (!name || !name.trim()) return;

    const activityName = name.trim();

    const row = document.createElement("div");
    row.className = "activity";

    const label = document.createElement("strong");
    label.textContent = activityName;

    const hours = document.createElement("input");
    hours.type = "number";
    hours.name = "hours";
    hours.min = "0";
    hours.max = "168";
    hours.step = "0.5";
    hours.placeholder = "Hours";
    hours.required = true;

    const limits = document.createElement("div");
    limits.className = "custom-limits";

    const minimum = document.createElement("input");
    minimum.type = "number";
    minimum.name = "custom_min";
    minimum.min = "0";
    minimum.max = "168";
    minimum.placeholder = "Min hrs";
    minimum.required = true;

    const maximum = document.createElement("input");
    maximum.type = "number";
    maximum.name = "custom_max";
    maximum.min = "0";
    maximum.max = "168";
    maximum.placeholder = "Max hrs";
    maximum.required = true;

    limits.append("Min:", minimum, "Max:", maximum);

    const hiddenName = document.createElement("input");
    hiddenName.type = "hidden";
    hiddenName.name = "activity_names";
    hiddenName.value = activityName;

    const hiddenType = document.createElement("input");
    hiddenType.type = "hidden";
    hiddenType.name = "activity_types";
    hiddenType.value = "custom";

    row.append(
        label, hours, limits, hiddenName, hiddenType
    );

    document.getElementById("activities").appendChild(row);
}
</script>

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def dashboard():

    results = None
    total = 0
    selected_week = ""
    week = date.today().isoformat()

    if request.method == "POST":

        selected_week = request.form.get("week", "")
        week = selected_week

        names = request.form.getlist("activity_names")
        types = request.form.getlist("activity_types")
        hours_list = request.form.getlist("hours")
        mins = request.form.getlist("custom_min")
        maxs = request.form.getlist("custom_max")

        results = []

        custom_index = 0

        for name, activity_type, value in zip(
            names, types, hours_list
        ):

            try:
                hours = float(value)

                if not 0 <= hours <= 168:
                    raise ValueError

                total += hours

                if activity_type == "fixed":
                    minimum, maximum = ACTIVITIES[name]

                else:
                    minimum = float(mins[custom_index])
                    maximum = float(maxs[custom_index])
                    custom_index += 1

                    if not (0 <= minimum <= maximum <= 168):
                        raise ValueError

                if minimum <= hours <= maximum:
                    color = "green"
                    message = "Within your weekly target!"
                else:
                    color = "red"
                    message = "Outside your weekly target."

                target_text = (
                    f"Your target: {minimum:g}–{maximum:g} hours"
                )

            except (ValueError, KeyError, IndexError):
                color = "red"
                message = "Invalid entry. Please check your numbers."
                target_text = "Please enter valid hours and limits."

            results.append({
                "name": name,
                "hours": value,
                "color": color,
                "message": message,
                "target": target_text
            })

    return render_template_string(
        PAGE,
        activities=ACTIVITIES,
        results=results,
        total=total,
        week=week,
        selected_week=selected_week
    )


if __name__ == "__main__":
    app.run(debug=True)
