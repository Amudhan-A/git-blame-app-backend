from .mongodb import functions_collection


def save_function(data):
    """
    Insert a new function analysis document
    """
    return functions_collection.insert_one(data)


def get_function(repo, filepath, function_name):
    """
    Retrieve a function record
    """
    return functions_collection.find_one({
        "repo": repo,
        "filepath": filepath,
        "function_name": function_name
    })


def update_function(repo, filepath, function_name, data):
    """
    Update existing function document
    """
    return functions_collection.update_one(
        {
            "repo": repo,
            "filepath": filepath,
            "function_name": function_name
        },
        {"$set": data},
        upsert=True
    )


def list_repo_functions(repo):
    """
    List all functions belonging to a repo
    """
    return list(functions_collection.find({"repo": repo}))

    
    
def get_existing_analysis(repo, filepath, function_name):
    return functions_collection.find_one({
        "repo": repo,
        "filepath": filepath,
        "function_name": function_name
    })