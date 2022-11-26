db = connect("mongodb://admin:password@localhost:27017/admin");

db.createUser({
    "user": "analysis",
    "pwd": "password",
    "roles": ["EEReadOnlyRole"]
})
