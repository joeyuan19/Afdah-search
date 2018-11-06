import sqlite3
import traceback

DB_NAME = 'afdah_library'

def write_err(err):
    print err
    print traceback.format_exc()

def execute(f,*args):
    try:
        conn = sqlite3.connect(DB_NAME, timeout = 10)
        cur = conn.cursor()
        val = None
        try:
            val = f(cur,*args)
        except:
            write_err(traceback.format_exc())
            raise
        finally:
            conn.commit()
            conn.close()
        return val
    except sqlite3.OperationalError:
        return None
