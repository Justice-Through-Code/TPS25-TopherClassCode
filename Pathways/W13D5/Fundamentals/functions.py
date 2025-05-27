# basic_functions.py
# Basic example of integrating simple functions together

def greet_user(name):
    """Function to greet a user by name"""
    return f"Hello, {name}!"

def get_age_category(age):
    """Function to categorize age groups"""
    if age < 13:
        return "child"
    elif age < 20:
        return "teenager" 
    elif age < 60:
        return "adult"
    else:
        return "senior"

def create_user_profile(name, age):
    """Integration function that combines greeting and age categorization"""
    greeting = greet_user(name)
    category = get_age_category(age)
    
    profile = {
        "greeting": greeting,
        "age_category": category,
        "full_message": f"{greeting} You are classified as a {category}."
    }
    
    return profile

# Example usage
if __name__ == "__main__":
    # Testing individual functions
    print("Testing individual functions:")
    print(greet_user("Alice"))
    print(get_age_category(16))
    
    print("\nTesting integrated function:")
    # Testing integrated function
    user_info = create_user_profile("Bob", 25)
    print(user_info["full_message"])
    
    # Multiple users
    users = [("Charlie", 12), ("Diana", 45), ("Eve", 67)]
    for name, age in users:
        profile = create_user_profile(name, age)
        print(profile["full_message"])