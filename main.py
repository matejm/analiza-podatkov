from download_data import DataGetter
from clean_data import load_names, clean_data


d = DataGetter(debug=False)
d.get_data()
d.cleanup()

load_names()
clean_data(d.DOWNLOAD_DIRECTORY, 'data/cleaned', 'data.csv')
