from datetime import date, timedelta


class Drug():
    def __init__(self, person_id: str, drug_name: str, start_dt: date, end_dt: date = None) -> None:
        self.person_id: str = person_id
        self.drug_name: str = drug_name
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
        self.other_therapy: list = []

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

    def get_regimen(self, as_string: bool = False):
        regimen = sorted(list(set([d.drug_name for d in self.drugs])))
        if as_string:
            return ','.join(regimen)
        else:
            return regimen 

    def is_mono_therapy(self):
        if len(self.get_regimen()) == 1:
            return True 
        else:
            return False
        
    def __str__(self) -> str:
        rtn = f'LineOfTherapy: \
                    \n\tlot: {self.lot} \
                    \n\tstart: {self.start} \
                    \n\tend: {self.end} \
                    \n\tdrug_cnt: {len(self.drugs)} \
                    \n\tregimen: {self.get_regimen()} \
                '
        return rtn

