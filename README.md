# CSCE3550-Project1

This project was completed with the assistance of Github Copilot and ChatGPT.
The following prompts were used to aid in development of this project (This list is not exhaustive and may not include prompts or automatic suggestions by Copilot ):

- Develop me a RESTful JWKS using in python.
- Implement key generation (key id).
- What packages would be helpful for this project?
- How do I develop a auth endpoint?
- What is the syntax for serving public keys and how to verify JWTS? What is some sample code?

# Requirements
- Setup Virtual envrionment on VScode or terminal and execution of project must be in .venv (virtual environment)
- Download python 3.13.7
- Install packages (listed in requirements.txt )using pip 

# Instructions to run (with gradebot)
After completing requirements, run "uvicorn main:app --port 8080" on terminal line,
then proceed to use gradebot to check against rubric
To run test suite "pytest --cov"
