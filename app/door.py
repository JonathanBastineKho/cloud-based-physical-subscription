import requests
from dotenv import load_dotenv
import os
import json

class DoorAPI():
	# Class attributes
	__test_server = "https://nokeyoneoffi.com/phonepass"
	__op_server = "https://ppass.co.kr/phonepass"

	def __init__(self, id, pw) -> None:
		# Instance attributes
		self.__phonepass_id = id
		self.__phonepass_pw = pw

	def print_api_key(self):
		"""
		Prints out the API keys used in the constructor. (FOR DEBUG PURPSOSES)
		"""
		print(f"ID = {self.__phonepass_id}, PW = {self.__phonepass_pw}")

	# Private Request Status METHOD
	def __request_status(self, doorID) -> requests.Response:
		"""
		Requests the status of door using POST Method.
		Parameters:
		- doorID = serialnumber/identifier of Door

		Returns a request Response
		"""
		param_data = {
			"id": self.__phonepass_id,
			"pw": self.__phonepass_pw,
			"sn": doorID
		}
		return requests.post(
			url=f"{self.__op_server}/p/iot/api/status.do",
			data=param_data
		)

	# Private Request Lock METHOD
	def __request_lock(self, doorID) -> requests.Response:
		"""
		Requests the locking of door using POST Method.
		Parameters:
		- doorID = serialnumber/identifier of Door

		Returns a request Response
		"""
		param_data = {
			"id": self.__phonepass_id,
			"pw": self.__phonepass_pw,
			"sn": doorID,
			"phone": "01011113333"
		}
		return requests.post(
			url=f"{self.__op_server}/p/iot/api/close.do",
			data=param_data
		)

	# Private Request Unlock METHOD
	def __request_unlock(self, doorID, delay=0) -> requests.Response:
		"""
		Requests the unlocking of door using POST Method.
		Parameters:
		- doorID(string) = serialnumber/identifier of Door
		- delay(int) = Locked waiting time in minutes (0-255). Defaults 0.

		Returns a request Response
		"""
		param_data = {
			"id": self.__phonepass_id,
			"pw": self.__phonepass_pw,
			"sn": doorID,
			"phone": "01011113333",
			"delay": delay
		}
		return requests.post(
			url=f"{self.__op_server}/p/iot/api/open.do",
			data=param_data
		)

	def check_status(self, doorID) -> str:
		"""
		Method to retrieve the status of a door
		Parameters:
		- doorID(string) = serialnumber/identifier of Door
		
		Returns door status (Bool, str) where,
			Bool represents the success of request.
			if Successful(SVC_CODE 100):
				str will represent the resultMsg (either Open, Close, Abnormal, Scan Fail, Already Running, Error, Bridge OFF)
			if Fail(SVC_CODE 302, 901, 904):
				str will represent the SVC_CODE : SVC_Message 
		"""
		request = self.__request_status(doorID)
		result_info = json.loads(request.content)
		result_svc = result_info.get("SVC_CODE")
		if result_svc == "100":
			return True, result_info.get("resultMsg")
		else:
			return False, f"RESPONSE {result_svc}: {result_info.get('SVC_MSGE')}"
	
	def lock(self, doorID):
		"""
		Method to lock a door
		Parameters:
		- doorID(string) = serialnumber/identifier of Door
		
		Returns door status (Bool, str) where,
			Bool represents the success of request.
			if Successful(SVC_CODE 100):
				str will represent the resultMsg (either Open, Close, Abnormal, Scan Fail, Already Running, Error, Bridge OFF)
			if Fail(SVC_CODE 302, 901, 904):
				str will represent the SVC_CODE : SVC_Message 
		"""
		request = self.__request_lock(doorID)
		result_info = json.loads(request.content)
		result_svc = result_info.get("SVC_CODE")
		if result_svc == "100":
			return True, result_info.get("resultMsg")
		else:
			return False, f"RESPONSE {result_svc}: {result_info.get('SVC_MSGE')}"

	def unlock(self, doorID, delay=0):
		"""
		Method to unlock a door
		Parameters:
		- doorID(string) = serialnumber/identifier of Door
		- delay(int) = Locked waiting time in minutes (0-255). Defaults 0.

		Returns door status (Bool, str) where,
			Bool represents the success of request.
			if Successful(SVC_CODE 100):
				str will represent the resultMsg (either Open, Close, Abnormal, Scan Fail, Already Running, Error, Bridge OFF)
			if Fail(SVC_CODE 302, 901, 904):
				str will represent the SVC_CODE : SVC_Message 
		"""
		request = self.__request_unlock(doorID, delay)
		result_info = json.loads(request.content)
		result_svc = result_info.get("SVC_CODE")
		if result_svc == "100":
			return True, result_info.get("resultMsg")
		else:
			return False, f"RESPONSE {result_svc}: {result_info.get('SVC_MSGE')}"

def main():
	load_dotenv("../.env")
	phonepass_id = os.environ.get("PHONEPASS_ID")
	phonepass_pw = os.environ.get("PHONEPASS_PW")
	phonepass_door = os.environ.get("PHONEPASS_DOOR")
	door = DoorAPI(phonepass_id, phonepass_pw)
	door.print_api_key()
	print("API TESTING\n")
	status = door.check_status(phonepass_door)
	print(status)
	print("UNLOCK")
	print(door.unlock(phonepass_door))
	print("STATUS=",door.check_status(phonepass_door))
	print("LOCK")
	print(door.lock(phonepass_door))
	print("STATUS=",door.check_status(phonepass_door))

if __name__ == "__main__":
	main()
