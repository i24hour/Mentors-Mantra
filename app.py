from flask import Flask, request, render_template, redirect, url_for
from supabase import create_client, Client
import os



# Try to get environment variables, use placeholders for local development
SUPABASE_URL = os.environ.get('url', 'https://placeholder-url.supabase.co')
SUPABASE_KEY = os.environ.get('key', 'placeholder-key')

# Initialize Supabase client with exception handling
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    print(f"Warning: Could not initialize Supabase: {e}")
    supabase = None


# Initialize Flask app
app = Flask(__name__, static_url_path='/static', static_folder='static')

# Create a simple HTML file that redirects to the Flask app when opened directly
@app.route('/create-redirect-file')
def create_redirect_file():
    with open('templates/direct-access.html', 'w') as f:
        f.write("""
        <!DOCTYPE html>
        <html>
        <head>
          <meta http-equiv="refresh" content="0;url=http://127.0.0.1:5000/">
          <title>Redirecting...</title>
        </head>
        <body>
          <p>Redirecting to Flask app. If you are not redirected, <a href="http://127.0.0.1:5000/">click here</a>.</p>
          <script>
            // Also try with different common ports
            window.addEventListener('load', function() {
              fetch('http://127.0.0.1:5000/')
                .then(response => { window.location = 'http://127.0.0.1:5000/'; })
                .catch(() => {
                  fetch('http://127.0.0.1:8000/')
                    .then(response => { window.location = 'http://127.0.0.1:8000/'; })
                    .catch(() => {
                      fetch('http://127.0.0.1:5500/')
                        .then(response => { window.location = 'http://127.0.0.1:5500/'; })
                        .catch(() => {
                          // The template will use relative paths if no Flask app is running
                          window.location = 'index.html';
                        });
                    });
                });
            });
          </script>
        </body>
        </html>
        """)
    return "Redirect file created"

# Route to render the homepage
@app.route('/')
def home():
    return render_template('index.html')

# Route to render the form
@app.route('/contact.html')
def contact_form():
    return render_template('contact.html')

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    if supabase is None:
        print("Supabase client not initialized. Form data will not be saved.")
        return render_template('index.html')
        
    try:
        # Get form data
        name = request.form['name']
        phone = int(request.form['phone'])
        exam = request.form['exam']
        question = request.form.get('question', '')

        print(f"Received form data: {name}, {phone}, {exam}, {question}")
        
        # Insert data into Supabase
        response = supabase.table('contact').insert({
            "name": name,
            "phone": phone,
            "exam": exam,
            "question": question
        }).execute()

        # Handle response
        if not response.data:  # If `data` is empty, there's an issue
            print("Error occurred:", response)
            return "Error occurred while inserting data.", 500
    except Exception as e:
        print(f"Error processing form: {e}")
        
    return render_template('index.html')

# Run the Flask app
if __name__ == '__main__':
    # Create the redirect file first
    with open('templates/direct-access.html', 'w') as f:
        f.write("""
        <!DOCTYPE html>
        <html>
        <head>
          <meta http-equiv="refresh" content="0;url=http://127.0.0.1:5000/">
          <title>Redirecting...</title>
        </head>
        <body>
          <p>Redirecting to Flask app. If you are not redirected, <a href="http://127.0.0.1:5000/">click here</a>.</p>
          <script>
            // Also try with different common ports
            window.addEventListener('load', function() {
              fetch('http://127.0.0.1:5000/')
                .then(response => { window.location = 'http://127.0.0.1:5000/'; })
                .catch(() => {
                  fetch('http://127.0.0.1:8000/')
                    .then(response => { window.location = 'http://127.0.0.1:8000/'; })
                    .catch(() => {
                      fetch('http://127.0.0.1:5500/')
                        .then(response => { window.location = 'http://127.0.0.1:5500/'; })
                        .catch(() => {
                          // The template will use relative paths if no Flask app is running
                          window.location = 'index.html';
                        });
                    });
                });
            });
          </script>
        </body>
        </html>
        """)
    app.run(debug=True, host='0.0.0.0')
