from database_logger import phase_component

class DParser:
    def check_dep(self,latest_phase,current_phase):
        current_phase_cmp = phase_component.get(current_phase)
        if latest_phase == current_phase_cmp.dependent_phase_id:
            return True
        else:
            return False
            
'''
dparser = DParser()
print(dparser.check_dep(0,1))
'''