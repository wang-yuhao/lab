db = connect("mongodb://admin:password@localhost:27017/admin");
db.createRole({ role: "EEReadOnlyRole", privileges: [{ resource: {db: "emotionalengine", collection: ""}, actions: ["find"]}], roles: []})
