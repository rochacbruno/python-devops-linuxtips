# openapi_client.AuthApi

All URIs are relative to *https://fakestoreapi.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**login_user**](AuthApi.md#login_user) | **POST** /auth/login | Login


# **login_user**
> LoginResponse login_user(login)

Login

Authenticate a user.

### Example


```python
import openapi_client
from openapi_client.models.login import Login
from openapi_client.models.login_response import LoginResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://fakestoreapi.com
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://fakestoreapi.com"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.AuthApi(api_client)
    login = openapi_client.Login() # Login | 

    try:
        # Login
        api_response = api_instance.login_user(login)
        print("The response of AuthApi->login_user:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AuthApi->login_user: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **login** | [**Login**](Login.md)|  | 

### Return type

[**LoginResponse**](LoginResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Login successful |  -  |
**400** | Bad request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

