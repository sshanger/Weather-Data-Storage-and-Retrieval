from service import UserService, DeviceService, WeatherDataService, DailyReportService
import datetime


# admin access path for problem 1
user_service = UserService('admin')
device_service = DeviceService(user_service)
wdata_service = WeatherDataService(user_service)
daily_report_service = DailyReportService(user_service)

print('Does \'admin\' have admin access?')
print(user_service.has_admin_access(), end='\n\n')


print('Is username based query possible for \'admin\'?')
user_doc = user_service.find_by_username('user_2')
if (user_doc == -1):
    print(user_service.latest_error, end='\n\n')
else:
    print(user_doc, end='\n\n')

print('Can \'admin\' add a new user?')
user_doc = user_service.insert('user_3', 'user_3@example.com', 'default', [{'did':'DT004','atype':'r'},{'did':'DH003','atype':'rw'}])
if (user_doc == -1):
    print(user_service.latest_error, end='\n\n')
else:
    print(user_doc, end='\n\n')

print('Can \'admin\' access device DT004?')
device_doc = device_service.find_by_device_id('DT004')
if (device_doc == -1):
    print(device_service.latest_error, end='\n\n')
else:
    print(device_doc, end='\n\n')

print('Can \'admin\' create device DT201?')
device_doc = device_service.insert('DT201', 'Temperature Sensor', 'Temperature', 'Acme')
if (device_doc == -1):
    print(device_service.latest_error, end='\n\n')
else:
    print(device_doc, end='\n\n')

print('Can \'admin\' read DT001 device data?')
wdata_doc = wdata_service.find_by_device_id_and_timestamp('DT001', datetime.datetime(2020, 12, 2, 13, 30, 0))
if (wdata_doc == -1):
    print(wdata_service.latest_error, end='\n\n')
else:
    print(wdata_doc, end='\n\n')

# admin access path for problem 2
print('Generate daily reports')
daily_report_service.create_reports()

print('Get daily report for one day')
daily_report = daily_report_service.find_by_device_id_and_date('DT004', datetime.datetime(2020, 12, 2))
print(daily_report, end='\n\n')

print('Get daily report for multiple days')
daily_reports = daily_report_service.find_by_device_id_and_date_range('DT004', datetime.datetime(2020, 12, 2), datetime.datetime(2020, 12, 4))
print(daily_reports, end='\n\n')

    

# default (user_1) access path for problem 1
user_service = UserService('user_1')
device_service = DeviceService(user_service)
wdata_service = WeatherDataService(user_service)

print('Does \'user_1\' have admin access?')
print(user_service.has_admin_access(), end='\n\n')

print('Is username based query possible for \'user_1\'?')
user_doc = user_service.find_by_username('user_2')
if (user_doc == -1):
    print(user_service.latest_error, end='\n\n')
else:
    print(user_doc, end='\n\n')

print('Can \'user_1\' add a new user?')
user_doc = user_service.insert('user_3', 'user_3@example.com', 'default', [{'did':'DT004','atype':'r'},{'did':'DH003','atype':'rw'}])
if (user_doc == -1):
    print(user_service.latest_error, end='\n\n')
else:
    print(user_doc, end='\n\n')

print('Can \'user_1\' access device DT004?')
device_doc = device_service.find_by_device_id('DT004')
if (device_doc == -1):
    print(device_service.latest_error, end='\n\n')
else:
    print(device_doc, end='\n\n')
    
print('Can \'user_1\' access device DT001?')
device_doc = device_service.find_by_device_id('DT001')
if (device_doc == -1):
    print(device_service.latest_error, end='\n\n')
else:
    print(device_doc, end='\n\n')

print('Can \'user_1\' create device DT202?')
device_doc = device_service.insert('DT202', 'Temperature Sensor', 'Temperature', 'Acme')
if (device_doc == -1):
    print(device_service.latest_error, end='\n\n')
else:
    print(device_doc, end='\n\n')

print('Can \'user_1\' read DT001 device data?')
wdata_doc = wdata_service.find_by_device_id_and_timestamp('DT001', datetime.datetime(2020, 12, 2, 13, 30, 0))
if (wdata_doc == -1):
    print(wdata_service.latest_error, end='\n\n')
else:
    print(wdata_doc, end='\n\n')

print('Can \'user_1\' read DT002 device data?')
wdata_doc = wdata_service.find_by_device_id_and_timestamp('DT002', datetime.datetime(2020, 12, 2, 13, 30, 0))
if (wdata_doc == -1):
    print(wdata_service.latest_error, end='\n\n')
else:
    print(wdata_doc, end='\n\n')

