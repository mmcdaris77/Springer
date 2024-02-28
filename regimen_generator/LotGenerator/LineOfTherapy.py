from datetime import date, timedelta


class Drug():
    def __init__(self, person_id: str, drug_name: str, start_dt: date, end_dt: date = None, drug_class: str = '',
                 drug_type: str = '', therapy_route: str = '') -> None:
        self.person_id: str = person_id
        self.drug_name: str = drug_name
        self.drug_class: str = drug_class
        self.drug_type: str = drug_type
        self.therapy_route: str = therapy_route
        self.start_dt: date = start_dt
        self.end_dt: date = self.default_end_date(end_dt)
    
    def default_end_date(self, end_dt): 
        if end_dt is None:
            return self.start_dt
        else:
            return end_dt

    def __str__(self) -> str:
        return f'Drug: {self.drug_name} --> StartDate: {self.start_dt} --> EndDate: {self.end_dt}'

class OtherTherapy():
    def __init__(self, person_id: str, therapy_name: str, start_dt: date, end_dt: date = None) -> None:
        self.person_id: str = person_id
        self.therapy_name: str = therapy_name
        self.start_dt: date = start_dt
        self.end_dt: date = self.default_end_date(end_dt)
    
    def default_end_date(self, end_dt): 
        if end_dt is None:
            return self.start_dt
        else:
            return end_dt

    def __str__(self) -> str:
        return f'Drug: {self.drug_name} --> StartDate: {self.start_dt} --> EndDate: {self.end_dt}'
    

class LineOfTherapy():
    def __init__(self, lot: int, drugs: list[Drug] = None, is_maint: bool = False) -> None: 
        self.lot: int = lot
        self.drugs: list[Drug] = drugs
        self.start: date 
        self.end: date
        self.is_maint: bool = is_maint
        self.lot_rule: str
        self.lot_flags: dict = {}

        self.set_start_date()
        self.set_end_date()


    def set_end_date(self, offset: int = 0): 
        _max_end_dt = max(self.drugs, key=lambda x:x.end_dt).end_dt
        _max_start_dt = max(self.drugs, key=lambda x:x.start_dt).start_dt
        self.end = (max(_max_end_dt, _max_start_dt) + timedelta(days=offset))

    def set_start_date(self):
        self.start = min(self.drugs, key=lambda x:x.start_dt).start_dt

    def add_drugs(self, drug_list: list[Drug]): 
        self.drugs += drug_list
        self.set_end_date()

    def get_regimen(self, as_string: bool = False) -> (str | list[str]):
        regimen = sorted(list(set([d.drug_name for d in self.drugs])))
        if as_string:
            return ','.join(regimen)
        else:
            return regimen 
        
    def get_classes(self, as_string: bool = False) -> (str | list[str]):
        classes = sorted(list(set([d.drug_class for d in self.drugs])))
        if as_string:
            return ','.join(classes)
        else:
            return classes 

    def is_mono_therapy(self):
        if len(self.get_regimen()) == 1:
            return True 
        else:
            return False
        
    def add_lot_flag_true(self, flag_name: str, lot_num: int = None) -> None:
        if not flag_name is None:
            self.lot_flags[flag_name] = True

    def add_lot_flag_false(self, flag_name: str, lot_num: int = None) -> None:
        if not flag_name is None:
            self.lot_flags[flag_name] = False

    def add_lot_flag_value(self, flag_name: str, flag_value: object, lot_num: int = None) -> None:
        if not flag_name is None:
            self.lot_flags[flag_name] = flag_value

    def adjust_lot_end(self, num_days: int, next_lot_start: date = None): 
        '''
            post process action: 
            add up to num_days or the day prior to the next lot
        '''
        self.set_end_date()
        add_days = timedelta(days=num_days)
        new_end = self.end + add_days
        if not next_lot_start is None and new_end >= next_lot_start:
            self.end = next_lot_start - timedelta(days=1)
        else:
            self.end = new_end    
                
        
    def __str__(self) -> str:
        rtn = f'LineOfTherapy: \
                    \n\tlot: {self.lot} \
                    \n\tstart: {self.start} \
                    \n\tend: {self.end} \
                    \n\tdrug_cnt: {len(self.drugs)} \
                    \n\tregimen: {self.get_regimen()} \
                    \n\tflags: {self.lot_flags} \
                '
        rtn += '\n'+'-'*60
        for d in self.drugs:
            rtn += f'\n\t\t{d}'
        return rtn


