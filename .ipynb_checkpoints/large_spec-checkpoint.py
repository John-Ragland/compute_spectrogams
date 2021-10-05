import pickle
import ooipy
import spec_tools

spec_dir = '/Volumes/Ocean_Acoustics/Spectrograms/Central_Caldera/2017/'
spec = spec_tools.merge(0,3000, spec_dir=spec_dir, verbose=False)

file_name = '/Volumes/Ocean_Acoustics/Spectrograms/Central_Caldera/2017_full_spec.pkl'

with open(file_name, 'wb') as f:
    pickle.dump(spec, f)