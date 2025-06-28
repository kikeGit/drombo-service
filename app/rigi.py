import requests


token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVhdGVkQXQiOjE3NTA5NDUyMjYyNTMsInVwZGF0ZWRBdCI6MTc1MTA2MjE0NTA2OSwiaWQiOjMwMDAwODAsImVtYWlsIjoibWFyaWJhcnRlc2FAZ21haWwuY29tIiwidXNlcm5hbWUiOiJtYXJpYmFydGVzYSIsInBhc3N3b3JkIjoiJDJiJDEwJEF3VG1sZWthNGd4MFFxOUowMXVWbE9QZzBhU1EvQVdxemRFRWtiWE4wYUt2NzhSYUNUZVkuIiwiaW5pdGlhbFJvdXRlIjoiL3Byb2plY3QvbWFuYWdlLzUxIiwicmVzZXRUb2tlbiI6IiIsInJlc2V0VG9rZW5FeHBpcmUiOm51bGwsImV4cGlyYXRpb25EYXRlIjpudWxsLCJzdGF0dXMiOjEsInJvbGUiOjYsImlhdCI6MTc1MTA2MzU4MywiZXhwIjoxNzY1NDYzNTgzfQ._yJ4IZG2sUwzfAlpbHWbe9ar8k0fLWXopQBOKErKVUY"
base_url = 'https://cloud.rigi.tech/api/1.0'
proyect_id = 51

headers = {
    "Authorization": token
}

class RestClient:
    def __init__(self, timeout=10):
        self.base_url = base_url
        self.headers = headers
        self.timeout = timeout

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