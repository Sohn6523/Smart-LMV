import datetime as dt
import pymysql


class DB:
    def __init__(self, host, port, db, user, pwd) -> None:
        self.conn = None
        self.cursor = None
        self.init(host, port, db, user, pwd)

    def __enter__(self):
        return self

    def execute(self, query):
        self.cursor.execute(query)

    def commit(self):
        self.conn.commit()

    def fetchall(self):
        return self.cursor.fetchall()

    def init(self, host, port, db, user, pwd):
        self.conn = pymysql.connect(
            host=host, db=db, user=user, password=pwd, port=port, charset="utf8")
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.close()
        self.cursor = None

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

def query_get_id(browsepath):
    return f'SELECT id FROM namekeyinfo WHERE browsePath="{browsepath}";'

def query_get_thdval(phase, id, start_date, end_date=None):
    phase = phase.lower()

    start, end = _convert_daterange(start_date, end_date)    

    return f'SELECT timestamp, value, `minValue`, `maxValue`, "{phase.upper()}" as `phase` FROM analyticsthdi{phase}1min WHERE id="{id}" AND timestamp >= "{start}" AND timestamp < "{end}";'

def query_get_thdval_h_m_timestamp(phase, id, start_date, end_date=None):
    phase = phase.lower()

    start, end = _convert_daterange(start_date, end_date)    

    return f'SELECT date_format(timestamp, "%Y-%m-%d %H:%m"), value, `minValue`, `maxValue`, "{phase.upper()}" as `phase` FROM analyticsthdi{phase}1min WHERE id="{id}" AND timestamp >= "{start}" AND timestamp < "{end}";'


def query_get_tddval(phase, id, start_date, end_date=None):
    phase = phase.lower()

    start, end = _convert_daterange(start_date, end_date)    

    return f'SELECT timestamp, value, `minValue`, `maxValue`, "{phase.upper()}" as `phase` FROM analyticstddi{phase}1min WHERE id="{id}" AND timestamp >= "{start}" AND timestamp < "{end}";'

def query_get_currentval(phase, id, start_date, end_date=None):
    phase = phase.lower()

    start, end = _convert_daterange(start_date, end_date)    

    return f'SELECT timestamp, value, `minValue`, `maxValue`, "{phase.upper()}" as `phase` FROM analyticsi{phase}1min WHERE id="{id}" AND timestamp >= "{start}" AND timestamp < "{end}";'

def query_get_voltageval(phase, id, start_date, end_date=None):
    phase = phase.lower()

    start, end = _convert_daterange(start_date, end_date)    

    return f'SELECT timestamp, value, `minValue`, `maxValue`, "{phase.upper()}" as `phase` FROM analyticsv{phase}1min WHERE id="{id}" AND timestamp >= "{start}" AND timestamp < "{end}";'

def query_get_other(tablename, id, start_date, end_date=None):
    start, end = _convert_daterange(start_date, end_date)    

    return f'SELECT timestamp, value, `minValue`, `maxValue` FROM {tablename} WHERE id="{id}" AND timestamp >= "{start}" AND timestamp < "{end}";'

def _convert_daterange(start, end=None):
    if end is None:
        start_date = dt.datetime.strptime(start, "%Y-%m-%d")
        end_date = start_date + dt.timedelta(days=1)
    else:
        end_date = dt.datetime.strptime(end, "%Y-%m-%d")
        end_date = end_date + dt.timedelta(days=1)
        
    end_date = end_date.strftime("%Y-%m-%d")
        
    return start, end_date