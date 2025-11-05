# openapi_client.CartsApi

All URIs are relative to *https://fakestoreapi.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_cart**](CartsApi.md#add_cart) | **POST** /carts | Add a new cart
[**delete_cart**](CartsApi.md#delete_cart) | **DELETE** /carts/{id} | Delete a cart
[**get_all_carts**](CartsApi.md#get_all_carts) | **GET** /carts | Get all carts
[**get_cart_by_id**](CartsApi.md#get_cart_by_id) | **GET** /carts/{id} | Get a single cart
[**update_cart**](CartsApi.md#update_cart) | **PUT** /carts/{id} | Update a cart


# **add_cart**
> Cart add_cart(cart)

Add a new cart

Create a new cart.

### Example


```python
import openapi_client
from openapi_client.models.cart import Cart
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
    api_instance = openapi_client.CartsApi(api_client)
    cart = openapi_client.Cart() # Cart | 

    try:
        # Add a new cart
        api_response = api_instance.add_cart(cart)
        print("The response of CartsApi->add_cart:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CartsApi->add_cart: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cart** | [**Cart**](Cart.md)|  | 

### Return type

[**Cart**](Cart.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Cart created successfully |  -  |
**400** | Bad request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_cart**
> delete_cart(id)

Delete a cart

Delete a specific cart by ID.

### Example


```python
import openapi_client
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
    api_instance = openapi_client.CartsApi(api_client)
    id = 56 # int | 

    try:
        # Delete a cart
        api_instance.delete_cart(id)
    except Exception as e:
        print("Exception when calling CartsApi->delete_cart: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Cart deleted successfully |  -  |
**400** | Bad request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_carts**
> List[Cart] get_all_carts()

Get all carts

Retrieve a list of all available carts.

### Example


```python
import openapi_client
from openapi_client.models.cart import Cart
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
    api_instance = openapi_client.CartsApi(api_client)

    try:
        # Get all carts
        api_response = api_instance.get_all_carts()
        print("The response of CartsApi->get_all_carts:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CartsApi->get_all_carts: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[Cart]**](Cart.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |
**400** | Bad request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_cart_by_id**
> Cart get_cart_by_id(id)

Get a single cart

Retrieve details of a specific cart by ID.

### Example


```python
import openapi_client
from openapi_client.models.cart import Cart
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
    api_instance = openapi_client.CartsApi(api_client)
    id = 56 # int | 

    try:
        # Get a single cart
        api_response = api_instance.get_cart_by_id(id)
        print("The response of CartsApi->get_cart_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CartsApi->get_cart_by_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 

### Return type

[**Cart**](Cart.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |
**400** | Bad request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_cart**
> Cart update_cart(id, cart)

Update a cart

Update an existing cart by ID.

### Example


```python
import openapi_client
from openapi_client.models.cart import Cart
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
    api_instance = openapi_client.CartsApi(api_client)
    id = 56 # int | 
    cart = openapi_client.Cart() # Cart | 

    try:
        # Update a cart
        api_response = api_instance.update_cart(id, cart)
        print("The response of CartsApi->update_cart:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CartsApi->update_cart: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 
 **cart** | [**Cart**](Cart.md)|  | 

### Return type

[**Cart**](Cart.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Cart updated successfully |  -  |
**400** | Bad request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

