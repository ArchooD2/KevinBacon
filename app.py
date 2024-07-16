from flask import Flask, render_template, request, jsonify, Response
from baconwaffle import find_shortest_path
import threading
import time

app = Flask(__name__)

search_state = {
    "current": "",
    "found": False
}

def sse_format(data):
    return f"data: {data}\n\n"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    global search_state
    data = request.get_json()
    start = data['start']
    try:
        end = data['end']
    except:
        end = None
    depth = data.get('depth', None)
    
    search_state["current"] = f"Searching from {start} to {end} with depth {depth}"
    search_state["found"] = False

    def run_search_path():
        result = find_shortest_path(start, end, depth)
        search_state["found"] = True
        if result:
            result_with_links = [f'<a href="https://en.wikipedia.org/wiki/{article.replace(" ", "_")}" target="_blank">{article}</a>' for article in result]
            final_result = "Found path:<br>" + "<br>".join(result_with_links)
        else:
            final_result = "No path found."
        search_state["current"] = final_result

    threading.Thread(target=run_search_path).start()
    return jsonify({'status': 'searching'})

@app.route('/events')
def events():
    def generate():
        while not search_state["found"]:
            yield sse_format(search_state["current"])
            time.sleep(1)
        yield sse_format(search_state["current"])
    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)
