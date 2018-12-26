from sqlobject import *
from datetime import datetime
sqlhub.processConnection = connectionForURI(
    "mysql://siddi:extenso@123@10.13.198.251/OPERATION_DATA")


class file_process_log(SQLObject):
    component_command_string = StringCol()
    result_string = StringCol()
    log_path = StringCol()
    status = StringCol()
    action_method = StringCol()
    file_id = IntCol()
    client_id = IntCol()
    phase_id = IntCol()
    component_id = IntCol()
    processed_by = StringCol()
    processed_on = DateTimeCol()
    updated_by = StringCol()
    updated_on = DateTimeCol()
    comment = StringCol()


class file_repo(SQLObject):
    file_name = StringCol()
    file_path = StringCol()
    file_arrived_date = DateCol()
    is_incremental = StringCol()
    file_type = StringCol()
    client_id = IntCol()
    module_layout_id = IntCol()
    latest_phase_id = IntCol()
    active_flag = IntCol()
    created_by = StringCol()
    created_on = DateCol()
    updated_by = StringCol()
    updated_on = DateTimeCol()
    comment = StringCol()


print(datetime.now())
file_process_log(component_command_string="test()",
                 result_string="test", log_path="test", status="test", action_method="test", file_id=12, client_id=12, phase_id=12, component_id=12, processed_by="siddi", processed_on=datetime.now(), updated_by='siddi', updated_on=datetime.now(), comment="test")
