% Read Spectrograms

filename = 'spectrogram001.pkl';
fid=py.open(filename,'rb');
data=py.pickle.load(fid);


spec_path = 'path_to_spectrogram';
month_start = ([0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])*24;

k = 1;
spec_start = int16(month_start(k));
spec_end = int16(month_start(k+1));

spec = py.merge_spectrogram.merge(spec_start, spec_end);


% times = double(py.numpy.array(spec(1)));
freq = double(py.numpy.array(spec(2)));
values = squeeze(double(py.numpy.array(spec(3))));



%%

