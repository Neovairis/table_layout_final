from sqlobject import *
from datetime import datetime
sqlhub.processConnection = connectionForURI(
    r"mysql://siddi:extenso@123@10.13.198.251/OPERATION_DATA")


class component(SQLObject):
    component = StringCol()
    success_comp_id = StringCol()
    failed_comp_id = StringCol()    
    command_string = StringCol() 
    num_of_param = StringCol() 
    param1 = StringCol()
    param2 = StringCol()
    param3 = StringCol()
    param4 = StringCol()
    param5 = StringCol()
    active_flag = IntCol()
    created_by = StringCol()
    created_on = DateCol()
    updated_by = StringCol()
    updated_on = DateCol()
    comment = StringCol()

class client(SQLObject):
    client_code = StringCol()
    client_name = StringCol()
    client_address  = StringCol()
    client_contact_number =IntCol()
    client_contact_person  = StringCol()
    client_email  = StringCol()
    client_website  = StringCol()
    client_num_of_brnch =IntCol()
    client_pan = IntCol()
    client_fax_number = IntCol() 
    active_flag = IntCol()
    created_by = StringCol()
    created_on = DateCol()
    updated_by  = StringCol()
    updated_on = DateCol()
    comment = StringCol()

class file_process_log(SQLObject):
    component_command_string = StringCol()
    result_string = StringCol()
    log_path = StringCol()
    status = StringCol(default = 'FAILURE')
    action_method = StringCol()
    file= ForeignKey('file_repo')
    client = ForeignKey('client')
    phase = ForeignKey('phase')
    component = ForeignKey('component')
    processed_by = StringCol(default = "SYSTEM")
    processed_on = DateTimeCol(default = datetime.now())
    updated_by = StringCol(default = "SYSTEM")
    updated_on = DateTimeCol(default = datetime.now())
    comment = StringCol(default = "AUTOMATIC")

class file_repo(SQLObject):
    file_name = StringCol()
    file_path = StringCol(default = None)
    file_arrived_date = DateCol()
    is_incremental = StringCol(length = 5,default = None)
    file_type = StringCol()
    client = ForeignKey('client')
    module_layout = ForeignKey('module_layout')
    latest_phase = ForeignKey('phase')
    active_flag = IntCol(default = 1)
    created_by = StringCol(default = 'SYSTEM')
    created_on = DateTimeCol(default = datetime.now())
    updated_by = StringCol(default = 'SYSTEM')
    updated_on = DateTimeCol(default = datetime.now())
    comment = StringCol(default = 'AUTOMATIC')

class layout(SQLObject):
    layout = StringCol()
    layout_desc  = StringCol()
    num_of_var = IntCol()
    delimiters  = StringCol()
    active_flag =IntCol()
    created_by = StringCol()
    created_on = DateTimeCol()
    updated_by = StringCol()
    updated_on = DateTimeCol()
    comment  = StringCol()
    target_table = StringCol()

class product(SQLObject):
    product_desc = StringCol()
    active_flag = IntCol()
    created_by = StringCol()
    created_on = DateTimeCol()
    updated_by = StringCol()
    updated_on = DateTimeCol()
    comment = StringCol()

class phase(SQLObject):
    phase = StringCol()
    active_flag = IntCol()
    created_by  = StringCol()
    created_on = DateTimeCol()
    updated_by = StringCol()
    updated_on = DateTimeCol()
    comment = StringCol()

class phase_component(SQLObject):
    next_phase_id = IntCol()
    dependent_phase_id = IntCol()
    is_synchronous = StringCol()
    wait_time  = StringCol()
    phase = ForeignKey('phase')
    component  = ForeignKey('component')
    active_flag = IntCol()
    created_by = StringCol()
    created_on = DateTimeCol()
    updated_by = StringCol()
    updated_on = DateTimeCol() 
    comment = StringCol()

class modules(SQLObject):
    module = StringCol() 
    module_desc = StringCol() 
    product  = ForeignKey('product')
    active_flag = IntCol()
    created_by  = StringCol() 
    created_on  = DateTimeCol()
    updated_by = StringCol() 
    updated_on= DateTimeCol()
    comment = StringCol() 

class module_layout(SQLObject):
    module_layout_desc = StringCol()
    module = ForeignKey('module')
    layout   = ForeignKey('layout')
    active_flag  = IntCol()
    created_by  = StringCol()
    created_on  = DateTimeCol()
    updated_by  = StringCol()
    updated_on  = DateTimeCol()
    comment  = StringCol()

'''
fr = file_repo(file_name = 'ss',file_path = '',file_arrived_date = datetime.now(),client = 1, module_layout = 1,is_incremental = 'y' ,latest_phase = 1,file_type = 'csv',comment = 'test')

#+
#fr = file_repo.selectBy(file_name = "gime_loan_bad_debt_11232018")

print(fr.id)
'''