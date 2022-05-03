Some generic notes about the solution:

User Access
1) We added the access list in the users collection itself. The main use case is picking one user info at a time for validation. Picking information about all users in an admin interface would also mostly be for device access changes. So the primary access use cases for a user require device access information. Hence, in this particular case, there isn't too much of a retrieval cost to store it in the same collection, the benefit being a simpler class structure. In any case, if the device list truly starts getting large, the correct notion would be to map users to groups of devices rather than individual large device listings.
2) The attributes did and atype are not as expressive as device_id and access_type, but they help save some storage cost as they are being repeated in the db for each user-device pairing
3) {did: "DT001", atype: "r"} is preferable over {"DT001": "r"} for creating indexes for faster access.


Service Layer
1) There are multiple ways to structure the validation checks in various models. 
    - A user name or a supplemental LoginManager can be passed in each call for all models
	- A singleton LoginManager or UserService can be easily accessed from everywhere. It's not generally advisable to use a Singleton for shared state
	- Different authorization types (admin, rw, read) can be implemented as decorators and used as annotations for various methods
	- A service layer can be created which handles authorization and can handle other business constraints like, say, a limit on the amount of data that can be fetched at a time. We went with this approach and tied the username to the service objects at creation. This provides an extensible solution. Keeping each object tied to a particular username also makes it cleaner. A new user access would normally not share objects in any case.
2) The service layer can have its own errors and will have to check and pass on errors from the model layer itself. These things are generally done by hierarchical exception handling. We haven't introduced that in this solution as it's a topic not discussed in detail in the course.


Reports
1) In normal production implementation, a cron job or equivalent will run every x days and aggregate data for the last x days. Since we are mimicking that here, we have implemented a one-shot aggregator which goes through all the data in the collection
2) The standard way of calculating average and other values after grouping the data is done in the app, so in python in this case. But MongoDB provides a very powerful aggregation pipeline functionality which makes it possible to do the aggregation in Mongo itself. We have implemented both versions just for demonstration. You can see them in __aggregate_data_mdb and __aggregate_data_py methods in the DailyReportService
3) You can see advanced searches based on complicated keys for both date range based search in reports ({'device_id': device_id, 'date': {'$gte': from_date, '$lte': to_date}}) and in device access query in user model ({'username': user_name, 'alist': {'$elemMatch': {'did': device_id, 'atype': {'$in': access_type_list}}}}) These are some of the ways you can query MongoDB in a deeper way similar to how relational databases can use various sql constructs like group by, join, between, etc.
