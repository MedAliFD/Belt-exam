from flask_app.config.mysqlconnection import connectToMySQL , DB
from flask_app.models.user import User



class Magazine:

    def __init__(self, data):
        self.id = data.get('id')
        self.title = data.get('title')
        self.content = data.get('description')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')
        self.user = None

        self.users_who_subscripted = []

        self.user_ids_who_subscripted = []


    @classmethod
    def get_by_id(cls, data):
        query = """
            SELECT * FROM magazines JOIN users ON magazine.user_id = users.id WHERE magazine.id = %(id)s;
            
        """
        results = connectToMySQL(DB).query_db(query , data)

        magazine = None
        if results:
            user_data = {
                'id': results[0]['users.id'],
                'first_name': results[0]['first_name'],
                'last_name': results[0]['last_name'],
                'email': results[0]['email'],
                'password': results[0]['password'],
                'created_at': results[0]['users.created_at'],
                'updated_at': results[0]['users.updated_at'],
            }
            magazine = cls(results[0])
            magazine.user = User(user_data)
        return magazine
    
    @classmethod
    def get_all(cls):
        query = """
                SELECT * FROM magazines JOIN users AS creators on magazines.user_id = creators.id
                LEFT JOIN users_sub_magazines ON magazines.id = users_sub_magazines.magazines_id
                LEFT JOIN users AS users_who_subscripted ON users_sub_magazines.users_id = users_who_subscripted.id
                ORDER BY magazines.id;
            """
        results = connectToMySQL(DB).query_db(query)
        subscriptions = []
        
        for row in results:

            new_subscription = True

            # Parse the data of the user that subscripted to the magazine to a dictionary
            user_who_subscripted_data = {
                'id': row['users_who_subscripted.id'],
                'email': row['users_who_subscripted.email'],
                'first_name': row['users_who_subscripted.first_name'],
                'last_name': row['users_who_subscripted.last_name'],
                'password': row['users_who_subscripted.password'],
                'created_at': row['users_who_subscripted.created_at'],
                'updated_at': row['users_who_subscripted.updated_at'],
            }

            # Storing the number of subscriptions added to the final list.
            number_of_subscripions = len(subscriptions)
            # We are checking if we are on the first iteration of the loop.
            if number_of_subscripions > 0:
                # Get the subscription of the last iteration
                last_sub = subscriptions[number_of_subscripions - 1]
                if last_sub.id == row['id']:
                    # Appending the user that subscribed to the last magazine's
                    last_sub.users_who_subscripted.append(User(user_who_subscripted_data))

                    last_sub.user_ids_who_subscripted.append(row['users_who_subscripted.id'])
                    new_subscription = False
            
            if new_subscription:
                # Creating an instance of the magazine
                magazine = cls(row)

                # Dictionary to create the user who created the review
                creator_dict = {
                    'id': row.get('creators.id'),
                    'first_name': row.get('first_name'),
                    'last_name': row.get('last_name'),
                    'email': row.get('email'),
                    'password': row.get('password'),
                    'created_at': row.get('creators.created_at'),
                    'updated_at': row.get('creators.updated_at'),
                }

                magazine.user = User(creator_dict)
                if row['users_who_subscripted.id']:
                    magazine.users_who_subscripted.append(User(user_who_subscripted_data))
                    magazine.users_who_subscripted.append(row['users_who_subscripted.id'])
                subscriptions.append(magazine)
                
        return subscriptions
    
    #Create --

    @classmethod 
    def create(cls , data):
        query = "INSERT INTO magazines (title , description, user_id) VALUES(%(title)s,%(description)s,%(user_id)s);"
        result = connectToMySQL(DB).query_db(query , data)
        return result
    


    
    #Delete
    
    @classmethod 
    def delete(cls, data):
        query = "DELETE FROM magazines WHERE id = %(id)s;"
        result = connectToMySQL(DB).query_db(query , data)
        return result
    
    #add to table 
    
    @classmethod 
    def add_user_sub(cls, data):
        query = "INSERT INTO users_sub_magazines (users_id, magazines_id) VALUES (%(users_id)s, %(magazines_id)s);"
        result = connectToMySQL(DB).query_db(query , data)
        return result
    
    #remove from table 


    @classmethod
    def remove_user_sub(cls , data):
        query = "DELETE FROM users_sub_magazines WHERE users_id = %(users_id)s AND magazines_id = %(magazines_id)s;"
        result = connectToMySQL(DB).query_db(query , data)
        return result
    
    #user's magazines
    @classmethod
    def get_user_magazines(cls, user_id):
        query = """
            SELECT * FROM magazines
            WHERE user_id = %(user_id)s
            ORDER BY created_at DESC;
        """
        data = {'user_id': user_id}
        results = connectToMySQL(DB).query_db(query, data)

        user_magazines = [cls(result) for result in results]
        return user_magazines

    def show_magazine(cls, magazine_id):
        query = """
            SELECT * FROM magazines
            JOIN users ON magazines.user_id = users.id
            WHERE magazines.id = %(magazine_id)s;
        """
        data = {'magazine_id': magazine_id}
        result = connectToMySQL(DB).query_db(query, data)

        if result:
            magazine_data = {
                'id': result[0]['magazines.id'],
                'title': result[0]['title'],
                'description': result[0]['description'],
                'created_at': result[0]['magazines.created_at'],
                'updated_at': result[0]['magazines.updated_at'],
                # Add other fields as needed
            }

            user_data = {
                'id': result[0]['users.id'],
                'first_name': result[0]['first_name'],
                'last_name': result[0]['last_name'],
                'email': result[0]['email'],
                'created_at': result[0]['users.created_at'],
                'updated_at': result[0]['users.updated_at'],
            }

            magazine = cls(magazine_data)
            magazine.user = User(user_data)
            return magazine

        return None
    
    # Inside flask_app.models.magazine


    @classmethod
    def get_by_id2(cls, data):
        query = "SELECT * FROM magazines JOIN users ON magazines.user_id = users.id WHERE magazines.id = %(id)s;"
        result = connectToMySQL(DB).query_db(query, data)

        # Check if any results were found
        if result:
            # Assuming the result is a dictionary representing a row in the database
            return cls(result[0])

        return None  # Return None if the magazine is not found

    @classmethod 
    def delete(cls, data):
        query = "DELETE FROM magazines WHERE id = %(id)s;"
        result = connectToMySQL(DB).query_db(query , data)
        return result