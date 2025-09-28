# Project Atlas

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

Update npm and node version before starting Fall 2025:
    package-lock and package will not update on `npm install` until the following steps are taken

Check for node versions using
    
    - `nvm ls`
    - Look for the newest version of node
    - Install using `nvm install <version>` then use with `nvm use <version>`
        
  How to run the FrontEnd:

    cd client
    npm run dev

how to run backend:

    cd server                               #you must be within the server folder
    python -m venv venv                     #this command creates the virtual environment
    source .\venv\Scripts\Activate.ps1            #this command activates the virtual environment.
    pip install -r requirements.txt         #this command ensures virual environment has all dependencies
    python manage.py runserver            #this command runs the client server
    deactivate                    #this command ends the virtual machine
