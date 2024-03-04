from flask import Flask, render_template, request
import plotly.graph_objs as go
import datetime

app = Flask(__name__)

moods_data = {'Happy': [], 'Sad': [], 'Excited': [], 'Calm': [], 'Angry': [], 'Stressed': []}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        mood = request.form['mood']
        moods_data[mood].append(datetime.datetime.now())
    
    return render_template('index_dropdown.html')

@app.route('/visualization')
def visualization():
    fig = go.Figure()

    mood_sequence = []
    for mood, times in moods_data.items():
        mood_transitions = [(time, mood) for time in times]
        mood_transitions.sort()
        mood_sequence.extend(mood_transitions)

    mood_sequence.sort()

    x_values = []
    y_values = []

    for i in range(len(mood_sequence)):
        if i == 0:
            x_values.append(mood_sequence[i][0])
            y_values.append(mood_sequence[i][1])
        else:
            if mood_sequence[i][1] != mood_sequence[i-1][1]:
                x_values.append(mood_sequence[i-1][0])
                y_values.append(mood_sequence[i-1][1])
                x_values.append(mood_sequence[i][0])
                y_values.append(mood_sequence[i][1])

    fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='lines+markers', name='Mood Transition'))

    fig.update_layout(title='Mood Transition over Time',
                      xaxis_title='Time',
                      yaxis_title='Mood')

    graphJSON = fig.to_json()

    return render_template('visualization_dropdown.html', graphJSON=graphJSON)

if __name__ == '__main__':
    app.run(debug=True)
