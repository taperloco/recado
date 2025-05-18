from flask import request
from flask_restful import Resource
from src.services.recados_service import RecadosService
from src.services.users_service import UsersService
from src.services.chats_service import ChatsService
from src.utils.auth import *
from src.utils.helper_functions import *

class Controller(Resource):
    def get(self):
        # Check auth
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
        else:
            return {"error": "Invalid authorization header"}, 401
        # Check that jwt token is correct and extract the user.
        user_id, error = check_token(token)
        if not user_id:
            # PASAR EL ERROR CONCRETO
            return {"error": "Invalid authorization header"}, 401
        # Call the services
        code =  request.path.rstrip("/").split("/")[-1]
        match code:
            # Borrar estos
            case "getrecados":
                service = RecadosService()
                return service.get_available_recados(user_id)
            case "getusers":
                service = UsersService()
                return service.get_available_users(user_id)
            case "getchat":
                send_to = request.headers.get("SendTo")
                print(send_to)
                if not send_to:
                    return {"Error": "Missing chat user"}, 400  
                service = ChatsService()
                return service.get_chat_messages(user_id, send_to)

            case _:
                return {"Error": f"Wrong code: {code}"}, 400
            

    def put(self):       
        code =  request.path.rstrip("/").split("/")[-1]
        user_id = None
        # Exclude authorization check when user registers
        if code != "users":
            # Ckeck if the authorization header contains a jwt token
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
            else:
                return {"error": "Invalid authorization header"}, 401    
            # Check that jwt token is correct and extract the user.
            user_id, error = check_token(token)
            if not user_id:
                return {"error": "Invalid jwt token"}, 401
        # Extract json body
        data = request.get_json()
        if not data:
            return {"Error": "Request body is empty"}, 400
        
        # Find service depending on the code (put_new_recado, put_current_location)      
        match code:
            case 'recados':
                if "text" not in data or not data["text"].strip():
                    return {"Error": "Text is required and cannot be empty"}, 400   
                service = RecadosService()
                return service.new_recado(user_id, data)
            
            case 'users':
                name = data.get('name')
                if not name:
                    return {"Error": "Name not found"}, 400       
                # Check email
                email = data.get('email')
                if not check_email(email):
                    return {"Error": "Email is not correct"}, 400
                # Check password
                password = data.get('password')
                if not is_strong_password(password):
                    return {"Error": "Password is not strong"}, 400
                # Add new user       
                service = UsersService()
                return service.new_user(name, email, password)
            
            case 'chats':
                text = data.get('text')
                if not text:
                    return {"Error": "Text not found"}, 400
                send_to = data.get('send_to')
                if not send_to:
                    return {"Error": "No recipient of the message found"}, 400                         
                service = ChatsService()
                return service.new_chat_message(user_id, text, send_to)

            case _:
                return {"Error": f"Wrong code: {code}"}, 400
            

    def post(self):
        code =  request.path.rstrip("/").split("/")[-1]
        if(code == "login"):
            # Extract json body
            data = request.get_json()
            if not data:
                return {"Error": "Request body is empty"}, 400  
            # Check email
            email = data.get('email')
            if not email:
                return {"Error": "Email not found"}, 400
            password = data.get('password')
            if not password:
                return {"Error": "Password not found"}, 400
            # Call service
            return UsersService().login_user(email, password)
        
        elif(code == "register"):
            # Extract json body
            data = request.get_json()
            if not data:
                return {"Error": "Request body is empty"}, 400  
            # Check name
            name = data.get('name')
            if not name:
                return {"Error": "Name not found"}, 400
            # Check email
            email = data.get('email')
            if not email:
                return {"Error": "Email not found"}, 400
            password = data.get('password')
            if not password:
                return {"Error": "Password not found"}, 400
            # Call service
            return UsersService().new_user(name, email, password)          
        
        elif(code == "token"):
            # Ckeck if the authorization header contains a jwt token
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
                return {"token": refresh_token(token)}, 200
            else:
                return {"error": "No authorization header found"}, 401  
        
        elif(code == "update"):
            # Ckeck if the authorization header contains a jwt token
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
            else:
                return {"error": "No authorization header found"}, 401    
            # Check that jwt token is correct and extract the user.
            user_id, error = check_token(token)
            if not user_id:
                return {"error": "Invalid jwt token"}, 401
            # Extract json body
            data = request.get_json()
            print(data)
            if not data:
                return {"Error": "Request body is empty"}, 400 
            # Update user location and activity
            UsersService().update_location(user_id, float(data["latitude"]), float(data["longitude"]))
            # Build response          
            updateData = {"recados": RecadosService().get_available_recados(user_id, data["map_radio"]),
                          "users": UsersService().get_available_users(user_id, data["map_radio"])}
            return updateData        
        else:
            return {"Error": f"Wrong code: {code}"}, 400
