Database Operations

    show dbs: Lists all databases.
    use <database_name>: Switches to or creates a database.
    db: Displays the current database.
    db.dropDatabase(): Deletes the current database.
3. Collection Operations

    show collections: Lists collections in the current database.
    db.createCollection('<collection_name>'): Creates a new collection.
    db.<collection_name>.drop(): Deletes a collection.

4)crud :
        1)insert:
            db.users.insertOne({
              name: "Alice",
              age: 30,
              email: "alice@example.com"
            });
            db.products.insertMany([
              { name: "Laptop", price: 1200, stock: 10 },
              { name: "Smartphone", price: 800, stock: 25 },
              { name: "Tablet", price: 400, stock: 15 }
            ]);
        2)read/filter:
            db.products.find({ price: { $gt: 500 } });
            db.products.find({ price: { $gte: 100, $lte: 1000 } });
            db.products.find({ name: { $in: ["Laptop", "Keyboard"] } });
            db.products.find().sort({ price: 1 }).limit(3);
            shaws>  db.products.find({$or:[{price:{$lt:600}},{name:{$in:["Smartphone"]}}]}) //nor 
        3)update:
            db.<collection>.updateMany({<filter>}, {$set: {<update_fields>}})
            db.products.updateMany(
              { price: { $lt: 500 } }, // filter criteria
              { $inc: { stock: 10 } } // increment stock by 10
            );
            db.products.updateOne(
          { name: "Mouse" }, // filter criteria
          { $set: { price: 25, stock: 30 } }, // update operation
          { upsert: true } // create if not found
            );
            db.products.replaceOne(
          { name: "Tablet" }, // filter criteria
          { name: "Tablet", price: 350, stock: 20 } // new document
        );
        db.products.updateOne(
          { name: "Laptop" },
          { $addToSet: { tags: "portable" } }//push if you want deplicate
        );
        db.products.updateOne(
          { name: "Laptop" },
          { $pullAll: { tags: ["old", "obsolete"] } }
        );
        db.products.updateOne(
      { name: "Laptop" },
      { $push: { tags: { $each: ["new", "sale"] } } }
        );
        db.products.updateMany(
      { name: "Laptop" }, // filter criteria
      { $unset: { field: "" } }
    );
    4)delete:
        db.products.deleteMany({});
    ///////////////////////////////////////////////////
    db.products.updateMany(
  {
    $and: [
      {
        $or: [
          { status: 1 },
          { status: 2 }
        ]
      },
      { category: "A" }
    ]
  },
  {
    $set: { price: 150 } // التحديث المطلوب
  }
);
///////////////////////////////////////////////
{
  "_id": 1,
  "name": "Mouss",
  "address": {
    "city": "Casablanca",
    "country": "Morocco",
    "postalCode": "20000"
  },
  "hobbies": ["reading", "traveling", "coding"]
}


db.users.find({
  "address.city": "Casablanca"
});

db.users.find({
  hobbies: "coding"
});
db.users.find({
  "address.city": { $regex: /^C/ }
});

//////////////////////////////


{
  "_id": 1,
  "title": "MongoDB Nested Arrays",
  "comments": [
    {
      "text": "Great post!",
      "tags": ["mongodb", "database", "nosql"],
      "author": "Alice"
    },
    {
      "text": "Very helpful, thanks!",
      "tags": ["mongodb", "tutorial"],
      "author": "Bob"
    }
  ]
}

db.posts.find({
  comments: {
    $elemMatch: {
      tags: "mongodb",
      author: "Alice"
    }
  }
})

db.posts.find({
  "comments.tags": {
    $all: ["mongodb", "database"]
  }
})

/////////////////////////////
    const cursor = db.users.find({ status: "active" });
    cursor.forEach(user => {
    print(`User: ${user.name}, Status: ${user.status}`);
    });
/////////////////////////////
db.products.aggregate([
  // 1. Filter: only active products
  { $match: { status: "active" } },
  // 2. Group: sum sales by category
  { $group: {
      _id: "$category",
      totalSales: { $sum: "$sales" }
  }},
  // 3. Sort: highest sales first
  { $sort: { totalSales: -1 } },
  // 4. Project: rename fields for clarity
  { $project: {
      category: "$_id",
      totalSales: 1, croissant
      _id: 0
  }}
])

