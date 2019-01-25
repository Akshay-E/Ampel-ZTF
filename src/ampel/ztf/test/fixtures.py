
from os.path import abspath, join, dirname
import pytest

@pytest.fixture(scope='session')
def alert_tarball():
	return join(dirname(__file__), 'test-data', 'ztf_public_20180819_mod1000.tar.gz')

@pytest.fixture(scope='session')
def alert_generator(alert_tarball):
	import itertools
	import fastavro
	from ampel.pipeline.t0.load.TarballWalker import TarballWalker
	def alerts(with_schema=False):
		atat = TarballWalker(alert_tarball)
		for fileobj in itertools.islice(atat.get_files(), 0, 1000, 1):
			reader = fastavro.reader(fileobj)
			alert = next(reader)
			if with_schema:
				yield alert, reader.schema
			else:
				yield alert
	return alerts

@pytest.fixture(scope='session')
def lightcurve_generator(alert_generator):
	from ampel.ztf.utils.ZIAlertUtils import ZIAlertUtils
	def lightcurves():
		for alert in alert_generator():
			lightcurve = ZIAlertUtils.to_lightcurve(content=alert)
			assert isinstance(lightcurve.get_photopoints(), tuple)
			yield lightcurve

	return lightcurves