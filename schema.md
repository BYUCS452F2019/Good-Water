## Good-Water Project Schema

Users (UserID, FirstName, LastName, Password, Email, Gender)

Campuses (CampusID, City, State, CampusName)

Buildings (BuildingID, BuildingName, Longitude, Latitude, CampusID)

- Foreign Key CampusID references Campuses

WaterFountains (WaterFountainID, BuildingID)

- Foreign Key BuildingID references Buildings

Ratings (RatingID, Score, Date, WaterFountainID, UserID)

- Foreign Key WaterFountainID references WaterFountains
- Foreign Key UserID references Users



### Explanations of table names, representations, relations, normalization and column names
Users

- Table Name: This name communicates that this table contains information about many users
- Representation: This table represents all the users who will use our product
- Relation: This table has no foreign keys, however, the ratings table will have a foreign key to this table’s UserID field because each rating will be submitted by a user
- Normalization: Instead of having a “ratings” field in this table and adding a rating each time the same user submits different ratings, normalization is implemented by making a seperate ratings table which references the UserID column
- Column Names:
 - UserID: A unique identifier given to each user
 - FirstName: First name of the user
 - The rest of the column names follow this pattern

Campuses

- Table Name: This name communicates that this table will contain information about the BYU campuses at a campus level
- Representation: This table represents all the BYU campuses
- Relation: This table has no foreign keys, however, the buildings table will have a foreign key to this table’s CampusID field because each building belongs to a Campus
- Normalization: Same concept, instead of adding a buildings field to this table and changing that field everytime there’s a new building, we just add a building row in the building table and reference the campusid field here
- Column Names:
 - CampusID: A unique identifier for each campus
 - City: Provo, Laie, Rexburg etc.
 - State: Utah, Idaho etc
 - CampusName: “BYU-Provo”, “BYU-Idaho” etc

Buildings

- Table Name: This name communicates that it represents buildings throughout the different BYU campuses
- Representation: Each row would represent one building
- Relation: This building has a foreign key reference to Campus because each building belongs to a campus and waterFountain references this table’s id field because each water fountain belongs to a building
- Normalization: We use normalization here by not adding a “fountains” field which changes every time a fountain is added or removed, instead the fountain table references the building id
- Column Names:
 - BuildingID: Unique identifier for each buliding
 - Building Name: JFSB, JSB etc.
 - Longitude: 35degrees etc.
 - Latitude: 35degrees etc.
 - CampusID: References the CampusID so like “4” if BYU-Provo had a campus ID of 4

WaterFountains

- Table Name: This name communicates that it contains information about each water fountain
- Representation: Each row of this table would represent one water fountain
- Relation: This has a foreign key to building because each water fountain belongs to a building
- Normalization: We use normalization here by not adding a “fountain” field to the buildings table and changing that field every time a water fountain is added or removed from a building. Instead we make a new row for each new water fountain and reference the buildingID as a foreign key
- Column Names:
 - WaterFountainID: Unique identifier for each water fountain
 - BuildingID: References the building ID to which this water fountain belongs

Ratings

- Table Name: This name communicates that this table contains information about all the ratings
- Representation: Each row would represent an individual rating specific to the time and place
- Relation: This table references UserID because each rating is submitted by a user as well as WaterFountainID because each rating is about a certain water fountain
- Normalization: Again, we use normalization here by not adding a “ratings” field into the waterFountain table and updating that field whenever a new rating is supplied, instead we make a new row here and reference the waterFountain ID
- Column Names:
 - RatingID: Unique id for each rating
 - Score: A score 1-5 inclusive about the water’s goodness
 - Date: The date the rating was submitted
 - WaterFountainID: the Id of the water fountain being scored
 - UserID: the id of the user submitting the rating

#### A simplified way to look at it

Campuses

- Campus ID
- City
- State
- Name

Buildings

- Foreign key to Campus ID
- Building ID
- Building Name
- Longitude
- Latitude

Water_Fountains

- Foreign key to Building ID
- Water Fountain ID

Ratings

- Foreign key to Water Fountain
- Foreign key to User ID
- RatingID
- Score
- Date

Users

- User ID
- FirstName
- LastName
- Password
- Email
- Gender
