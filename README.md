# airline-project

Group Name : Ctrl+Alt+Elite

Group Members: Amaan Jamil Siddiqui,
               Daniel Podgornyy,
               Juan Correa,
               Ivan Rivas,
               Jacob Gewin
Dev Log:
    Starting a new IDE:
        Create Python environment for efficient package testing and management
            -Install python3
            -Create venv file in source location(python3 -m venv name-of-file)
        Activate environment
            -source C:/path/to/bin/activate
        
    how to run the FrontEnd:

    cd client
    npm run dev

how to run backend:

    cd server                               #you must be within the server folder
    python -m venv venv                     #this command creates the virtual environment
    .\venv\Scripts\Activate.ps1            #this command activates the virtual environment.
    pip install -r requirements.txt         #this command ensures virual environment has all dependencies
    python manage.py runserver            #this command runs the client server
    deactivate                    #this command ends the virtual machine
Research new models without limits