import tempfile, glob, datetime, os
from pathlib import Path

class CertCheck:
	def __init__(self):
		self.__updateDate()

	def __niceTime(unixTime):
		return datetime.datetime.fromtimestamp(unixTime).strftime('%d-%m-%Y %H:%M:%S')

	def __getNewestCertFileDate():
		certFiles = glob.glob('/etc/letsencrypt/**/*', recursive=True)
		if len(certFiles) == 0:
			return None
		newestModifiedDate = -1
		for certFilePath in certFiles:
			fileTime = os.path.getmtime(certFilePath)
			if fileTime > newestModifiedDate:
				newestModifiedDate = fileTime
		return newestModifiedDate

	def __getTimestampFilePath():
		timestampFilePath = os.path.join(
			tempfile.gettempdir(), 
			'cron-cert-check-timestamp-file'
		)
		return timestampFilePath

	def __updateDate(self):
		timestampFilePath = CertCheck.__getTimestampFilePath()
		try:
			print('Checking timestamp file date which indicates last time certificates were updated. Will compare it with certificate files\' dates to decide whether new certificates are available.')
			timestampFileTime = os.path.getmtime(timestampFilePath)
			self.__timestampAlreadyExists = True
			print('Current file timestamp is {}. Checking modified date of certificate files.'
				.format(CertCheck.__niceTime(timestampFileTime)))
			newestModifiedDate = CertCheck.__getNewestCertFileDate()
			if newestModifiedDate == None:
				# The certs directory is empty, so use epoch start for timestamp.
				newestModifiedDate = 0

			if newestModifiedDate > timestampFileTime:
				self.__newDate = newestModifiedDate
			else:
				self.__newDate = None

		except FileNotFoundError:
			print('Timestamp file doesn\'t exist.')
			self.__timestampAlreadyExists = False
			newestModifiedDate = CertCheck.__getNewestCertFileDate()
			if newestModifiedDate == None:
				newestModifiedDate = 0
			
			self.__newDate = newestModifiedDate

		if newestModifiedDate == None:
			print('There are no cert files present.')
		else:
			print('Newest file in certificates folder has time {}. If there were no certificate files, the date was set to epoch.'.format(CertCheck.__niceTime(newestModifiedDate)))

	def shouldServerUpdate(self):
		return self.__newDate != None

	def updateTimestamp(self):
		timestampFilePath = CertCheck.__getTimestampFilePath()
		if not self.__timestampAlreadyExists:
			tempTimestampFilePath = timestampFilePath + '.temp'
			Path(tempTimestampFilePath).touch()
			os.utime(tempTimestampFilePath, (self.__newDate, self.__newDate))
			os.rename(tempTimestampFilePath, timestampFilePath)
			print('There was no saved timestamp. Created a new one and set it to newest certificate file date.')
		else:
			os.utime(timestampFilePath, (self.__newDate, self.__newDate))
			print('Saved timestamp updated to newest certificate file date.')