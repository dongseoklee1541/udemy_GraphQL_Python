from graphene import Schema, ObjectType, String, Int, Field, List, Mutation

class UserType(ObjectType):
    id = Int()
    name = String()
    age = Int()

class CreateUser(Mutation):
    class Arguments:
        name = String()
        age = Int()
        
    user = Field(UserType)
    
    def mutate(root , info, name, age): 
        user= {"id" : len(Query.users) + 1, "name" : name, "age" : age}
        Query.users.append(user)
        return CreateUser(user=user)
    
class UpdateUser(Mutation):
    class Arguments:
        user_id = Int(required=True)
        name = String()
        age = Int()
    
    user = Field(UserType)

    def mutate(root, info, user_id, name=None, age=None):
        user = None
        for u in Query.users:
            if u["id"] == user_id:
                user = u
                break
        
        if not user:
            return None
        
        if name:
            user["name"] = name
        
        if age:
            user["age"] = age
        return UpdateUser(user=user)

class DeleteUser(Mutation):
    class Arguments:
        user_id = Int(required=True)
        # name = String(required=True)
        # age = Int(required=True)

    user = Field(UserType)

    def mutate(root, info, user_id):
        user = None
        for u in Query.users:
            if u["id"] == user_id:
                user = u
                Query.users.remove(u)
                return DeleteUser(user=user)
        
        if not user:
            return None
        

                


class Query(ObjectType):
    user = Field(UserType, user_id=Int())
    user_min_age = List(UserType, min_age=Int())
    
    
    users = [
        {"id" : 1, "name": "fira", "age" : 25},
        {"id" : 2, "name": "hirai", "age" : 30},
        {"id" : 3, "name": "geng", "age" : 35}
        ]
    
    
    def resolve_user(root, info, user_id):
        match_user = [user for user in Query.users if user["id"] == user_id] 
        return match_user[0] if match_user else None
    
    def resolve_user_min_age(root, info, min_age):
        match_users = [user for user in Query.users if user['age'] >= min_age]
        return match_users if match_users else None


class Mutation(ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
    
    
schema = Schema(query=Query, mutation=Mutation)

gql = '''
query{
    user(userId: 1)
    {
        id
        name
        age
    }
}
'''

# gql = '''
# query{
#     userMinAge(minAge: 29)
#     {
#         id
#         name
#         age
#     }
# }
# '''

append_gql = '''
mutation{
    createUser(name: "young", age: 12)
    {
        user{
            id
            name
            age
        }
    }
}
'''

update_gql = '''
mutation{
    updateUser(userId : 1, name: "updated User", age: 49)
    {
        user{
            id
            name
            age
        }
    }
}
'''

delete_gql = '''
mutation{
    deleteUser(userId: 4)
    {
        user{
            id
            name
            age
        }
    }
}

'''

if __name__ == "__main__":
    result = schema.execute(delete_gql)
    print(result)
    result = schema.execute(gql)
    print(result)