# Voice-Controlled SQL Query Generator

This project allows users to generate and execute SQL queries using voice commands. It leverages speech recognition, natural language processing, and a large language model (LLM) to convert spoken English into SQL queries, which are then executed against a PostgreSQL database.

## Features

-   **Voice-to-SQL Conversion:** Converts spoken English queries into SQL queries using speech recognition and a language model.
-   **Database Interaction:** Executes generated SQL queries against a PostgreSQL database.
-   **Feedback Loop:** Incorporates user feedback to refine and improve the accuracy of generated SQL queries.
-   **Schema Awareness:** Uses a schema description to guide the generation of SQL queries.
-   **Error Handling:** Provides informative error messages for invalid queries or database issues.

## Prerequisites

-   Python 3.6+
-   PostgreSQL database
-   Ollama (for running the Mistral language model)
-   Required Python packages (see Installation)

## Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

    **requirements.txt:**

    ```
    SQLAlchemy==2.0.27
    psycopg2-binary==2.9.9
    python-dotenv==1.0.1
    ollama==0.1.27
    SpeechRecognition==3.14.0
    pandas==2.2.1
    ```

3.  **Set up your PostgreSQL database:**

    -   Create a database and user with appropriate permissions.
    -   Update the `.env` file with your database credentials.

4.  **Download and run the Mistral language model using Ollama:**

    ```bash
    ollama pull mistral
    ```

## Configuration

1.  **Create a `.env` file** in the project root directory.

2.  **Add the following environment variables to the `.env` file:**

    ```
    DB_USER=<your_database_user>
    DB_PASS=<your_database_password>
    DB_HOST=<your_database_host> #e.g., localhost
    DB_PORT=<your_database_port> #e.g., 5432
    DB_NAME=<your_database_name>
    ```

    **Example:**

    ```
    DB_USER=myuser
    DB_PASS=mypassword
    DB_HOST=localhost
    DB_PORT=5432
    DB_NAME=mydatabase
    ```

3.  **Update the `db_url` variable** in the `main.py` file to reflect your database connection string.  The provided code already constructs this using the environment variables, so ensure those are set correctly.

4.  **Update the `env_path` variable** in `main.py` to point to the location of your `.env` file.

## Usage

1.  **Run the `main.py` script:**

    ```bash
    python main.py
    ```

2.  **Speak your SQL query** when prompted.

3.  **Review the generated SQL query** and the results.

4.  **Provide feedback** on the accuracy of the query and results.  If the query is incorrect, explain the issue, and the system will attempt to refine the query.

5.  **Repeat steps 2-4** until you are satisfied with the results.

6.  **Say "exit" or "quit"** to end the program.

## Example

1.  **User:** "What are the names of all employees in the sales department?"

2.  **System:**

    ```sql
    SELECT e.ename
    FROM emp e
    JOIN dept d ON e.deptno = d.deptno
    WHERE d.dname = 'SALES';
    ```

    ```
     ename
    -------
     ALLEN
     WARD
     MARTIN
     TURNER
     JAMES
    (5 rows)
    ```

3.  **User:** "yes" (if the query and results are correct)


