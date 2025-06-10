import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import pandas as pd
from ollama import chat
from ollama import ChatResponse
import speech_recognition as sr
from pathlib import Path

env_path = Path(r"C:\Users\samee\Desktop\Python\.ipynb_checkpoints\ollama_db.env")
load_dotenv(dotenv_path=env_path)

user = os.getenv("DB_USER")
password = os.getenv("DB_PASS")

db_url = f"postgresql+psycopg2://{user}:{password}@localhost:5432/analytics_db"
engine = create_engine(db_url)


schema_description = """
Database schema:
Table: dept
  - deptno: Department number
  - dname: Department name
  - loc: Department location

Table: emp
  - empno: Employee number
  - ename: Employee name
  - job: Job title
  - mgr: Manager ID
  - hiredate: Date of hire
  - comm: Commission
  - deptno: Department number (foreign key)
  - Don't include commission unless mentioned explicitly in the query
"""



system_prompt=("""You are an expert sql assistant. You are given a natural language query and you 
need to convert it into a sql query.And only give the SQL query no explanation just the query.
The database we are using is PostGres.
IMPORTANT:
- Don't include commission unless mentioned explicitly in the query
- Don't give nay other assuming message or anything just the sql query nothing else""")



def speech_to_text():
    r=sr.Recognizer()
    m=sr.Microphone()
    with m as source:
        r.adjust_for_ambient_noise(source)
        print("Please speak now")
        audio=r.listen(source)
        try:
            text=r.recognize_google(audio,language="en-IN")
            return text
        except sr.UnknownValueError:
            print("Could not understand audio.")
            return None
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
            return None

            

def clean_sql_response(assistant_response: str) -> str:
    cleaned = assistant_response.strip()
    # Remove markdown code fences (``` or ```sql)
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        # Remove first line if it's a code fence
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        # Remove last line if it's a closing code fence
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        cleaned = "\n".join(lines).strip()
    return cleaned




# converting english to sql

def english_to_sql(history,prompt):
    history.append({"role":"user","content":prompt})

    
    response: ChatResponse=chat(
        
        model="mistral",# using the mistral model
        messages=history,# list of messages
    
    )
    assistant_response=response['message']['content']
    history.append({"role":"assistant","content":assistant_response})
    
    cleaned_response = clean_sql_response(assistant_response)
    return cleaned_response,history




def query_to_sql(query):
    try:
        if query.strip().lower().startswith("select"):
            #if the query starts with select then pandas will execute the query
            df=pd.read_sql(query,engine)#executing the query
            return df
        else:
            #if the query does not start with select then we will use cursor to execute the query
            with engine.begin() as conn: # handles commit and rollback automatically
                conn.execute(query)
                return "Query executed successfully"
    except Exception as e:
        return f"Error: {e}"
    



    
def main_voice():
    print("Welcome to the SQL Query Generator!")
    history = [
        {
            "role": "system",
            "content": (
                system_prompt+schema_description
            )
        }
    ]

    while True:
        user_input = speech_to_text()
        if not user_input:
            continue
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break


        assistant_reply, history = english_to_sql(history, user_input)
        print("\nSQL Query:", assistant_reply)
        print("\n\n\n")
            
            
        result = query_to_sql(assistant_reply)
        if isinstance(result, pd.DataFrame):
                print(result.to_string(index=False))
        else:
                print(result)

        
        print("""\nIf the query/result is correct, write 'yes'.\n
        Otherwise, please explain what's wrong or how to improve it:\n""")
        feedback_input=input("Enter your feedback: ")
        if feedback_input.lower() == "yes":
                break  # proceed to next user input
        
        else:
            feedback=speech_to_text()
        
            correction_prompt = (
                    "The previous SQL query did not give correct results or was incorrect. "
                    "User feedback: " + feedback + "\n"
                    f"Original question: {user_input}\n"
                    f"Previous SQL query:\n{assistant_reply}\n"
                    "Please revise the SQL query accordingly."
                )
            assistant_reply, history = english_to_sql(history, correction_prompt)

        print("\n---\n")



if __name__=="__main__":
    main_voice()
        
        
