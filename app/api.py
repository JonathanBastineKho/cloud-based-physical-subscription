import requests
from dotenv import load_dotenv
import os
import json
from abc import ABC, abstractmethod


# Abstract Class
class API(ABC):
	@abstractmethod
	def print_api_key(self):
		pass


# Door API
class DoorAPI(API):
	# Class attributes
	__test_server = "https://nokeyoneoffi.com/phonepass"
	__op_server = "https://ppass.co.kr/phonepass"

	def __init__(self, id:str, pw:str) -> None:
		"""
		Initialize a DoorAPI instance object.

		Parameters:
		- ID(str) = secret API ID for PhonePass API
		- PW(str) = secret API Password for PhonePass API
		"""
		# Instance attributes
		self.__phonepass_id = id
		self.__phonepass_pw = pw

	def print_api_key(self):
		"""
		Prints out the API keys used in the constructor. (FOR DEBUG PURPSOSES)
		"""
		print(f"ID = {self.__phonepass_id}, PW = {self.__phonepass_pw}")

	# Private Request Status METHOD
	def __request_status(self, doorID:str) -> requests.Response:
		"""
		Requests the status of door using POST Method.

		Parameters:
		- doorID(str) = serialnumber/identifier of Door

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
	def __request_lock(self, doorID:str) -> requests.Response:
		"""
		Requests the locking of door using POST Method.

		Parameters:
		- doorID(str) = serialnumber/identifier of Door

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
	def __request_unlock(self, doorID:str, delay:int=0) -> requests.Response:
		"""
		Requests the unlocking of door using POST Method.

		Parameters:
		- doorID(str) = serialnumber/identifier of Door
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

	def check_status(self, doorID:str) -> str:
		"""
		Method to retrieve the status of a door

		Parameters:
		- doorID(str) = serialnumber/identifier of Door
		
		Returns door status dictionary with keys:
			- "success": (Bool) represents the success of request. 
			- "result": (str) represents the result of the requests (differ depending on "success")
				if Successful(SVC_CODE 100):
					"result" will represent the resultMsg (either Open, Close, Abnormal, Scan Fail, Already Running, Error, Bridge OFF)
				if Fail(SVC_CODE 302, 901, 904):
					"result" will represent the SVC_CODE : SVC_Message 
		"""
		request = self.__request_status(doorID)
		result_info = json.loads(request.content)
		result_svc = result_info.get("SVC_CODE")
		if result_svc == "100":
			return {"success": True, "result": result_info.get("resultMsg")}
		else:
			return {"success": False, "result": f"RESPONSE {result_svc}: {result_info.get('SVC_MSGE')}"}
	
	def lock(self, doorID:str):
		"""
		Method to lock a door

		Parameters:
		- doorID(str) = serialnumber/identifier of Door
		
		Returns door status dictionary with keys:
			- "success": (Bool) represents the success of request. 
			- "result": (str) represents the result of the requests (differ depending on "success")
				if Successful(SVC_CODE 100):
					"result" will represent the resultMsg (either Open, Close, Abnormal, Scan Fail, Already Running, Error, Bridge OFF)
				if Fail(SVC_CODE 302, 901, 904):
					"result" will represent the SVC_CODE : SVC_Message 
		"""
		request = self.__request_lock(doorID)
		result_info = json.loads(request.content)
		result_svc = result_info.get("SVC_CODE")
		if result_svc == "100":
			return {"success": True, "result": result_info.get("resultMsg")}
		else:
			return {"success": False, "result": f"RESPONSE {result_svc}: {result_info.get('SVC_MSGE')}"}

	def unlock(self, doorID:str, delay:int=0):
		"""
		Method to unlock a door

		Parameters:
		- doorID(str) = serialnumber/identifier of Door
		- delay(int) = Locked waiting time in minutes (0-255). Defaults 0.

		Returns door status dictionary with keys:
			- "success": (Bool) represents the success of request. 
			- "result": (str) represents the result of the requests (differ depending on "success")
				if Successful(SVC_CODE 100):
					"result" will represent the resultMsg (either Open, Close, Abnormal, Scan Fail, Already Running, Error, Bridge OFF)
				if Fail(SVC_CODE 302, 901, 904):
					"result" will represent the SVC_CODE : SVC_Message 
		"""
		request = self.__request_unlock(doorID, delay)
		result_info = json.loads(request.content)
		result_svc = result_info.get("SVC_CODE")
		if result_svc == "100":
			return {"success": True, "result": result_info.get("resultMsg")}
		else:
			return {"success": False, "result": f"RESPONSE {result_svc}: {result_info.get('SVC_MSGE')}"}


# Product API
class ProductAPI(API):
	# Class attributes
	__server = "https://api.steppay.kr/api/v1"
	def __init__(self, token:str) -> None:
		"""
		Initialize a ProductAPI instance object.

		Parameters:
		- token(str) = secret token for STEPPAY API.
		"""

		# Instance attributes
		self.__token = token
	
	def print_api_key(self):
		"""
		Prints out the API keys used in the constructor. (FOR DEBUG PURPSOSES)
		"""
		print(f"TOKEN = {self.__token}")
	
	def __request_create_product(self, name:str, imageURL:str, description:str) -> requests.Response: 
		"""
		Requests the creation of a new product using POST Method.

		Parameters:
		- name(str) = Product name.
		- imageURL(str) = url to product image.
		- description(str) = Product description.

		Returns a request Response
		"""
		header = {
			"accept": "*/*",
			"content-type": "application/json",
			"Secret-Token": self.__token
		}
		param_data = {
			"type": "SOFTWARE",
			"status": "UNSOLD",
			"name": name,
			"featuredImageUrl": imageURL,
			"description": description,
		}

		return requests.post(
			url=f"{self.__server}/products",
			headers=header,
			json=param_data
		)

	def __request_create_price(self, productID:int, price:float, interval:str, unit:str) -> requests.Response: 
		"""
		Requests the creation of a new price plan for a specified product using POST Method.

		Parameters:
		- productID(int) = Product ID.
		- price(float) = Product price (per interval)
		- interval(str) = interval of payment either ["DAY", "WEEK", "MONTH", "YEAR"].
		- unit(str) = unit of price.

		Returns a request Response
		"""
		header = {
			"accept": "*/*",
			"content-type": "application/json",
			"Secret-Token": self.__token
		}
		param_data = {
			"plan": {
				"name": "Default",
				"description": "Default Price",
			},
			"recurring": {
				"intervalCount": 1,
				"interval": interval,
				"usageType": "LICENSED",
				"aggregateUsageType": "SUM"
			},
			"price": price,
			"unit": unit,
			"type": "FLAT"
		}

		return requests.post(
			url=f"{self.__server}/products/{productID}/prices",
			headers=header,
			json=param_data
		)
	
	def __request_update_data(self, productID:int, name:str=None, imageURL:str=None, description:str=None) -> requests.Response:
		"""
		Requests the update of a specified product's data using PUT Method.

		Parameters:
		- productID(int) = Product ID.

		Optional parameters (Leaving them blank would not update the data):
		- name(str) = Product name.
		- imageURL(str) = url to product image.
		- description(str) = Product description.

		Returns a request Response
		"""
		header = {
			"accept": "*/*",
			"content-type": "application/json",
			"Secret-Token": self.__token
		}
		param_data = {}
		if name != None:
			param_data["name"] = name 
		if imageURL != None:
			param_data["featuredImageUrl"] = imageURL 
		if description != None:
			param_data["description"] = description 

		return requests.put(
			url=f"{self.__server}/products/{productID}",
			headers=header,
			json=param_data
		)

	def __request_update_price(self, productID:int, priceID:int, price:float=None, interval:str=None, unit:str=None) -> requests.Response:
		"""
		Requests the update of a specified price plan's data using PUT Method.

		Parameters:
		- productID(int) = Product ID.
		- priceID(int) = Price plan ID.

		Optional parameters (Leaving them blank would not update the data):
		- price(float) = Product price (per interval)
		- interval(str) = interval of payment either ["DAY", "WEEK", "MONTH", "YEAR"].
		- unit(str) = unit of price.

		Returns a request Response
		"""
		header = {
			"accept": "*/*",
			"content-type": "application/json",
			"Secret-Token": self.__token
		}
		param_data = {
			"plan": {
				"name": "Default",
				"description": "Default Price",
			}
		}
		if price != None:
			param_data["price"] = price 
		# if interval != None:
		# 	param_data["recurring"]["interval"] = interval 
		if unit != None:
			param_data["unit"] = unit 

		return requests.put(
			url=f"{self.__server}/products/{productID}/prices/{priceID}",
			headers=header,
			json=param_data
		)

	def __request_update_status(self, productID:int, status:str) -> requests.Response:
		"""
		Requests the update of a specified product's posting status using PATCH Method.

		Parameters:
		- productID(int) = Product ID.
		- status(str) = Posting status, either ["SALE", "OUT_OF_STOCK", "UNSOLD", "WAITING_FOR_APPROVAL", "REJECTED"].

		Returns a request Response
		"""
		headers = {
			"accept": "*/*",
			"Secret-Token": self.__token
		}
		return requests.patch(
			url=f"{self.__server}/products/{productID}/status?status={status}", 
			headers=headers)

	def __request_info(self, productCode:str) -> requests.Response:
		"""
		Requests a specified product's information using GET Method.

		Parameters:
		- productCode(str) = Product Code.

		Returns a request Response
		"""
		header = {
			"accept": "*/*",
			"Secret-Token": "f94276067531989d16964ff07710860407a4b175c2f2a2179a89d0876f4d4755"
		}
		return requests.get(
			url=f"{self.__server}/products/{productCode}",
			headers=header,
		)
	
	def __request_delete(self, productID:int) -> requests.Response:
		"""
		Requests the deletion of a specified product using DELETE Method.

		Parameters:
		- productID(int) = Product ID.

		Returns a request Response
		"""
		header = {
			"accept": "*/*",
			"Secret-Token": "f94276067531989d16964ff07710860407a4b175c2f2a2179a89d0876f4d4755"
		}
		return requests.delete(
			url=f"{self.__server}/products/{productID}",
			headers=header,
		)

	def create(self, name:str, imageURL:str, description:str, price:float, interval:str="MONTH", unit:str="SGD") -> dict:
		"""
		Creates a new product ready for SALE.

		Parameters:
		- name(str) = Product name.
		- imageURL(str) = url to product image.
		- description(str) = Product description.
		- price(float) = Product price (per interval)
		- interval(str) = interval of payment either ["DAY", "WEEK", "MONTH", "YEAR"]. Defaults to "MONTH".
		- unit(str) = Unit of the price. Defaults to "SGD".

		Returns a dictionary with keys:
			"success": (bool) True if everything went through perfectly without any issues.
			"message": (str) success message (details about success or errors).
		"""
		product = self.__request_create_product(name, imageURL, description)
		if product.status_code != 201:
			return {"success": False, "message": f"Failed to create Product."}
		msg =  json.loads(product.text)
		pricing = self.__request_create_price(msg["id"], price, interval, unit)
		if pricing.status_code != 201:
			return {"success": False, "message": f"Successfully created Product {msg['id']}, but failed to create price plan."}
		msg["prices"] = json.loads(pricing.text)
		status = self.__request_update_status(msg["id"], "SALE")
		if status.status_code != 200:
			return {"success": False, "message": f"Successfully created Product {msg['id']} with Pricing {pricing['id']}, BUT Failed to update STATUS"}
		msg["status"] = json.loads(status.text)
		return {"success": True,  "message": msg}

	def update_posting_status(self, productID:int, status:str="SALE") -> dict:
		"""
		Updates a specified product's posting status.

		Parameters:
		- productID(int) = Product ID.
		- status(str) = Posting status, either ["SALE", "OUT_OF_STOCK", "UNSOLD", "WAITING_FOR_APPROVAL", "REJECTED"].

		Returns a dictionary with keys:
			"success": (bool) True if everything went through perfectly without any issues.
			"message": (str) success message (details about success or errors).
		"""
		res = self.__request_update_status(productID, status)
		if res.status_code == 200:
			return {"success": True,  "message": f"Successfully set status of product {productID} to '{status}'."}
		return {"success": False,  "message": f"Failed to set status of product {productID} to '{status}'."}
		 
	def update_data(self, product_id:int, price_id:int, name:str=None, imageURL:str=None, 
							description:str=None, price:float=None, interval:str=None, unit:str=None) -> dict:
		"""
		Updates a specified product's data.

		Parameters:
		- productID(int) = Product ID.
		- priceID(int) = Price plan ID.

		Optional parameters (Leaving them blank would not update the data):
		- name(str) = Product name.
		- imageURL(str) = url to product image.
		- description(str) = Product description.
		- price(float) = Product price (per interval)
		- interval(str) = interval of payment either ["DAY", "WEEK", "MONTH", "YEAR"].
		- unit(str) = unit of price

		Returns a dictionary with keys:
			"success": (bool) True if everything went through perfectly without any issues.
			"message": (str) success message (details about success or errors).
		"""
		if name!=None or imageURL!=None or description!=None:
			update_product = self.__request_update_data(product_id, name, imageURL, description)
			if update_product.status_code != 200:
				return {"success": False, "message": f"Failed to update Product data."}
		if price!=None or interval!=None or unit!=None:
			update_price = self.__request_update_price(product_id, price_id, price, interval, unit)
			if update_price.status_code != 200:
				return {"success": False, "message": f"Failed to update Product's pricing data."}
		msg = json.loads(update_product.text)
		msg["prices"] = json.loads(update_price.text)
		return {"success": True,  "message": msg}

	def info(self, productCode:str, onlyPrice:bool=False) -> dict:
		"""
		Retrieves a specified product's data.

		Parameters:
		- productCode(str) = Product Code.
		- onlyPrice(bool) = If True, only retrieves the price plan data. Defaults to False.

		Returns a dictionary with keys:
			"success": (bool) True if everything went through perfectly without any issues.
			"message": (str) success message (details about success or errors).
		"""
		res = self.__request_info(productCode)
		if res.status_code != 200:
			return {"success": False, "message": f"Failed to retrieve customer {productCode}'s data."}
		info = json.loads(res.text)
		if onlyPrice:
			return {"success": True,  "message": info["prices"]}
		return {"success": True,  "message": info}

	def delete(self, productID:int) -> dict:
		"""
		Deletes a specified product.

		Parameters:
		- productID(int) = Product ID.

		Returns a dictionary with keys:
			"success": (bool) True if everything went through perfectly without any issues.
			"message": (str) success message (details about success or errors).
		"""
		res = self.__request_delete(productID)
		if res.status_code != 200:
			return {"success": False, "message": f"Failed to delete customer {productID}."}
		return {"success": True,  "message": f"Successfully deleted customer {productID}."}
	
		
# Customer API
class CustomerAPI(API):
	# Class attributes
	__server = "https://api.steppay.kr/api/v1"
	def __init__(self, token:str) -> None:
		"""
		Initialize a CustomerAPI instance object.

		Parameters:
		- token(str) = secret token for STEPPAY API.
		"""

		# Instance attributes
		self.__token = token
	
	def print_api_key(self):
		"""
		Prints out the API keys used in the constructor. (FOR DEBUG PURPSOSES)
		"""
		print(f"TOKEN = {self.__token}")
	
	def __request_create(self, name:str, email:str, phone:str) -> requests.Response:
		"""
		Requests the creation of a new customer using POST Method.

		Parameters:
		- name(str) = Customer name.
		- email(str) = Customer email.
		- phone(str) = Customer phone number.

		Returns a request Response
		"""
		header = {
			"accept": "*/*",
			"content-type": "application/json",
			"Secret-Token": self.__token
		}
		param_data = {
			"name": name,
			"email": email,
			"phone": phone,
		}

		return requests.post(
			url=f"{self.__server}/customers",
			headers=header,
			json=param_data
		)

	def __request_update(self, customerID:int, name:str, email:str, phone:str=None) -> requests.Response:
		"""
		Requests the update of a specified customer's data using PUT Method.

		Parameters:
		- customerID(int) = Customer ID.
		- name(str) = Customer name.
		- email(str) = Customer email.

		Optional parameters:
		- phone(str) = Customer phone number.

		Returns a request Response
		"""
		header = {
			"accept": "*/*",
			"content-type": "application/json",
			"Secret-Token": self.__token
		}
		param_data = {
			"name": name,
			"email": email,
		}
		if phone != None:
			param_data["phone"] = phone

		return requests.put(
			url=f"{self.__server}/customers/{customerID}",
			headers=header,
			json=param_data
		)
	
	def __request_info(self, customerID:int) -> requests.Response:
		"""
		Requests a specified customer's information using GET Method.

		Parameters:
		- customerID(int) = Customer ID.

		Returns a request Response
		"""
		header = {
			"accept": "*/*",
			"Secret-Token": "f94276067531989d16964ff07710860407a4b175c2f2a2179a89d0876f4d4755"
		}
		return requests.get(
			url=f"{self.__server}/customers/{customerID}",
			headers=header,
		)
	
	def __request_delete(self, customerID:int) -> requests.Response:
		"""
		Requests the deletion of a specified customer using DELETE method.

		Parameters:
		- customerID(int) = Customer ID.

		Returns a request Response
		"""
		header = {
			"accept": "*/*",
			"Secret-Token": "f94276067531989d16964ff07710860407a4b175c2f2a2179a89d0876f4d4755"
		}
		return requests.delete(
			url=f"{self.__server}/customers/{customerID}",
			headers=header,
		)

	def create(self, name:str, email:str, phone:str) -> dict:
		"""
		Creates a new customer.

		Parameters:
		- name(str) = Customer name.
		- email(str) = Customer email.
		- phone(str) = Customer phone number.

		Returns a dictionary with keys:
			"success": (bool) True if everything went through perfectly without any issues.
			"message": (str) success message (details about success or errors).
		"""
		res = self.__request_create(name, email, phone)
		if res.status_code != 201:
			return {"success": False, "message": f"Failed to create new customer."}
		return {"success": True,  "message": json.loads(res.text)}
	
	def update(self, customerID:int, name:str, email:str, phone:str=None) -> dict:
		"""
		Updates a specified customer's data.

		Parameters:
		- customerID(int) = Customer ID.
		- name(str) = Customer name.
		- email(str) = Customer email.
		
		Optional parameters:
		- phone(str) = Customer phone number. 

		Returns a dictionary with keys:
			"success": (bool) True if everything went through perfectly without any issues.
			"message": (str) success message (details about success or errors).
		"""
		res = self.__request_update(customerID, name, email, phone)
		if res.status_code != 200:
			return {"success": False, "message": f"Failed to update customer {customerID}'s data."}
		return {"success": True,  "message": json.loads(res.text)}

	def info(self, customerID:int) -> dict:
		"""
		Retrieves a specified customer's data.

		Parameters:
		- customerID(int) = Customer ID.

		Returns a dictionary with keys:
			"success": (bool) True if everything went through perfectly without any issues.
			"message": (str) success message (details about success or errors).
		"""
		res = self.__request_info(customerID)
		if res.status_code != 200:
			return {"success": False, "message": f"Failed to retrieve customer {customerID}'s data."}
		return {"success": True,  "message": json.loads(res.text)}

	def delete(self, customerID:int) -> dict:
		"""
		Deletes a specified customer.
		Parameters:
		- customerID(int) = Customer ID.

		Returns a dictionary with keys:
			"success": (bool) True if everything went through perfectly without any issues.
			"message": (str) success message (details about success or errors).
		"""
		res = self.__request_delete(customerID)
		if res.status_code != 200:
			return {"success": False, "message": f"Failed to delete customer {customerID}."}
		return {"success": True,  "message": f"Successfully deleted customer {customerID}."}


# Order API
class OrderAPI(API):
	# Class attributes
	__server = "https://api.steppay.kr/api/v1"
	def __init__(self, token:str) -> None:
		"""
		Initialize an OrderAPI instance object.

		Parameters:
		- token(str) = secret token for STEPPAY API.
		"""

		# Instance attributes
		self.__token = token
	
	def print_api_key(self):
		"""
		Prints out the API keys used in the constructor. (FOR DEBUG PURPSOSES)
		"""
		print(f"TOKEN = {self.__token}")
	
	def __request_create(self, customerCode:str, productCode:str, priceCode:str) -> requests.Response:
		"""
		Requests the creation of a new order using POST Method.

		Parameters:
		- customerCode(str) = Customer Code.
		- productCode(str) = Product Code.
		- priceCode(str) = Price Plan Code.

		Returns a request Response
		"""
		header = {
			"accept": "*/*",
			"content-type": "application/json",
			"Secret-Token": self.__token
		}
		param_data = {
			"customerCode": customerCode,
			"items": [{
				"currency": "SGD",
				"minimumQuantity": 0,
				"productCode": productCode,
				"priceCode": priceCode
			}]
		}

		return requests.post(
			url=f"{self.__server}/orders",
			headers=header,
			json=param_data
		)
	
	def __request_info(self, orderCode:str) -> requests.Response:
		"""
		Requests the information of a specified order using GET Method.

		Parameters:
		- orderCode(str) = Order code or ID.

		Returns a request Response
		"""
		header = {
			"accept": "*/*",
			"Secret-Token": self.__token
		}

		return requests.get(
			url=f"{self.__server}/orders/{orderCode}",
			headers=header,
		)
	
	def create(self, customerCode:str, productCode:str, priceCode:str) -> dict:
		"""
		Creates a new order.

		Parameters:
		- customerCode(str) = Customer Code.
		- productCode(str) = Product Code.
		- priceCode(str) = Price Plan Code.

		Returns a dictionary with keys:
			"success": (bool) True if everything went through perfectly without any issues.
			"message": (str) success message (details about success or errors).
		"""
		res = self.__request_create(customerCode, productCode, priceCode)
		if res.status_code != 200:
			return {"success": False, "message": f"Failed to create order for customer({customerCode}), product({productCode}), price({priceCode})."}
		return {"success": True,  "message": json.loads(res.text)}

	def info(self, orderCode:str) -> dict:
		"""
		Retrieves the information of a specified order.

		Parameters:
		- orderCode(str) = Order code or ID.

		Returns a dictionary with keys:
			"success": (bool) True if everything went through perfectly without any issues.
			"message": (str) success message (details about success or errors).
		"""
		res = self.__request_info(orderCode)
		if res.status_code != 200:
			return {"success": False, "message": f"Failed to retrieve Order {orderCode}'s data."}
		return {"success": True,  "message": json.loads(res.text)}

def main():
	load_dotenv("../.env")
	# phonepass_id = os.environ.get("PHONEPASS_ID")
	# phonepass_pw = os.environ.get("PHONEPASS_PW")
	# phonepass_door = os.environ.get("PHONEPASS_DOOR")
	# door = DoorAPI(phonepass_id, phonepass_pw)
	# door.print_api_key()
	# print("API TESTING\n")
	# status = door.check_status(phonepass_door)
	# print(status)
	# print("UNLOCK")
	# print(door.unlock(phonepass_door))
	# print("STATUS=",door.check_status(phonepass_door))
	# print("LOCK")
	# print(door.lock(phonepass_door))
	# print("STATUS=",door.check_status(phonepass_door))

	steppay_key = os.environ.get("STEPPAY_SECRET_KEY")
	c = CustomerAPI(steppay_key)
	p = ProductAPI(steppay_key)
	o = OrderAPI(steppay_key)
	res = o.info("order_qXb1fDEnK")
	print(res)

if __name__ == "__main__":
	main()
