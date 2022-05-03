from model import UserModel, DeviceModel, WeatherDataModel, DailyReportModel
import math, datetime

# user service for user model manipulation and for access control validations
class UserService:

    ADMIN_ROLE = 'admin'
    DEFAULT_ROLE = 'default'
    READ_ACCESS = 'r'
    RW_ACCESS = 'rw'
    
    # Attaches user name in creation so that it can be used for validation of all calls
    # Also creates an instance of UserModel to be called internally
    def __init__(self, user_name):
        self._user_name = user_name
        self._latest_error = ''
        self._model = UserModel()
    
    # Latest error is used to store the error string in case an issue. It's reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error
    
    # Check to validate if the username attached at construction is an admin
    def has_admin_access(self):
        user = self._model.find_by_username(self._user_name)
        return (user['role'] == UserService.ADMIN_ROLE)
        
    # Check to see if the user has read write access to a particular device id
    def has_rw_access(self, device_id):
        user = self._model.find_by_did_access(self._user_name, device_id, [UserService.RW_ACCESS])
        if (user):
            return True
        else:
            return False
    
    # Check to see if the user has read access to a particular device id
    # rw access includes read access so both need to be checked
    def has_read_access(self, device_id):
        user = self._model.find_by_did_access(self._user_name, device_id, [UserService.READ_ACCESS, UserService.RW_ACCESS])
        if (user):
            return True
        else:
            return False
    
    # Wrapper over model function with authorization check, only admins allowed to query users
    def find_by_username(self, username):
        self._latest_error = ''
        if (not self.has_admin_access()):
            self._latest_error = f'Query failed, Admin access required!'
            return -1
        
        return self._model.find_by_username(username)
    
    def find_by_object_id(self, obj_id):
        self._latest_error = ''
        if (not self.has_admin_access()):
            self._latest_error = f'Query failed, Admin access required!'
            return -1
        
        return self._model.find_by_object_id(obj_id)    
    
    # Wrapper over model function with authorization check, only admins allowed to insert users
    def insert(self, username, email, role, access_list):
        self._latest_error = ''
        if (not self.has_admin_access()):
            self._latest_error = f'Insert failed, Admin access required!'
            return -1
        
        user_doc = self._model.insert(username, email, role, access_list)
        if (user_doc == -1):
            self._latest_error = self._model.latest_error
        return user_doc
        
        
class DeviceService:
    
    # Attaches user service in creation so that it can be used for validation of all calls
    # Also creates an instance of DeviceModel to be called internally
    def __init__(self, user_service):
        self._user_service = user_service
        self._latest_error = ''
        self._model = DeviceModel()
    
    # Latest error is used to store the error string in case an issue. It's reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error
    
    # Wrapper over model function with authorization check, only admins or 
    # normal users with read access to the device allowed to query device info
    def find_by_device_id(self, device_id):
        self._latest_error = ''
        if (not (self._user_service.has_admin_access() or self._user_service.has_read_access(device_id))):
            self._latest_error = f'Read access not allowed to {device_id}'
            return -1
        
        return self._model.find_by_device_id(device_id)
    
    # Wrapper over model function with authorization check, only admins allowed to create new devices
    # Normal users can't have any access mapped to a device that doesn't yet exist
    def insert(self, device_id, desc, type, manufacturer):
        self._latest_error = ''
        if (not self._user_service.has_admin_access()):
            self._latest_error = f'Insert failed, Admin access required!'
            return -1
        
        device_doc = self._model.insert(device_id, desc, type, manufacturer)
        if (device_doc == -1):
            self._latest_error = self._model.latest_error
        return device_doc
    
class WeatherDataService:
    
    # Attaches user service in creation so that it can be used for validation of all calls
    # Also creates an instance of WeatherDataModel to be called internally
    def __init__(self, user_service):
        self._user_service = user_service
        self._latest_error = ''
        self._model = WeatherDataModel()
    
    # Latest error is used to store the error string in case an issue. It's reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error
    
    # Wrapper over model function with authorization check, only admins or 
    # normal users with read access to the device allowed to query device weather data
    def find_by_device_id_and_timestamp(self, device_id, timestamp):
        self._latest_error = ''
        if (not (self._user_service.has_admin_access() or self._user_service.has_read_access(device_id))):
            self._latest_error = f'Read access not allowed to {device_id} data'
            return -1
        
        return self._model.find_by_device_id_and_timestamp(device_id, timestamp)
    
    # Wrapper over model function with authorization check, only admins are allowed
    # to run pipelines across all device weather data
    def aggregate(self, pipeline):       
        self._latest_error = ''
        if (not self._user_service.has_admin_access()):
            self._latest_error = f'Only admins can run aggregate'
            return -1
        
        wdata_docs = self._model.aggregate(pipeline)
        return wdata_docs


    # Wrapper over model function with authorization check, only admins or 
    # normal users with read-write access to the device allowed to insert device weather data
    def insert(self, device_id, value, timestamp):
        self._latest_error = ''
        if (not (self._user_service.has_admin_access() or self._user_service.has_rw_access(device_id))):
            self._latest_error = f'Insert failed, Write access not allowed for {device_id} data'
            return -1
        
        wdata_doc = self._model.insert(device_id, value, timestamp)
        if (wdata_doc == -1):
            self._latest_error = self._model.latest_error
        return wdata_doc
    
class DailyReportService:

    # Attaches user service in creation so that it can be used for validation of all calls
    # Also creates an instance of DailyReportModel to be called internally
    def __init__(self, user_service):
        self._user_service = user_service
        self._latest_error = ''
        self._model = DailyReportModel()
    
    # Latest error is used to store the error string in case an issue. It's reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error

    # Wrapper over model function with authorization check, only admins or 
    # normal users with read access to a specific device are allowed
    # to query specific device daily report data
    def find_by_device_id_and_date(self, device_id, date):
        self._latest_error = ''
        if (not (self._user_service.has_admin_access() or self._user_service.has_read_access(device_id))):
            self._latest_error = f'Read access not allowed to {device_id} daily report data'
            return -1
        
        dr_doc = self._model.find_by_device_id_and_date(device_id, date)
        return {'device_id': dr_doc['device_id'], 'avg_value': dr_doc['avg_value'], 'min_value': dr_doc['min_value'], 'max_value': dr_doc['max_value'], 'date': dr_doc['date'].date().isoformat()}
    
    # Wrapper over model function with authorization check, only admins or 
    # normal users with read access to a specific device are allowed
    # to query specific device daily report data for a date range
    def find_by_device_id_and_date_range(self, device_id, from_date, to_date):
        self._latest_error = ''
        if (not (self._user_service.has_admin_access() or self._user_service.has_read_access(device_id))):
            self._latest_error = f'Read access not allowed to {device_id} daily report data'
            return -1
        
        dr_docs = self._model.find_by_device_id_and_date_range(device_id, from_date, to_date)
        dr_data = []
        for dr_doc in dr_docs:
            dr_single = {'device_id': dr_doc['device_id'], 'avg_value': dr_doc['avg_value'], 'min_value': dr_doc['min_value'], 'max_value': dr_doc['max_value'], 'date': dr_doc['date'].date().isoformat()}
            dr_data.append(dr_single)
        return dr_data

    # Wrapper over model function with authorization check, only admins or 
    # normal users with read-write  access to a specific device are allowed
    # to insert specific device daily report data
    def insert(self, device_id, avg_value, min_value, max_value, date):
        self._latest_error = ''
        if (not (self._user_service.has_admin_access() or self._user_service.has_rw_access(device_id))):
            self._latest_error = f'Insert failed, Write access not allowed for {device_id} daily report data'
            return -1
        
        dr_doc = self._model.insert(device_id, avg_value, min_value, max_value, date)
        if (dr_doc == -1):
            self._latest_error = self._model.latest_error
        return dr_doc

    # Wrapper over model function with authorization check, only admins or 
    # normal users with read-write  access to a specific device are allowed
    # to insert specific device daily report data in bulk
    def insert_multiple(self, dr_docs):
        self._latest_error = ''
        if (not (self._user_service.has_admin_access())):
            self._latest_error = f'Bulk insert failed, only admins can do bulk insert'
            return -1
        
        dr_obj_ids = self._model.insert_multiple(dr_docs)
        return dr_obj_ids
        
    # One-shot weather data aggregation at a day level and insertion into the daily_report collection
    # Please note that there are two ways to aggregate - 
    # 1. Get all the data and do it in python
    # 2. Do the aggregation in Mongo itself using aggregation pipeline
    # Both methods are implemented and either can be used
    def create_reports(self):
        self._latest_error = ''
        if (not self._user_service.has_admin_access()):
            self._latest_error = f'Only admin can create reports'
            return -1

        dr_data = self.__aggregate_data_mdb()
        #dr_data = self.__aggregate_data_py()
        self.insert_multiple(dr_data)
        
        return True
    
    # Get data from mongo after relevant aggregation and return pre-created docs that can be bulk inserted
    def __aggregate_data_mdb(self):
        pipeline = [
            {
                '$group': {
                    '_id': {'device_id': '$device_id', 'date': {'$dateToString': {'format': '%Y-%m-%d', 'date': '$timestamp'}}},
                    'average': {'$avg': '$value'},
                    'min': {'$min': '$value'},
                    'max': {'$max': '$value'},

                }
            }
        ]
        wdata_model = WeatherDataModel()
        
        dr_data = []
        agg_docs = wdata_model.aggregate(pipeline)
        for agg_doc in agg_docs:
            dr_doc = {
                        'device_id': agg_doc['_id']['device_id'], 
                        'avg_value': round(agg_doc['average'], 2), 
                        'min_value': agg_doc['min'], 
                        'max_value': agg_doc['max'], 
                        'date': datetime.datetime.fromisoformat(agg_doc['_id']['date'])
                    }
            dr_data.append(dr_doc)
        return dr_data
    
    # Get data from mongo and do the aggregation in python, return pre-created docs that can be bulk inserted
    def __aggregate_data_py(self):
        wdata_model = WeatherDataModel()
        agg_data = {}
        for wdata in wdata_model.find_all():
            device_id = wdata['device_id']
            date = wdata['timestamp'].date()
            value = wdata['value']
            
            if (device_id not in agg_data):
                agg_data[device_id] = {}
            if (date not in agg_data[device_id]):
                agg_data[device_id][date] = {'sum': 0, 'count': 0, 'min': math.inf, 'max': -math.inf}
            
            agg_data[device_id][date]['sum'] += value
            agg_data[device_id][date]['count'] += 1
                    
            if (value < agg_data[device_id][date]['min']):
                agg_data[device_id][date]['min'] = value
            
            if (value > agg_data[device_id][date]['max']):
                agg_data[device_id][date]['max'] = value
        
        dr_data = []
        for device_id in agg_data:
            for date in agg_data[device_id]:
                dr_doc = {
                'device_id': device_id, 
                'avg_value': round(agg_data[device_id][date]['sum'] / agg_data[device_id][date]['count'], 2), 
                'min_value': agg_data[device_id][date]['min'], 
                'max_value': agg_data[device_id][date]['max'], 
                'date': datetime.datetime(date.year, date.month, date.day)
                }
                dr_data.append(dr_doc)
        
        return dr_data
                
            

