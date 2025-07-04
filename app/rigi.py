import json
import requests

import asyncio
import socketio
import logging

logging.basicConfig(level=logging.DEBUG)
#logging.getLogger("socketio").setLevel(logging.WARNING)
#logging.getLogger("engineio").setLevel(logging.WARNING)

token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVhdGVkQXQiOjE3NTA5NDUyMjYyNTMsInVwZGF0ZWRBdCI6MTc1MTA2MjE0NTA2OSwiaWQiOjMwMDAwODAsImVtYWlsIjoibWFyaWJhcnRlc2FAZ21haWwuY29tIiwidXNlcm5hbWUiOiJtYXJpYmFydGVzYSIsInBhc3N3b3JkIjoiJDJiJDEwJEF3VG1sZWthNGd4MFFxOUowMXVWbE9QZzBhU1EvQVdxemRFRWtiWE4wYUt2NzhSYUNUZVkuIiwiaW5pdGlhbFJvdXRlIjoiL3Byb2plY3QvbWFuYWdlLzUxIiwicmVzZXRUb2tlbiI6IiIsInJlc2V0VG9rZW5FeHBpcmUiOm51bGwsImV4cGlyYXRpb25EYXRlIjpudWxsLCJzdGF0dXMiOjEsInJvbGUiOjYsImlhdCI6MTc1MTQ5NTU1MCwiZXhwIjoxNzY1ODk1NTUwfQ.-dJDvOUKbkBuSiS5V67PcM7ODb8jKbKbdiD4mC4NmpM"
base_url = 'https://cloudtest.rigi.tech/api/1.0'
proyect_id = 51

ws_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVhdGVkQXQiOjE3NTA5NDUyMjYyNTMsInVwZGF0ZWRBdCI6MTc1MTA2MjE0NTA2OSwiaWQiOjMwMDAwODAsImVtYWlsIjoibWFyaWJhcnRlc2FAZ21haWwuY29tIiwidXNlcm5hbWUiOiJtYXJpYmFydGVzYSIsInBhc3N3b3JkIjoiJDJiJDEwJEF3VG1sZWthNGd4MFFxOUowMXVWbE9QZzBhU1EvQVdxemRFRWtiWE4wYUt2NzhSYUNUZVkuIiwiaW5pdGlhbFJvdXRlIjoiL3Byb2plY3QvbWFuYWdlLzUxIiwicmVzZXRUb2tlbiI6IiIsInJlc2V0VG9rZW5FeHBpcmUiOm51bGwsImV4cGlyYXRpb25EYXRlIjpudWxsLCJzdGF0dXMiOjEsInJvbGUiOjYsImlhdCI6MTc1MTQ5NTU1MCwiZXhwIjoxNzY1ODk1NTUwfQ.-dJDvOUKbkBuSiS5V67PcM7ODb8jKbKbdiD4mC4NmpM"
ws_base_url = 'https://cloudtest.rigi.tech'

headers = {
    "Authorization": token
}


# Create an async Socket.IO client
#sio = socketio.AsyncClient()

class WebSocket:
    def __init__(self):
        self.sio = socketio.AsyncClient()

        # Register event handlers
        self.sio.on('connect', self.on_connect)
        self.sio.on('disconnect', self.on_disconnect)
        #self.sio.on('telemetry', self.on_telemetry)
        self.sio.on('download_plan', self.on_download_plan)
        self.sio.on('status_message', self.status_message)
        #self.sio.off("telemetry")


        # Start the async main
        asyncio.run(self.main())   # ✅ Correct: no keyword argument here

    async def on_connect(self):
        print("✅ Connected to the server")

    async def on_disconnect(self):
        print("❌ Disconnected from the server")

    async def on_telemetry(self, data):
        print("Received telemetry:", data)

    async def on_download_plan(self, data):
        print("Received Plan:", data)

    async def status_message(self, data):
        print("Received MESSAGESSS:", data)

    async def main(self):
        # Connect
        await self.sio.connect(
            f"{ws_base_url}?token={ws_token}",
            transports=['websocket']
        )
        # Keep alive
        await self.sio.wait()




class RestClient:
    def __init__(self, timeout=10):
        self.base_url = base_url
        self.headers = headers
        self.timeout = timeout

    def delete_operation(self, id):
        url = f"{self.base_url}/operation/{id}"

        response = requests.delete(
            url=url,
            headers={**self.headers, **(headers or {})},
            timeout=self.timeout
        )

        self._check_response(response)
        print(response.json())

        return response.json()
    
    def get_simulator_list(self):
        url = f"{self.base_url}/drones?project={51}"
        response = requests.get(
            url=url,
            headers={**self.headers, **(headers or {})},
            timeout=self.timeout
        )
        
        self._check_response(response)
        print(response.json())

        return response.json()

    def start_simulator(self):
        url = f"{self.base_url}/simulator/{42}/start"

        payload = {
            "lat": 37.7749,
            "lon": -122.4194,
            "alt": 120.0,
            "speed": 3
        }

        response = requests.post(
            url,
            headers=self.headers,
            data=json.dumps(payload)
        )
        
        self._check_response(response)
        print(response.json())

        return response.json()

    def get_routes(self):
        url = f"{self.base_url}/routes?project={proyect_id}"

        response = requests.get(
            url=url,
            headers={**self.headers, **(headers or {})},
            timeout=self.timeout
        )

        self._check_response(response)
        print(response.json())

        return response.json()
    

    def get_operation_by_id(self, id):
        url = f"{self.base_url}/operation/{id}"

        response = requests.get(
            url=url,
            headers={**self.headers, **(headers or {})},
            timeout=self.timeout
        )

        self._check_response(response)
        print(response.json())

        return response.json()

    def create_operation(self, payload):
        url = f"{self.base_url}/operation"

        try:
            # Send the POST request
            response = requests.post(
                url,
                headers=self.headers,
                data=json.dumps(payload)
            )

            # Check status
            if response.ok:
                data = response.json()
                print("✅ Success:")
                print(json.dumps(data, indent=2))
            else:
                if response.status_code == 400:
                    error = response.json()
                    print("⚠️ 400 Bad Request:", json.dumps(error, indent=2))
                elif response.status_code == 403:
                    print("❌ 403 Forbidden access to data")
                elif response.status_code == 404:
                    print("❌ 404 Address not found")
                else:
                    try:
                        error = response.json()
                        print(f"❌ Error {response.status_code}: {json.dumps(error, indent=2)}")
                    except Exception:
                        print(f"❌ Error {response.status_code}: No JSON body")

        except requests.RequestException as e:
            print("❌ Error fetching data:", e)
        return

    def get(self, endpoint, params=None, headers=None):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = requests.get(
            url,
            params=params,
            headers={**self.headers, **(headers or {})},
        )
        self._check_response(response)
        return response.json()


    def _check_response(self, response):
        if not response.ok:
            raise requests.HTTPError(
                f"Error {response.status_code}: {response.text}"
            )